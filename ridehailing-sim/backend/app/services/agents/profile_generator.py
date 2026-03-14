"""
Agent Profile 生成器
对应 MiroFish 的 oasis_profile_generator.py
将「社交媒体人设生成」改造为「司机/乘客人设生成」
保留 LLM 驱动的多样化人设创建能力
"""

import random
import uuid
from typing import List, Optional, Dict, Any

from ...models.entities import DriverProfile, PassengerProfile, Location
from ..geo.spatial import random_location_in_radius, CITY_CENTERS
from ...utils.logger import get_logger

logger = get_logger('ridehailing.profile_generator')

# 中国常见姓名
SURNAMES = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴",
            "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗"]
MALE_NAMES = ["伟", "强", "磊", "军", "勇", "杰", "涛", "明", "超", "刚",
              "平", "辉", "鹏", "飞", "志", "建", "斌", "宏", "波", "龙"]
FEMALE_NAMES = ["芳", "娟", "敏", "静", "丽", "玲", "艳", "慧", "婷", "洁",
                "颖", "雪", "红", "萍", "琴", "莉", "燕", "梅", "蓉", "霞"]

VEHICLE_TYPES = ["sedan", "suv", "luxury"]
VEHICLE_WEIGHTS = [0.7, 0.25, 0.05]

STRATEGIES = ["aggressive", "balanced", "conservative"]
STRATEGY_WEIGHTS = [0.2, 0.6, 0.2]

TRIP_PATTERNS = ["commuter", "random", "nightlife"]
TRIP_PATTERN_WEIGHTS = [0.6, 0.3, 0.1]

MEMBERSHIPS = ["normal", "silver", "gold", "platinum"]
MEMBERSHIP_WEIGHTS = [0.5, 0.25, 0.15, 0.1]

PREFERRED_VEHICLES = ["economy", "comfort", "premium"]
PREFERRED_VEHICLE_WEIGHTS = [0.65, 0.28, 0.07]


def _random_name(gender: str = "male") -> str:
    surname = random.choice(SURNAMES)
    if gender == "male":
        given = random.choice(MALE_NAMES)
    else:
        given = random.choice(FEMALE_NAMES)
    return surname + given


def _weighted_choice(items: list, weights: list):
    return random.choices(items, weights=weights, k=1)[0]


def generate_driver_profiles(
    count: int,
    city: str = "beijing",
    city_radius_km: float = 20.0,
) -> List[DriverProfile]:
    """
    批量生成司机 Profile
    对应 MiroFish 的 generate_profiles_from_entities，但使用规则生成
    """
    center = CITY_CENTERS.get(city, CITY_CENTERS["beijing"])
    profiles = []

    for i in range(count):
        gender = "male" if random.random() < 0.85 else "female"  # 司机男性比例高
        home = random_location_in_radius(center, city_radius_km * 0.8)

        # 根据策略设定在线时段
        strategy = _weighted_choice(STRATEGIES, STRATEGY_WEIGHTS)
        if strategy == "aggressive":
            online_hours = list(range(6, 24))   # 全天在线
        elif strategy == "conservative":
            online_hours = list(range(7, 12)) + list(range(17, 22))  # 仅高峰
        else:
            online_hours = list(range(7, 23))   # 白天

        profile = DriverProfile(
            driver_id=f"driver_{uuid.uuid4().hex[:8]}",
            name=_random_name(gender),
            age=random.randint(25, 55),
            gender=gender,
            experience_years=random.randint(1, 10),
            vehicle_type=_weighted_choice(VEHICLE_TYPES, VEHICLE_WEIGHTS),
            home_location=home,
            preferred_zones=[],
            online_hours=online_hours,
            acceptance_rate=random.uniform(0.7, 0.95),
            cancel_rate=random.uniform(0.01, 0.05),
            avg_speed_kmh=random.uniform(20, 40),
            strategy=strategy,
            price_sensitivity=random.uniform(0.3, 0.9),
            distance_preference=random.choice(["short", "medium", "long"]),
            rating=round(random.uniform(4.5, 5.0), 1),
        )
        profiles.append(profile)

    logger.info(f"生成 {count} 个司机 Profile, 城市={city}")
    return profiles


