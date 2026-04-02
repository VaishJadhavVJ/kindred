import pytest
import os
from unittest.mock import MagicMock, AsyncMock
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """FastAPI test client fixture."""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_neo4j():
    """Mock for Neo4jClient."""
    mock = MagicMock()
    # Add common return values for the mock
    mock.get_person_context.return_value = {"name": "Test User", "id": "test_id"}
    mock.find_warm_path.return_value = {"hops": 1, "path": [{"name": "User A"}, {"name": "User B"}]}
    mock.compute_serendipity.return_value = {"score": 50, "reasons": ["Shared interest"], "primary_reason": "Shared interest"}
    mock.get_top_recommendations.return_value = []
    mock.find_triangular_matches.return_value = []
    return mock

@pytest.fixture
def mock_rocketride():
    """Mock for RocketRideClient."""
    mock = AsyncMock()
    mock.connected = True
    mock.generate_text.return_value = '{"icebreaker": "Hello!", "exit_strategy": "Bye!", "reasoning": "Test"}'
    mock.transcribe_audio.return_value = "Test transcript"
    return mock

@pytest.fixture
def mock_openai():
    """Mock for OpenAIClient."""
    mock = AsyncMock()
    mock.client = MagicMock()
    mock.generate_text.return_value = '{"icebreaker": "Fallback Hello!", "exit_strategy": "Fallback Bye!", "reasoning": "Fallback"}'
    mock.transcribe_audio.return_value = "Fallback transcript"
    return mock
