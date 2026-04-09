from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check_endpoint():
    """Validates the API fails safely on empty prompts like expected."""
    response = client.post("/generate", json={"code": "  ", "language": "python"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Source code cannot be empty."
    
def test_mock_fallback_structure():
    """Validates the standard response structure returns all requested properties in Mock."""
    # Assuming MOCK is default True in CI
    response = client.post("/generate", json={"code": "def example(): pass", "language": "python"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "unit_tests" in data["results"]
