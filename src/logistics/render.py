from typing import Dict, List, Tuple


def render_ascii_map(coords: List[Tuple[float, float]], labels: List[str], width: int = 64, height: int = 20) -> str:
    if not coords:
        return "(no coordinates)"
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    lon_span = max(max_lon - min_lon, 1e-9)
    lat_span = max(max_lat - min_lat, 1e-9)
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for idx, ((lon, lat), _label) in enumerate(zip(coords, labels)):
        x = int((lon - min_lon) / lon_span * (width - 1))
        y = int((max_lat - lat) / lat_span * (height - 1))
        char = "D" if idx == 0 else str(idx % 10)
        grid[y][x] = char
    return "\n".join("".join(row) for row in grid)


def route_lines(plan: Dict) -> List[str]:
    lines = []
    for route in plan.get("routes", []):
        lines.append(f"{route['driver_name']} ({route['vehicle_id']})")
        for stop in route.get("stops", []):
            lines.append(
                f"  {stop['order_id']} | arrive {stop['arrival_time']} | service {stop['service_start']} | depart {stop['departure_time']}"
            )
    return lines