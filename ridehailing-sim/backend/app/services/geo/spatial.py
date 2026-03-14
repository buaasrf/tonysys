"""
地理空间服务
替代 MiroFish 中没有的地理空间能力
提供路网、路径规划、区域划分、距离计算等核心功能
"""

import math
import random
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass

from ...models.entities import Location
from ...utils.logger import get_logger

logger = get_logger('ridehailing.geo')


def haversine_distance(loc1: Location, loc2: Location) -> float:
    """
    计算两点间的球面距离（公里）
    """
    R = 6371.0
    lat1, lng1 = math.radians(loc1.lat), math.radians(loc1.lng)
    lat2, lng2 = math.radians(loc2.lat), math.radians(loc2.lng)

    dlat = lat2 - lat1
    dlng = lng2 - lng1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def estimate_travel_time(distance_km: float, speed_kmh: float = 30.0) -> float:
    """估算行驶时间（分钟），考虑城市道路绕路系数"""
    detour_factor = 1.3  # 城市道路绕路系数
    actual_distance = distance_km * detour_factor
    return (actual_distance / speed_kmh) * 60


def road_distance(loc1: Location, loc2: Location) -> float:
    """
    估算道路距离（公里）
    使用直线距离 × 绕路系数近似
    未来可接入 OSRM/GraphHopper 获取真实路径
    """
    straight = haversine_distance(loc1, loc2)
    return straight * 1.3  # 曼哈顿距离近似


def random_location_in_radius(
    center: Location,
    radius_km: float,
    weight_center: float = 0.3
) -> Location:
    """
    在指定中心和半径内生成随机位置
    weight_center: 越大越集中在中心（模拟城市热点分布）
    """
    # 使用加权随机距离（偏向中心）
    r = radius_km * (random.random() ** (1 / (1 + weight_center)))
    theta = random.uniform(0, 2 * math.pi)

    # 经纬度偏移
    dlat = (r / 111.0) * math.cos(theta)
    dlng = (r / (111.0 * math.cos(math.radians(center.lat)))) * math.sin(theta)

    return Location(
        lat=center.lat + dlat,
        lng=center.lng + dlng
    )


# ============== H3 六边形网格（轻量实现） ==============

class HexGrid:
    """
    六边形网格系统
    轻量化实现，不依赖 h3-py 库
    用于区域划分和供需计算
    """

    def __init__(self, center: Location, radius_km: float, resolution: int = 7):
        self.center = center
        self.radius_km = radius_km
        self.resolution = resolution

        # 根据分辨率计算六边形边长
        # H3 分辨率 7 ≈ 0.66 km² 面积，边长 ≈ 0.5 km
        self._hex_size_km = 1.2 / (2 ** (resolution - 5))

        self._grid: Dict[str, Dict[str, Any]] = {}
        self._build_grid()

    def _build_grid(self):
        """构建覆盖区域的六边形网格"""
        hex_size = self._hex_size_km
        # 简化：使用方形网格近似六边形
        n = int(self.radius_km / hex_size) + 1

        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                lat_offset = i * hex_size / 111.0
                lng_offset = j * hex_size / (111.0 * math.cos(math.radians(self.center.lat)))

                hex_center = Location(
                    lat=self.center.lat + lat_offset,
                    lng=self.center.lng + lng_offset
                )

                dist = haversine_distance(self.center, hex_center)
                if dist <= self.radius_km:
                    hex_id = f"hex_{i + n}_{j + n}"
                    self._grid[hex_id] = {
                        "center": hex_center,
                        "neighbors": [],
                    }

        # 构建邻居关系
        coords = {}
        for hex_id in self._grid:
            parts = hex_id.split("_")
            coords[hex_id] = (int(parts[1]), int(parts[2]))

        for hex_id, (ci, cj) in coords.items():
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    neighbor_id = f"hex_{ci + di}_{cj + dj}"
                    if neighbor_id in self._grid:
                        self._grid[hex_id]["neighbors"].append(neighbor_id)

        logger.info(f"六边形网格构建完成: {len(self._grid)} 个单元格, "
                    f"半径 {self.radius_km}km, 分辨率 {self.resolution}")

    def locate(self, location: Location) -> Optional[str]:
        """定位一个坐标所在的六边形 ID（O(1) 直接计算）"""
        hex_size = self._hex_size_km
        n = int(self.radius_km / hex_size) + 1

        # 直接计算最近的网格索引
        dlat = (location.lat - self.center.lat) * 111.0
        dlng = (location.lng - self.center.lng) * 111.0 * math.cos(math.radians(self.center.lat))

        i = round(dlat / hex_size) + n
        j = round(dlng / hex_size) + n

        hex_id = f"hex_{i}_{j}"
        if hex_id in self._grid:
            return hex_id

        # 如果不在网格内，检查相邻单元格
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                candidate = f"hex_{i + di}_{j + dj}"
                if candidate in self._grid:
                    return candidate

        return None

    def get_hex_center(self, hex_id: str) -> Optional[Location]:
        if hex_id in self._grid:
            return self._grid[hex_id]["center"]
        return None

    def get_neighbors(self, hex_id: str) -> List[str]:
        if hex_id in self._grid:
            return self._grid[hex_id]["neighbors"]
        return []

    def get_all_hex_ids(self) -> List[str]:
        return list(self._grid.keys())

    def get_nearby_hexes(self, hex_id: str, rings: int = 2) -> List[str]:
        """获取指定范围内的所有六边形（BFS）"""
        visited = {hex_id}
        frontier = [hex_id]

        for _ in range(rings):
            next_frontier = []
            for h in frontier:
                for neighbor in self.get_neighbors(h):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_frontier.append(neighbor)
            frontier = next_frontier

        return list(visited)


