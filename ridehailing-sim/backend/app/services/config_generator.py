"""
仿真配置智能生成器
改造自 MiroFish 的 simulation_config_generator.py
将「社交媒体行为参数」替换为「网约车运营参数」
保留 LLM 驱动的智能配置生成能力
"""

import json
from typing import Optional, Dict, Any

from ..config import Config
from ..models.simulation import (
    SimulationConfig, TimeConfig, CityConfig,
    SupplyDemandConfig, MatchingConfig, PricingConfig,
)
from ..utils.llm_client import LLMClient
from ..utils.logger import get_logger

logger = get_logger('ridehailing.config_gen')

# 中国城市出行时段配置（对应 MiroFish 的 CHINA_TIMEZONE_CONFIG）
CHINA_TRAFFIC_CONFIG = {
    "早高峰": {"hours": [7, 8, 9], "demand_multiplier": 2.5, "description": "通勤上班，需求集中"},
    "上午": {"hours": [10, 11], "demand_multiplier": 1.0, "description": "需求平稳"},
    "午间": {"hours": [12, 13], "demand_multiplier": 1.3, "description": "午餐出行小高峰"},
    "下午": {"hours": [14, 15, 16], "demand_multiplier": 0.9, "description": "需求平稳偏低"},
    "晚高峰": {"hours": [17, 18, 19], "demand_multiplier": 3.0, "description": "通勤下班+社交，全天最高"},
    "晚间": {"hours": [20, 21, 22], "demand_multiplier": 1.5, "description": "娱乐出行"},
    "深夜": {"hours": [23, 0, 1], "demand_multiplier": 0.5, "description": "夜间出行减少"},
    "凌晨": {"hours": [2, 3, 4, 5, 6], "demand_multiplier": 0.1, "description": "几乎无需求"},
}


class SimulationConfigGenerator:
    """
    仿真配置智能生成器
    对应 MiroFish 的 SimulationConfigGenerator
    使用 LLM 根据场景描述自动生成最优仿真参数
    """

    def __init__(self):
        self.llm_client = None
        try:
            self.llm_client = LLMClient()
        except ValueError:
            logger.warning("LLM 未配置，将使用规则生成配置")

    def generate_config(
        self,
        scenario_description: str,
        city: str = "beijing",
        simulation_hours: int = 24,
    ) -> SimulationConfig:
        """
        智能生成仿真配置
        对应 MiroFish 的 generate_config 方法
        """
        if self.llm_client:
            try:
                return self._generate_with_llm(scenario_description, city, simulation_hours)
            except Exception as e:
                logger.warning(f"LLM 配置生成失败: {e}, 回退到规则生成")

        return self._generate_with_rules(scenario_description, city, simulation_hours)

    def _generate_with_llm(
        self,
        scenario_description: str,
        city: str,
        simulation_hours: int,
    ) -> SimulationConfig:
        """使用 LLM 生成配置（对应 MiroFish 的 LLM 配置生成）"""
        prompt = f"""你是网约车运营专家。请根据以下场景生成仿真配置参数。

## 场景描述
{scenario_description}

## 城市: {city}
## 仿真时长: {simulation_hours} 小时

## 中国城市出行特征参考
{json.dumps(CHINA_TRAFFIC_CONFIG, ensure_ascii=False, indent=2)}

请返回 JSON 格式的仿真配置：
{{
    "total_drivers": <司机总数, 1000-100000>,
    "base_demand_per_hour": <基础每小时需求量, 100-50000>,
    "morning_peak_multiplier": <早高峰需求倍率, 1.5-4.0>,
    "evening_peak_multiplier": <晚高峰需求倍率, 2.0-5.0>,
    "off_peak_multiplier": <低谷需求倍率, 0.05-0.3>,
    "online_rate_peak": <高峰在线率, 0.5-0.95>,
    "online_rate_offpeak": <平峰在线率, 0.1-0.5>,
    "matching_strategy": "greedy 或 batch",
    "max_pickup_distance_km": <最大接驾距离, 2-8>,
    "base_fare": <起步价, 8-20>,
    "per_km_fare": <每公里价格, 1.5-4.0>,
    "max_surge": <最大溢价倍率, 1.5-5.0>,
    "surge_sensitivity": <溢价灵敏度, 0.5-2.0>,
    "avg_trip_distance_km": <平均行程距离, 3-15>,
    "reasoning": "<配置推理说明>"
}}"""

        result = self.llm_client.chat_json(
            messages=[
                {"role": "system", "content": "你是网约车运营分析专家。返回纯JSON配置。"},
                {"role": "user", "content": prompt}
            ]
        )

        import uuid
        config = SimulationConfig(
            simulation_id=f"sim_{uuid.uuid4().hex[:12]}",
            project_name=scenario_description[:50],
            description=scenario_description,
            time_config=TimeConfig(
                total_hours=simulation_hours,
                morning_peak_multiplier=result.get("morning_peak_multiplier", 2.5),
                evening_peak_multiplier=result.get("evening_peak_multiplier", 3.0),
                off_peak_multiplier=result.get("off_peak_multiplier", 0.2),
            ),
            city_config=CityConfig(city_name=city),
            supply_demand_config=SupplyDemandConfig(
                total_drivers=result.get("total_drivers", 5000),
                base_demand_per_hour=result.get("base_demand_per_hour", 2000),
                online_rate_peak=result.get("online_rate_peak", 0.8),
                online_rate_offpeak=result.get("online_rate_offpeak", 0.3),
                avg_trip_distance_km=result.get("avg_trip_distance_km", 8.0),
            ),
            matching_config=MatchingConfig(
                strategy=result.get("matching_strategy", "greedy"),
                max_pickup_distance_km=result.get("max_pickup_distance_km", 5.0),
            ),
            pricing_config=PricingConfig(
                strategy="dynamic",
                base_fare=result.get("base_fare", 13.0),
                per_km_fare=result.get("per_km_fare", 2.3),
                max_surge=result.get("max_surge", 3.0),
                surge_sensitivity=result.get("surge_sensitivity", 1.0),
            ),
            generation_reasoning=result.get("reasoning", "LLM 生成"),
        )

        logger.info(f"LLM 生成配置完成: {config.simulation_id}")
        return config

    def _generate_with_rules(
        self,
        scenario_description: str,
        city: str,
        simulation_hours: int,
    ) -> SimulationConfig:
        """规则生成默认配置"""
        import uuid

        # 根据城市规模调整参数
        city_scale = {
            "beijing": (10000, 5000),
            "shanghai": (10000, 5000),
            "guangzhou": (8000, 4000),
            "shenzhen": (8000, 4000),
        }
        drivers, demand = city_scale.get(city.lower(), (5000, 2000))

        config = SimulationConfig(
            simulation_id=f"sim_{uuid.uuid4().hex[:12]}",
            project_name=scenario_description[:50] if scenario_description else f"{city}网约车仿真",
            description=scenario_description,
            time_config=TimeConfig(total_hours=simulation_hours),
            city_config=CityConfig(city_name=city),
            supply_demand_config=SupplyDemandConfig(
                total_drivers=drivers,
                base_demand_per_hour=demand,
            ),
            matching_config=MatchingConfig(strategy="greedy"),
            pricing_config=PricingConfig(strategy="dynamic"),
            generation_reasoning="规则生成默认配置",
        )

        return config
