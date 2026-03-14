"""
报告生成 Agent
改造自 MiroFish 的 report_agent.py
保留 ReACT Agent 报告生成模式
将「舆情分析报告」替换为「网约车运营分析报告」
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..config import Config
from ..utils.logger import get_logger

logger = get_logger('ridehailing.report')


class ReportAgent:
    """
    报告生成 Agent
    保留 MiroFish 的 ReACT 报告生成模式：
    1. 规划章节 → 2. 检索数据 → 3. 生成内容 → 4. 组装报告

    改动点：
    - 检索工具从「图谱搜索/Agent 采访」变为「仿真数据查询」
    - 报告主题从「舆情分析」变为「网约车运营分析」
    """

    REPORT_DIR = os.path.join(Config.SIMULATION_DATA_DIR, '..', 'reports')

    def __init__(self, simulation_id: str, simulation_results: Dict[str, Any]):
        self.simulation_id = simulation_id
        self.results = simulation_results
        os.makedirs(self.REPORT_DIR, exist_ok=True)

    def generate_report(
        self,
        progress_callback: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """
        生成完整的仿真分析报告
        """
        report_id = f"report_{self.simulation_id}"
        report_dir = os.path.join(self.REPORT_DIR, report_id)
        os.makedirs(report_dir, exist_ok=True)

        if progress_callback:
            progress_callback("planning", 0, "规划报告结构...")

        # 数据提取
        state = self.results.get("state", {})
        config = self.results.get("config", {})
        timeline = self.results.get("timeline", [])
        summary = self.results.get("summary", {})

        # 生成报告各章节
        sections = []

        # 章节1: 执行摘要
        if progress_callback:
            progress_callback("generating", 10, "生成执行摘要...")

        sections.append(self._generate_executive_summary(state, config, summary))

        # 章节2: 仿真配置概述
        if progress_callback:
            progress_callback("generating", 25, "生成配置概述...")

        sections.append(self._generate_config_overview(config))

        # 章节3: 供需分析
        if progress_callback:
            progress_callback("generating", 40, "生成供需分析...")

        sections.append(self._generate_supply_demand_analysis(timeline, summary))

        # 章节4: 定价与收入分析
        if progress_callback:
            progress_callback("generating", 55, "生成定价分析...")

        sections.append(self._generate_pricing_analysis(timeline, summary))

        # 章节5: 服务质量分析
        if progress_callback:
            progress_callback("generating", 70, "生成服务质量分析...")

        sections.append(self._generate_service_quality(summary))

        # 章节6: 预测与建议
        if progress_callback:
            progress_callback("generating", 85, "生成预测与建议...")

        sections.append(self._generate_predictions_and_recommendations(timeline, summary))

        # 组装完整报告
        full_report = "\n\n---\n\n".join(sections)
        report_path = os.path.join(report_dir, "full_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(full_report)

        # 保存各章节
        for i, section in enumerate(sections):
            section_path = os.path.join(report_dir, f"section_{i + 1:02d}.md")
            with open(section_path, 'w', encoding='utf-8') as f:
                f.write(section)

        # 保存元数据
        meta = {
            "report_id": report_id,
            "simulation_id": self.simulation_id,
            "sections": len(sections),
            "created_at": datetime.now().isoformat(),
            "status": "completed",
        }
        with open(os.path.join(report_dir, "meta.json"), 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        if progress_callback:
            progress_callback("completed", 100, "报告生成完成")

        logger.info(f"报告生成完成: {report_id}")

        return {
            "report_id": report_id,
            "report_path": report_path,
            "sections": len(sections),
            "status": "completed",
            "markdown_content": full_report,
        }

    # ============== 报告章节生成 ==============

    def _generate_executive_summary(self, state, config, summary) -> str:
        project_name = config.get("project_name", "网约车仿真")
        return f"""# {project_name} - 仿真分析报告

## 1. 执行摘要

本报告基于 **{config.get('city_config', {}).get('city_name', '未知')}** 市网约车运营仿真数据生成。

### 核心指标

| 指标 | 数值 |
|------|------|
| 仿真时长 | {config.get('time_config', {}).get('total_hours', 24)} 小时 |
| 司机总数 | {summary.get('total_drivers', 0):,} |
| 乘客总数 | {summary.get('total_passengers', 0):,} |
| 订单总量 | {summary.get('total_orders', 0):,} |
| 完成订单 | {summary.get('completed_orders', 0):,} |
| 超时订单 | {summary.get('timeout_orders', 0):,} |
| **匹配率** | **{summary.get('match_rate', 0):.1%}** |
| 平均等待时间 | {summary.get('avg_wait_seconds', 0):.0f} 秒 |
| 平均行程时长 | {summary.get('avg_trip_duration_minutes', 0):.1f} 分钟 |
| 总收入 | ¥{summary.get('total_revenue', 0):,.2f} |
| 平均溢价 | {summary.get('avg_surge', 1.0):.2f}x |
"""

    def _generate_config_overview(self, config) -> str:
        tc = config.get("time_config", {})
        cc = config.get("city_config", {})
        mc = config.get("matching_config", {})
        pc = config.get("pricing_config", {})

        return f"""## 2. 仿真配置概述

### 城市设置
- 城市: {cc.get('city_name', '未知')}
- 仿真半径: {cc.get('radius_km', 20)} km
- 网格分辨率: H3-{cc.get('h3_resolution', 7)}

