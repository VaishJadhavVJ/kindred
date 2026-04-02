"""
Intelligence Engine — RocketRide AI is the ONLY AI layer.

All LLM calls and audio transcription go through RocketRide pipelines.
Neo4j provides the graph context. RocketRide provides the intelligence.
"""

import json
from typing import Optional

from app.neo4j_client import Neo4jClient
from app.rocketride_client import RocketRideClient


class IntelligenceEngine:
    def __init__(self, neo4j: Neo4jClient, rocketride: RocketRideClient):
        self.neo4j = neo4j
        self.rr = rocketride

    # ------------------------------------------------------------------
    # Core: send prompts through RocketRide's LLM pipeline
    # ------------------------------------------------------------------
    async def _llm_generate(self, system_prompt: str, user_prompt: str) -> str:
        result = await self.rr.generate_text(system_prompt, user_prompt)
        if result:
            return result
        return '{"error": "RocketRide engine not available. Start it with: docker run -p 5565:5565 ghcr.io/rocketride-org/rocketride-engine:latest"}'

    # ------------------------------------------------------------------
    # Core: transcribe audio through RocketRide's Whisper pipeline
    # ------------------------------------------------------------------
    async def _transcribe(self, audio_path: str) -> str:
        result = await self.rr.transcribe_audio(audio_path)
        if result:
            return result
        return "[Transcription unavailable — RocketRide engine not running]"

    # ------------------------------------------------------------------
    # MATCH — warm path + serendipity score
    # ------------------------------------------------------------------
    async def find_match(self, user_id: str, target_id: str) -> dict:
        warm_path = self.neo4j.find_warm_path(user_id, target_id)
        serendipity = self.neo4j.compute_serendipity(user_id, target_id)
        return {
            "user_id": user_id,
            "target_id": target_id,
            "warm_path": warm_path,
            "serendipity": serendipity,
        }

    # ------------------------------------------------------------------
    # ICEBREAKER — graph-grounded opening line via RocketRide LLM
    # ------------------------------------------------------------------
    async def generate_icebreaker(self, user_id: str, target_id: str) -> dict:
        user_ctx = self.neo4j.get_person_context(user_id)
        target_ctx = self.neo4j.get_person_context(target_id)
        serendipity = self.neo4j.compute_serendipity(user_id, target_id)
        warm_path = self.neo4j.find_warm_path(user_id, target_id)

        system = """You are a networking intelligence assistant. Generate a natural,
specific icebreaker for starting a conversation at a professional event.

Rules:
- Ground the icebreaker in ACTUAL shared context (interests, events, skills, connections)
- Never be generic like "You both like AI"
- Reference specific overlap from the graph data
- Keep it conversational, 1-2 sentences
- Also generate a polite exit strategy (1 sentence)

Respond ONLY in JSON: {"icebreaker": "...", "exit_strategy": "...", "reasoning": "..."}"""

        user_prompt = f"""
User: {json.dumps(user_ctx, default=str)}
Target: {json.dumps(target_ctx, default=str)}
Shared overlap: {json.dumps(serendipity, default=str)}
Connection path: {json.dumps(warm_path, default=str)}
"""

        raw = await self._llm_generate(system, user_prompt)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"icebreaker": raw, "exit_strategy": "", "reasoning": ""}

        return {
            "target_name": target_ctx.get("name", target_id),
            "graph_icebreaker": parsed.get("icebreaker", raw),
            "exit_strategy": parsed.get("exit_strategy", ""),
            "reasoning": parsed.get("reasoning", ""),
            "serendipity": serendipity,
        }

    # ------------------------------------------------------------------
    # FOLLOW-UPS — tri-variant messages via RocketRide LLM
    # ------------------------------------------------------------------
    async def generate_followups(
        self, user_id: str, contact_name: str, conversation_notes: str
    ) -> dict:
        user_ctx = self.neo4j.get_person_context(user_id)

        system = """You are a networking follow-up assistant. Generate three variants
of a follow-up message after meeting someone at an event.

- Professional: formal, references shared professional interests, clear next step
- Casual: warm, friendly, references personal/fun overlap, low-pressure
- Creative: memorable, references a surprising shared interest or inside joke

Each should be 2-4 sentences. Include the person's name naturally.

Respond ONLY in JSON: {"professional": "...", "casual": "...", "creative": "..."}"""

        user_prompt = f"""
Your profile: {json.dumps(user_ctx, default=str)}
Person you met: {contact_name}
What you talked about: {conversation_notes}
"""

        raw = await self._llm_generate(system, user_prompt)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"professional": raw, "casual": raw, "creative": raw}

        return {"contact_name": contact_name, "follow_up_variants": parsed}

    # ------------------------------------------------------------------
    # MICRO-CIRCLES — triangular ask/offer matches (pure graph, no LLM)
    # ------------------------------------------------------------------
    async def find_micro_circles(self, user_id: str, max_size: int = 3) -> dict:
        circles = self.neo4j.find_triangular_matches(user_id, max_size)
        return {"user_id": user_id, "micro_circles": circles, "count": len(circles)}

    # ------------------------------------------------------------------
    # FULL RECOMMENDATION — match + icebreaker for a specific target
    # ------------------------------------------------------------------
    async def full_recommendation(self, user_id: str, target_id: str) -> dict:
        match = await self.find_match(user_id, target_id)
        icebreaker = await self.generate_icebreaker(user_id, target_id)

        return {
            "target_name": icebreaker.get("target_name", target_id),
            "serendipity_score": match["serendipity"]["score"],
            "warm_path": match["warm_path"],
            "insights": {
                "graph_icebreaker": icebreaker["graph_icebreaker"],
                "exit_strategy": icebreaker["exit_strategy"],
                "reasoning": icebreaker["reasoning"],
            },
            "serendipity_reasons": match["serendipity"]["reasons"],
        }

    # ------------------------------------------------------------------
    # TOP RECOMMENDATIONS — ranked list (pure graph, no LLM)
    # ------------------------------------------------------------------
    async def top_recommendations(self, user_id: str, limit: int = 5) -> list:
        ranked = self.neo4j.get_top_recommendations(user_id, limit)
        return [
            {
                "id": r["id"],
                "name": r["name"],
                "role": r["role"],
                "company": r.get("company"),
                "match_score": r["match_score"],
                "complementarity": r["complementarity"],
                "shared_topics": r["shared_topics"],
                "distance": r["distance"],
            }
            for r in ranked
        ]

    # ------------------------------------------------------------------
    # FULL PIPELINE — the Golden Path demo
    # Voice → RocketRide Whisper → Neo4j context → RocketRide LLM → JSON
    # ------------------------------------------------------------------
    async def full_pipeline(
        self, user_id: str, target_id: str, audio_path: str
    ) -> dict:
        # 1. Transcribe via RocketRide Whisper pipeline
        transcript = await self._transcribe(audio_path)

        # 2. Graph queries (Neo4j)
        match = await self.find_match(user_id, target_id)
        target_ctx = self.neo4j.get_person_context(target_id)
        contact_name = target_ctx.get("name", target_id)

        # 3. Icebreaker via RocketRide LLM pipeline
        icebreaker_data = await self.generate_icebreaker(user_id, target_id)

        # 4. Follow-ups via RocketRide LLM pipeline
        followup_data = await self.generate_followups(user_id, contact_name, transcript)

        # 5. Golden JSON contract
        return {
            "target_name": contact_name,
            "serendipity_score": match["serendipity"]["score"],
            "transcript": transcript,
            "insights": {
                "graph_icebreaker": icebreaker_data["graph_icebreaker"],
                "exit_strategy": icebreaker_data["exit_strategy"],
            },
            "follow_up_variants": followup_data["follow_up_variants"],
            "warm_path": match["warm_path"],
            "serendipity_reasons": match["serendipity"]["reasons"],
        }
