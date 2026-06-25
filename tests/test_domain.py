from logistics.domain import TimeWindow

def test_time_window_initialization():
    """Verify TimeWindow stores start and end times correctly."""
    # Example: 8 AM to 6 PM in seconds
    start_time = 8 * 3600
    end_time = 18 * 3600
    
    tw = TimeWindow(start_time, end_time)
    
    # Adjust these assertions to match the actual property names in your class
    assert tw.start == 28800
    assert tw.end == 64800
    
    # Example of testing a class method (if you have one)
    # assert tw.duration() == 36000