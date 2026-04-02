"""
Intelligence Engine — RocketRide AI is the ONLY AI layer.

All LLM calls and audio transcription go through RocketRide pipelines.
Neo4j provides the graph context. RocketRide provides the intelligence.
"""

import json
import logging
import re
from typing import Optional

from app.neo4j_client import Neo4jClient
from app.rocketride_client import RocketRideClient

logger = logging.getLogger(__name__)


class IntelligenceEngine:
    def __init__(self, neo4j: Neo4jClient, rocketride: RocketRideClient, openai=None):
        self.neo4j = neo4j
        self.rr = rocketride
        self.openai = openai

    # ------------------------------------------------------------------
    # Core: send prompts through RocketRide's LLM pipeline
    # ------------------------------------------------------------------
    async def _llm_generate(self, system_prompt: str, user_prompt: str) -> str:
        result = await self.rr.generate_text(system_prompt, user_prompt)
        if result:
            logger.info("[IntelligenceEngine] RocketRide successfully generated text.")
            return result
            
        if self.openai:
            logger.info("[IntelligenceEngine] RocketRide unavailable, using OpenAI fallback for LLM generation.")
            fallback_result = await self.openai.generate_text(system_prompt, user_prompt)
            if fallback_result:
                return fallback_result
                
        logger.error("[IntelligenceEngine] CRITICAL: Both LLM engines unavailable.")
        return '{"error": "Both RocketRide and OpenAI fallback are unavailable."}'

    # ------------------------------------------------------------------
    # Core: transcribe audio through RocketRide's Whisper pipeline
    # ------------------------------------------------------------------
    async def _transcribe(self, audio_path: str) -> str:
        result = await self.rr.transcribe_audio(audio_path)
        if result:
            logger.info("[IntelligenceEngine] RocketRide successfully transcribed audio.")
            return result
            
        if self.openai:
            logger.info("[IntelligenceEngine] RocketRide unavailable, using OpenAI fallback for transcription.")
            fallback_result = await self.openai.transcribe_audio(audio_path)
            if fallback_result:
                return fallback_result
                
        logger.warning("[IntelligenceEngine] Transcription unavailable, returning placeholder.")
        return "[Transcription unavailable — both engines not running]"

    # --- HELPER: SAFE JSON PARSING ---

    def _safe_parse_json(self, text: str, fallback: dict) -> dict:
        """Sanitize and parse JSON from LLM output."""
        if not text or "error" in text:
            return fallback
        try:
            # Try to find JSON block if LLM wrapped it in markdown
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                text = match.group(0)
            data = json.loads(text)
            if "error" in data:
                return fallback
            return data
        except Exception:
            logger.warning("LLM returned invalid JSON, using fact-based fallback.")
            return fallback

    # ------------------------------------------------------------------
    # MATCH — warm path + serendipity score
    # ------------------------------------------------------------------
    async def find_match(self, user_id: str, target_id: str) -> dict:
        warm_path = self.neo4j.find_warm_path(user_id, target_id)
        serendipity = self.neo4j.compute_serendipity(user_id, target_id)
        
        # Calculate strategic reason
        hops = warm_path.get("hops", -1)
        path_nodes = warm_path.get("nodes", [])
        
        # Priority 1: Complementarity (Direct utility)
        if serendipity.get("complementarity_found"):
            reason = f"Direct Synergy: They have expertise you're looking for ({serendipity['primary_reason']})."
        # Priority 2: Strong Warm Path (Social proof)
        elif 0 < hops < 99 and len(path_nodes) > 1:
            intro_person = path_nodes[1]["name"]
            strength = warm_path.get("strength_score", 0.0)
            strength_desc = "high-trust" if strength > 0.7 else "social"
            reason = f"Warm intro possible via {strength_desc} connection {intro_person} ({hops} hops)."
        # Priority 3: Niche Serendipity
        else:
            reason = serendipity.get("primary_reason", "High potential for serendipity based on shared interests.")

        return {
            "user_id": user_id,
            "target_id": target_id,
            "warm_path": warm_path,
            "serendipity": serendipity,
            "strategic_reason": reason,
            "hop_count": hops if hops != 99 else -1,
        }

    # ------------------------------------------------------------------
    # ICEBREAKER — fact-grounded language generation
    # ------------------------------------------------------------------
    async def generate_icebreaker(self, user_id: str, target_id: str) -> dict:
        """Construct a grounded prompt using both user and target graph facts."""
        user_ctx = self.neo4j.get_person_context(user_id)
        target_ctx = self.neo4j.get_person_context(target_id)
        match = await self.find_match(user_id, target_id)
        
        serendipity = match["serendipity"]
        warm_path = match["warm_path"]
        
        # Build strict fact context
        context = {
            "user": {"name": user_ctx.get("name"), "interests": user_ctx.get("interests"), "asks": user_ctx.get("asks")},
            "target": {"name": target_ctx.get("name"), "interests": target_ctx.get("interests"), "offers": target_ctx.get("offers")},
            "shared": {
                "topics": serendipity["reasons"],
                "warm_path": f"{warm_path['hops']} hops via {warm_path['nodes'][1]['name']}" if warm_path["hops"] > 0 and len(warm_path["nodes"]) > 1 else "None",
                "complementarity": match["strategic_reason"]
            }
        }

        system_prompt = (
            "You are a strategic networking concierge for an event. "
            "Write exactly ONE SENTENCE for each field. Be natural, peer-to-peer, and zero-fluff. "
            "STRICT RULE: Use the provided graph facts for personalization. "
            "JSON Format: {'icebreaker': '...', 'exit_strategy': '...', 'reasoning': '...'}"
        )
        user_prompt = f"Fact Context: {json.dumps(context)}. Write the icebreaker."

        raw_res = await self._llm_generate(system_prompt, user_prompt)
        
        # Fallback values
        best_reason = serendipity["reasons"][0] if serendipity["reasons"] else "shared interests"
        fact_fallback = {
            "icebreaker": f"Hey {target_ctx.get('name', 'there')}, I saw that {best_reason}!",
            "exit_strategy": "Great meeting you! I'm going to grab a refill, but let's connect on LinkedIn.",
            "reasoning": "LLM fallback triggered."
        }
        
        parsed = self._safe_parse_json(raw_res, fact_fallback)
        
        return {
            "target_name": target_ctx.get("name", "Unknown"),
            "graph_icebreaker": parsed.get("icebreaker", fact_fallback["icebreaker"]),
            "exit_strategy": parsed.get("exit_strategy", fact_fallback["exit_strategy"]),
            "reasoning": parsed.get("reasoning", "Grounded graph synthesis"),
            "serendipity": serendipity
        }

    # ------------------------------------------------------------------
    # FOLLOW-UP — grounded in shared context
    # ------------------------------------------------------------------
    async def generate_followup(self, user_id: str, target_id: str) -> dict:
        """Grounded follow-up suggestions."""
        target_ctx = self.neo4j.get_person_context(target_id)
        match = await self.find_match(user_id, target_id)
        
        system_prompt = (
            "Write three short follow-up message variants (professional, casual, creative). "
            "Use the provided context to suggest a specific next step (e.g. sharing a community or repo). "
            "JSON Format: {'professional': '...', 'casual': '...', 'creative': '...'}"
        )
        user_prompt = f"Target: {target_ctx.get('name')}. Context: {match['strategic_reason']}. Reasons: {match['serendipity']['reasons']}"

        raw_res = await self._llm_generate(system_prompt, user_prompt)
        
        default_followup = {
            "professional": f"Hi {target_ctx.get('name')}, great meeting you! Let's follow up on our shared interest in {match['serendipity']['reasons'][0] if match['serendipity']['reasons'] else 'networking'}.",
            "casual": "Hey! Loved our chat. Let's grab coffee soon.",
            "creative": "Hey—still thinking about our brainstorm. Let's keep the loop open!"
        }
        
        parsed = self._safe_parse_json(raw_res, default_followup)
        
        return {
            "contact_name": target_ctx.get("name", "Unknown"),
            "follow_up_variants": parsed
        }

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
            "strategic_reason": match["strategic_reason"],
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
                "shared_communities": r["shared_communities"],
                "shared_universities": r["shared_universities"],
                "shared_events": r["shared_events"],
                "distance": r["distance"],
                "short_reason": r["short_reason"],
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
        """The Golden Path: Transcribe -> Match -> Icebreaker -> Follow-up."""
        logger.info(f"[IntelligenceEngine] Starting full pipeline for User:{user_id} and Target:{target_id}")
        
        # 1. Transcribe (Resilient)
        transcript = await self._transcribe(audio_path)

        # 2. Graph queries
        match = await self.find_match(user_id, target_id)
        target_ctx = self.neo4j.get_person_context(target_id)
        contact_name = target_ctx.get("name", target_id)

        # 3. Icebreaker (Grounded)
        icebreaker_data = await self.generate_icebreaker(user_id, target_id)

        # 4. Follow-ups (Grounded)
        followup_data = await self.generate_followup(user_id, target_id)

        logger.info("[IntelligenceEngine] Full pipeline completed successfully.")
        
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
