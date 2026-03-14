# RideHailing-Sim 网约车多智能体仿真平台

基于 [MiroFish](https://github.com/mirofish) 多智能体 AI 架构改造的网约车仿真平台，通过离散时间步模拟司机/乘客 Agent 的行为决策、订单匹配、动态定价与需求预测。

## 核心特性

- **多智能体仿真**：数百至数千个司机/乘客 Agent，各自具有独立策略和行为参数
- **车型品类定价**：经济型 / 舒适型 / 豪华型，不同品类独立计价
- **动态定价引擎**：供需比驱动的 Surge 定价（1.0x–3.0x），平峰时段运营活动自动触发优惠
- **会员体系**：普通 / 银牌(95折) / 金牌(9折) / 铂金(88折)
- **预派单**：行程剩余 ≤ 5 分钟的司机可提前接下一单
- **排队加价**：等待中的乘客可加价 10%-30% 调度更远的车
- **平台抽成上限**：27%
- **智能配参**：LLM 驱动的自然语言场景 → 仿真参数生成
- **六边形空间网格**：轻量级 H3-like 实现，无需 h3-py 依赖

## 快速开始

```bash
# 安装依赖
cd ridehailing-sim/backend
pip install -r requirements.txt

# 配置环境变量（可选，LLM 用于智能配参和报告生成）
cp ../. env.example ../.env
# 编辑 .env 填入 LLM API 配置

# 启动 Flask 服务
python run.py
# 服务默认运行在 http://localhost:5001

# 或运行独立 Demo（300 司机，北京早高峰 4 小时）
python scripts/run_demo.py
```

## API 接口

### 仿真管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/simulation/create` | 创建仿真配置 |
| POST | `/api/simulation/create-smart` | LLM 智能创建配置 |
| POST | `/api/simulation/run` | 运行仿真 |
| GET | `/api/simulation/<id>` | 查询仿真状态 |
| GET | `/api/simulation/list` | 列出所有仿真 |
| GET | `/api/simulation/<id>/results` | 获取仿真结果 |
| GET | `/api/simulation/<id>/timeline` | 获取时序数据 |

### 报告

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/report/generate` | 生成分析报告 |
| GET | `/api/report/<id>` | 获取报告 |
| GET | `/api/report/<id>/download` | 下载 Markdown 报告 |

### 示例：创建并运行仿真

```bash
# 创建
curl -X POST http://localhost:5001/api/simulation/create \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "北京早高峰",
    "city": "beijing",
    "total_drivers": 5000,
    "base_demand_per_hour": 2000,
    "total_hours": 24
  }'

# 运行
curl -X POST http://localhost:5001/api/simulation/run \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "sim_xxxxx"}'

# 生成报告
curl -X POST http://localhost:5001/api/report/generate \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "sim_xxxxx"}'
```

## 车型品类与定价

| 品类 | 对应车型 | 起步价 | 里程费(/km) | 时长费(/min) |
|------|----------|--------|-------------|-------------|
| 经济型 | sedan | ¥13 | ¥1.6 | ¥0.35 |
| 舒适型 | suv | ¥14 | ¥2.3 | ¥0.4 |
| 豪华型 | luxury | ¥25 | ¥3.8 | ¥0.8 |

## 项目结构

```
ridehailing-sim/backend/
├── run.py                          # Flask 服务入口
├── requirements.txt
├── scripts/run_demo.py             # 独立 Demo
└── app/
    ├── __init__.py                 # Flask App Factory
    ├── config.py                   # 配置管理
    ├── api/
    │   ├── simulation.py           # 仿真 API
    │   └── report.py               # 报告 API
    ├── models/
    │   ├── entities.py             # Order, Driver, Passenger 实体
    │   └── simulation.py           # 仿真配置与状态
    ├── services/
    │   ├── simulation_engine.py    # 核心仿真引擎（时间步主循环）
    │   ├── simulation_manager.py   # 仿真生命周期管理
    │   ├── config_generator.py     # LLM 智能配参
    │   ├── report_agent.py         # ReACT 报告生成
    │   ├── agents/
    │   │   ├── driver_agent.py     # 司机行为模型
    │   │   ├── passenger_agent.py  # 乘客行为模型
    │   │   └── profile_generator.py # Agent 档案生成
    │   ├── matching/engine.py      # 订单匹配（贪心/批量）
    │   ├── pricing/engine.py       # 动态定价 + 品类 + 会员 + 促销
    │   ├── geo/spatial.py          # 六边形网格 + 地理计算
    │   └── prediction/
    │       └── demand_forecast.py  # 需求预测
    └── utils/
        ├── llm_client.py           # OpenAI 兼容 LLM 客户端
        └── logger.py
```

## 仿真主循环

每个时间步（默认 60 秒）依次执行：

1. **司机决策** — 上线/下线/空闲移动
2. **乘客决策** — 是否叫车（受时段、surge、价格敏感度影响）
3. **排队加价** — 等待中乘客决定是否加价调度更远车辆
4. **订单匹配** — 贪心/批量匹配，按品类过滤，加价单扩大搜索半径
5. **预派单** — 行程即将结束的司机提前接下一单
6. **行程推进** — 接驾 → 载客 → 送达，含位置插值
7. **定价更新** — 区域供需比 → Surge 系数平滑更新
8. **超时处理** — 清理超时未匹配订单
9. **指标记录** — 在线/空闲/载客司机数、待匹配订单、加价订单等

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `LLM_API_KEY` | LLM API 密钥（可选） | — |
| `LLM_BASE_URL` | LLM API 地址 | dashscope |
| `LLM_MODEL_NAME` | 模型名称 | qwen-plus |
| `FLASK_PORT` | 服务端口 | 5001 |
| `DEFAULT_CITY` | 默认城市 | beijing |
| `GEO_GRID_RESOLUTION` | 六边形网格分辨率 | 7 |

## 技术栈

- Python 3.11+ / Flask 3.0+
- OpenAI SDK（兼容通义千问等 API）
- 无外部数据库，结果持久化为 JSON 文件

## 文档

- [MiroFish 网约车仿真可行性分析](docs/mirofish-rideshare-feasibility-analysis.md)
