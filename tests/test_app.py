"""
Backend tests for Mergington High School API.
Uses the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities to their initial state before each test"""
    # Reset to initial state
    app_module.activities.clear()
    app_module.activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Join the basketball team for practices and games",
            "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training and friendly competitions",
            "schedule": "Tuesdays and Fridays, 3:00 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media projects",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["chloe@mergington.edu", "logan@mergington.edu"]
        },
        "Drama Club": {
            "description": "Practice acting, improv, and put on school performances",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu", "henry@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots for competitions and learning",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["sophia@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["olivia@mergington.edu", "ethan@mergington.edu"]
        }
    })
    yield


client = TestClient(app_module.app)


class TestGetActivities:
    """Test GET /activities endpoint"""

    def test_get_activities_returns_200(self):
        """Test that GET /activities returns a 200 status and activities data"""
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Swimming Club",
            "Art Studio",
            "Drama Club",
            "Robotics Club",
            "Debate Team",
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        for activity_name in expected_activities:
            assert activity_name in activities
            assert "description" in activities[activity_name]
            assert "schedule" in activities[activity_name]
            assert "max_participants" in activities[activity_name]
            assert "participants" in activities[activity_name]


class TestSignup:
    """Test POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_email(self):
        """Test that duplicate email signup is rejected with 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already a participant

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower() or "already registered" in data["detail"].lower()

    def test_signup_invalid_activity(self):
        """Test that signup for non-existent activity returns 404"""
        # Arrange
        activity_name = "Non Existent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()


class TestRemoveParticipant:
    """Test DELETE /activities/{activity_name}/participants endpoint"""

    def test_remove_participant_success(self):
        """Test successful removal of a participant"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Known existing participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_missing_participant(self):
        """Test that removing non-existent participant returns 404"""
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_remove_from_invalid_activity(self):
        """Test that removing from non-existent activity returns 404"""
        # Arrange
        activity_name = "Non Existent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
