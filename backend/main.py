"""
Project Kindred — FastAPI Backend
Neo4j (graph) + RocketRide AI (intelligence) — no other AI dependencies.
"""

import os
import tempfile
import logging
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings, setup_logging
from app.neo4j_client import Neo4jClient
from app.rocketride_client import RocketRideClient
from app.intelligence import IntelligenceEngine
from app.openai_client import OpenAIClient

neo4j_client: Optional[Neo4jClient] = None
intel_engine: Optional[IntelligenceEngine] = None
rr_client: Optional[RocketRideClient] = None
openai_client: Optional[OpenAIClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global neo4j_client, intel_engine, rr_client, openai_client

    setup_logging()
    logger = logging.getLogger("kindred.startup")
    settings = get_settings()

    logger.info("Initializing Neo4j Graph client...")
    neo4j_client = Neo4jClient(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )

    logger.info("Initializing RocketRide Engine client...")
    rr_client = RocketRideClient(uri=settings.rocketride_uri)
    await rr_client.try_connect()

    logger.info("Initializing OpenAI client (fallback)...")
    openai_client = OpenAIClient()

    # Wire them together
    intel_engine = IntelligenceEngine(
        neo4j=neo4j_client, 
        rocketride=rr_client,
        openai=openai_client
    )

    yield

    if neo4j_client:
        neo4j_client.close()
    if rr_client:
        await rr_client.disconnect()


app = FastAPI(title="Project Kindred", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"[GlobalError] Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. The Kindred team has been notified."}
    )


from app.schemas import (
    HealthResponse, MatchRequest, MatchResponse, 
    IcebreakerResponse, FollowUpRequest, FollowUpResponse, 
    VoiceCaptureResponse, MicroCircleRequest, MicroCircleResponse,
    RecommendationListResponse, FullRecommendationResponse,
    ErrorResponse
)


# --- Routes ---

@app.get("/health", response_model=HealthResponse)
async def health():
    neo4j_up = neo4j_client is not None
    rr_up = rr_client is not None and rr_client.connected
    openai_fallback = openai_client is not None and openai_client.client is not None
    
    return {
        "status": "ok" if (neo4j_up and (rr_up or openai_fallback)) else "degraded",
        "services": {
            "neo4j": "connected" if neo4j_up else "disconnected",
            "rocketride": "connected" if rr_up else "disconnected",
            "openai_fallback": "configured" if openai_fallback else "missing_key",
        },
        "intelligence_mode": "rocketride" if rr_up else ("openai_fallback" if openai_fallback else "unavailable")
    }


@app.post("/api/match", response_model=MatchResponse, responses={500: {"model": ErrorResponse}})
async def match(req: MatchRequest):
    """Warm intro path + serendipity score."""
    try:
        return await intel_engine.find_match(req.user_id, req.target_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Match computation failed: {str(e)}")


@app.post("/api/icebreaker", response_model=IcebreakerResponse, responses={500: {"model": ErrorResponse}})
async def icebreaker(req: MatchRequest):
    """Graph-explained icebreaker via Intelligence LLM."""
    try:
        return await intel_engine.generate_icebreaker(req.user_id, req.target_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Icebreaker generation failed: {str(e)}")


@app.post("/api/followup", response_model=FollowUpResponse, responses={500: {"model": ErrorResponse}})
async def followup(req: FollowUpRequest):
    """Tri-variant follow-up messages via Intelligence LLM."""
    try:
        return await intel_engine.generate_followup(
            req.user_id, req.target_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Follow-up generation failed: {str(e)}")


@app.post("/api/voice-capture", response_model=VoiceCaptureResponse, responses={500: {"model": ErrorResponse}})
async def voice_capture(
    user_id: str,
    target_id: str,
    audio: UploadFile = File(...),
):
    """
    THE GOLDEN PATH.
    Audio → Whisper → Neo4j graph → LLM → JSON contract.
    """
    suffix = os.path.splitext(audio.filename or "audio.webm")[1] or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        return await intel_engine.full_pipeline(
            user_id=user_id, target_id=target_id, audio_path=tmp_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice capture pipeline failed: {str(e)}")
    finally:
        os.unlink(tmp_path)


@app.post("/api/micro-circle", response_model=MicroCircleResponse, responses={500: {"model": ErrorResponse}})
async def micro_circle(req: MicroCircleRequest):
    """Triangular ask/offer matches from the graph."""
    try:
        return await intel_engine.find_micro_circles(req.user_id, req.max_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Micro-circle generation failed: {str(e)}")


@app.get("/api/recommend/{user_id}", responses={
    200: {
        "description": "Either a list of recommendations, or a full detailed profile if target_id is passed",
        "content": {
            "application/json": {}
        }
    },
    500: {"model": ErrorResponse}
})
async def recommend(user_id: str, target_id: Optional[str] = None):
    """Full recommendation. With target_id: warm path + icebreaker. Without: top 5."""
    try:
        if target_id:
            data = await intel_engine.full_recommendation(user_id, target_id)
            return FullRecommendationResponse(**data)
        
        data = await intel_engine.top_recommendations(user_id, limit=5)
        return RecommendationListResponse(user_id=user_id, recommendations=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation pipeline failed: {str(e)}")
