import os 

os.environ["ORS_API_KEY"] = "REPLACE_WITH_YOUR_ORS_API_KEY="

from logistics.geo import geocode_address

def test_geocode_simply():
    result = geocode_address("London")
    
    # Adding the second part prints the exact error from geo.py if it fails
    assert result["ok"] is True, f"API Failed! Reason: {result.get('error')}"

