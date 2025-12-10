import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister?email={test_email}")
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response2.status_code == 400
    # Unregister
    response3 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response3.status_code == 200
    assert f"Unregistered {test_email}" in response3.json()["message"]
    # Unregister again should fail
    response4 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response4.status_code == 400

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404

def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 308)  # Redirect or OK
