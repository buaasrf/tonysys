#!/usr/bin/env python3
"""
快速演示脚本
无需启动 Flask 服务器，直接运行一次完整仿真

用法: python scripts/run_demo.py
"""

import sys
import os
import json

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models.simulation import (
    SimulationConfig, TimeConfig, CityConfig,
    SupplyDemandConfig, MatchingConfig, PricingConfig,
)
from app.services.simulation_engine import TransportSimulationEngine
from app.services.report_agent import ReportAgent


def main():
    print("=" * 60)
    print("  RideHailing-Sim 快速演示")
    print("  基于 MiroFish 架构的网约车仿真平台")
    print("=" * 60)

    # 创建仿真配置（小规模快速演示）
    config = SimulationConfig(
        simulation_id="demo_001",
        project_name="北京网约车运营仿真演示",
        description="模拟北京市早高峰到午间的网约车运营",
        time_config=TimeConfig(
            start_hour=7,  # 从早上7点开始
            total_hours=4,  # 演示只跑 4 小时 (7:00-11:00)
            time_step_seconds=120,  # 每步 2 分钟
        ),
        city_config=CityConfig(
            city_name="beijing",
            radius_km=10.0,  # 缩小范围提高匹配密度
        ),
        supply_demand_config=SupplyDemandConfig(
            total_drivers=300,  # 演示用少量司机
            base_demand_per_hour=100,
        ),
        matching_config=MatchingConfig(
            strategy="greedy",
            max_pickup_distance_km=5.0,
        ),
        pricing_config=PricingConfig(
            strategy="dynamic",
            base_fare=13.0,
            per_km_fare=2.3,
            max_surge=2.5,
        ),
    )

    # 初始化引擎
    print("\n[1/4] 初始化仿真引擎...")
    engine = TransportSimulationEngine(config)
    engine.initialize()
    print(f"  - 司机: {engine.state.total_drivers}")
    print(f"  - 乘客: {engine.state.total_passengers}")
    print(f"  - 六边形网格: {len(engine.hex_grid.get_all_hex_ids())} 个单元格")
    print(f"  - 总步数: {engine.total_steps}")

    # 运行仿真
    print("\n[2/4] 运行仿真...")

    def progress(stage, pct, msg, **kwargs):
        if pct % 20 == 0:
            print(f"  [{stage}] {pct}% - {msg}")

    engine.run(progress_callback=progress)

    # 输出结果
    print("\n[3/4] 仿真结果:")
    results = engine.get_results()
    summary = results["summary"]
    print(f"  - 订单总量: {summary['total_orders']}")
    print(f"  - 完成订单: {summary['completed_orders']}")
    print(f"  - 超时订单: {summary['timeout_orders']}")
    print(f"  - 匹配率: {summary['match_rate']:.1%}")
    print(f"  - 平均等待: {summary['avg_wait_seconds']:.0f} 秒")
    print(f"  - 总收入: ¥{summary['total_revenue']:,.2f}")
    print(f"  - 平均溢价: {summary['avg_surge']:.2f}x")

    # 保存结果
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'simulations', 'demo_001')
    engine.save_results(output_dir)

    # 生成报告
    print("\n[4/4] 生成分析报告...")
    agent = ReportAgent("demo_001", results)
    report = agent.generate_report()
    print(f"  - 报告已保存: {report['report_path']}")

    print("\n" + "=" * 60)
    print("  演示完成！")
    print(f"  结果目录: {output_dir}")
    print(f"  报告文件: {report['report_path']}")
    print("=" * 60)


if __name__ == '__main__':
    main()
