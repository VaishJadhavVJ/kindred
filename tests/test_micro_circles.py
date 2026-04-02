import pytest
from unittest.mock import AsyncMock, MagicMock
from app.intelligence import IntelligenceEngine

@pytest.mark.asyncio
async def test_find_micro_circles_success(mock_neo4j, mock_rocketride, mock_openai):
    """Verify that micro-circle discovery returns structured loop data."""
    mock_neo4j.find_triangular_matches.return_value = [
        {
            "members": [
                {"id": "u1", "name": "Alice", "role": "Dev", "contribution": "TypeScript"},
                {"id": "u2", "name": "Bob", "role": "Designer", "contribution": "UI Design"},
                {"id": "u3", "name": "Charlie", "role": "PM", "contribution": "Product Strategy"}
            ],
            "why_this_circle": "Value Loop: Strategy -> UI -> Dev",
            "loop_strength": 1.2,
            "direct_value": "Direct utility found",
            "indirect_value": "Indirect utility found"
        }
    ]
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    result = await engine.find_micro_circles("u1")
    
    assert result["count"] == 1
    assert "Alice" in [m["name"] for m in result["micro_circles"][0]["members"]]
    assert result["micro_circles"][0]["loop_strength"] == 1.2

@pytest.mark.asyncio
async def test_find_micro_circles_empty(mock_neo4j, mock_rocketride, mock_openai):
    """Verify clean handling of no loops found."""
    mock_neo4j.find_triangular_matches.return_value = []
    
    engine = IntelligenceEngine(neo4j=mock_neo4j, rocketride=mock_rocketride, openai=mock_openai)
    result = await engine.find_micro_circles("u1")
    
    assert result["count"] == 0
    assert result["micro_circles"] == []
