"""
Signup flow tests (AAA pattern) covering signup, duplicate signup, removal,
and error cases for missing activities.
"""

def test_signup_and_remove_flow(client, sample_activity_name, sample_email):
    # Arrange
    activity = sample_activity_name
    email = sample_email

    # Act — signup
    signup_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert — signup succeeded
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json().get("message", "")

    # Act — verify participant present
    activities_resp = client.get("/activities")
    assert activities_resp.status_code == 200
    participants = activities_resp.json()[activity]["participants"]
    assert email in participants

    # Act — duplicate signup should fail
    dup_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert — duplicate returns 400 with helpful detail
    assert dup_resp.status_code == 400
    assert dup_resp.json().get("detail") == "Student already signed up for this activity"

    # Act — remove participant
    remove_resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert — removal succeeded
    assert remove_resp.status_code == 200
    assert "Removed" in remove_resp.json().get("message", "")

    # Act — removing again should fail
    remove_again = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert — returns 400 with helpful detail
    assert remove_again.status_code == 400
    assert remove_again.json().get("detail") == "Student is not signed up for this activity"


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    fake_activity = "Nonexistent Activity"
    email = "noone@example.com"

    # Act
    resp = client.post(f"/activities/{fake_activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Activity not found"
