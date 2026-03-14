"""
司机 Agent 行为模型
替代 MiroFish 中 OASIS Agent 的社交媒体交互逻辑
实现司机在出行场景中的决策行为
"""

import random
from typing import Optional, List

from ...models.entities import (
    DriverProfile, DriverStatus, Order, Location
)
from ..geo.spatial import haversine_distance, random_location_in_radius
from ...utils.logger import get_logger

logger = get_logger('ridehailing.agent.driver')


class DriverAgent:
    """
    司机 Agent
    对应 MiroFish 中 OASIS 的 Agent 实例
    但交互模式从「发帖/评论」变为「接单/行驶/送客」
    """

    def __init__(self, profile: DriverProfile):
        self.profile = profile

    @property
    def driver_id(self) -> str:
        return self.profile.driver_id

    @property
    def status(self) -> DriverStatus:
        return self.profile.status

    @property
    def location(self) -> Optional[Location]:
        return self.profile.current_location

    def decide_go_online(self, current_hour: int) -> bool:
        """决定是否上线（类似 MiroFish Agent 决定是否发帖）"""
        if current_hour in self.profile.online_hours:
            # 基础上线概率 + 随机波动
            base_prob = 0.9 if self.profile.strategy == "aggressive" else 0.7
            return random.random() < base_prob
        return False

    def decide_accept_order(self, order: Order) -> bool:
        """
        决策：是否接受订单
        类似 MiroFish Agent 决定对帖子的态度，但这里是经济理性决策
        """
        if self.profile.status != DriverStatus.IDLE:
            return False

        pickup_dist = haversine_distance(self.profile.current_location, order.origin)

        # 距离太远，拒绝
        if pickup_dist > 5.0:
            return False

        # 综合评估
        score = 0.0

        # 接驾距离（近的更好）
        score += max(0, (5.0 - pickup_dist) / 5.0) * 0.3

        # 行程距离（根据偏好）
        trip_dist = order.distance_km
        if self.profile.distance_preference == "short" and trip_dist < 5:
            score += 0.3
        elif self.profile.distance_preference == "long" and trip_dist > 15:
            score += 0.3
        else:
            score += 0.15

        # 溢价（价格敏感的司机更喜欢溢价单）
        surge_bonus = (order.surge_multiplier - 1.0) * self.profile.price_sensitivity
        score += min(surge_bonus, 0.3)

        # 策略影响
        if self.profile.strategy == "aggressive":
            score += 0.1  # 激进型更容易接单
        elif self.profile.strategy == "conservative":
            score -= 0.1

        # 基础接单率
        accept_prob = self.profile.acceptance_rate * (0.5 + score)
        accept_prob = max(0.1, min(1.0, accept_prob))

        return random.random() < accept_prob

    def decide_idle_movement(self, hotspot_locations: List[Location]) -> Optional[Location]:
        """
        空闲时的移动决策
        类似 MiroFish Agent 的自主行为，但这里是空间移动
        """
        if self.profile.status != DriverStatus.IDLE:
            return None

        # 30% 概率保持不动
        if random.random() < 0.3:
            return None

        # 50% 概率向最近热点移动
        if hotspot_locations and random.random() < 0.5:
            nearest = min(
                hotspot_locations,
                key=lambda h: haversine_distance(self.profile.current_location, h)
            )
            # 向热点方向移动一小段距离
            move_ratio = random.uniform(0.1, 0.3)
            new_lat = self.location.lat + (nearest.lat - self.location.lat) * move_ratio
            new_lng = self.location.lng + (nearest.lng - self.location.lng) * move_ratio
            return Location(lat=new_lat, lng=new_lng)

        # 20% 概率随机漫游
        return random_location_in_radius(self.profile.current_location, 1.0)

    def update_position_during_trip(
        self,
        origin: Location,
        destination: Location,
        progress: float  # 0.0 - 1.0
    ) -> Location:
        """行程中更新位置（线性插值近似）"""
        lat = origin.lat + (destination.lat - origin.lat) * progress
        lng = origin.lng + (destination.lng - origin.lng) * progress
        return Location(lat=lat, lng=lng)

    def complete_trip(self, fare: float):
        """完成行程"""
        self.profile.total_trips += 1
        self.profile.total_revenue += fare
        self.profile.status = DriverStatus.IDLE
        self.profile.current_order_id = None

    def go_online(self, location: Location):
        self.profile.status = DriverStatus.IDLE
        self.profile.current_location = location

    def go_offline(self):
        self.profile.status = DriverStatus.OFFLINE
        self.profile.current_order_id = None

    def accept_order(self, order_id: str):
        self.profile.status = DriverStatus.DISPATCHED
        self.profile.current_order_id = order_id

    def start_trip(self):
        self.profile.status = DriverStatus.IN_TRIP

    def to_dict(self):
        return self.profile.to_dict()
