import os
import pytest

os.environ["ORS_API_KEY"] = "REPLACE_WITH_YOUR_ORS_API_KEY="

from logistics.agent import build_dispatch_plan_tool


def test_agent_dispatch_tool_success():
    """Verify the agent tool successfully retrieves a valid plan."""
    # Act: Call the tool exactly as the AI would
    result = build_dispatch_plan_tool()
    
    
    assert result.get("ok") is True, f"Planner failed: {result.get('errors')}"
    # You can add more checks here later, like assert "routes" in result

def test_agent_dispatch_tool_handles_failure():
    """Verify the agent tool passes errors up cleanly when geo fails."""
    # Arrange: Temporarily remove the API key to force a failure
    if "ORS_API_KEY" in os.environ:
        del os.environ["ORS_API_KEY"]
        
    # Act
    result = build_dispatch_plan_tool()
    
    # Assert: The agent should hand us back the graceful failure dictionary
    assert result.get("ok") is False
    assert "errors" in result