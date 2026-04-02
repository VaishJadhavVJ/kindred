"""
Project Kindred — FastAPI Backend
Neo4j (graph) + RocketRide AI (intelligence) — no other AI dependencies.
"""

import os
import tempfile
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from app.neo4j_client import Neo4jClient
from app.rocketride_client import RocketRideClient
from app.intelligence import IntelligenceEngine

load_dotenv()

neo4j_client: Optional[Neo4jClient] = None
intel_engine: Optional[IntelligenceEngine] = None
rr_client: Optional[RocketRideClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global neo4j_client, intel_engine, rr_client

    # Neo4j
    neo4j_client = Neo4jClient(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD", "password"),
    )

    # RocketRide engine
    rr_client = RocketRideClient(
        uri=os.getenv("ROCKETRIDE_URI", "http://localhost:5565")
    )
    await rr_client.try_connect()

    # Wire them together
    intel_engine = IntelligenceEngine(neo4j=neo4j_client, rocketride=rr_client)

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


# --- Request models ---
class MatchRequest(BaseModel):
    user_id: str
    target_id: str


class FollowUpRequest(BaseModel):
    user_id: str
    contact_name: str
    conversation_notes: str


class MicroCircleRequest(BaseModel):
    user_id: str
    max_size: int = 3


# --- Routes ---

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "neo4j": neo4j_client is not None,
        "rocketride": rr_client is not None and rr_client.connected,
    }


@app.post("/api/match")
async def match(req: MatchRequest):
    """Warm intro path + serendipity score."""
    return await intel_engine.find_match(req.user_id, req.target_id)


@app.post("/api/icebreaker")
async def icebreaker(req: MatchRequest):
    """Graph-explained icebreaker via RocketRide LLM."""
    return await intel_engine.generate_icebreaker(req.user_id, req.target_id)


@app.post("/api/followup")
async def followup(req: FollowUpRequest):
    """Tri-variant follow-up messages via RocketRide LLM."""
    return await intel_engine.generate_followups(
        req.user_id, req.contact_name, req.conversation_notes
    )


@app.post("/api/voice-capture")
async def voice_capture(
    user_id: str,
    target_id: str,
    audio: UploadFile = File(...),
):
    """
    THE GOLDEN PATH.
    Audio → RocketRide Whisper → Neo4j graph → RocketRide LLM → JSON contract.
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
    finally:
        os.unlink(tmp_path)


@app.post("/api/micro-circle")
async def micro_circle(req: MicroCircleRequest):
    """Triangular ask/offer matches from the graph."""
    return await intel_engine.find_micro_circles(req.user_id, req.max_size)


@app.get("/api/recommend/{user_id}")
async def recommend(user_id: str, target_id: Optional[str] = None):
    """Full recommendation. With target_id: warm path + icebreaker. Without: top 5."""
    if target_id:
        return await intel_engine.full_recommendation(user_id, target_id)
    return {
        "user_id": user_id,
        "recommendations": await intel_engine.top_recommendations(user_id, limit=5),
    }
