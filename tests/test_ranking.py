import pytest
from unittest.mock import AsyncMock, MagicMock
from app.intelligence import IntelligenceEngine

@pytest.mark.asyncio
async def test_ranking_reasons_complementarity(mock_neo4j, mock_rocketride, mock_openai):
    """Verify that complementarity yields the 'Exactly what you need' reason."""
    mock_neo4j.get_top_recommendations.return_value = [
        {
            "id": "u1", "name": "Expert", "role": "Dev", "company": "Co",
            "match_score": 100, "complementarity": 2, "shared_topics": 0,
            "shared_communities": 0, "shared_universities": 0, "shared_events": 0,
            "distance": 3, "short_reason": "Offers exactly what you need"
        }
    ]
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    results = await engine.top_recommendations("you")
    
    assert len(results) == 1
    assert results[0]["short_reason"] == "Offers exactly what you need"

@pytest.mark.asyncio
async def test_ranking_reasons_university(mock_neo4j, mock_rocketride, mock_openai):
    """Verify that university overlap yields the alumni reason."""
    mock_neo4j.get_top_recommendations.return_value = [
        {
            "id": "u2", "name": "Alum", "role": "PM", "company": "Co",
            "match_score": 60, "complementarity": 0, "shared_topics": 0,
            "shared_communities": 0, "shared_universities": 1, "shared_events": 0,
            "distance": 4, "short_reason": "Fellow UIC alumni"
        }
    ]
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    results = await engine.top_recommendations("you")
    
    assert results[0]["short_reason"] == "Fellow UIC alumni"

@pytest.mark.asyncio
async def test_ranking_reasons_warm_intro(mock_neo4j, mock_rocketride, mock_openai):
    """Verify that distance=2 yields the warm intro reason."""
    mock_neo4j.get_top_recommendations.return_value = [
        {
            "id": "u3", "name": "Friend", "role": "Designer", "company": "Co",
            "match_score": 50, "complementarity": 0, "shared_topics": 0,
            "shared_communities": 0, "shared_universities": 0, "shared_events": 0,
            "distance": 2, "short_reason": "Intro possible via mutual connection"
        }
    ]
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    results = await engine.top_recommendations("you")
    
    assert results[0]["short_reason"] == "Intro possible via mutual connection"
