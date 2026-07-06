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
```

📄 File Overview
Core Application
cli.py: The front-door application router for commands like plan and show-plan

config.py: Stores the static definitions for the sample depot, available drivers, vehicles, and daily orders.

domain.py: Establishes the core data models (Driver, Vehicle, Order, RoutePlan).

render.py: Translates raw JSON routing data into human-readable terminal schedules and ASCII maps.

Routing & AI Logic
agent.py: Manages the OpenAI-compatible tool loop, allowing the AI to interface with the routing engine.

planner.py: Orchestrates deterministic constraint logic, actively managing capacity, driver skills, stop limits, time windows, and final route assignments.

geo.py: Provides robust wrappers for the OpenRouteService (ORS) API. Handles geocoding, distance matrices, directions, and the core optimization model (supporting capacities, time windows, skills, and service durations).

```mermaid
graph LR
    User((In/CLI User Request)) --> Orchestrator[Orchestrator Agent<br/>cli.py]
    
    subgraph Workers [Parallel Worker Agents]
        Worker_LLM[Reasoning Agent<br/>agent.py]
        Worker_Plan[Optimization Agent<br/>planner.py]
        Worker_Geo[Geo-Service Agent<br/>geo.py]
    end
    
    Orchestrator -.-> Worker_LLM
    Orchestrator -.-> Worker_Plan
    Orchestrator -.-> Worker_Geo
    
    Worker_LLM -.-> Synthesizer[Synthesizer Agent<br/>render.py]
    Worker_Plan -.-> Synthesizer
    Worker_Geo -.-> Synthesizer
    
    Synthesizer --> Final((Out/Terminal Output<br/>Displays Schedule))

    %% Formatting %%
    linkStyle 0,1,2,3,4,5,6,7 stroke-width:1px,stroke-dasharray: 3 3,stroke:grey;
    linkStyle default stroke-width:1px,stroke:grey;

    %% Define Agent Styles %%
    classDef agent fill:#e8f5e9,stroke:#4caf50,stroke-width:1px,rx:2,ry:2,font-family:Arial,color:darkgrey;
    classDef io fill:#fff3e0,stroke:#ff9800,stroke-width:1px,font-family:Arial,color:darkgrey;
    
    %% Apply Styles %%
    class Orchestrator,Worker_LLM,Worker_Plan,Worker_Geo,Synthesizer agent;
    class User,Final io;
    ```