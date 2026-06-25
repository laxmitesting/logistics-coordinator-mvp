import json
import os
from typing import Any, Dict, List, override

from dotenv import load_dotenv
from openai import OpenAI

from .planner import build_dispatch_plan

load_dotenv(override=True)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def tool_spec() -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "build_dispatch_plan",
                "description": "Build a dispatch plan with driver, vehicle, capacity, skills, and time-window constraints.",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
        }
    ]


def build_dispatch_plan_tool() -> Dict[str, Any]:
    return build_dispatch_plan()


def summarize_plan(plan: Dict[str, Any]) -> str:
    if not plan.get("ok"):
        return json.dumps(plan, indent=2)

    lines = ["Dispatch plan:"]
    for route in plan.get("routes", []):
        lines.append(
            f"- {route['driver_name']} ({route['vehicle_id']}): "
            f"{len(route['stops'])} stops, {route['route_distance_m']} m, {route['route_duration_s']} s, "
            f"feasible={route['feasible_with_constraints']}"
        )
        for stop in route.get("stops", []):
            lines.append(
                f"  - {stop['order_id']} arrive {stop['arrival_time']} service {stop['service_start']} "
                f"depart {stop['departure_time']} within={stop['within_constraints']}"
            )

    if plan.get("unassigned_orders"):
        lines.append("Unassigned orders:")
        for item in plan["unassigned_orders"]:
            lines.append(f"- {item['order_id']}: {item['reason']}")

    return "\n".join(lines)


def run_agent(user_prompt: str, max_iters: int = 4) -> str:
    messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are a logistics coordinator. Use tools to build a dispatch plan and summarize the result. "
                "Do not invent routing facts; rely on the planner output."
            ),
        },
        {"role": "user", "content": user_prompt},
    ]

    for _ in range(max_iters):
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tool_spec(),
            tool_choice="auto",
            parallel_tool_calls=False,
        )
        msg = resp.choices[0].message

        if getattr(msg, "tool_calls", None):
            messages.append(
                {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
                }
            )
            for tc in msg.tool_calls:
                if tc.function.name == "build_dispatch_plan":
                    result = build_dispatch_plan_tool()
                else:
                    result = {"ok": False, "error": f"Unknown tool: {tc.function.name}"}
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result),
                    }
                )
            continue

        return msg.content or ""

    final_plan = build_dispatch_plan()
    return summarize_plan(final_plan)