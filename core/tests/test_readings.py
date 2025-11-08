import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import Sensor, Reading
from django.utils import timezone
from datetime import timedelta

def bearer(t):
    # Helper: adds the authorization header with the user's token
    return {"HTTP_AUTHORIZATION": f"Bearer {t}"}

@pytest.mark.django_db
def test_readings_filter_and_order(client):
    """GET /api/sensors/{id}/readings should return filtered and newest first readings"""

    # Create user and token
    user = User.objects.create_user(username="readingtest", password="test1234")
    token,  _ = Token.objects.get_or_create(user=user)

    # Create sensor for this user
    sensor = Sensor.objects.create(name="TestSensor", type="Env", owner=user)

    # Create two readings with different timestamps
    now = timezone.now()
    old = Reading.objects.create(sensor=sensor, temperature=18, humidity=44, timestamp=now - timedelta(minutes=3))
    new = Reading.objects.create(sensor=sensor, temperature=24, humidity=49, timestamp=now - timedelta(minutes=1))

    # Send GET request with auth token
    res = client.get(f"/api/sensors/{sensor.id}/readings", HTTP_AUTHORIZATION=f"Bearer {token.key}")

    # Check response is ok and ordered newest first
    assert res.status_code == 200
    data = res.json()
    assert [r["id"] for r in data] == [new.id, old.id]


@pytest.mark.django_db
def test_readings_filter_by_date_range(client):
    """GET /api/sensors/{id}/readings respects timestamp_from/to"""

    # Create a test user and get token
    u = User.objects.create_user(username="u", password="p")
    tok, _ = Token.objects.get_or_create(user=u)

    # Create a sensor fot this user
    s = Sensor.objects.create(name="S", type="Env", owner=u)

    # Create three readings at different times 
    now = timezone.now()
    r_old = Reading.objects.create(sensor=s, temperature=18, humidity=44, timestamp=now - timedelta(hours=2))
    r_mid = Reading.objects.create(sensor=s, temperature=20, humidity=45, timestamp=now - timedelta(minutes=45))
    r_new = Reading.objects.create(sensor=s, temperature=22, humidity=46, timestamp=now - timedelta(minutes=5))

    # Show only readings from the last 60 to 10 minutes
    qs = f"?timestamp_from={(now - timedelta(minutes=60)).isoformat()}&timestamp_to={(now - timedelta(minutes=10)).isoformat()}"

    # Send GET request with Bearer token
    res = client.get(
    f"/api/sensors/{s.id}/readings",
    {
        "timestamp_from": (now - timedelta(minutes=60)).isoformat(),
        "timestamp_to":   (now - timedelta(minutes=10)).isoformat(),
    },
    HTTP_AUTHORIZATION=f"Bearer {tok.key}",
)

    # Response should be OK
    assert res.status_code == 200

    # Check that only the middle reading is returned
    ids = [x["id"] for x in res.json()]
    assert ids == [r_mid.id]


@pytest.mark.django_db
def test_create_reading_requires_auth_and_allows_with_token(client):
    """POST /api/sensors/{id}/readings requires token and creates a reading"""

    # Create a test user and token
    u = User.objects.create_user(username="u2", password="p")
    tok, _ = Token.objects.get_or_create(user=u)

    # Create a sensor owned by this user
    s = Sensor.objects.create(name="S2", type="Env", owner=u)

    # Prepare the reading data
    payload = {
        "temperature": 21.5,
        "humidity": 50.0,
        "timestamp": timezone.now().isoformat()
    }

    # Try to send request without token, that should fail with 401
    r401 = client.post(f"/api/sensors/{s.id}/readings", data=payload, content_type="application/json")
    assert r401.status_code == 401

    # Try again with valid token, that should work with 200 or 201
    r_ok = client.post(
        f"/api/sensors/{s.id}/readings",
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {tok.key}",
    )

    # Check success
    assert r_ok.status_code in (200, 201)
    data = r_ok.json()
    assert float(data["temperature"]) == 21.5
    assert float(data["humidity"]) == 50.0