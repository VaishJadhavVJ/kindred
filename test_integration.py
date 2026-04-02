import os
import asyncio
import sys

from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    print("Testing Seeded Data flows...")

    with TestClient(app) as client:
        # 1. Test /health
        resp = client.get("/health")
        assert resp.status_code == 200
        print("[Health] OK:", resp.json())

        # 2. Test /api/match
        resp = client.post("/api/match", json={"user_id": "you", "target_id": "nina"})
        assert resp.status_code == 200
        print("[Match] OK:", resp.json())

        # 3. Test /api/icebreaker (Uses Fallback LLM internally if available)
        resp = client.post("/api/icebreaker", json={"user_id": "you", "target_id": "nina"})
        assert resp.status_code == 200
        print("[Icebreaker] OK:", resp.json()["graph_icebreaker"])

        # 4. Test /api/recommend without target (top 5)
        resp = client.get("/api/recommend/you")
        assert resp.status_code == 200
        print(f"[Recommend All] OK: Found {len(resp.json()['recommendations'])} recommendations.")

        # 5. Test /api/recommend with target (full recommendation payload)
        resp = client.get("/api/recommend/you?target_id=nina")
        assert resp.status_code == 200
        print("[Recommend Target] OK:", resp.json()["serendipity_score"])

        # 6. Test /api/followup
        resp = client.post("/api/followup", json={"user_id": "you", "target_id": "nina"})
        assert resp.status_code == 200
        print(f"[Follow-up] OK for nina: {resp.json()['follow_up_variants']['professional']}")

        # 7. Test /api/micro-circle
        resp = client.post("/api/micro-circle", json={"user_id": "you", "max_size": 3})
        assert resp.status_code == 200
        circles = resp.json()["micro_circles"]
        print(f"[Micro-Circle] OK: Found {len(circles)} loops.")

        # 8. Test sparse data fallback
        resp = client.get("/api/recommend/ghost_user")
        assert resp.status_code == 200
        print(f"[Fallback Test] OK for ghost_user: {resp.json().get('recommendations', [])}")

if __name__ == "__main__":
    run_tests()
    print("All integration flows succeed against the Neo4j seed!")
