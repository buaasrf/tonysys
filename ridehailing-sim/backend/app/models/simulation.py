"""
仿真状态与配置模型
对应 MiroFish 的 SimulationState + SimulationParameters
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional


class SimulationStatus(str, Enum):
    """仿真状态（复用 MiroFish 的状态机模式）"""
    CREATED = "created"
    PREPARING = "preparing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"
    FAILED = "failed"


# ============== 仿真配置（对应 MiroFish 的 SimulationParameters） ==============

@dataclass
class TimeConfig:
    """时间配置（对应 MiroFish 的 TimeSimulationConfig）"""
    # 仿真时间范围
    start_hour: int = 0            # 仿真起始小时 (0-23)
    total_hours: int = 24          # 仿真总时长（小时）
    time_step_seconds: int = 60    # 每步长代表的秒数

    # 高峰/平峰定义（中国城市出行特征）
    morning_peak: List[int] = field(default_factory=lambda: [7, 8, 9])
    evening_peak: List[int] = field(default_factory=lambda: [17, 18, 19])
    off_peak: List[int] = field(default_factory=lambda: [0, 1, 2, 3, 4, 5, 22, 23])

    # 需求倍率
    morning_peak_multiplier: float = 2.5
    evening_peak_multiplier: float = 3.0
    off_peak_multiplier: float = 0.2
    normal_multiplier: float = 1.0


@dataclass
class CityConfig:
    """城市配置"""
    city_name: str = "北京"
    center_lat: float = 39.9042
    center_lng: float = 116.4074
    radius_km: float = 20.0       # 仿真区域半径
    h3_resolution: int = 7        # H3 六边形分辨率

    # 热点区域（POI）
    hotspots: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SupplyDemandConfig:
    """供需配置"""
    # 需求
    base_demand_per_hour: int = 5000      # 基础每小时需求量
    demand_distribution: str = "poisson"   # poisson / uniform / historical

    # 供给
    total_drivers: int = 10000
    online_rate_peak: float = 0.8          # 高峰在线率
    online_rate_offpeak: float = 0.3       # 平峰在线率

    # 行为
    avg_trip_distance_km: float = 8.0
    avg_trip_duration_minutes: float = 25.0


@dataclass
class MatchingConfig:
    """匹配策略配置"""
    strategy: str = "greedy"        # greedy / batch / optimal
    batch_interval_seconds: int = 3
    max_pickup_distance_km: float = 5.0
    max_wait_seconds: int = 300
    consider_direction: bool = True  # 是否考虑司机行驶方向


@dataclass
class PricingConfig:
    """定价策略配置"""
    strategy: str = "dynamic"       # fixed / dynamic / ml_based
    base_fare: float = 13.0
    per_km_fare: float = 2.3
    per_minute_fare: float = 0.4
    min_surge: float = 1.0
    max_surge: float = 3.0
    surge_sensitivity: float = 1.0   # 溢价灵敏度


@dataclass
class SimulationConfig:
    """
    完整仿真配置
    对应 MiroFish 的 SimulationParameters
    """
    simulation_id: str
    project_name: str
    description: str = ""

    time_config: TimeConfig = field(default_factory=TimeConfig)
    city_config: CityConfig = field(default_factory=CityConfig)
    supply_demand_config: SupplyDemandConfig = field(default_factory=SupplyDemandConfig)
    matching_config: MatchingConfig = field(default_factory=MatchingConfig)
    pricing_config: PricingConfig = field(default_factory=PricingConfig)

    # LLM 生成元数据（复用 MiroFish 模式）
    generation_reasoning: str = ""
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "project_name": self.project_name,
            "description": self.description,
            "time_config": asdict(self.time_config),
            "city_config": asdict(self.city_config),
            "supply_demand_config": asdict(self.supply_demand_config),
            "matching_config": asdict(self.matching_config),
            "pricing_config": asdict(self.pricing_config),
            "generation_reasoning": self.generation_reasoning,
            "generated_at": self.generated_at,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============== 仿真状态（对应 MiroFish 的 SimulationState） ==============

@dataclass
class SimulationState:
    """仿真运行时状态"""
    simulation_id: str
    status: SimulationStatus = SimulationStatus.CREATED

    # 规模
    total_drivers: int = 0
    total_passengers: int = 0
    total_orders: int = 0

    # 运行时
    current_step: int = 0
    current_sim_time: str = ""   # HH:MM 格式
    elapsed_real_seconds: float = 0.0

    # 聚合指标
    completed_orders: int = 0
    cancelled_orders: int = 0
    timeout_orders: int = 0
    total_revenue: float = 0.0
    avg_wait_seconds: float = 0.0
    avg_trip_duration_minutes: float = 0.0
    avg_surge_multiplier: float = 1.0
    match_rate: float = 0.0

    # 时间戳
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "status": self.status.value,
            "total_drivers": self.total_drivers,
            "total_passengers": self.total_passengers,
            "total_orders": self.total_orders,
            "current_step": self.current_step,
            "current_sim_time": self.current_sim_time,
            "completed_orders": self.completed_orders,
            "cancelled_orders": self.cancelled_orders,
            "timeout_orders": self.timeout_orders,
            "total_revenue": self.total_revenue,
            "avg_wait_seconds": self.avg_wait_seconds,
            "avg_trip_duration_minutes": self.avg_trip_duration_minutes,
            "avg_surge_multiplier": self.avg_surge_multiplier,
            "match_rate": self.match_rate,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "error": self.error,
        }
