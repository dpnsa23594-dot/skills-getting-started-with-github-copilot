"""Tests for GET /activities endpoint."""

import pytest


def test_get_activities_success(client):
    """Test successful retrieval of all activities."""
    # Arrange: TestClient is provided by fixture

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status code and response structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Should have 9 activities

    # Check that expected activities are present
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Studio", "Music Band", "Science Club", "Debate Team"
    ]
    for activity in expected_activities:
        assert activity in data
        assert "description" in data[activity]
        assert "schedule" in data[activity]
        assert "max_participants" in data[activity]
        assert "participants" in data[activity]
        assert isinstance(data[activity]["participants"], list)