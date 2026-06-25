Logistics coordinator MVP
This is a simple Python MVP for a logistics coordinator agent built with:
- an OpenAI-compatible chat completions endpoint
- openrouteservice (ORS) for geocoding, matrix, and directions
- driver/vehicle/order constraints 
- route planning function with dispatch plan 
Inspired by - https://docs.cloud.google.com/architecture/agentic-ai-system-with-grounding-using-maps

Files Structure
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

Files
cli.py for simple commands like plan, show-plan, and show-map.
config.py: sample depot, drivers, vehicles, and orders.
domain.py for data models: Driver, Vehicle, Order, RoutePlan.
planner.py for deterministic constraint logic: capacity, skills, stop limits, time windows, and route assignment.
geo.py for ORS wrappers: geocode, matrix, directions, and optional optimization. ORS supports capacities, time windows, skills, and service duration in its optimization model.
agent.py for the OpenAI-compatible tool loop.
render.py for console output

Setup
Create a virtual environment.

Install dependencies:

bash
pip install -r requirements.txt
Copy .env.example to .env and fill in values.


Commands
Create a new plan:
bash
python cli.py plan
Show the latest stored plan:
bash
python cli.py show-plan

The MVP models:  
- drivers with skills, availability, and shift windows
- vehicles with capacity and stop limits
- orders with amounts, required skills, service durations, and delivery time windows
- a dispatch planner that checks these constraints before building routes
