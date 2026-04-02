import pytest
from unittest.mock import AsyncMock
from app.main import app

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data

def test_match_endpoint(client, monkeypatch):
    """Test the /api/match endpoint with mocked IntelligenceEngine."""
    mock_intel = AsyncMock()
    mock_intel.find_match.return_value = {
        "user_id": "u1", "target_id": "u2", 
        "warm_path": {"nodes": [{"id": "u1", "name": "U1", "role": "R1"}], "edges": [], "hops": 1, "strength_score": 1.0}, 
        "serendipity": {"score": 50, "reasons": [], "primary_reason": "Spark", "complementarity_found": False},
        "strategic_reason": "Test reason", "hop_count": 1
    }
    
    import app.main
    monkeypatch.setattr(app.main, "intel_engine", mock_intel)
    
    response = client.post("/api/match", json={"user_id": "u1", "target_id": "u2"})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "u1"
    assert data["strategic_reason"] == "Test reason"

def test_recommend_endpoint(client, monkeypatch):
    """Test the /api/recommend/{user_id} endpoint."""
    mock_intel = AsyncMock()
    mock_intel.top_recommendations.return_value = [
        {"id": "r1", "name": "Rec 1", "role": "Role 1", "match_score": 90, 
         "complementarity": 1, "shared_topics": 2, "shared_communities": 1, 
         "shared_universities": 0, "shared_events": 0, "distance": 2,
         "short_reason": "Test reason"}
    ]
    
    import app.main
    monkeypatch.setattr(app.main, "intel_engine", mock_intel)
    
    response = client.get("/api/recommend/u1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "u1"
    assert len(data["recommendations"]) == 1
    assert data["recommendations"][0]["name"] == "Rec 1"

def test_icebreaker_endpoint(client, monkeypatch):
    """Test the /api/icebreaker endpoint."""
    mock_intel = AsyncMock()
    mock_intel.generate_icebreaker.return_value = {
        "target_name": "Target", "graph_icebreaker": "Hello!", 
        "exit_strategy": "Bye!", "reasoning": "Test", 
        "serendipity": {"score": 50}
    }
    
    import app.main
    monkeypatch.setattr(app.main, "intel_engine", mock_intel)
    
    response = client.post("/api/icebreaker", json={"user_id": "u1", "target_id": "u2"})
    assert response.status_code == 200
    assert response.json()["graph_icebreaker"] == "Hello!"

def test_micro_circle_endpoint(client, monkeypatch):
    """Test the /api/micro-circle endpoint."""
    mock_intel = AsyncMock()
    mock_intel.find_micro_circles.return_value = {
        "user_id": "u1", "micro_circles": [], "count": 0
    }
    
    import app.main
    monkeypatch.setattr(app.main, "intel_engine", mock_intel)
    
    response = client.post("/api/micro-circle", json={"user_id": "u1", "max_size": 3})
    assert response.status_code == 200
    assert response.json()["count"] == 0

def test_followup_endpoint(client, monkeypatch):
    """Test the /api/followup endpoint."""
    mock_intel = AsyncMock()
    mock_intel.generate_followup.return_value = {
        "contact_name": "Bob", 
        "follow_up_variants": {"professional": "P", "casual": "C", "creative": "Cr"}
    }
    
    import app.main
    monkeypatch.setattr(app.main, "intel_engine", mock_intel)
    
    response = client.post("/api/followup", json={"user_id": "u1", "target_id": "u2"})
    assert response.status_code == 200
    assert response.json()["contact_name"] == "Bob"
