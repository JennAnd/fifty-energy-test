import pytest
from django.contrib.auth.models import User

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


@pytest.mark.django_db
def test_register_returns_token(client):
    """Checks that /api/auth/register creates user and returns a token."""
    res = client.post("/api/auth/register?username=newuser&password=secret123")

    # Should return 200 or 201 when registration succeeds
    assert res.status_code in (200, 201)

    data = res.json()
    assert "token" in data

    # Confirm that the user was created in the database
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_login_wrong_password_returns_error(client):
    """Checks that /api/auth/token returns 401 when password is wrong."""

    # Create a user with correct password
    User.objects.create_user(username="u1", password="right")

    # Try login with wrong password
    res = client.post("/api/auth/token?username=u1&password=wrong")

    # Should return 401 because password is incorrect
    assert res.status_code == 401


@pytest.mark.django_db
def test_protected_endpoint_allows_with_valid_token(client):
    """Checks that /api/sensors can be accessed with valid Bearer token."""
    
    # Create user and get a real token via login
    User.objects.create_user(username="owner", password="p")
    login = client.post("/api/auth/token?username=owner&password=p")
    assert login.status_code == 200

    token = login.json()["token"]

    # Access protected endpoint using valid token
    res = client.get("/api/sensors", HTTP_AUTHORIZATION=f"Bearer {token}")

    # Should return 200 OK
    assert res.status_code == 200