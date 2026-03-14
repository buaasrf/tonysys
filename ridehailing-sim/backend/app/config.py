"""
配置管理
模仿 MiroFish 的配置模式，统一从 .env 文件加载配置
"""

import os
from dotenv import load_dotenv

project_root_env = os.path.join(os.path.dirname(__file__), '../../.env')

if os.path.exists(project_root_env):
    load_dotenv(project_root_env, override=True)
else:
    load_dotenv(override=True)


class Config:
    """Flask 配置类"""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'ridehailing-sim-secret')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    JSON_AS_ASCII = False

    # LLM 配置（用于智能参数生成和报告，复用 MiroFish 模式）
    LLM_API_KEY = os.environ.get('LLM_API_KEY')
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1')
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'gpt-4o-mini')

    # 文件上传配置
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')

    # 仿真配置
    SIMULATION_DATA_DIR = os.path.join(os.path.dirname(__file__), '../uploads/simulations')
    DEFAULT_TIME_STEP_SECONDS = 60  # 默认时间步长: 1 分钟
    DEFAULT_MAX_STEPS = 1440  # 默认最大步数: 24 小时
    DEFAULT_CITY = os.environ.get('DEFAULT_CITY', 'beijing')

    # 地理空间配置
    GEO_GRID_RESOLUTION = int(os.environ.get('GEO_GRID_RESOLUTION', '7'))  # H3 分辨率
    ROAD_NETWORK_CACHE_DIR = os.path.join(os.path.dirname(__file__), '../cache/road_networks')

    # 匹配引擎配置
    MATCHING_INTERVAL_SECONDS = 3  # 匹配周期: 每 3 秒
    MAX_PICKUP_DISTANCE_KM = 5.0  # 最大接驾距离
    MAX_WAIT_TIME_SECONDS = 300  # 最大等待时间: 5 分钟

    # 定价引擎配置
    BASE_FARE = 13.0  # 起步价 (元)
    PER_KM_FARE = 2.3  # 每公里价格 (元)
    PER_MINUTE_FARE = 0.4  # 每分钟价格 (元)
    MIN_SURGE_MULTIPLIER = 1.0
    MAX_SURGE_MULTIPLIER = 3.0

    # Report Agent 配置（复用 MiroFish 模式）
    REPORT_AGENT_MAX_TOOL_CALLS = int(os.environ.get('REPORT_AGENT_MAX_TOOL_CALLS', '5'))
    REPORT_AGENT_TEMPERATURE = float(os.environ.get('REPORT_AGENT_TEMPERATURE', '0.5'))

    @classmethod
    def validate(cls):
        errors = []
        if not cls.LLM_API_KEY:
            errors.append("LLM_API_KEY 未配置（可选，仅影响智能参数生成和报告）")
        return errors
