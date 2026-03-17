def test_get_activities_returns_expected_shape(client):
    # Arrange

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_get_activities_entries_include_required_fields(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    for activity in data.values():
        assert required_fields.issubset(activity.keys())
        assert isinstance(activity["participants"], list)
