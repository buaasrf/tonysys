"""
仿真管理器
改造自 MiroFish 的 simulation_manager.py
保留生命周期管理、状态持久化、进度回调模式
将 Twitter/Reddit 平台管理替换为交通仿真管理
"""

import os
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..config import Config
from ..models.simulation import (
    SimulationConfig, SimulationState, SimulationStatus,
    TimeConfig, CityConfig, SupplyDemandConfig, MatchingConfig, PricingConfig,
)
from .simulation_engine import TransportSimulationEngine
from ..utils.logger import get_logger

logger = get_logger('ridehailing.manager')


class SimulationManager:
    """
    仿真管理器
    保留 MiroFish 的核心管理模式：
    1. create → prepare → run → completed
    2. 状态持久化到 JSON 文件
    3. 进度回调机制
    """

    SIMULATION_DATA_DIR = Config.SIMULATION_DATA_DIR

    def __init__(self):
        os.makedirs(self.SIMULATION_DATA_DIR, exist_ok=True)
        self._simulations: Dict[str, SimulationState] = {}
        self._engines: Dict[str, TransportSimulationEngine] = {}

    def _get_simulation_dir(self, simulation_id: str) -> str:
        sim_dir = os.path.join(self.SIMULATION_DATA_DIR, simulation_id)
        os.makedirs(sim_dir, exist_ok=True)
        return sim_dir

    def _save_state(self, state: SimulationState):
        sim_dir = self._get_simulation_dir(state.simulation_id)
        state.updated_at = datetime.now().isoformat()
        with open(os.path.join(sim_dir, "state.json"), 'w', encoding='utf-8') as f:
            json.dump(state.to_dict(), f, ensure_ascii=False, indent=2)
        self._simulations[state.simulation_id] = state

    def _load_state(self, simulation_id: str) -> Optional[SimulationState]:
        if simulation_id in self._simulations:
            return self._simulations[simulation_id]

        state_file = os.path.join(self._get_simulation_dir(simulation_id), "state.json")
        if not os.path.exists(state_file):
            return None

        with open(state_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        state = SimulationState(
            simulation_id=simulation_id,
            status=SimulationStatus(data.get("status", "created")),
            total_drivers=data.get("total_drivers", 0),
            total_passengers=data.get("total_passengers", 0),
            total_orders=data.get("total_orders", 0),
            current_step=data.get("current_step", 0),
            current_sim_time=data.get("current_sim_time", ""),
            completed_orders=data.get("completed_orders", 0),
            cancelled_orders=data.get("cancelled_orders", 0),
            timeout_orders=data.get("timeout_orders", 0),
            total_revenue=data.get("total_revenue", 0.0),
            avg_wait_seconds=data.get("avg_wait_seconds", 0.0),
            match_rate=data.get("match_rate", 0.0),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            error=data.get("error"),
        )
        self._simulations[simulation_id] = state
        return state

    # ============== 核心方法（对应 MiroFish 的流水线） ==============

    def create_simulation(
        self,
        project_name: str,
        description: str = "",
        city: str = "beijing",
        total_drivers: int = 1000,
        base_demand_per_hour: int = 500,
        total_hours: int = 24,
        matching_strategy: str = "greedy",
        pricing_strategy: str = "dynamic",
    ) -> SimulationConfig:
        """
        创建仿真配置
        对应 MiroFish 的 create_simulation + prepare_simulation 的参数收集
        """
        simulation_id = f"sim_{uuid.uuid4().hex[:12]}"

        config = SimulationConfig(
            simulation_id=simulation_id,
            project_name=project_name,
            description=description,
            time_config=TimeConfig(total_hours=total_hours),
            city_config=CityConfig(city_name=city),
            supply_demand_config=SupplyDemandConfig(
                total_drivers=total_drivers,
                base_demand_per_hour=base_demand_per_hour,
            ),
            matching_config=MatchingConfig(strategy=matching_strategy),
            pricing_config=PricingConfig(strategy=pricing_strategy),
        )

        # 保存配置
        sim_dir = self._get_simulation_dir(simulation_id)
        with open(os.path.join(sim_dir, "config.json"), 'w', encoding='utf-8') as f:
            f.write(config.to_json())

        # 初始化状态
        state = SimulationState(simulation_id=simulation_id)
        self._save_state(state)

        logger.info(f"创建仿真: {simulation_id}, 项目={project_name}, 城市={city}")
        return config

    def prepare_and_run(
        self,
        simulation_id: str,
        progress_callback: Optional[callable] = None,
        max_steps: Optional[int] = None,
    ) -> SimulationState:
        """
        准备并运行仿真
        对应 MiroFish 的 prepare_simulation + SimulationRunner.start_simulation
        """
        state = self._load_state(simulation_id)
        if not state:
            raise ValueError(f"仿真不存在: {simulation_id}")

        sim_dir = self._get_simulation_dir(simulation_id)

        # 加载配置
        config_path = os.path.join(sim_dir, "config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        config = SimulationConfig(
            simulation_id=simulation_id,
            project_name=config_data.get("project_name", ""),
            description=config_data.get("description", ""),
            time_config=TimeConfig(**config_data.get("time_config", {})),
            city_config=CityConfig(**config_data.get("city_config", {})),
            supply_demand_config=SupplyDemandConfig(**config_data.get("supply_demand_config", {})),
            matching_config=MatchingConfig(**config_data.get("matching_config", {})),
            pricing_config=PricingConfig(**config_data.get("pricing_config", {})),
        )

        try:
            # 阶段1: 准备
            state.status = SimulationStatus.PREPARING
            self._save_state(state)

            if progress_callback:
                progress_callback("preparing", 0, "初始化仿真引擎...")

            engine = TransportSimulationEngine(config)
            engine.initialize()
            self._engines[simulation_id] = engine

            state.total_drivers = engine.state.total_drivers
            state.total_passengers = engine.state.total_passengers
            self._save_state(state)

            if progress_callback:
                progress_callback("preparing", 100, "初始化完成")

            # 阶段2: 运行
            engine.run(progress_callback=progress_callback, max_steps=max_steps)

            # 阶段3: 保存结果
            engine.save_results(sim_dir)
            state = engine.state
            self._save_state(state)

            return state

        except Exception as e:
            logger.error(f"仿真执行失败: {simulation_id}, error={str(e)}")
            state.status = SimulationStatus.FAILED
            state.error = str(e)
            self._save_state(state)
            raise

    def get_simulation(self, simulation_id: str) -> Optional[SimulationState]:
        return self._load_state(simulation_id)

    def list_simulations(self) -> List[SimulationState]:
        simulations = []
        if os.path.exists(self.SIMULATION_DATA_DIR):
            for sim_id in os.listdir(self.SIMULATION_DATA_DIR):
                sim_path = os.path.join(self.SIMULATION_DATA_DIR, sim_id)
                if sim_id.startswith('.') or not os.path.isdir(sim_path):
                    continue
                state = self._load_state(sim_id)
                if state:
                    simulations.append(state)
        return simulations

    def get_results(self, simulation_id: str) -> Optional[Dict[str, Any]]:
        engine = self._engines.get(simulation_id)
        if engine:
            return engine.get_results()

        # 从文件加载
        sim_dir = self._get_simulation_dir(simulation_id)
        results = {}

        for filename in ["state.json", "config.json", "timeline.json"]:
            filepath = os.path.join(sim_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    results[filename.replace('.json', '')] = json.load(f)

        return results if results else None

    def get_timeline(self, simulation_id: str) -> Optional[List[Dict]]:
        sim_dir = self._get_simulation_dir(simulation_id)
        filepath = os.path.join(sim_dir, "timeline.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def get_events(self, simulation_id: str, limit: int = 100, offset: int = 0) -> List[Dict]:
        sim_dir = self._get_simulation_dir(simulation_id)
        filepath = os.path.join(sim_dir, "events.jsonl")
        if not os.path.exists(filepath):
            return []

        events = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < offset:
                    continue
                if len(events) >= limit:
                    break
                events.append(json.loads(line))
        return events