def generate_passenger_profiles(
    count: int,
    city: str = "beijing",
    city_radius_km: float = 20.0,
) -> List[PassengerProfile]:
    """
    批量生成乘客 Profile
    """
    center = CITY_CENTERS.get(city, CITY_CENTERS["beijing"])
    profiles = []

    for i in range(count):
        gender = "male" if random.random() < 0.5 else "female"
        home = random_location_in_radius(center, city_radius_km * 0.7)
        work = random_location_in_radius(center, city_radius_km * 0.5, weight_center=0.5)

        trip_pattern = _weighted_choice(TRIP_PATTERNS, TRIP_PATTERN_WEIGHTS)

        membership = _weighted_choice(MEMBERSHIPS, MEMBERSHIP_WEIGHTS)
        preferred_vehicle = _weighted_choice(PREFERRED_VEHICLES, PREFERRED_VEHICLE_WEIGHTS)

        # 高会员等级的乘客倾向选择更高品类车型
        if membership in ("gold", "platinum") and random.random() < 0.4:
            preferred_vehicle = _weighted_choice(
                ["comfort", "premium"], [0.6, 0.4])

        profile = PassengerProfile(
            passenger_id=f"passenger_{uuid.uuid4().hex[:8]}",
            name=_random_name(gender),
            age=random.randint(18, 60),
            gender=gender,
            home_location=home,
            work_location=work,
            commute_hours=[7, 8, 9, 17, 18, 19],
            trips_per_day=random.uniform(0.5, 3.0),
            price_sensitivity=random.uniform(0.2, 0.9),
            max_wait_minutes=random.uniform(5, 15),
            cancel_probability=random.uniform(0.02, 0.1),
            surge_tolerance=random.uniform(1.3, 2.5),
            trip_pattern=trip_pattern,
            membership=membership,
            preferred_vehicle=preferred_vehicle,
        )
        profiles.append(profile)

    logger.info(f"生成 {count} 个乘客 Profile, 城市={city}")
    return profiles


def generate_driver_profiles_with_llm(
    count: int,
    city: str = "beijing",
    scenario_description: str = "",
    llm_client=None
) -> List[DriverProfile]:
    """
    使用 LLM 智能生成司机 Profile（对应 MiroFish 的 LLM 增强人设生成）
    LLM 根据场景描述生成差异化的司机群体画像
    """
    if not llm_client:
        logger.warning("LLM 未配置，回退到规则生成")
        return generate_driver_profiles(count, city)

    prompt = f"""你是网约车仿真专家。请为以下场景生成 {min(count, 10)} 种司机类型分布。

场景：{scenario_description or f'{city}市日常运营'}

为每种类型返回 JSON：
{{
    "driver_types": [
        {{
            "type_name": "全职老司机",
            "ratio": 0.3,
            "age_range": [35, 50],
            "experience_range": [3, 8],
            "strategy": "balanced",
            "online_hours": [6, 7, ..., 22],
            "acceptance_rate": 0.9,
            "avg_speed_kmh": 35,
            "price_sensitivity": 0.7,
            "distance_preference": "medium"
        }}
    ]
}}

策略选项: aggressive（跑单量）/ balanced（均衡）/ conservative（挑单）
距离偏好: short（短途）/ medium（中距离）/ long（长途）"""

    try:
        result = llm_client.chat_json(
            messages=[
                {"role": "system", "content": "你是网约车运营分析师。返回纯JSON。"},
                {"role": "user", "content": prompt}
            ]
        )

        driver_types = result.get("driver_types", [])
        profiles = []
        center = CITY_CENTERS.get(city, CITY_CENTERS["beijing"])

        for dt in driver_types:
            type_count = max(1, int(count * dt.get("ratio", 0.1)))
            age_range = dt.get("age_range", [25, 50])
            exp_range = dt.get("experience_range", [1, 5])

            for _ in range(type_count):
                if len(profiles) >= count:
                    break

                gender = "male" if random.random() < 0.85 else "female"
                home = random_location_in_radius(center, 20.0)

                profile = DriverProfile(
                    driver_id=f"driver_{uuid.uuid4().hex[:8]}",
                    name=_random_name(gender),
                    age=random.randint(age_range[0], age_range[1]),
                    gender=gender,
                    experience_years=random.randint(exp_range[0], exp_range[1]),
                    vehicle_type=_weighted_choice(VEHICLE_TYPES, VEHICLE_WEIGHTS),
                    home_location=home,
                    online_hours=dt.get("online_hours", list(range(7, 23))),
                    acceptance_rate=dt.get("acceptance_rate", 0.85),
                    avg_speed_kmh=dt.get("avg_speed_kmh", 30) + random.uniform(-5, 5),
                    strategy=dt.get("strategy", "balanced"),
                    price_sensitivity=dt.get("price_sensitivity", 0.5),
                    distance_preference=dt.get("distance_preference", "medium"),
                    rating=round(random.uniform(4.5, 5.0), 1),
                )
                profiles.append(profile)

        # 补足数量
        while len(profiles) < count:
            profiles.extend(generate_driver_profiles(count - len(profiles), city))
            profiles = profiles[:count]

        logger.info(f"LLM 生成 {len(profiles)} 个司机 Profile, {len(driver_types)} 种类型")
        return profiles

    except Exception as e:
        logger.warning(f"LLM 生成失败: {e}, 回退到规则生成")
        return generate_driver_profiles(count, city)
