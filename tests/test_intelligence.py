import pytest
from unittest.mock import AsyncMock, MagicMock
from app.intelligence import IntelligenceEngine

@pytest.mark.asyncio
async def test_llm_generate_rocketride_success(mock_neo4j, mock_rocketride, mock_openai):
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    mock_rocketride.generate_text.return_value = '{"success": true}'
    
    result = await engine._llm_generate("sys", "user")
    assert result == '{"success": true}'
    mock_rocketride.generate_text.assert_called_once()
    mock_openai.generate_text.assert_not_called()

@pytest.mark.asyncio
async def test_llm_generate_openai_fallback(mock_neo4j, mock_rocketride, mock_openai):
    mock_rocketride.generate_text.return_value = None
    mock_openai.generate_text.return_value = '{"fallback": true}'
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    result = await engine._llm_generate("sys", "user")
    
    assert result == '{"fallback": true}'
    mock_openai.generate_text.assert_called_once()

@pytest.mark.asyncio
async def test_find_match_logic(mock_neo4j, mock_rocketride, mock_openai):
    mock_neo4j.find_warm_path.return_value = {
        "nodes": [{"id": "u1", "name": "U1"}, {"id": "i", "name": "Inter"}, {"id": "u2", "name": "U2"}],
        "edges": [{"trust": 0.8}],
        "hops": 2,
        "strength_score": 0.8
    }
    mock_neo4j.compute_serendipity.return_value = {
        "score": 80, "reasons": ["Spark"], "primary_reason": "Spark", "complementarity_found": False
    }
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    result = await engine.find_match("u1", "u2")
    
    assert "Warm intro possible via high-trust connection Inter" in result["strategic_reason"]
    assert result["hop_count"] == 2

@pytest.mark.asyncio
async def test_icebreaker_fallback_logic(mock_neo4j, mock_rocketride, mock_openai):
    # Simulate both AIs failing to return a valid JSON or being offline
    mock_rocketride.generate_text.return_value = None
    mock_openai.generate_text.return_value = None
    mock_neo4j.find_warm_path.return_value = {"nodes": [], "edges": [], "hops": -1, "strength_score": 0.0}
    mock_neo4j.compute_serendipity.return_value = {"reasons": ["niche interest in synths"], "primary_reason": "synths", "score": 90, "complementarity_found": False}
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    result = await engine.generate_icebreaker("u1", "u2")
    
    # Verify it uses the fact-based fallback
    assert "niche interest in synths" in result["graph_icebreaker"]
    assert result["reasoning"] == "LLM fallback triggered."
