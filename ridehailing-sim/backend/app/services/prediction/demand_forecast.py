"""
需求预测模块
基于仿真数据分析未来供需趋势
"""

import math
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

from ...utils.logger import get_logger

logger = get_logger('ridehailing.prediction')


class DemandForecaster:
    """
    需求预测器
    基于仿真历史数据，预测未来各时段各区域的需求量
    """

    def __init__(self):
        self._historical_data: List[Dict[str, Any]] = []

    def load_timeline(self, timeline_data: List[Dict[str, Any]]):
        """加载仿真时间线数据"""
        self._historical_data = timeline_data
        logger.info(f"加载 {len(timeline_data)} 条时间线数据")

    def forecast_hourly_demand(self, forecast_hours: int = 24) -> List[Dict[str, Any]]:
        """
        预测未来每小时的需求量
        使用加权移动平均 + 时段模式匹配
        """
        if not self._historical_data:
            return []

        # 按小时聚合历史数据
        hourly_orders = defaultdict(list)
        for record in self._historical_data:
            hour = record.get("hour", 0)
            orders = record.get("total_orders", 0)
            hourly_orders[hour].append(orders)

        # 计算每小时的平均需求和标准差
        hourly_stats = {}
        for hour, values in hourly_orders.items():
            if values:
                mean = sum(values) / len(values)
                variance = sum((v - mean) ** 2 for v in values) / len(values)
                std = math.sqrt(variance)
                hourly_stats[hour] = {"mean": mean, "std": std, "count": len(values)}

        # 生成预测
        forecasts = []
        last_hour = self._historical_data[-1].get("hour", 0) if self._historical_data else 0

        for i in range(forecast_hours):
            forecast_hour = (last_hour + i + 1) % 24
            stats = hourly_stats.get(forecast_hour, {"mean": 0, "std": 0})

            # 趋势调整（简单线性外推）
            trend_factor = 1.0
            if len(self._historical_data) > 48:  # 超过2天的数据
                recent = [r.get("total_orders", 0) for r in self._historical_data[-24:]]
                earlier = [r.get("total_orders", 0) for r in self._historical_data[-48:-24]]
                if sum(earlier) > 0:
                    trend_factor = sum(recent) / max(sum(earlier), 1)

            predicted = stats["mean"] * trend_factor

            forecasts.append({
                "hour": forecast_hour,
                "forecast_offset": i + 1,
                "predicted_demand": round(predicted, 1),
                "confidence_low": round(max(0, predicted - stats["std"] * 1.96), 1),
                "confidence_high": round(predicted + stats["std"] * 1.96, 1),
                "trend_factor": round(trend_factor, 3),
            })

        return forecasts

    def forecast_supply_gap(
        self,
        timeline_data: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        预测供需缺口
        供给 = idle_drivers, 需求 = pending_orders + in_trip
        """
        gaps = []

        for record in timeline_data:
            hour = record.get("hour", 0)
            supply = record.get("idle_drivers", 0)
            demand = record.get("pending_orders", 0) + record.get("in_trip_drivers", 0)

            gap = supply - demand
            gap_ratio = supply / max(demand, 1)

            gaps.append({
                "step": record.get("step", 0),
                "hour": hour,
                "sim_time": record.get("sim_time", ""),
                "supply": supply,
                "demand": demand,
                "gap": gap,
                "gap_ratio": round(gap_ratio, 3),
                "status": "surplus" if gap > 0 else "shortage",
                "severity": "high" if abs(gap_ratio - 1.0) > 0.5 else "medium" if abs(gap_ratio - 1.0) > 0.2 else "low",
            })

        return gaps

    def analyze_peak_patterns(
        self,
        timeline_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """分析高峰模式"""
        hourly_demand = defaultdict(list)
        hourly_surge = defaultdict(list)

        for record in timeline_data:
            hour = record.get("hour", 0)
            hourly_demand[hour].append(record.get("total_orders", 0))
            hourly_surge[hour].append(record.get("avg_surge", 1.0))

        peak_analysis = {}
        for hour in range(24):
            demands = hourly_demand.get(hour, [0])
            surges = hourly_surge.get(hour, [1.0])
            avg_demand = sum(demands) / len(demands) if demands else 0
            avg_surge = sum(surges) / len(surges) if surges else 1.0

            peak_analysis[hour] = {
                "avg_demand": round(avg_demand, 1),
                "avg_surge": round(avg_surge, 2),
                "is_peak": avg_surge > 1.3,
            }

        # 识别高峰时段
        peak_hours = [h for h, v in peak_analysis.items() if v["is_peak"]]
        off_peak_hours = [h for h, v in peak_analysis.items() if v["avg_demand"] < 1]

        return {
            "hourly_analysis": peak_analysis,
            "peak_hours": sorted(peak_hours),
            "off_peak_hours": sorted(off_peak_hours),
            "peak_surge_max": max((v["avg_surge"] for v in peak_analysis.values()), default=1.0),
        }
