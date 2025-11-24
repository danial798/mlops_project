import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.main import app

client = TestClient(app)

def test_health_check():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_predict_endpoint():
    """Test the prediction endpoint with valid data"""
    test_data = {
        "fixed_acidity": 7.4,
        "volatile_acidity": 0.7,
        "citric_acid": 0.0,
        "residual_sugar": 1.9,
        "chlorides": 0.076,
        "free_sulfur_dioxide": 11.0,
        "total_sulfur_dioxide": 34.0,
        "density": 0.9978,
        "pH": 3.51,
        "sulphates": 0.56,
        "alcohol": 9.4
    }
    
    response = client.post("/predict", json=test_data)
    
    # If model is loaded, should return 200, otherwise 503
    if response.status_code == 200:
        assert "quality_prediction" in response.json()
        assert isinstance(response.json()["quality_prediction"], float)
    elif response.status_code == 503:
        assert "Model not loaded" in response.json()["detail"]
    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")

def test_predict_invalid_data():
    """Test the prediction endpoint with invalid data"""
    invalid_data = {
        "fixed_acidity": "invalid",  # Should be float
        "volatile_acidity": 0.7
    }
    
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # Validation error
