from logistics.config import DEPOT, DRIVERS, VEHICLES, ORDERS

# ==========================================
# CONFIG TESTS
# ==========================================
def test_depot_config():
    """Verify the depot is configured correctly."""
    assert DEPOT["name"] == "London Depot"
    assert "address" in DEPOT
    assert "time_window" in DEPOT

def test_drivers_config():
    """Verify driver data is loaded correctly."""
    assert len(DRIVERS) == 2
    
    # Test specific driver attributes
    first_driver = DRIVERS[0]
    assert first_driver["driver_id"] == "DRV-01"
    assert first_driver["status"] == "available"
    assert first_driver["skills"] == [1]

def test_vehicles_config():
    """Verify vehicle data is loaded correctly."""
    assert len(VEHICLES) == 2
    
    # Test specific vehicle attributes
    second_vehicle = VEHICLES[1]
    assert second_vehicle["vehicle_id"] == "VAN-02"
    assert second_vehicle["capacity"] == [8]
    assert second_vehicle["max_stops"] == 4

def test_orders_config():
    """Verify order data is loaded correctly."""
    assert len(ORDERS) == 3
    
    # Test specific order attributes
    first_order = ORDERS[0]
    assert first_order["order_id"] == "ORD-1001"
    assert first_order["priority"] == 9
    assert first_order["required_skills"] == [1]