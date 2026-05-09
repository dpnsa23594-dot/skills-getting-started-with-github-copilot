"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_success(client):
    """Test successful signup for an activity."""
    # Arrange: Choose an activity and a new email
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check status code and response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" in data["message"]

    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity."""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act: Make POST request
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 404
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_email(client):
    """Test signup with email already signed up for the activity."""
    # Arrange: First, sign up a student
    activity_name = "Programming Class"
    email = "duplicatestudent@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act: Try to sign up the same email again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 400
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up" in data["detail"]


def test_signup_missing_email(client):
    """Test signup without providing email parameter."""
    # Arrange: Activity name
    activity_name = "Gym Class"

    # Act: Make POST request without email
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert: Should return 422 (Unprocessable Entity) for missing required param
    assert response.status_code == 422