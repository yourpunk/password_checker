from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_check_password_returns_score_and_category():
    response = client.post("/api/check", json={"password": "Tr@v3l$2024!Nz"})
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "category" in data
    assert "criteria" in data
    assert "suggestions" in data

def test_check_weak_password():
    response = client.post("/api/check", json={"password": "abc"})
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "weak"

def test_check_strong_password():
    response = client.post("/api/check", json={"password": "Tr@v3l$2024!Nz"})
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "strong"
    assert data["score"] >= 80

def test_empty_password():
    response = client.post("/api/check", json={"password": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 0

def test_check_password_criteria_structure():
    response = client.post("/api/check", json={"password": "TestPass1!"})
    data = response.json()
    criteria_names = {c["name"] for c in data["criteria"]}
    assert "length" in criteria_names
    assert "character_variety" in criteria_names
    assert "repetition" in criteria_names
    assert "sequences" in criteria_names
    assert "common_patterns" in criteria_names

def test_check_password_missing_field_returns_422():
    response = client.post("/api/check", json={})
    assert response.status_code == 422