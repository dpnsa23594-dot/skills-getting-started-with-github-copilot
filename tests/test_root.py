"""Tests for GET / root endpoint."""

import pytest


def test_root_redirect(client):
    """Test that root path redirects to static index.html."""
    # Arrange: TestClient is provided by fixture

    # Act: Make GET request to root
    response = client.get("/", follow_redirects=False)  # Don't follow redirect

    # Assert: Check for redirect response
    assert response.status_code == 307  # Temporary Redirect status
    assert response.headers["location"] == "/static/index.html"