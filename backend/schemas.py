from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class HealthResponse(BaseModel):
    status: str
    services: Dict[str, str]
    intelligence_mode: str

class MatchRequest(BaseModel):
    user_id: str
    target_id: str

class MatchResponse(BaseModel):
    user_id: str
    target_id: str
    warm_path: Dict[str, Any]
    serendipity: Dict[str, Any]

class IcebreakerResponse(BaseModel):
    target_name: str
    graph_icebreaker: str
    exit_strategy: str
    reasoning: str
    serendipity: Dict[str, Any]

class FollowUpRequest(BaseModel):
    user_id: str
    target_id: str
    conversation_notes: str = ""

class FollowUpResponse(BaseModel):
    contact_name: str
    follow_up_variants: Dict[str, str]

class VoiceCaptureResponse(BaseModel):
    target_name: str
    serendipity_score: int
    transcript: str
    insights: Dict[str, str]
    follow_up_variants: Dict[str, str]
    warm_path: Dict[str, Any]
    serendipity_reasons: List[str]

class MicroCircleRequest(BaseModel):
    user_id: str
    max_size: int = 3

class MicroCircleResponse(BaseModel):
    user_id: str
    micro_circles: List[Dict[str, Any]]
    count: int

class RecommendationItem(BaseModel):
    id: str
    name: str
    role: str
    company: Optional[str] = None
    match_score: int
    complementarity: int
    shared_topics: int
    distance: int

class RecommendationListResponse(BaseModel):
    user_id: str
    recommendations: List[Dict[str, Any]]

class FullRecommendationResponse(BaseModel):
    target_name: str
    serendipity_score: int
    warm_path: Dict[str, Any]
    insights: Dict[str, str]
    serendipity_reasons: List[str]

class ErrorResponse(BaseModel):
    detail: str
