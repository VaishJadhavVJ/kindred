from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# --- Shared Utilities ---

class ServiceHealth(BaseModel):
    neo4j: str
    rocketride: str
    openai_fallback: str

class HealthResponse(BaseModel):
    status: str
    services: ServiceHealth
    intelligence_mode: str

class ErrorResponse(BaseModel):
    detail: str

# --- /api/match ---

class MatchRequest(BaseModel):
    user_id: str
    target_id: str

class PathNode(BaseModel):
    id: str
    name: str
    role: str

class PathEdge(BaseModel):
    type: str
    trust: float = 1.0
    context: Optional[str] = None

class WarmPathDetails(BaseModel):
    nodes: List[PathNode]
    edges: List[PathEdge]
    hops: int
    strength_score: float

class SerendipityDetails(BaseModel):
    score: int
    reasons: List[str]
    primary_reason: str
    complementarity_found: bool

class MatchResponse(BaseModel):
    user_id: str
    target_id: str
    warm_path: WarmPathDetails
    serendipity: SerendipityDetails
    strategic_reason: str
    hop_count: int

# --- /api/icebreaker ---

class IcebreakerResponse(BaseModel):
    target_name: str
    graph_icebreaker: str
    exit_strategy: str
    reasoning: str
    serendipity: Dict[str, Any]

# --- /api/followup ---

class FollowUpRequest(BaseModel):
    user_id: str
    target_id: str
    conversation_notes: Optional[str] = None

class FollowUpVariants(BaseModel):
    professional: str
    casual: str
    creative: str

class FollowUpResponse(BaseModel):
    contact_name: str
    follow_up_variants: FollowUpVariants

# --- /api/voice-capture ---

class VoiceCaptureInsights(BaseModel):
    graph_icebreaker: str
    exit_strategy: str

class VoiceCaptureResponse(BaseModel):
    target_name: str
    serendipity_score: int
    transcript: str
    insights: VoiceCaptureInsights
    follow_up_variants: FollowUpVariants
    warm_path: WarmPathDetails
    serendipity_reasons: List[str]

# --- /api/micro-circle ---

class MicroCircleRequest(BaseModel):
    user_id: str
    max_size: int = 3

class MicroCircleMember(BaseModel):
    id: str
    name: str
    role: str
    contribution: str # What they offer that the loop needs

class MicroCircleItem(BaseModel):
    members: List[MicroCircleMember]
    why_this_circle: str
    loop_strength: float
    direct_value: str
    indirect_value: str

class MicroCircleResponse(BaseModel):
    user_id: str
    micro_circles: List[MicroCircleItem]
    count: int

# --- /api/recommend ---

class RecommendationItem(BaseModel):
    id: str
    name: str
    role: str
    company: Optional[str] = None
    match_score: float
    complementarity: int
    shared_topics: int
    shared_communities: int
    shared_universities: int
    shared_events: int # New
    distance: int
    short_reason: str # New: Explainable ranking signal

class RecommendationListResponse(BaseModel):
    user_id: str
    recommendations: List[RecommendationItem]

# Note: Full recommendation when target_id is present inherits structures 
# from VoiceCaptureResponse practically, but we reuse existing models.
class FullRecommendationResponse(BaseModel):
    target_name: str
    serendipity_score: int
    strategic_reason: str
    warm_path: WarmPathDetails
    insights: VoiceCaptureInsights
    serendipity_reasons: List[str]
