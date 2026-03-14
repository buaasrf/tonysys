# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ride-hailing multi-agent simulation platform adapted from the MiroFish architecture. Simulates driver/passenger agents, order matching, dynamic pricing, and demand forecasting for cities (default: Beijing).

## Commands

```bash
# Install dependencies
cd ridehailing-sim/backend && pip install -r requirements.txt

# Run Flask server (default: http://0.0.0.0:5001)
python ridehailing-sim/backend/run.py

# Run standalone demo (300 drivers, 4-hour Beijing morning rush)
python ridehailing-sim/backend/scripts/run_demo.py
```

No test suite exists yet. No linter is configured.

## Architecture

The system is a **discrete time-step simulation** (default 60s/step) with multi-agent behavior:

**Simulation lifecycle**: `SimulationManager` creates config → initializes `TransportSimulationEngine` → runs time-step loop → saves results to `uploads/`.

**Core loop per step** (`services/simulation_engine.py`):
1. Driver online/offline decisions (`agents/driver_agent.py`)
2. Passenger ride requests (`agents/passenger_agent.py`)
3. Order matching via greedy algorithm (`matching/engine.py`)
4. Dynamic surge pricing update (`pricing/engine.py`)
5. Trip state progression (PENDING → MATCHED → PICKUP → IN_TRIP → COMPLETED)
6. Metrics aggregation per hex cell

**Key engines:**
- `MatchingEngine` — greedy nearest-driver matching with scoring (distance, direction, strategy)
- `PricingEngine` — supply/demand ratio surge multiplier (1.0x–3.0x), fare = base + per_km + per_min × surge
- `HexGrid` (`geo/spatial.py`) — lightweight H3-like hex grid for spatial partitioning (no h3-py dependency)
- `ConfigGenerator` — LLM-driven config from natural language scenario descriptions, with rule-based fallback
- `ReportAgent` — ReACT-style markdown report generation from simulation results
- `DemandForecaster` (`prediction/demand_forecast.py`) — hourly demand/supply-gap forecasting

**Agent models:**
- `DriverAgent`: strategies (aggressive/balanced/conservative) affect acceptance decisions
- `PassengerAgent`: trip patterns (commuter/random/nightlife) affect request timing; price sensitivity suppresses demand under surge

**API layer** (Flask blueprints):
- `api/simulation.py` — CRUD + run simulations, get results/timeline
- `api/report.py` — generate/retrieve/download analysis reports

**Data persistence**: JSON files under `uploads/simulations/{id}/` and `uploads/reports/{id}/` (no database).

## Environment Configuration

Copy `ridehailing-sim/.env.example` to `.env`. LLM config is optional (enables smart config generation):
- `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL_NAME` — OpenAI-compatible API for ConfigGenerator and ReportAgent
- `FLASK_PORT` — default 5001
- `DEFAULT_CITY` — default "beijing"

## Key Defaults

- Time step: 60 seconds
- Simulation duration: 1440 steps (24 hours)
- Max pickup distance: 5.0 km
- Pricing (Beijing): ¥13 base, ¥2.3/km, ¥0.4/min
- Hex grid resolution: 7 (~0.66 km² per cell)
