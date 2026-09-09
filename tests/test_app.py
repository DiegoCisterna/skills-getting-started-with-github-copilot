"""Tests for the Mergington High School Activities API."""
from src.app import activities as app_activities


def test_root_redirects_to_static_index(client):
    # Arrange: no additional setup required beyond the shared client fixture

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange: no additional setup required beyond the shared client fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == set(app_activities.keys())

    for name, activity in data.items():
        assert activity["description"] == app_activities[name]["description"]
        assert activity["schedule"] == app_activities[name]["schedule"]
        assert activity["max_participants"] == app_activities[name]["max_participants"]
        assert activity["participants"] == app_activities[name]["participants"]


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in app_activities[activity_name]["participants"]


def test_signup_for_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
