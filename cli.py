# cli.py
import argparse
import json
import os
import sys
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))
env_path = os.path.join(BASE_DIR, ".env")

# Load the environment variables
load_dotenv()

# Import the agent and render modules
from logistics.agent import build_dispatch_plan_tool
from logistics.render import route_lines

PLAN_FILE = "latest_plan.json"


def custom_json_encoder(obj):
    # 1. If it is a Pydantic model
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    if hasattr(obj, 'dict'):
        return obj.dict()
    # 2. If it is a standard Dataclass
    if hasattr(obj, '__dataclass_fields__'):
        from dataclasses import asdict
        return asdict(obj)
    # 3. If it is a NamedTuple or standard class
    if hasattr(obj, '_asdict'):
        return obj._asdict()
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    # 4. Final fallback
    return str(obj)


def handle_plan():
    """Generates a new plan and saves it to a file."""
    print("Building new dispatch plan...")
    result = build_dispatch_plan_tool()
    
    # Check for failures
    if isinstance(result, dict) and result.get("ok") is False:
        print(f"\n❌ PLAN FAILED:")
        print(result.get("errors", "Unknown error"))
        return
    elif isinstance(result, str):
        print(f"\n⚠️ AGENT ERROR: {result}")
        return

    # Use our custom encoder here!
    with open(PLAN_FILE, "w") as f:
        json.dump(result, f, indent=4, default=custom_json_encoder)
        
    print(f"\n✅ PLAN SUCCESSFUL!")
    print(f"Plan saved to {PLAN_FILE}. Run 'python cli.py show-plan' to view it.")


def handle_show_plan():
    """Reads the latest plan from the file and displays it."""
    if not os.path.exists(PLAN_FILE):
        print(f"❌ No plan found! Run 'python cli.py plan' first to generate one.")
        return
        
    print("Loading latest dispatch plan...\n")
    print("==========================================")
    print("🚚 DISPATCH SCHEDULE")
    print("==========================================\n")
    
    with open(PLAN_FILE, "r") as f:
        plan_data = json.load(f)
        
    # Use your render.py function to make it beautiful!
    formatted_schedule = route_lines(plan_data)
    
    # Print out each line of the beautiful schedule
    if not formatted_schedule:
        print("No routes assigned for today.")
    else:
        for line in formatted_schedule:
            print(line)
            
    print("\n==========================================")


def main():
    # Set up the command parser
    parser = argparse.ArgumentParser(description="Logistics Coordinator CLI")
    
    # We add a 'subparsers' to handle the different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Command 1: 'plan'
    subparsers.add_parser("plan", help="Generate a new dispatch plan")
    
    # Command 2: 'show-plan'
    subparsers.add_parser("show-plan", help="Show the latest stored dispatch plan")
    
    args = parser.parse_args()
    
    # Route to the correct function based on what the user typed
    if args.command == "plan":
        handle_plan()
    elif args.command == "show-plan":
        handle_show_plan()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()