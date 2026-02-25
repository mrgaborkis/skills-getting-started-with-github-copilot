"""
Basic tests for the activities endpoints using the AAA (Arrange-Act-Assert) pattern.
"""

def test_get_activities_returns_expected_keys(client):
    # Arrange
    # (client fixture provided)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"].get("participants"), list)
