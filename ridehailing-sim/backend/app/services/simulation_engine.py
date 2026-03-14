"""
网约车仿真引擎（核心）
替代 MiroFish 的 OASIS 社交媒体仿真引擎
实现基于时间步的离散事件仿真

MiroFish 架构对应关系：
- OASIS Twitter/Reddit 引擎  →  TransportSimulationEngine
- Agent 发帖/评论/点赞       →  Agent 叫车/接单/行驶/完单
- 轮次(Round)推进            →  时间步(TimeStep)推进
- 社交媒体动作日志           →  出行事件日志
"""

import json
import os
import time
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import defaultdict

from ..models.entities import (
    Order, OrderStatus, DriverProfile, DriverStatus,
    PassengerProfile, Location, ZoneMetrics,
)
from ..models.simulation import (
    SimulationConfig, SimulationState, SimulationStatus,
    TimeConfig, SupplyDemandConfig,
)
from .geo.spatial import (
    HexGrid, haversine_distance, road_distance, estimate_travel_time,
    random_location_in_radius, Hotspot, CITY_HOTSPOTS, CITY_CENTERS,
)
from .agents.driver_agent import DriverAgent
from .agents.passenger_agent import PassengerAgent
from .agents.profile_generator import generate_driver_profiles, generate_passenger_profiles
from .matching.engine import MatchingEngine
from .pricing.engine import PricingEngine
from ..utils.logger import get_logger

logger = get_logger('ridehailing.engine')


