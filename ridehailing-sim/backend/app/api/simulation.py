"""
仿真 API 路由
对应 MiroFish 的 api/simulation.py
"""

import threading
import traceback
from flask import request, jsonify

from . import simulation_bp
from ..services.simulation_manager import SimulationManager
from ..services.config_generator import SimulationConfigGenerator
from ..utils.logger import get_logger

logger = get_logger('ridehailing.api.simulation')

_manager = SimulationManager()


@simulation_bp.route('/create', methods=['POST'])
def create_simulation():
    """
    创建仿真

    请求（JSON）：
        {
            "project_name": "北京早高峰仿真",
            "description": "模拟北京市工作日早高峰出行场景",
            "city": "beijing",
            "total_drivers": 5000,
            "base_demand_per_hour": 2000,
            "total_hours": 24,
            "matching_strategy": "greedy",
            "pricing_strategy": "dynamic"
        }
    """
    try:
        data = request.get_json() or {}

        config = _manager.create_simulation(
            project_name=data.get("project_name", "默认仿真"),
            description=data.get("description", ""),
            city=data.get("city", "beijing"),
            total_drivers=data.get("total_drivers", 1000),
            base_demand_per_hour=data.get("base_demand_per_hour", 500),
            total_hours=data.get("total_hours", 24),
            matching_strategy=data.get("matching_strategy", "greedy"),
            pricing_strategy=data.get("pricing_strategy", "dynamic"),
        )

        return jsonify({
            "success": True,
            "data": {
                "simulation_id": config.simulation_id,
                "config": config.to_dict(),
                "message": "仿真创建成功，调用 /run 开始运行",
            }
        })

    except Exception as e:
        logger.error(f"创建仿真失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@simulation_bp.route('/create-smart', methods=['POST'])
def create_smart_simulation():
    """
    智能创建仿真（LLM 自动配参）
    对应 MiroFish 的 LLM 配置生成

    请求（JSON）：
        {
            "scenario": "模拟北京暴雨天气对网约车供需的影响",
            "city": "beijing",
            "hours": 24
        }
    """
    try:
        data = request.get_json() or {}
        scenario = data.get("scenario", "")

        if not scenario:
            return jsonify({"success": False, "error": "请提供 scenario 描述"}), 400

        generator = SimulationConfigGenerator()
        config = generator.generate_config(
            scenario_description=scenario,
            city=data.get("city", "beijing"),
            simulation_hours=data.get("hours", 24),
        )

        # 保存配置
        import os, json
        sim_dir = _manager._get_simulation_dir(config.simulation_id)
        with open(os.path.join(sim_dir, "config.json"), 'w', encoding='utf-8') as f:
            f.write(config.to_json())

        from ..models.simulation import SimulationState
        state = SimulationState(simulation_id=config.simulation_id)
        _manager._save_state(state)

        return jsonify({
            "success": True,
            "data": {
                "simulation_id": config.simulation_id,
                "config": config.to_dict(),
                "reasoning": config.generation_reasoning,
                "message": "智能配置生成完成",
            }
        })

    except Exception as e:
        logger.error(f"智能创建失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@simulation_bp.route('/run', methods=['POST'])
def run_simulation():
    """
    运行仿真（异步）

    请求（JSON）：
        {
            "simulation_id": "sim_xxxx",
            "max_steps": 1440  // 可选，限制步数
        }
    """
    try:
        data = request.get_json() or {}
        simulation_id = data.get("simulation_id")

        if not simulation_id:
            return jsonify({"success": False, "error": "请提供 simulation_id"}), 400

        max_steps = data.get("max_steps")

        def run_async():
            try:
                _manager.prepare_and_run(simulation_id, max_steps=max_steps)
            except Exception as e:
                logger.error(f"仿真异步运行失败: {e}")

        thread = threading.Thread(target=run_async, daemon=True)
        thread.start()

        return jsonify({
            "success": True,
            "data": {
                "simulation_id": simulation_id,
                "status": "running",
                "message": "仿真已启动，通过 /status 查询进度",
            }
        })

    except Exception as e:
        logger.error(f"运行仿真失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@simulation_bp.route('/status/<simulation_id>', methods=['GET'])
def get_status(simulation_id: str):
    """获取仿真状态"""
    state = _manager.get_simulation(simulation_id)
    if not state:
        return jsonify({"success": False, "error": "仿真不存在"}), 404

    return jsonify({"success": True, "data": state.to_dict()})


@simulation_bp.route('/results/<simulation_id>', methods=['GET'])
def get_results(simulation_id: str):
    """获取仿真结果"""
    results = _manager.get_results(simulation_id)
    if not results:
        return jsonify({"success": False, "error": "结果不存在"}), 404

    return jsonify({"success": True, "data": results})


@simulation_bp.route('/timeline/<simulation_id>', methods=['GET'])
def get_timeline(simulation_id: str):
    """获取时间线数据"""
    timeline = _manager.get_timeline(simulation_id)
    if not timeline:
        return jsonify({"success": False, "error": "时间线数据不存在"}), 404

    return jsonify({"success": True, "data": timeline})


@simulation_bp.route('/events/<simulation_id>', methods=['GET'])
def get_events(simulation_id: str):
    """获取事件日志"""
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    events = _manager.get_events(simulation_id, limit=limit, offset=offset)
    return jsonify({"success": True, "data": events, "count": len(events)})


@simulation_bp.route('/list', methods=['GET'])
def list_simulations():
    """列出所有仿真"""
    simulations = _manager.list_simulations()
    return jsonify({
        "success": True,
        "data": [s.to_dict() for s in simulations],
        "count": len(simulations),
    })
