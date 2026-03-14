"""
乘客 Agent 行为模型
替代 MiroFish 中 OASIS Agent 的社交媒体交互逻辑
实现乘客在出行场景中的决策行为
"""

import random
from typing import Optional, Tuple

from ...models.entities import PassengerProfile, Location, Order
from ..geo.spatial import random_location_in_radius, haversine_distance
from ...utils.logger import get_logger

logger = get_logger('ridehailing.agent.passenger')


class PassengerAgent:
    """
    乘客 Agent
    对应 MiroFish 中 OASIS 的 Agent 实例
    交互模式从「发帖/评论」变为「叫车/等待/取消」
    """

    def __init__(self, profile: PassengerProfile):
        self.profile = profile
        self._last_trip_hour: int = -1

    @property
    def passenger_id(self) -> str:
        return self.profile.passenger_id

    def decide_request_ride(self, current_hour: int, surge_multiplier: float = 1.0) -> bool:
        """
        决策：是否发起叫车请求
        类似 MiroFish Agent 决定是否发帖
        """
        # 基础概率：根据出行模式和时段
        base_prob = self._get_hourly_trip_probability(current_hour)

        # 溢价抑制需求
        if surge_multiplier > self.profile.surge_tolerance:
            # 超过容忍度，需求大幅下降
            base_prob *= 0.1
        elif surge_multiplier > 1.0:
            # 部分抑制
            price_effect = 1.0 - (surge_multiplier - 1.0) * self.profile.price_sensitivity * 0.5
            base_prob *= max(0.2, price_effect)

        # 避免同一小时内重复叫车
        if current_hour == self._last_trip_hour:
            base_prob *= 0.1

        should_request = random.random() < base_prob
        if should_request:
            self._last_trip_hour = current_hour

        return should_request

    def generate_trip(
        self,
        current_hour: int,
        city_center: Location,
        city_radius_km: float,
        hotspot_locations: Optional[list] = None
    ) -> Tuple[Location, Location]:
        """
        生成出行的起终点
        通勤模式：早高峰 家→公司，晚高峰 公司→家
        随机模式：随机起终点
        """
        if self.profile.trip_pattern == "commuter" and self.profile.home_location and self.profile.work_location:
            if current_hour in [7, 8, 9]:
                return self.profile.home_location, self.profile.work_location
            elif current_hour in [17, 18, 19]:
                return self.profile.work_location, self.profile.home_location

        # 随机出行：如果有热点，优先使用热点作为起终点
        if hotspot_locations and len(hotspot_locations) >= 2 and random.random() < 0.6:
            origin_spot = random.choice(hotspot_locations)
            dest_spot = random.choice(hotspot_locations)
            while dest_spot == origin_spot and len(hotspot_locations) > 1:
                dest_spot = random.choice(hotspot_locations)

            origin = random_location_in_radius(origin_spot, 1.0, weight_center=0.5)
            destination = random_location_in_radius(dest_spot, 1.0, weight_center=0.5)
        else:
            origin = random_location_in_radius(city_center, city_radius_km * 0.6, weight_center=0.4)
            destination = random_location_in_radius(city_center, city_radius_km * 0.6, weight_center=0.4)

        # 确保起终点距离合理 (1-30 km)
        dist = haversine_distance(origin, destination)
        while dist < 1.0 or dist > 30.0:
            destination = random_location_in_radius(origin, 8.0, weight_center=0.3)
            dist = haversine_distance(origin, destination)

        return origin, destination

    def decide_cancel(self, wait_seconds: int, surge_multiplier: float = 1.0) -> bool:
        """
        决策：是否取消订单
        等待时间越长、溢价越高，取消概率越大
        """
        # 超过最大等待时间，高概率取消
        max_wait = self.profile.max_wait_minutes * 60
        if wait_seconds > max_wait:
            return random.random() < 0.8

        # 基础取消概率 + 等待时间影响 + 溢价影响
        wait_factor = (wait_seconds / max_wait) ** 2
        surge_factor = max(0, (surge_multiplier - 1.0) * self.profile.price_sensitivity * 0.3)

        cancel_prob = self.profile.cancel_probability + wait_factor * 0.3 + surge_factor
        cancel_prob = min(cancel_prob, 0.9)

        return random.random() < cancel_prob

    def _get_hourly_trip_probability(self, hour: int) -> float:
        """获取每小时的出行概率"""
        # 基于出行模式的时段概率分布
        daily_rate = self.profile.trips_per_day / 24.0  # 平均每小时

        if self.profile.trip_pattern == "commuter":
            hourly_weights = {
                7: 3.0, 8: 4.0, 9: 2.0,  # 早高峰
                12: 1.0, 13: 0.5,  # 午休
                17: 2.0, 18: 4.0, 19: 3.0,  # 晚高峰
                20: 1.0, 21: 0.5,
            }
        elif self.profile.trip_pattern == "nightlife":
            hourly_weights = {
                18: 1.0, 19: 2.0, 20: 3.0, 21: 3.0,
                22: 4.0, 23: 3.0, 0: 2.0, 1: 1.0,
            }
        else:  # random
            hourly_weights = {h: 1.0 for h in range(7, 23)}

        weight = hourly_weights.get(hour, 0.1)
        total_weight = sum(hourly_weights.values())

        return (self.profile.trips_per_day * weight / total_weight)

    def to_dict(self):
        return self.profile.to_dict()