# ============== 热点区域管理 ==============

@dataclass
class Hotspot:
    """城市热点区域"""
    name: str
    location: Location
    category: str  # residential / commercial / transport_hub / entertainment
    demand_weight: float = 1.0  # 需求权重
    supply_weight: float = 1.0  # 供给权重
    peak_hours: List[int] = None

    def __post_init__(self):
        if self.peak_hours is None:
            if self.category == "residential":
                self.peak_hours = [7, 8, 9, 17, 18, 19]
            elif self.category == "commercial":
                self.peak_hours = [8, 9, 10, 17, 18, 19, 20]
            elif self.category == "transport_hub":
                self.peak_hours = list(range(6, 22))
            elif self.category == "entertainment":
                self.peak_hours = [18, 19, 20, 21, 22, 23]
            else:
                self.peak_hours = list(range(8, 20))


# 预定义城市热点
BEIJING_HOTSPOTS = [
    Hotspot("国贸CBD", Location(39.9087, 116.4605), "commercial", 2.0, 1.5),
    Hotspot("中关村", Location(39.9836, 116.3168), "commercial", 1.8, 1.3),
    Hotspot("西二旗", Location(40.0580, 116.3065), "commercial", 1.5, 1.2),
    Hotspot("望京", Location(39.9908, 116.4747), "commercial", 1.5, 1.2),
    Hotspot("北京站", Location(39.9028, 116.4271), "transport_hub", 1.8, 1.5),
    Hotspot("北京西站", Location(39.8952, 116.3223), "transport_hub", 2.0, 1.5),
    Hotspot("首都机场T3", Location(40.0799, 116.6031), "transport_hub", 2.5, 1.0),
    Hotspot("三里屯", Location(39.9340, 116.4530), "entertainment", 1.5, 1.0),
    Hotspot("天通苑", Location(40.0768, 116.4179), "residential", 2.0, 0.5),
    Hotspot("回龙观", Location(40.0744, 116.3367), "residential", 1.8, 0.5),
    Hotspot("通州", Location(39.9073, 116.6571), "residential", 1.5, 0.3),
]

SHANGHAI_HOTSPOTS = [
    Hotspot("陆家嘴", Location(31.2397, 121.5000), "commercial", 2.5, 1.5),
    Hotspot("人民广场", Location(31.2304, 121.4737), "commercial", 2.0, 1.3),
    Hotspot("虹桥站", Location(31.1949, 121.3319), "transport_hub", 2.0, 1.5),
    Hotspot("浦东机场", Location(31.1443, 121.8083), "transport_hub", 2.5, 1.0),
    Hotspot("张江", Location(31.2027, 121.5907), "commercial", 1.5, 1.2),
    Hotspot("徐家汇", Location(31.1957, 121.4392), "entertainment", 1.5, 1.0),
]

CITY_HOTSPOTS = {
    "beijing": BEIJING_HOTSPOTS,
    "shanghai": SHANGHAI_HOTSPOTS,
}

CITY_CENTERS = {
    "beijing": Location(39.9042, 116.4074),
    "shanghai": Location(31.2304, 121.4737),
}
