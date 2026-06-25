Markdown
# Logistics Coordinator CLI

An AI-powered command-line interface for intelligent route planning and dispatch coordination.

## 📂 Project Structure

```text
logistics-coordinator/
├─ README.md
├─ .env
├─ .env.example
├─ requirements.txt
├─ cli.py
├─ src/
│  └─ logistics/
│     ├─ __init__.py
│     ├─ config.py
│     ├─ domain.py
│     ├─ geo.py
│     ├─ planner.py
│     ├─ agent.py
│     └─ render.py
└─ tests/
   ├─ __init__.py
   ├─ test_agent.py
   ├─ test_config.py
   ├─ test_domain.py
   └─ test_geo.py

📄 File Overview
Core Application
cli.py: The front-door application router for commands like plan, show-plan, and show-map.

config.py: Stores the static definitions for the sample depot, available drivers, vehicles, and daily orders.

domain.py: Establishes the core data models (Driver, Vehicle, Order, RoutePlan).

render.py: Translates raw JSON routing data into human-readable terminal schedules and ASCII maps.

Routing & AI Logic
agent.py: Manages the OpenAI-compatible tool loop, allowing the AI to interface with the routing engine.

planner.py: Orchestrates deterministic constraint logic, actively managing capacity, driver skills, stop limits, time windows, and final route assignments.

geo.py: Provides robust wrappers for the OpenRouteService (ORS) API. Handles geocoding, distance matrices, directions, and the core optimization model (supporting capacities, time windows, skills, and service durations).