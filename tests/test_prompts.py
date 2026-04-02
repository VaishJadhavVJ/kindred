import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from app.intelligence import IntelligenceEngine

@pytest.mark.asyncio
async def test_safe_parse_json_markdown(mock_neo4j, mock_rocketride, mock_openai):
    """Ensure _safe_parse_json can handle markdown-wrapped JSON blocks."""
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    dirty_json = "Here is the response: ```json\n{\"icebreaker\": \"Hello!\"}\n```"
    
    result = engine._safe_parse_json(dirty_json, {"icebreaker": "Fallback"})
    assert result["icebreaker"] == "Hello!"

@pytest.mark.asyncio
async def test_icebreaker_prompt_grounding(mock_neo4j, mock_rocketride, mock_openai):
    """Verify that build_icebreaker passes graph facts into the LLM logic."""
    mock_neo4j.get_person_context.side_effect = [
        {"name": "Alice", "interests": ["AI"]},
        {"name": "Bob", "interests": ["Web3"]}
    ]
    mock_neo4j.find_warm_path.return_value = {"nodes": [], "hops": -1}
    mock_neo4j.compute_serendipity.return_value = {"reasons": ["Both code"], "complementarity_found": False}
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    
    # We want to see what is passed to _llm_generate
    mock_rocketride.generate_text.return_value = '{"icebreaker": "Prompt Test"}'
    
    await engine.generate_icebreaker("u1", "u2")
    
    # Check the user prompt sent to RocketRide
    args, kwargs = mock_rocketride.generate_text.call_args
    user_prompt = args[1]
    
    assert "Alice" in user_prompt
    assert "Bob" in user_prompt
    assert "Both code" in user_prompt

@pytest.mark.asyncio
async def test_generate_followup_grounding(mock_neo4j, mock_rocketride, mock_openai):
    """Verify follow-up uses strategic reasons for grounding."""
    mock_neo4j.get_person_context.return_value = {"name": "Bob"}
    # find_match result
    mock_neo4j.find_warm_path.return_value = {"nodes": [], "hops": -1}
    mock_neo4j.compute_serendipity.return_value = {"reasons": ["Niche interest"], "complementarity_found": False}
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    mock_rocketride.generate_text.return_value = '{"professional": "P", "casual": "C", "creative": "Cr"}'
    
    await engine.generate_followup("u1", "u2")
    
    args, kwargs = mock_rocketride.generate_text.call_args
    user_prompt = args[1]
    
    assert "Niche interest" in user_prompt
