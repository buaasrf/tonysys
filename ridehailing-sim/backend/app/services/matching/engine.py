"""
订单匹配引擎
这是 MiroFish 完全不具备的核心模块
实现贪心匹配和批量匹配算法
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from ...models.entities import Order, OrderStatus, DriverProfile, DriverStatus, Location
from ..pricing.engine import VEHICLE_TYPE_TO_CATEGORY
from ..geo.spatial import haversine_distance
from ...utils.logger import get_logger

logger = get_logger('ridehailing.matching')


@dataclass
class MatchResult:
    """匹配结果"""
    order_id: str
    driver_id: str
    pickup_distance_km: float
    pickup_eta_minutes: float
    score: float  # 匹配得分（越高越好）


class MatchingEngine:
    """
    匹配引擎
    对应 MiroFish 中不存在的核心调度能力
    """

    def __init__(
        self,
        max_pickup_distance_km: float = 5.0,
        consider_direction: bool = True,
    ):
        self.max_pickup_distance_km = max_pickup_distance_km
        self.consider_direction = consider_direction

    def greedy_match(
        self,
        pending_orders: List[Order],
        idle_drivers: List[DriverProfile],
    ) -> List[MatchResult]:
        """
        贪心匹配：为每个订单找到最近的可用司机
        时间复杂度 O(M*N)，适合中小规模仿真
        """
        results = []
        matched_drivers = set()

        # 按创建时间排序（先到先服务）
        sorted_orders = sorted(pending_orders, key=lambda o: o.created_at)

        for order in sorted_orders:
            best_match = None
            best_score = -1

            for driver in idle_drivers:
                if driver.driver_id in matched_drivers:
                    continue
                if driver.status != DriverStatus.IDLE:
                    continue
                if not driver.current_location:
                    continue

                pickup_dist = haversine_distance(driver.current_location, order.origin)

                if pickup_dist > self.max_pickup_distance_km:
                    continue

                # 品类过滤：premium 订单不匹配 economy 车型
                driver_cat = VEHICLE_TYPE_TO_CATEGORY.get(driver.vehicle_type, "economy")
                order_cat = getattr(order, 'vehicle_category', 'economy')
                if order_cat == "premium" and driver_cat == "economy":
                    continue

                score = self._compute_match_score(order, driver, pickup_dist)

                if score > best_score:
                    best_score = score
                    pickup_eta = (pickup_dist * 1.3 / max(driver.avg_speed_kmh, 10)) * 60
                    best_match = MatchResult(
                        order_id=order.order_id,
                        driver_id=driver.driver_id,
                        pickup_distance_km=pickup_dist,
                        pickup_eta_minutes=pickup_eta,
                        score=score,
                    )

            if best_match:
                results.append(best_match)
                matched_drivers.add(best_match.driver_id)

        return results

    def batch_match(
        self,
        pending_orders: List[Order],
        idle_drivers: List[DriverProfile],
    ) -> List[MatchResult]:
        """
        批量匹配：收集一个时间窗口内的订单和司机，全局最优匹配
        使用贪心近似（真正的最优需要 KM 算法，此处简化）
        """
        # 计算所有可行配对及其得分
        candidates: List[Tuple[float, str, str, float, float]] = []

        for order in pending_orders:
            for driver in idle_drivers:
                if driver.status != DriverStatus.IDLE or not driver.current_location:
                    continue

                pickup_dist = haversine_distance(driver.current_location, order.origin)
                if pickup_dist > self.max_pickup_distance_km:
                    continue

                # 品类过滤
                driver_cat = VEHICLE_TYPE_TO_CATEGORY.get(driver.vehicle_type, "economy")
                order_cat = getattr(order, 'vehicle_category', 'economy')
                if order_cat == "premium" and driver_cat == "economy":
                    continue

                score = self._compute_match_score(order, driver, pickup_dist)
                pickup_eta = (pickup_dist * 1.3 / max(driver.avg_speed_kmh, 10)) * 60
                candidates.append((score, order.order_id, driver.driver_id, pickup_dist, pickup_eta))

        # 按得分降序排列
        candidates.sort(key=lambda x: x[0], reverse=True)

        # 贪心分配（每个订单和司机只匹配一次）
        results = []
        matched_orders = set()
        matched_drivers = set()

        for score, order_id, driver_id, pickup_dist, pickup_eta in candidates:
            if order_id in matched_orders or driver_id in matched_drivers:
                continue

            results.append(MatchResult(
                order_id=order_id,
                driver_id=driver_id,
                pickup_distance_km=pickup_dist,
                pickup_eta_minutes=pickup_eta,
                score=score,
            ))
            matched_orders.add(order_id)
            matched_drivers.add(driver_id)

        return results

    def _compute_match_score(
        self,
        order: Order,
        driver: DriverProfile,
        pickup_distance_km: float,
    ) -> float:
        """计算匹配得分"""
        score = 0.0

        # 1. 距离得分（近距离优先，权重最大）
        distance_score = max(0, (self.max_pickup_distance_km - pickup_distance_km)) / self.max_pickup_distance_km
        score += distance_score * 0.5

        # 2. 司机评分
        rating_score = (driver.rating - 4.0) / 1.0  # 4.0-5.0 -> 0-1
        score += rating_score * 0.15

        # 3. 司机接单率
        score += driver.acceptance_rate * 0.15

        # 4. 行程距离匹配度
        if order.distance_km > 0:
            if driver.distance_preference == "short" and order.distance_km < 5:
                score += 0.1
            elif driver.distance_preference == "long" and order.distance_km > 15:
                score += 0.1
            elif driver.distance_preference == "medium":
                score += 0.05

        # 5. 车型品类匹配
        driver_category = VEHICLE_TYPE_TO_CATEGORY.get(driver.vehicle_type, "economy")
        order_category = getattr(order, 'vehicle_category', 'economy')
        if driver_category == order_category:
            score += 0.15  # 品类完全匹配
        elif driver_category == "comfort" and order_category == "economy":
            score += 0.05  # 舒适型可降级服务经济型
        elif driver_category == "economy" and order_category != "economy":
            score -= 0.2   # 经济型车不适合服务高品类订单

        return score
