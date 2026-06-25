import math
from typing import Any, Dict, List

from .config import DRIVERS, ORDERS, VEHICLES, DEPOT
from .geo import geocode_address, get_directions, get_matrix


def fmt_hhmm(seconds):
    if seconds is None:
        return None
    seconds = int(seconds)
    return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}"


def optimize_stop_order(locations: List[List[float]]) -> List[int]:
    if len(locations) <= 2:
        return list(range(len(locations)))
    durations = get_matrix(locations)["durations"]
    unvisited = set(range(1, len(locations)))
    route = [0]
    current = 0
    while unvisited:
        nxt = min(unvisited, key=lambda j: durations[current][j] if durations[current][j] is not None else math.inf)
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    route.append(0)
    return route


def build_dispatch_plan() -> Dict[str, Any]:
    depot_geo = geocode_address(DEPOT["address"])
    if not depot_geo.get("ok"):
        return {"ok": False, "errors": [depot_geo]}

    geos = {}
    for order in ORDERS:
        geo = geocode_address(order["address"])
        if not geo.get("ok"):
            return {"ok": False, "errors": [geo]}
        geos[order["order_id"]] = geo

    plans = []
    for d in DRIVERS:
        if d["status"] != "available":
            continue
        vehicle = next((v for v in VEHICLES if v["vehicle_id"] == d["vehicle_id"]), None)
        if vehicle is None:
            continue
        plans.append({
            "driver_id": d["driver_id"],
            "driver_name": d["name"],
            "vehicle_id": vehicle["vehicle_id"],
            "profile": vehicle["profile"],
            "remaining_capacity": vehicle["capacity"][0],
            "max_stops": vehicle["max_stops"],
            "shift_start": d["shift_start"],
            "shift_end": d["shift_end"],
            "stops": []
        })

    unassigned = []
    for order in sorted(ORDERS, key=lambda x: (-x["priority"], x["time_window"].start)):
        candidates = []
        for p in plans:
            driver = next(x for x in DRIVERS if x["driver_id"] == p["driver_id"])
            if set(order.get("required_skills", [])).issubset(set(driver.get("skills", []))) and order["amount"][0] <= p["remaining_capacity"] and len(p["stops"]) < p["max_stops"]:
                candidates.append(p)
        if not candidates:
            unassigned.append({"order_id": order["order_id"], "reason": "No feasible driver/vehicle under current constraints."})
            continue
        best = max(candidates, key=lambda p: (p["remaining_capacity"], p["shift_end"] - p["shift_start"]))
        best["stops"].append(order)
        best["remaining_capacity"] -= order["amount"][0]

    routes = []
    for p in plans:
        if not p["stops"]:
            continue
        coords = [[depot_geo["lon"], depot_geo["lat"]]] + [[geos[s["order_id"]]["lon"], geos[s["order_id"]]["lat"]] for s in p["stops"]]
        idxs = optimize_stop_order(coords)[1:-1]
        ordered = [p["stops"][i - 1] for i in idxs]
        route_coords = [[depot_geo["lon"], depot_geo["lat"]]] + [[geos[s["order_id"]]["lon"], geos[s["order_id"]]["lat"]] for s in ordered] + [[depot_geo["lon"], depot_geo["lat"]]]
        matrix = get_matrix(route_coords, p["profile"])["durations"]
        directions = get_directions(route_coords, p["profile"])
        current_time = p["shift_start"]
        stop_rows = []
        feasible = True
        for i, stop in enumerate(ordered, start=1):
            travel = matrix[i - 1][i]
            arrival = current_time + travel
            tw_start, tw_end = stop["time_window"].start, stop["time_window"].end
            service_start = max(arrival, tw_start)
            departure = service_start + stop["service_s"]
            within = service_start <= tw_end and departure <= p["shift_end"]
            feasible = feasible and within
            stop_rows.append({
                "order_id": stop["order_id"],
                "arrival_time": fmt_hhmm(arrival),
                "service_start": fmt_hhmm(service_start),
                "departure_time": fmt_hhmm(departure),
                "time_window": [fmt_hhmm(tw_start), fmt_hhmm(tw_end)],
                "within_constraints": within,
            })
            current_time = departure
        routes.append({
            "driver_id": p["driver_id"],
            "driver_name": p["driver_name"],
            "vehicle_id": p["vehicle_id"],
            "remaining_capacity": p["remaining_capacity"],
            "route_distance_m": directions.get("distance_m"),
            "route_duration_s": directions.get("duration_s"),
            "feasible_with_constraints": feasible,
            "stops": stop_rows,
        })

    return {"ok": True, "depot": DEPOT, "routes": routes, "unassigned_orders": unassigned}