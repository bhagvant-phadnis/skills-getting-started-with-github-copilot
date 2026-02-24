from urllib.parse import quote


def test_get_activities_contains_chess_club(client):
    # Arrange
    # (no special setup required)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    keys = set(data["Chess Club"].keys())
    assert keys >= {"description", "schedule", "max_participants", "participants"}


def test_post_signup_success_adds_participant(client):
    activity = "Chess Club"
    email = "newparticipant@mergington.edu"

    # Arrange
    before = client.get("/activities").json()[activity]["participants"][:]
    assert email not in before

    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    after = client.get("/activities").json()[activity]["participants"]
    assert email in after


def test_post_signup_duplicate_returns_400(client):
    activity = "Chess Club"
    email = "duplicate@mergington.edu"

    # Arrange - sign up once
    resp1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp1.status_code == 200

    # Act - try to sign up again
    resp2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp2.status_code == 400


def test_delete_remove_participant_success(client):
    activity = "Chess Club"
    participant = "michael@mergington.edu"

    # Arrange - ensure participant exists
    assert participant in client.get("/activities").json()[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": participant})

    # Assert
    assert resp.status_code == 200
    assert participant not in client.get("/activities").json()[activity]["participants"]


def test_delete_nonexistent_participant_returns_404(client):
    activity = "Chess Club"
    participant = "notfound@mergington.edu"

    # Arrange - ensure participant does not exist
    assert participant not in client.get("/activities").json()[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": participant})

    # Assert
    assert resp.status_code == 404
