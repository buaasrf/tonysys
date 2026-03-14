"""
网约车仿真核心数据模型
对应 MiroFish 的 models/project.py + models/task.py
在此统一定义所有仿真实体
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Tuple


# ============== 地理坐标 ==============

@dataclass
class Location:
    """地理坐标"""
    lat: float
    lng: float

    def to_tuple(self) -> Tuple[float, float]:
        return (self.lat, self.lng)

    def to_dict(self) -> Dict[str, float]:
        return {"lat": self.lat, "lng": self.lng}


# ============== 订单相关 ==============

class OrderStatus(str, Enum):
    PENDING = "pending"           # 等待匹配
    MATCHED = "matched"           # 已匹配，等待接驾
    PICKUP = "pickup"             # 司机前往接乘客
    IN_TRIP = "in_trip"           # 行程中
    COMPLETED = "completed"       # 已完成
    CANCELLED = "cancelled"       # 已取消
    TIMEOUT = "timeout"           # 超时未匹配


@dataclass
class Order:
    """出行订单"""
    order_id: str
    passenger_id: str
    origin: Location
    destination: Location

    # 时间戳
    created_at: int = 0          # 创建时间（仿真秒）
    matched_at: Optional[int] = None
    pickup_at: Optional[int] = None
    trip_start_at: Optional[int] = None
    completed_at: Optional[int] = None
    cancelled_at: Optional[int] = None

    # 匹配信息
    driver_id: Optional[str] = None
    status: OrderStatus = OrderStatus.PENDING

    # 行程信息
    distance_km: float = 0.0     # 行程距离
    duration_minutes: float = 0.0  # 行程时长
    pickup_distance_km: float = 0.0  # 接驾距离
    pickup_duration_minutes: float = 0.0  # 接驾时长

    # 费用
    base_fare: float = 0.0
    surge_multiplier: float = 1.0
    total_fare: float = 0.0

    # 车型品类
    vehicle_category: str = "economy"  # economy / comfort / premium

    # 区域信息
    origin_hex: str = ""         # H3 六边形 ID
    destination_hex: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "order_id": self.order_id,
            "passenger_id": self.passenger_id,
            "driver_id": self.driver_id,
            "origin": self.origin.to_dict(),
            "destination": self.destination.to_dict(),
            "status": self.status.value,
            "created_at": self.created_at,
            "matched_at": self.matched_at,
            "pickup_at": self.pickup_at,
            "trip_start_at": self.trip_start_at,
            "completed_at": self.completed_at,
            "distance_km": self.distance_km,
            "duration_minutes": self.duration_minutes,
            "pickup_distance_km": self.pickup_distance_km,
            "total_fare": self.total_fare,
            "surge_multiplier": self.surge_multiplier,
            "origin_hex": self.origin_hex,
            "destination_hex": self.destination_hex,
        }


# ============== 司机相关 ==============

class DriverStatus(str, Enum):
    OFFLINE = "offline"           # 不在线
    IDLE = "idle"                 # 空闲等单
    DISPATCHED = "dispatched"     # 已派单，前往接客
    IN_TRIP = "in_trip"           # 载客中
    PRE_DISPATCHED = "pre_dispatched"  # 行程即将结束，已预派下一单
    RETURNING = "returning"       # 送完客回程


@dataclass
class DriverProfile:
    """
    司机 Agent 档案
    对应 MiroFish 的 OasisAgentProfile
    """
    driver_id: str
    name: str

    # 基础属性
    age: int = 35
    gender: str = "male"
    experience_years: int = 3
    vehicle_type: str = "sedan"    # sedan / suv / luxury

    # 行为参数
    home_location: Optional[Location] = None
    preferred_zones: List[str] = field(default_factory=list)  # H3 hex IDs
    online_hours: List[int] = field(default_factory=lambda: list(range(7, 23)))
    acceptance_rate: float = 0.85  # 接单率
    cancel_rate: float = 0.02     # 取消率
    avg_speed_kmh: float = 30.0   # 平均车速

    # 性格特征（类似 MiroFish 的 persona）
    strategy: str = "balanced"     # aggressive / balanced / conservative
    price_sensitivity: float = 0.5  # 对价格的敏感度 0-1
    distance_preference: str = "medium"  # short / medium / long

    # 运行时状态
    status: DriverStatus = DriverStatus.OFFLINE
    current_location: Optional[Location] = None
    current_order_id: Optional[str] = None
    next_order_id: Optional[str] = None   # 预派单（行程结束前5分钟可接下一单）

    # 统计
    total_trips: int = 0
    total_revenue: float = 0.0
    rating: float = 4.8

    def to_dict(self) -> Dict[str, Any]:
        return {
            "driver_id": self.driver_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "experience_years": self.experience_years,
            "vehicle_type": self.vehicle_type,
            "strategy": self.strategy,
            "acceptance_rate": self.acceptance_rate,
            "online_hours": self.online_hours,
            "avg_speed_kmh": self.avg_speed_kmh,
            "status": self.status.value,
            "current_location": self.current_location.to_dict() if self.current_location else None,
            "total_trips": self.total_trips,
            "total_revenue": self.total_revenue,
            "rating": self.rating,
        }


# ============== 乘客相关 ==============

@dataclass
class PassengerProfile:
    """
    乘客 Agent 档案
    对应 MiroFish 的 OasisAgentProfile
    """
    passenger_id: str
    name: str

    # 基础属性
    age: int = 30
    gender: str = "female"

    # 行为参数
    home_location: Optional[Location] = None
    work_location: Optional[Location] = None
    commute_hours: List[int] = field(default_factory=lambda: [8, 9, 17, 18])
    trips_per_day: float = 1.5

    # 偏好
    price_sensitivity: float = 0.6  # 价格敏感度 0-1
    max_wait_minutes: float = 8.0   # 最大等待时间
    cancel_probability: float = 0.05  # 取消概率
    surge_tolerance: float = 1.5     # 最大可接受溢价倍数

    # 出行模式
    trip_pattern: str = "commuter"   # commuter / random / nightlife

    # 会员等级: normal / silver / gold / platinum
    membership: str = "normal"
    # 偏好车型: economy / comfort / premium (对应 sedan / suv / luxury)
    preferred_vehicle: str = "economy"

    # 排队加价意愿：愿意加价调度更远的车
    willing_to_pay_extra: bool = False      # 是否愿意加价
    extra_surge_ratio: float = 0.0          # 额外加价比例 (0.2 = 加价20%)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passenger_id": self.passenger_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "price_sensitivity": self.price_sensitivity,
            "max_wait_minutes": self.max_wait_minutes,
            "surge_tolerance": self.surge_tolerance,
            "trip_pattern": self.trip_pattern,
            "trips_per_day": self.trips_per_day,
        }


# ============== 区域统计 ==============

@dataclass
class ZoneMetrics:
    """区域指标（用于预测和报告）"""
    hex_id: str
    time_step: int

    # 供需
    demand_count: int = 0          # 需求量（订单数）
    supply_count: int = 0          # 供给量（空闲司机数）
    supply_demand_ratio: float = 0.0

    # 匹配
    matched_count: int = 0
    match_rate: float = 0.0
    avg_wait_seconds: float = 0.0
    avg_pickup_distance_km: float = 0.0

    # 定价
    surge_multiplier: float = 1.0
    avg_fare: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hex_id": self.hex_id,
            "time_step": self.time_step,
            "demand_count": self.demand_count,
            "supply_count": self.supply_count,
            "supply_demand_ratio": self.supply_demand_ratio,
            "matched_count": self.matched_count,
            "match_rate": self.match_rate,
            "avg_wait_seconds": self.avg_wait_seconds,
            "surge_multiplier": self.surge_multiplier,
            "avg_fare": self.avg_fare,
        }
