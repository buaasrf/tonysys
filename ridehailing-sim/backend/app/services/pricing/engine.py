"""
动态定价引擎
MiroFish 完全不具备的核心模块
实现供需比驱动的实时价格调节
"""

import math
from typing import Dict
from dataclasses import dataclass

from ...utils.logger import get_logger

logger = get_logger('ridehailing.pricing')


@dataclass
class FareEstimate:
    """费用估算"""
    base_fare: float
    distance_fare: float
    time_fare: float
    subtotal: float
    surge_multiplier: float
    total_fare: float


class PricingEngine:
    """
    动态定价引擎
    """

    def __init__(
        self,
        base_fare: float = 13.0,
        per_km_fare: float = 2.3,
        per_minute_fare: float = 0.4,
        min_surge: float = 1.0,
        max_surge: float = 3.0,
        surge_sensitivity: float = 1.0,
    ):
        self.base_fare = base_fare
        self.per_km_fare = per_km_fare
        self.per_minute_fare = per_minute_fare
        self.min_surge = min_surge
        self.max_surge = max_surge
        self.surge_sensitivity = surge_sensitivity

        # 各区域的溢价缓存
        self._zone_surge: Dict[str, float] = {}

    def calculate_fare(
        self,
        distance_km: float,
        duration_minutes: float,
        surge_multiplier: float = 1.0,
    ) -> FareEstimate:
        """计算订单费用"""
        distance_fare = distance_km * self.per_km_fare
        time_fare = duration_minutes * self.per_minute_fare
        subtotal = self.base_fare + distance_fare + time_fare

        surge = max(self.min_surge, min(self.max_surge, surge_multiplier))
        total = subtotal * surge

        return FareEstimate(
            base_fare=self.base_fare,
            distance_fare=round(distance_fare, 2),
            time_fare=round(time_fare, 2),
            subtotal=round(subtotal, 2),
            surge_multiplier=round(surge, 2),
            total_fare=round(total, 2),
        )

    def compute_surge_multiplier(
        self,
        demand_count: int,
        supply_count: int,
    ) -> float:
        """
        根据供需比计算溢价系数

        核心逻辑：
        - supply/demand > 1.5 → 无溢价 (1.0)
        - supply/demand ≈ 1.0 → 轻微溢价 (1.0-1.3)
        - supply/demand < 0.5 → 高溢价 (1.5-3.0)
        """
        if demand_count == 0:
            return self.min_surge

        if supply_count == 0 and demand_count > 0:
            return self.max_surge

        ratio = supply_count / demand_count

        if ratio >= 1.5:
            return self.min_surge

        # 使用 sigmoid 函数平滑过渡
        # ratio 从 1.5 降到 0 时，surge 从 1.0 升到 max_surge
        x = (1.0 - ratio) * self.surge_sensitivity * 3
        surge = self.min_surge + (self.max_surge - self.min_surge) * (1 / (1 + math.exp(-x)))

        return round(max(self.min_surge, min(self.max_surge, surge)), 2)

    def update_zone_surge(self, zone_id: str, demand: int, supply: int):
        """更新区域溢价"""
        surge = self.compute_surge_multiplier(demand, supply)
        # 平滑更新（避免价格剧烈波动）
        old_surge = self._zone_surge.get(zone_id, 1.0)
        smoothed = old_surge * 0.7 + surge * 0.3
        self._zone_surge[zone_id] = round(smoothed, 2)

    def get_zone_surge(self, zone_id: str) -> float:
        """获取区域溢价"""
        return self._zone_surge.get(zone_id, 1.0)

    def get_all_zone_surges(self) -> Dict[str, float]:
        return dict(self._zone_surge)
