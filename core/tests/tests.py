import pytest
from django.contrib.auth.models import User

# ------------ Auth: Login returns token test
@pytest.mark.django_db
def test_login_returns_token(client):
    """POST /api/auth/token should return a token."""
    # Create test user
    User.objects.create_user(username="u1", password="p1")

    # Send a POST request to the login endpoint the the username and password
    res = client.post(
        "/api/auth/token?username=u1&password=p1")
     
    # Check response status code is ok
    assert res.status_code == 200 
    assert "token" in res.json()

# ------------ Sensor: Create sensor requires authentication
@pytest.mark.django_db
def test_create_sensor_requires_auth(client):
    """POST /api/sensors should require authentication"""
        
    # Try to create a sensor without token
    r = client.post("/api/sensors", data={"name": "Test Sensor", "type": "Env"})
        
    # Expect 401 Unathorized
    assert r.status_code == 401

