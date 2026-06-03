from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_new_student(client):
    email = "tester@mergington.edu"
    activity = "Chess Club"
    url = f"/activities/{quote(activity)}/signup"
    resp = client.post(url, params={"email": email})
    assert resp.status_code == 200
    assert f"Signed up {email} for {activity}" in resp.json().get("message", "")

    # Verify participant present
    all_resp = client.get("/activities")
    assert email in all_resp.json()[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    email = "dup@mergington.edu"
    activity = "Programming Class"
    url = f"/activities/{quote(activity)}/signup"
    r1 = client.post(url, params={"email": email})
    assert r1.status_code == 200
    r2 = client.post(url, params={"email": email})
    assert r2.status_code == 400


def test_unregister_existing_student(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Ensure starting assumption
    start = client.get("/activities").json()
    assert email in start[activity]["participants"]

    url = f"/activities/{quote(activity)}/participants"
    r = client.delete(url, params={"email": email})
    assert r.status_code == 200

    after = client.get("/activities").json()
    assert email not in after[activity]["participants"]


def test_unregister_nonexistent_returns_404(client):
    activity = "Chess Club"
    email = "noone@mergington.edu"
    url = f"/activities/{quote(activity)}/participants"
    r = client.delete(url, params={"email": email})
    assert r.status_code == 404
