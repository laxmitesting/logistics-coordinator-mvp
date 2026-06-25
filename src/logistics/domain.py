from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class TimeWindow:
    start: int
    end: int


@dataclass(frozen=True)
class Order:
    order_id: str
    address: str
    priority: int
    amount: List[int]
    service_s: int
    required_skills: List[int] = field(default_factory=list)
    time_window: TimeWindow = field(default_factory=lambda: TimeWindow(0, 24 * 3600))
    customer_message: str = ""


@dataclass(frozen=True)
class Vehicle:
    vehicle_id: str
    profile: str
    capacity: List[int]
    max_stops: int
    start_address: str
    end_address: str


@dataclass(frozen=True)
class Driver:
    driver_id: str
    name: str
    vehicle_id: str
    status: str
    skills: List[int]
    shift_start: int
    shift_end: int


@dataclass
class StopPlan:
    order_id: str
    arrival_time: Optional[str]
    service_start: Optional[str]
    departure_time: Optional[str]
    time_window: List[Optional[str]]
    within_constraints: bool


@dataclass
class RoutePlan:
    driver_id: str
    driver_name: str
    vehicle_id: str
    remaining_capacity: int
    route_distance_m: Optional[float]
    route_duration_s: Optional[float]
    feasible_with_constraints: bool
    stops: List[StopPlan]