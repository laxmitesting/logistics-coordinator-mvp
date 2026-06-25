from .domain import TimeWindow

DEPOT = {
    "name": "London Depot",
    "address": "King's Cross Station, London",
    "time_window": TimeWindow(8 * 3600, 18 * 3600),
}

DRIVERS = [
    {
        "driver_id": "DRV-01",
        "name": "A. Peter",
        "vehicle_id": "VAN-01",
        "status": "available",
        "skills": [1],
        "shift_start": 8 * 3600,
        "shift_end": 17 * 3600,
    },
    {
        "driver_id": "DRV-02",
        "name": "L. Smith",
        "vehicle_id": "VAN-02",
        "status": "available",
        "skills": [2],
        "shift_start": 9 * 3600,
        "shift_end": 18 * 3600,
    },
]

VEHICLES = [
    {
        "vehicle_id": "VAN-01",
        "profile": "driving-car",
        "capacity": [12],
        "max_stops": 5,
        "start_address": DEPOT["address"],
        "end_address": DEPOT["address"],
    },
    {
        "vehicle_id": "VAN-02",
        "profile": "driving-car",
        "capacity": [8],
        "max_stops": 4,
        "start_address": DEPOT["address"],
        "end_address": DEPOT["address"],
    },
]

ORDERS = [
    {
        "order_id": "ORD-1001",
        "address": "10 Downing Street, London",
        "priority": 9,
        "amount": [2],
        "service_s": 600,
        "required_skills": [1],
        "time_window": TimeWindow(9 * 3600, 12 * 3600),
        "customer_message": "Your parcel is planned for late morning delivery.",
    },
    {
        "order_id": "ORD-1002",
        "address": "221B Baker Street, London",
        "priority": 6,
        "amount": [3],
        "service_s": 480,
        "required_skills": [2],
        "time_window": TimeWindow(10 * 3600, 15 * 3600),
        "customer_message": "Your delivery is currently planned for early afternoon.",
    },
    {
        "order_id": "ORD-1003",
        "address": "Paddington Station, London",
        "priority": 4,
        "amount": [1],
        "service_s": 300,
        "required_skills": [],
        "time_window": TimeWindow(11 * 3600, 17 * 3600),
        "customer_message": "Your delivery remains on schedule for today.",
    },
]