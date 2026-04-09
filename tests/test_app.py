import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_redirect(client):
    # Arrange: No special setup needed

    # Act: Make GET request to root
    response = client.get("/")

    # Assert: Should serve the index.html content (redirect followed in test client)
    assert response.status_code == 200
    assert "Mergington High School" in response.text


def test_get_activities(client):
    # Arrange: No special setup needed

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Should return 200 and activities data
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_success(client):
    # Arrange: Use a new email not in the list
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 200 and success message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]


def test_signup_for_activity_duplicate(client):
    # Arrange: Use an email already signed up
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 400 with error message
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_for_activity_invalid(client):
    # Arrange: Use a non-existent activity
    activity_name = "NonExistent Club"
    email = "test@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_remove_participant_success(client):
    # Arrange: First signup a participant
    activity_name = "Programming Class"
    email = "removeme@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act: Make DELETE request to remove participant
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert: Should return 200 and success message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]


def test_remove_participant_not_found(client):
    # Arrange: Use an email not in participants
    activity_name = "Programming Class"
    email = "notsignedup@mergington.edu"

    # Act: Make DELETE request to remove participant
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]


def test_remove_participant_invalid_activity(client):
    # Arrange: Use a non-existent activity
    activity_name = "Invalid Club"
    email = "test@mergington.edu"

    # Act: Make DELETE request to remove participant
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]