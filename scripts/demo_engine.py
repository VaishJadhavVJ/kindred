import json
import time
import logging
from fastapi.testclient import TestClient
from app.main import app

# Silence noisy library logs for a clean narrative
logging.getLogger("neo4j").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("httpcore").setLevel(logging.ERROR)
logging.getLogger("kindred").setLevel(logging.ERROR)

def print_header(text):
    print("\n" + " ✨ " + "="*56 + " ✨ ")
    print(f"  {text}")
    print(" " + "="*60 + " \n")

def print_step(step, text):
    time.sleep(0.8) # "Thinking" pause for realism
    print(f"\n 🔹 [STEP {step}] {text}")
    time.sleep(0.4)

def main():
    with TestClient(app) as client:
        print_header("KINDRED INTELLIGENCE ENGINE — NARRATIVE DEMO")
        print(" 📖 SCENARIO: Vaishnavi arrives at the UIC ML Symposium.")
        print("    She wants to find meaningful connections for her project.")

        # 1. Health Check
        print_step(1, "Waking up Kindred Intelligence...")
        resp = client.get("/health")
        data = resp.json()
        print(f"    ✓ Status: {data['status'].upper()}")
        print(f"    ✓ Mode:   {data['intelligence_mode']}")

        # 2. Recommendation
        print_step(2, "Vaishnavi asks: 'Who should I talk to for my Knowledge Graph project?'")
        resp = client.get("/api/recommend/you")
        recs = resp.json()["recommendations"]
        print(f"    ⭐ Found {len(recs)} strategic matches.")
        for r in recs[:2]:
            print(f"    ➔ {r['name']} ({r['role']}): {r['short_reason']} [Score: {r['match_score']}]")

        # 3. Targeted Match
        print_step(3, "She sees Nina Patel. Is there a warm path?")
        resp = client.post("/api/match", json={"user_id": "you", "target_id": "nina"})
        match = resp.json()
        print(f"    🤝 Match Score: {match['serendipity']['score']}")
        print(f"    🤝 Connection:  {match['strategic_reason']}")
        print(f"    🤝 Path:        {match['hop_count']} hops via Sam Chen")

        # 4. Icebreaker
        print_step(4, "Generating a grounded opening line for Nina...")
        resp = client.post("/api/icebreaker", json={"user_id": "you", "target_id": "nina"})
        ice = resp.json()
        print(f"    💬 Icebreaker:  \"{ice['graph_icebreaker']}\"")
        if ice['reasoning'] == "LLM fallback triggered.":
            print(f"    ✨ Synthesis:   Fact-Grounded Graph Logic (LLM offline)")
        else:
            print(f"    ✨ Synthesis:   GPT-4 Vision & Reasoning")

        # 5. Micro-Circle
        print_step(5, "Discovery: Are there any high-utility loops?")
        resp = client.post("/api/micro-circle", json={"user_id": "you", "max_size": 3})
        circles = resp.json()["micro_circles"]
        if circles:
            c = circles[0]
            print(f"    🔄 Value Loop Found!")
            print(f"    ➔ {c['why_this_circle']}")
            print(f"    ➔ Benefit: {c['direct_value']}")
        else:
            print("    ∅ No loops found for current constraints.")

        # 6. Follow-up
        print_step(6, "The event ends. Drafting follow-ups...")
        resp = client.post("/api/followup", json={"user_id": "you", "target_id": "nina"})
        fol = resp.json()
        print(f"    ✉️ Professional: {fol['follow_up_variants']['professional'][:70]}...")
        print(f"    ✉️ Casual:       {fol['follow_up_variants']['casual'][:70]}...")

        print_header("DEMO COMPLETE — KINDRED ENGINE READY")

if __name__ == "__main__":
    main()
