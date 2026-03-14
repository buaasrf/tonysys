"""
报告 API 路由
对应 MiroFish 的 api/report.py
"""

import os
import traceback
from flask import request, jsonify, send_file

from . import report_bp
from ..services.simulation_manager import SimulationManager
from ..services.report_agent import ReportAgent
from ..utils.logger import get_logger

logger = get_logger('ridehailing.api.report')

_manager = SimulationManager()


@report_bp.route('/generate', methods=['POST'])
def generate_report():
    """
    生成仿真分析报告

    请求（JSON）：
        {
            "simulation_id": "sim_xxxx"
        }
    """
    try:
        data = request.get_json() or {}
        simulation_id = data.get("simulation_id")

        if not simulation_id:
            return jsonify({"success": False, "error": "请提供 simulation_id"}), 400

        results = _manager.get_results(simulation_id)
        if not results:
            return jsonify({"success": False, "error": "仿真结果不存在，请先运行仿真"}), 404

        agent = ReportAgent(simulation_id, results)
        report = agent.generate_report()

        return jsonify({
            "success": True,
            "data": report,
        })

    except Exception as e:
        logger.error(f"报告生成失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }), 500


@report_bp.route('/<report_id>', methods=['GET'])
def get_report(report_id: str):
    """获取报告"""
    report_dir = os.path.join(ReportAgent.REPORT_DIR, report_id)

    if not os.path.exists(report_dir):
        return jsonify({"success": False, "error": "报告不存在"}), 404

    report_path = os.path.join(report_dir, "full_report.md")
    meta_path = os.path.join(report_dir, "meta.json")

    result = {}
    if os.path.exists(meta_path):
        import json
        with open(meta_path, 'r', encoding='utf-8') as f:
            result["meta"] = json.load(f)

    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            result["markdown_content"] = f.read()

    return jsonify({"success": True, "data": result})


@report_bp.route('/<report_id>/download', methods=['GET'])
def download_report(report_id: str):
    """下载报告"""
    report_path = os.path.join(ReportAgent.REPORT_DIR, report_id, "full_report.md")

    if not os.path.exists(report_path):
        return jsonify({"success": False, "error": "报告不存在"}), 404

    return send_file(report_path, as_attachment=True, download_name=f"{report_id}.md")
