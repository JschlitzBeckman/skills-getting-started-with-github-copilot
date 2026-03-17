import urllib.parse


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    encoded_activity_name = urllib.parse.quote(activity_name, safe="")
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"

    # Act
    encoded_activity_name = urllib.parse.quote(activity_name, safe="")
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_missing_participant(client):
    # Arrange
    activity_name = "Programming Class"
    missing_email = "not.enrolled@mergington.edu"

    # Act
    encoded_activity_name = urllib.parse.quote(activity_name, safe="")
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_repeat_delete_returns_not_found(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    encoded_activity_name = urllib.parse.quote(activity_name, safe="")
    client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