class TransportSimulationEngine:
    """
    网约车仿真引擎
    对应 MiroFish 的 OASIS 引擎 + SimulationRunner 的组合

    核心循环：
    每个时间步(time_step):
        1. 更新时间 → 对应 MiroFish 的轮次推进
        2. 司机上下线决策 → 对应 Agent 活跃度变化
        3. 乘客叫车决策 → 对应 Agent 发帖行为
        4. 订单匹配 → 这是全新的核心逻辑
        5. 行程推进 → Agent 状态更新
        6. 定价更新 → 供需动态调节
        7. 指标统计 → 数据记录
    """

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.state = SimulationState(simulation_id=config.simulation_id)

        # 核心组件
        city_center = CITY_CENTERS.get(
            config.city_config.city_name.lower(),
            Location(config.city_config.center_lat, config.city_config.center_lng)
        )
        self.hex_grid = HexGrid(
            center=city_center,
            radius_km=config.city_config.radius_km,
            resolution=config.city_config.h3_resolution,
        )
        self.matching_engine = MatchingEngine(
            max_pickup_distance_km=config.matching_config.max_pickup_distance_km,
        )
        self.pricing_engine = PricingEngine(
            base_fare=config.pricing_config.base_fare,
            per_km_fare=config.pricing_config.per_km_fare,
            per_minute_fare=config.pricing_config.per_minute_fare,
            min_surge=config.pricing_config.min_surge,
            max_surge=config.pricing_config.max_surge,
            surge_sensitivity=config.pricing_config.surge_sensitivity,
        )

        # Agent 容器
        self.drivers: Dict[str, DriverAgent] = {}
        self.passengers: Dict[str, PassengerAgent] = {}

        # 订单池
        self.orders: Dict[str, Order] = {}
        self.pending_orders: List[str] = []  # 等待匹配的订单 ID

        # 热点
        city_key = config.city_config.city_name.lower()
        hotspots = CITY_HOTSPOTS.get(city_key, CITY_HOTSPOTS.get("beijing", []))
        self.hotspot_locations = [h.location for h in hotspots]
        self.hotspots = hotspots

        # 时间步
        self.current_step = 0
        self.time_step_seconds = config.time_config.time_step_seconds
        self.total_steps = (config.time_config.total_hours * 3600) // self.time_step_seconds

        # 事件日志（对应 MiroFish 的 actions.jsonl）
        self.event_log: List[Dict[str, Any]] = []

        # 每步指标
        self.step_metrics: List[Dict[str, Any]] = []

        # 区域指标
        self.zone_metrics: Dict[str, ZoneMetrics] = {}

    def initialize(self):
        """
        初始化仿真环境
        对应 MiroFish 的 prepare_simulation
        """
        logger.info(f"初始化仿真: {self.config.simulation_id}")

        # 生成 Agent
        sd_config = self.config.supply_demand_config
        city = self.config.city_config.city_name.lower()
        radius = self.config.city_config.radius_km

        driver_profiles = generate_driver_profiles(sd_config.total_drivers, city, radius)
        for p in driver_profiles:
            self.drivers[p.driver_id] = DriverAgent(p)

        passenger_count = int(sd_config.base_demand_per_hour * self.config.time_config.total_hours * 0.8)
        passenger_count = min(passenger_count, sd_config.total_drivers * 5)
        passenger_profiles = generate_passenger_profiles(passenger_count, city, radius)
        for p in passenger_profiles:
            self.passengers[p.passenger_id] = PassengerAgent(p)

        self.state.total_drivers = len(self.drivers)
        self.state.total_passengers = len(self.passengers)
        self.state.status = SimulationStatus.READY

        logger.info(f"初始化完成: {len(self.drivers)} 司机, {len(self.passengers)} 乘客, "
                    f"{self.total_steps} 步")

    def run(self, progress_callback=None, max_steps: Optional[int] = None):
        """
        运行仿真主循环
        对应 MiroFish SimulationRunner 的 start_simulation
        """
        self.state.status = SimulationStatus.RUNNING
        start_time = time.time()
        steps_to_run = max_steps or self.total_steps

        logger.info(f"开始仿真: {steps_to_run} 步")

        try:
            for step in range(steps_to_run):
                self.current_step = step
                sim_seconds = self.config.time_config.start_hour * 3600 + step * self.time_step_seconds
                current_hour = (sim_seconds // 3600) % 24
                current_minute = (sim_seconds % 3600) // 60

                self.state.current_step = step
                self.state.current_sim_time = f"{current_hour:02d}:{current_minute:02d}"

                # === 仿真主循环 ===
                self._step_driver_decisions(current_hour)
                self._step_passenger_decisions(current_hour, sim_seconds)
                self._step_passenger_bidding(sim_seconds)
                self._step_matching()
                self._step_pre_dispatch(sim_seconds)
                self._step_trip_progress(sim_seconds)
                self._step_pricing_update()
                self._step_order_timeout(sim_seconds)
                self._step_metrics(step, current_hour)

                # 进度回调
                if progress_callback and step % 10 == 0:
                    progress = int(step / steps_to_run * 100)
                    progress_callback(
                        "running", progress,
                        f"步骤 {step}/{steps_to_run}, 时间 {self.state.current_sim_time}",
                        current=step, total=steps_to_run
                    )

            self.state.status = SimulationStatus.COMPLETED
            self.state.elapsed_real_seconds = time.time() - start_time

            self._compute_final_metrics()
            logger.info(f"仿真完成: 耗时 {self.state.elapsed_real_seconds:.1f}s, "
                        f"订单 {self.state.total_orders}, "
                        f"完成 {self.state.completed_orders}, "
                        f"匹配率 {self.state.match_rate:.1%}")

        except Exception as e:
            self.state.status = SimulationStatus.FAILED
            self.state.error = str(e)
            logger.error(f"仿真失败: {e}")
            raise

    # ============== 仿真步骤 ==============

    def _step_driver_decisions(self, current_hour: int):
        """司机上下线决策（对应 MiroFish Agent 的活跃状态变化）"""
        for driver in self.drivers.values():
            if driver.status == DriverStatus.OFFLINE:
                if driver.decide_go_online(current_hour):
                    location = driver.profile.home_location or random_location_in_radius(
                        CITY_CENTERS.get(self.config.city_config.city_name.lower(),
                                         Location(self.config.city_config.center_lat,
                                                  self.config.city_config.center_lng)),
                        self.config.city_config.radius_km * 0.7
                    )
                    driver.go_online(location)
                    self._log_event("driver_online", driver_id=driver.driver_id)

            elif driver.status == DriverStatus.IDLE:
                # 非在线时段则下线
                if current_hour not in driver.profile.online_hours:
                    driver.go_offline()
                    self._log_event("driver_offline", driver_id=driver.driver_id)
                else:
                    # 空闲移动
                    new_loc = driver.decide_idle_movement(self.hotspot_locations)
                    if new_loc:
                        driver.profile.current_location = new_loc

    def _step_passenger_decisions(self, current_hour: int, sim_seconds: int):
        """乘客叫车决策（对应 MiroFish Agent 的发帖行为）"""
        city_center = CITY_CENTERS.get(
            self.config.city_config.city_name.lower(),
            Location(self.config.city_config.center_lat, self.config.city_config.center_lng)
        )

        # 计算当前时段需求倍率
        tc = self.config.time_config
        if current_hour in tc.morning_peak:
            multiplier = tc.morning_peak_multiplier
        elif current_hour in tc.evening_peak:
            multiplier = tc.evening_peak_multiplier
        elif current_hour in tc.off_peak:
            multiplier = tc.off_peak_multiplier
        else:
            multiplier = tc.normal_multiplier

        for passenger in self.passengers.values():
            # 获取乘客所在区域的溢价
            surge = 1.0
            if passenger.profile.home_location:
                hex_id = self.hex_grid.locate(passenger.profile.home_location)
                if hex_id:
                    surge = self.pricing_engine.get_zone_surge(hex_id)

            # 考虑时段倍率的叫车概率
            base_decision = passenger.decide_request_ride(current_hour, surge)
            # 额外用倍率调整（高峰期更多人叫车）
            if not base_decision and multiplier > 1.0:
                import random
                if random.random() < (multiplier - 1.0) * 0.1:
                    base_decision = True

            if base_decision:
                origin, destination = passenger.generate_trip(
                    current_hour, city_center,
                    self.config.city_config.radius_km,
                    self.hotspot_locations
                )

                distance = road_distance(origin, destination)
                duration = estimate_travel_time(distance)

                origin_hex = self.hex_grid.locate(origin) or ""
                dest_hex = self.hex_grid.locate(destination) or ""
                zone_surge = self.pricing_engine.get_zone_surge(origin_hex) if origin_hex else 1.0

                is_off_peak = current_hour in self.config.time_config.off_peak
                # 乘客偏好车型 → 品类定价
                vehicle_category = passenger.profile.preferred_vehicle
                membership = passenger.profile.membership
                fare = self.pricing_engine.calculate_fare(
                    distance, duration, zone_surge, is_off_peak,
                    vehicle_category=vehicle_category, membership=membership)

                order = Order(
                    order_id=f"order_{uuid.uuid4().hex[:10]}",
                    passenger_id=passenger.passenger_id,
                    origin=origin,
                    destination=destination,
                    created_at=sim_seconds,
                    distance_km=round(distance, 2),
                    duration_minutes=round(duration, 1),
                    surge_multiplier=zone_surge,
                    total_fare=fare.total_fare,
                    base_fare=fare.subtotal,
                    vehicle_category=vehicle_category,
                    origin_hex=origin_hex,
                    destination_hex=dest_hex,
                )

                self.orders[order.order_id] = order
                self.pending_orders.append(order.order_id)
                self.state.total_orders += 1

                self._log_event("order_created",
                                order_id=order.order_id,
                                passenger_id=passenger.passenger_id,
                                distance_km=distance,
                                surge=zone_surge,
                                fare=fare.total_fare)

    def _step_passenger_bidding(self, sim_seconds: int):
        """排队乘客加价决策：等待中的乘客可能愿意加价来调度更远的车"""
        for oid in list(self.pending_orders):
            order = self.orders.get(oid)
            if not order or order.status != OrderStatus.PENDING:
                continue

            passenger = self.passengers.get(order.passenger_id)
            if not passenger:
                continue

            wait_seconds = sim_seconds - order.created_at
            if passenger.decide_bid_extra(wait_seconds, order.surge_multiplier):
                # 乘客加价：更新订单的 surge 和费用
                extra_ratio = passenger.profile.extra_surge_ratio
                new_surge = order.surge_multiplier + extra_ratio
                new_surge = min(new_surge, self.pricing_engine.max_surge)
                order.surge_multiplier = round(new_surge, 2)

                # 重新计算费用
                is_off_peak = False  # 加价单不享受平峰优惠
                fare = self.pricing_engine.calculate_fare(
                    order.distance_km, order.duration_minutes, new_surge, is_off_peak)
                order.total_fare = fare.total_fare

                self._log_event("passenger_bid_extra",
                                order_id=order.order_id,
                                passenger_id=order.passenger_id,
                                extra_ratio=extra_ratio,
                                new_surge=new_surge,
                                new_fare=fare.total_fare,
                                wait_seconds=wait_seconds)

    def _step_matching(self):
        """订单匹配（MiroFish 完全没有的核心逻辑）"""
        if not self.pending_orders:
            return

        pending = [self.orders[oid] for oid in self.pending_orders
                   if self.orders[oid].status == OrderStatus.PENDING]
        idle_drivers = [d.profile for d in self.drivers.values()
                        if d.status == DriverStatus.IDLE]

        if not pending or not idle_drivers:
            # 即使没有空闲司机，加价订单可能匹配更远的车（扩大搜索半径）
            if not pending:
                return

        # 对加价乘客扩大匹配搜索半径
        bid_orders = [o for o in pending if self.passengers.get(o.passenger_id)
                      and self.passengers[o.passenger_id].profile.willing_to_pay_extra]
        normal_orders = [o for o in pending if o not in bid_orders]

        # 常规匹配
        if normal_orders and idle_drivers:
            if self.config.matching_config.strategy == "batch":
                matches = self.matching_engine.batch_match(normal_orders, idle_drivers)
            else:
                matches = self.matching_engine.greedy_match(normal_orders, idle_drivers)
            self._apply_matches(matches)

        # 加价订单扩大搜索半径（最大接驾距离 × 1.5）
        if bid_orders:
            remaining_idle = [d.profile for d in self.drivers.values()
                              if d.status == DriverStatus.IDLE]
            if remaining_idle:
                original_max = self.matching_engine.max_pickup_distance_km
                self.matching_engine.max_pickup_distance_km = original_max * 1.5
                bid_matches = self.matching_engine.greedy_match(bid_orders, remaining_idle)
                self.matching_engine.max_pickup_distance_km = original_max
                self._apply_matches(bid_matches, is_bid=True)

    def _step_pre_dispatch(self, sim_seconds: int):
        """
        预派单：即将送达（剩余 ≤ 5 分钟）的司机可以接下一单
        减少司机空闲等待时间，提高整体运力利用率
        """
        if not self.pending_orders:
            return

        pending = [self.orders[oid] for oid in self.pending_orders
                   if self.orders[oid].status == OrderStatus.PENDING]
        if not pending:
            return

        for driver in self.drivers.values():
            if driver.status not in (DriverStatus.IN_TRIP, DriverStatus.PRE_DISPATCHED):
                continue
            if driver.profile.next_order_id is not None:
                continue  # 已有预派单

            current_order = self.orders.get(driver.profile.current_order_id)
            if not current_order or current_order.status != OrderStatus.IN_TRIP:
                continue

            # 计算剩余行程时间
            trip_seconds = current_order.duration_minutes * 60
            elapsed = sim_seconds - (current_order.trip_start_at or sim_seconds)
            remaining = trip_seconds - elapsed

            if not driver.is_pre_dispatchable(remaining):
                continue

            # 为这个即将空闲的司机找一个合适的订单
            # 用行程终点而非当前位置来计算距离
            best_order = None
            best_dist = float('inf')
            for order in pending:
                dist = haversine_distance(current_order.destination, order.origin)
                if dist < self.matching_engine.max_pickup_distance_km and dist < best_dist:
                    best_dist = dist
                    best_order = order

            if best_order and driver.decide_accept_pre_dispatch(best_order, remaining):
                driver.accept_pre_dispatch(best_order.order_id)
                best_order.status = OrderStatus.MATCHED
                best_order.driver_id = driver.driver_id
                best_order.matched_at = sim_seconds
                best_order.pickup_distance_km = best_dist
                best_order.pickup_duration_minutes = (best_dist * 1.3 / max(driver.profile.avg_speed_kmh, 10)) * 60

                if best_order.order_id in self.pending_orders:
                    self.pending_orders.remove(best_order.order_id)

                self._log_event("pre_dispatch",
                                order_id=best_order.order_id,
                                driver_id=driver.driver_id,
                                remaining_seconds=round(remaining, 0),
                                pickup_dist_from_dest=round(best_dist, 2))

    def _apply_matches(self, matches, is_bid: bool = False):
        """应用匹配结果"""
        for match in matches:
            order = self.orders[match.order_id]
            driver = self.drivers[match.driver_id]

            # 司机决定是否接单
            if driver.decide_accept_order(order):
                order.status = OrderStatus.MATCHED
                order.driver_id = match.driver_id
                order.matched_at = order.created_at + 5  # 假设 5 秒匹配
                order.pickup_distance_km = match.pickup_distance_km
                order.pickup_duration_minutes = match.pickup_eta_minutes

                driver.accept_order(order.order_id)

                if order.order_id in self.pending_orders:
                    self.pending_orders.remove(order.order_id)

                event_type = "order_matched_bid" if is_bid else "order_matched"
                self._log_event(event_type,
                                order_id=order.order_id,
                                driver_id=match.driver_id,
                                pickup_dist=match.pickup_distance_km,
                                score=match.score)

    def _step_trip_progress(self, sim_seconds: int):
        """推进行程中的订单（Agent 在地理空间中移动）"""
        for order in list(self.orders.values()):
            if order.status == OrderStatus.MATCHED and order.driver_id:
                driver = self.drivers.get(order.driver_id)
                if not driver:
                    continue

                # 计算接驾进度
                pickup_seconds = order.pickup_duration_minutes * 60
                elapsed = sim_seconds - (order.matched_at or sim_seconds)

                if elapsed >= pickup_seconds:
                    # 到达乘客位置，开始行程
                    order.status = OrderStatus.IN_TRIP
                    order.pickup_at = sim_seconds
                    order.trip_start_at = sim_seconds
                    driver.start_trip()
                    driver.profile.current_location = order.origin

                    self._log_event("trip_started",
                                    order_id=order.order_id,
                                    driver_id=order.driver_id)
                else:
                    # 更新司机位置（向乘客移动）
                    progress = elapsed / max(pickup_seconds, 1)
                    driver.profile.current_location = driver.update_position_during_trip(
                        driver.location, order.origin, min(progress, 1.0)
                    )

            elif order.status == OrderStatus.IN_TRIP and order.driver_id:
                driver = self.drivers.get(order.driver_id)
                if not driver:
                    continue

                trip_seconds = order.duration_minutes * 60
                elapsed = sim_seconds - (order.trip_start_at or sim_seconds)

                if elapsed >= trip_seconds:
                    # 行程完成
                    order.status = OrderStatus.COMPLETED
                    order.completed_at = sim_seconds
                    driver.profile.current_location = order.destination

                    # 司机完成行程（如有预派单会自动切换）
                    has_next = driver.profile.next_order_id is not None
                    driver.complete_trip(order.total_fare)
                    self.state.completed_orders += 1

                    # 重置乘客加价状态
                    passenger = self.passengers.get(order.passenger_id)
                    if passenger:
                        passenger.reset_bid_state()

                    self._log_event("trip_completed",
                                    order_id=order.order_id,
                                    driver_id=order.driver_id,
                                    fare=order.total_fare,
                                    distance=order.distance_km,
                                    has_pre_dispatch=has_next)
                else:
                    # 更新位置
                    progress = elapsed / max(trip_seconds, 1)
                    driver.profile.current_location = driver.update_position_during_trip(
                        order.origin, order.destination, min(progress, 1.0)
                    )

    def _step_pricing_update(self):
        """更新区域溢价（供需动态调节）- 每 10 步更新一次以提高性能"""
        if self.current_step % 10 != 0:
            return

        zone_demand = defaultdict(int)
        zone_supply = defaultdict(int)

        # 统计各区域需求
        for oid in self.pending_orders:
            order = self.orders.get(oid)
            if order and order.origin_hex:
                zone_demand[order.origin_hex] += 1

        # 统计各区域供给
        for driver in self.drivers.values():
            if driver.status == DriverStatus.IDLE and driver.location:
                hex_id = self.hex_grid.locate(driver.location)
                if hex_id:
                    zone_supply[hex_id] += 1

        # 更新溢价
        all_zones = set(zone_demand.keys()) | set(zone_supply.keys())
        for zone_id in all_zones:
            self.pricing_engine.update_zone_surge(
                zone_id,
                zone_demand.get(zone_id, 0),
                zone_supply.get(zone_id, 0)
            )

    def _step_order_timeout(self, sim_seconds: int):
        """处理超时订单"""
        max_wait = self.config.matching_config.max_wait_seconds
        timeout_orders = []

        for oid in list(self.pending_orders):
            order = self.orders.get(oid)
            if not order:
                continue
            if order.status == OrderStatus.PENDING:
                wait_time = sim_seconds - order.created_at
                if wait_time > max_wait:
                    order.status = OrderStatus.TIMEOUT
                    self.state.timeout_orders += 1
                    timeout_orders.append(oid)
                    self._log_event("order_timeout",
                                    order_id=order.order_id,
                                    wait_seconds=wait_time)

        for oid in timeout_orders:
            if oid in self.pending_orders:
                self.pending_orders.remove(oid)

    def _step_metrics(self, step: int, current_hour: int):
        """记录每步指标"""
        online_drivers = sum(1 for d in self.drivers.values()
                             if d.status != DriverStatus.OFFLINE)
        idle_drivers = sum(1 for d in self.drivers.values()
                           if d.status == DriverStatus.IDLE)
        in_trip_drivers = sum(1 for d in self.drivers.values()
                              if d.status in (DriverStatus.IN_TRIP, DriverStatus.PRE_DISPATCHED))
        pre_dispatched = sum(1 for d in self.drivers.values()
                             if d.status == DriverStatus.PRE_DISPATCHED)
        pending_count = len(self.pending_orders)
        bidding_orders = sum(1 for oid in self.pending_orders
                             if self.passengers.get(self.orders[oid].passenger_id)
                             and self.passengers[self.orders[oid].passenger_id].profile.willing_to_pay_extra)

        surges = list(self.pricing_engine.get_all_zone_surges().values())
        avg_surge = sum(surges) / len(surges) if surges else 1.0

        metrics = {
            "step": step,
            "sim_time": self.state.current_sim_time,
            "hour": current_hour,
            "online_drivers": online_drivers,
            "idle_drivers": idle_drivers,
            "in_trip_drivers": in_trip_drivers,
            "pre_dispatched_drivers": pre_dispatched,
            "pending_orders": pending_count,
            "bidding_orders": bidding_orders,
            "total_orders": self.state.total_orders,
            "completed_orders": self.state.completed_orders,
            "timeout_orders": self.state.timeout_orders,
            "avg_surge": round(avg_surge, 2),
        }
        self.step_metrics.append(metrics)

    # ============== 辅助方法 ==============

    def _log_event(self, event_type: str, **kwargs):
        """记录事件（对应 MiroFish 的 actions.jsonl）"""
        event = {
            "step": self.current_step,
            "sim_time": self.state.current_sim_time,
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            **kwargs,
        }
        self.event_log.append(event)

    def _compute_final_metrics(self):
        """计算最终指标"""
        completed = [o for o in self.orders.values() if o.status == OrderStatus.COMPLETED]
        if completed:
            wait_times = [(o.matched_at - o.created_at) for o in completed if o.matched_at]
            self.state.avg_wait_seconds = sum(wait_times) / len(wait_times) if wait_times else 0
            self.state.avg_trip_duration_minutes = sum(o.duration_minutes for o in completed) / len(completed)
            self.state.total_revenue = sum(o.total_fare for o in completed)

        if self.state.total_orders > 0:
            self.state.match_rate = self.state.completed_orders / self.state.total_orders

        surges = [o.surge_multiplier for o in self.orders.values()]
        self.state.avg_surge_multiplier = sum(surges) / len(surges) if surges else 1.0

    def get_results(self) -> Dict[str, Any]:
        """获取仿真结果"""
        return {
            "state": self.state.to_dict(),
            "config": self.config.to_dict(),
            "summary": {
                "total_orders": self.state.total_orders,
                "completed_orders": self.state.completed_orders,
                "cancelled_orders": self.state.cancelled_orders,
                "timeout_orders": self.state.timeout_orders,
                "match_rate": round(self.state.match_rate, 4),
                "avg_wait_seconds": round(self.state.avg_wait_seconds, 1),
                "avg_trip_duration_minutes": round(self.state.avg_trip_duration_minutes, 1),
                "total_revenue": round(self.state.total_revenue, 2),
                "avg_surge": round(self.state.avg_surge_multiplier, 2),
                "total_drivers": self.state.total_drivers,
                "total_passengers": self.state.total_passengers,
            },
            "timeline": self.step_metrics[-100:],  # 最近 100 步
            "event_count": len(self.event_log),
        }

    def save_results(self, output_dir: str):
        """保存仿真结果到文件"""
        os.makedirs(output_dir, exist_ok=True)

        # 状态
        with open(os.path.join(output_dir, "state.json"), 'w', encoding='utf-8') as f:
            json.dump(self.state.to_dict(), f, ensure_ascii=False, indent=2)

        # 配置
        with open(os.path.join(output_dir, "config.json"), 'w', encoding='utf-8') as f:
            json.dump(self.config.to_dict(), f, ensure_ascii=False, indent=2)

        # 时间线指标
        with open(os.path.join(output_dir, "timeline.json"), 'w', encoding='utf-8') as f:
            json.dump(self.step_metrics, f, ensure_ascii=False, indent=2)

        # 事件日志（JSONL 格式，与 MiroFish 一致）
        with open(os.path.join(output_dir, "events.jsonl"), 'w', encoding='utf-8') as f:
            for event in self.event_log:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')

        # 订单摘要
        orders_data = [o.to_dict() for o in self.orders.values()]
        with open(os.path.join(output_dir, "orders.json"), 'w', encoding='utf-8') as f:
            json.dump(orders_data, f, ensure_ascii=False, indent=2)

        logger.info(f"结果已保存到: {output_dir}")
