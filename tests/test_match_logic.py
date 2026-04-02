import pytest
from unittest.mock import AsyncMock
from app.intelligence import IntelligenceEngine

@pytest.mark.asyncio
async def test_match_priority_complementarity(mock_neo4j, mock_rocketride, mock_openai):
    """Priority 1: Complementarity should be the strategic reason."""
    mock_neo4j.find_warm_path.return_value = {"nodes": [], "edges": [], "hops": -1, "strength_score": 0.0}
    mock_neo4j.compute_serendipity.return_value = {
        "score": 90, "reasons": ["Offers Python expertise"], 
        "primary_reason": "Python expertise", "complementarity_found": True
    }
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    result = await engine.find_match("u1", "u2")
    
    assert "Direct Synergy" in result["strategic_reason"]
    assert "Python expertise" in result["strategic_reason"]

@pytest.mark.asyncio
async def test_match_priority_high_trust_path(mock_neo4j, mock_rocketride, mock_openai):
    """Priority 2: High-trust warm path (if no complementarity)."""
    mock_neo4j.find_warm_path.return_value = {
        "nodes": [{"name": "A"}, {"name": "Connector"}, {"name": "B"}], 
        "edges": [{"trust": 0.9}], "hops": 2, "strength_score": 0.9
    }
    mock_neo4j.compute_serendipity.return_value = {
        "score": 30, "reasons": ["Both in Chicago"], 
        "primary_reason": "Chicago", "complementarity_found": False
    }
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    result = await engine.find_match("u1", "u2")
    
    assert "high-trust connection Connector" in result["strategic_reason"]

@pytest.mark.asyncio
async def test_match_no_path_found(mock_neo4j, mock_rocketride, mock_openai):
    """Scenario: No social path, but shared interest exists."""
    mock_neo4j.find_warm_path.return_value = {"nodes": [], "edges": [], "hops": -1, "strength_score": 0.0}
    mock_neo4j.compute_serendipity.return_value = {
        "score": 40, "reasons": ["Both like AI"], 
        "primary_reason": "Both like AI", "complementarity_found": False
    }
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    result = await engine.find_match("u1", "u2")
    
    assert result["hop_count"] == -1
    assert "Both like AI" in result["strategic_reason"]