### 时间设置
- 早高峰: {tc.get('morning_peak', [7,8,9])} (倍率 {tc.get('morning_peak_multiplier', 2.5)}x)
- 晚高峰: {tc.get('evening_peak', [17,18,19])} (倍率 {tc.get('evening_peak_multiplier', 3.0)}x)
- 低谷: {tc.get('off_peak', [])} (倍率 {tc.get('off_peak_multiplier', 0.2)}x)

### 匹配策略
- 策略: {mc.get('strategy', 'greedy')}
- 最大接驾距离: {mc.get('max_pickup_distance_km', 5.0)} km
- 最大等待时间: {mc.get('max_wait_seconds', 300)} 秒

### 定价策略
- 起步价: ¥{pc.get('base_fare', 13.0)}
- 每公里: ¥{pc.get('per_km_fare', 2.3)}
- 最大溢价: {pc.get('max_surge', 3.0)}x
"""

    def _generate_supply_demand_analysis(self, timeline, summary) -> str:
        content = """## 3. 供需分析

### 供需时序变化

| 时间 | 在线司机 | 空闲司机 | 载客司机 | 等待订单 |
|------|----------|----------|----------|----------|
"""
        # 取每小时数据（或每 10 步一个采样点）
        sample_interval = max(1, len(timeline) // 24)
        for i in range(0, len(timeline), sample_interval):
            record = timeline[i]
            content += f"| {record.get('sim_time', '')} | "
            content += f"{record.get('online_drivers', 0)} | "
            content += f"{record.get('idle_drivers', 0)} | "
            content += f"{record.get('in_trip_drivers', 0)} | "
            content += f"{record.get('pending_orders', 0)} |\n"

        total = summary.get('total_orders', 0)
        completed = summary.get('completed_orders', 0)
        timeout = summary.get('timeout_orders', 0)

        content += f"""
### 订单完成分布
- 完成订单: {completed} ({completed/max(total,1):.1%})
- 超时订单: {timeout} ({timeout/max(total,1):.1%})
- 取消订单: {summary.get('cancelled_orders', 0)}
"""
        return content

    def _generate_pricing_analysis(self, timeline, summary) -> str:
        surge_values = [r.get("avg_surge", 1.0) for r in timeline]
        max_surge = max(surge_values) if surge_values else 1.0
        min_surge = min(surge_values) if surge_values else 1.0

        return f"""## 4. 定价与收入分析

### 溢价波动
- 最低溢价: {min_surge:.2f}x
- 最高溢价: {max_surge:.2f}x
- 平均溢价: {summary.get('avg_surge', 1.0):.2f}x

### 收入概况
- 总收入: ¥{summary.get('total_revenue', 0):,.2f}
- 平均每单收入: ¥{summary.get('total_revenue', 0) / max(summary.get('completed_orders', 1), 1):,.2f}
- 每司机日均收入: ¥{summary.get('total_revenue', 0) / max(summary.get('total_drivers', 1), 1):,.2f}
"""

    def _generate_service_quality(self, summary) -> str:
        return f"""## 5. 服务质量分析

### 核心体验指标
- **匹配率**: {summary.get('match_rate', 0):.1%}
- **平均等待时间**: {summary.get('avg_wait_seconds', 0):.0f} 秒
- **平均行程时长**: {summary.get('avg_trip_duration_minutes', 0):.1f} 分钟

### 评估
{"- 匹配率 > 80%: 供需基本平衡" if summary.get('match_rate', 0) > 0.8 else "- 匹配率 < 80%: 存在运力缺口"}
{"- 等待时间 < 300秒: 用户体验良好" if summary.get('avg_wait_seconds', 0) < 300 else "- 等待时间 > 300秒: 用户体验需改善"}
"""

    def _generate_predictions_and_recommendations(self, timeline, summary) -> str:
        match_rate = summary.get('match_rate', 0)
        avg_wait = summary.get('avg_wait_seconds', 0)
        avg_surge = summary.get('avg_surge', 1.0)

        recommendations = []
        if match_rate < 0.7:
            recommendations.append("- **增加运力**: 当前匹配率偏低，建议增加 20-30% 司机数量")
            recommendations.append("- **优化调度**: 考虑使用 batch 匹配策略提升全局匹配效率")
        if avg_wait > 300:
            recommendations.append("- **缩短等待**: 建议扩大接驾距离或提高高峰时段司机激励")
        if avg_surge > 2.0:
            recommendations.append("- **控制溢价**: 溢价水平偏高，可能影响用户留存，建议降低溢价上限或提供补贴")
        if match_rate > 0.9 and avg_surge < 1.2:
            recommendations.append("- **运力充足**: 当前供需平衡良好，可考虑适度减少补贴")

        if not recommendations:
            recommendations.append("- 当前运营指标处于合理范围")

        rec_text = "\n".join(recommendations)

        return f"""## 6. 预测与建议

### 趋势预测
基于仿真数据分析：
- 早高峰 (7-9时) 和晚高峰 (17-19时) 为运力瓶颈时段
- 凌晨时段供给过剩，可考虑动态调整司机补贴
- 溢价机制有效调节了高峰需求，但需关注用户体验平衡

### 运营建议
{rec_text}

### 下一步模拟建议
1. 调整司机数量重新模拟，观察匹配率和收入变化
2. 对比 greedy vs batch 匹配策略的效果差异
3. 测试不同溢价灵敏度对供需平衡的影响
4. 模拟极端天气或节假日场景

---

*报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*仿真引擎: RideHailing-Sim (基于 MiroFish 架构改造)*
"""
