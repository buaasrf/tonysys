"""
动态定价引擎
MiroFish 完全不具备的核心模块
实现供需比驱动的实时价格调节
"""

import math
import random
from typing import Dict, Optional
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
    vehicle_category: str = "economy"     # 车型品类
    membership_discount: float = 0.0      # 会员折扣减免金额
    promotion_discount: float = 0.0       # 平峰优惠减免金额
    platform_commission: float = 0.0      # 平台抽成
    driver_income: float = 0.0            # 司机实际收入


@dataclass
class VehicleCategoryPricing:
    """车型品类定价"""
    base_fare: float
    per_km_fare: float
    per_minute_fare: float


# 不同品类的定价标准
VEHICLE_CATEGORY_PRICING = {
    # 经济型 (sedan)
    "economy": VehicleCategoryPricing(base_fare=13.0, per_km_fare=1.6, per_minute_fare=0.35),
    # 舒适型 (suv)
    "comfort": VehicleCategoryPricing(base_fare=14.0, per_km_fare=2.3, per_minute_fare=0.4),
    # 豪华型 (luxury)
    "premium": VehicleCategoryPricing(base_fare=25.0, per_km_fare=3.8, per_minute_fare=0.8),
}

# 车型到品类的映射
VEHICLE_TYPE_TO_CATEGORY = {
    "sedan": "economy",
    "suv": "comfort",
    "luxury": "premium",
}

# 会员折扣
MEMBERSHIP_DISCOUNT = {
    "normal": 1.0,       # 无折扣
    "silver": 0.95,      # 95 折
    "gold": 0.90,        # 9 折
    "platinum": 0.88,    # 88 折
}


@dataclass
class PromotionConfig:
    """平峰运营活动配置"""
    enabled: bool = True
    discount_rate: float = 0.15           # 平峰折扣率（85折）
    coupon_probability: float = 0.3       # 乘客获得优惠券的概率
    coupon_amount: float = 3.0            # 优惠券面值（元）
    min_fare_for_coupon: float = 15.0     # 使用优惠券的最低消费
    activity_message: str = "平峰特惠"


class PricingEngine:
    """
    动态定价引擎
    """

    # 平台抽成上限
    MAX_COMMISSION_RATE = 0.27

    def __init__(
        self,
        base_fare: float = 13.0,
        per_km_fare: float = 2.3,
        per_minute_fare: float = 0.4,
        min_surge: float = 1.0,
        max_surge: float = 3.0,
        surge_sensitivity: float = 1.0,
        commission_rate: float = 0.20,
        promotion_config: Optional[PromotionConfig] = None,
    ):
        self.base_fare = base_fare
        self.per_km_fare = per_km_fare
        self.per_minute_fare = per_minute_fare
        self.min_surge = min_surge
        self.max_surge = max_surge
        self.surge_sensitivity = surge_sensitivity
        self.commission_rate = min(commission_rate, self.MAX_COMMISSION_RATE)
        self.promotion_config = promotion_config or PromotionConfig()

        # 各区域的溢价缓存
        self._zone_surge: Dict[str, float] = {}

        # 运营活动统计
        self.promotion_stats = {
            "discount_orders": 0,
            "coupon_orders": 0,
            "total_discount_amount": 0.0,
        }

    def calculate_fare(
        self,
        distance_km: float,
        duration_minutes: float,
        surge_multiplier: float = 1.0,
        is_off_peak: bool = False,
        vehicle_category: str = "economy",
        membership: str = "normal",
    ) -> FareEstimate:
        """计算订单费用，含车型品类定价、会员折扣、平峰优惠和平台抽成"""
        # 根据车型品类获取定价
        category_pricing = VEHICLE_CATEGORY_PRICING.get(
            vehicle_category, VEHICLE_CATEGORY_PRICING["economy"])

        distance_fare = distance_km * category_pricing.per_km_fare
        time_fare = duration_minutes * category_pricing.per_minute_fare
        subtotal = category_pricing.base_fare + distance_fare + time_fare

        surge = max(self.min_surge, min(self.max_surge, surge_multiplier))
        total = subtotal * surge

        # 会员折扣
        membership_rate = MEMBERSHIP_DISCOUNT.get(membership, 1.0)
        membership_discount = 0.0
        if membership_rate < 1.0:
            membership_discount = total * (1.0 - membership_rate)
            total -= membership_discount

        # 平峰运营活动优惠
        promotion_discount = 0.0
        if is_off_peak and self.promotion_config.enabled and surge <= 1.0:
            # 折扣优惠
            discount = total * self.promotion_config.discount_rate
            promotion_discount += discount

            # 随机优惠券
            if (total >= self.promotion_config.min_fare_for_coupon
                    and random.random() < self.promotion_config.coupon_probability):
                promotion_discount += self.promotion_config.coupon_amount
                self.promotion_stats["coupon_orders"] += 1

            self.promotion_stats["discount_orders"] += 1
            self.promotion_stats["total_discount_amount"] += promotion_discount

        total_after_discount = max(category_pricing.base_fare, total - promotion_discount)

        # 平台抽成（上限 27%）
        effective_commission_rate = min(self.commission_rate, self.MAX_COMMISSION_RATE)
        platform_commission = round(total_after_discount * effective_commission_rate, 2)
        driver_income = round(total_after_discount - platform_commission, 2)

        return FareEstimate(
            base_fare=category_pricing.base_fare,
            distance_fare=round(distance_fare, 2),
            time_fare=round(time_fare, 2),
            subtotal=round(subtotal, 2),
            surge_multiplier=round(surge, 2),
            total_fare=round(total_after_discount, 2),
            vehicle_category=vehicle_category,
            membership_discount=round(membership_discount, 2),
            promotion_discount=round(promotion_discount, 2),
            platform_commission=platform_commission,
            driver_income=driver_income,
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
