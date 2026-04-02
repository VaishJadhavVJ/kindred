# Project Kindred — Event Networking Intelligence Engine

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js Frontend (PM)                 │
│         Antigravity + 21st.dev components                │
└──────────────────────┬──────────────────────────────────┘
                       │  REST API calls
                       ▼
┌─────────────────────────────────────────────────────────┐
│               FastAPI Backend (This Code)                │
│                                                          │
│  POST /api/match          → Warm path + serendipity      │
│  POST /api/icebreaker     → Graph-explained icebreaker   │
│  POST /api/followup       → Tri-variant follow-ups       │
│  POST /api/voice-capture  → Voice→text→graph→insights    │
│  POST /api/micro-circle   → Triangular match finder      │
│  GET  /api/recommend/{id} → Full recommendation payload  │
└────────┬──────────────────────────┬─────────────────────┘
         │                          │
         ▼                          ▼
┌─────────────────┐    ┌──────────────────────────┐
│   Neo4j AuraDB  │    │   RocketRide AI Engine    │
│  (Graph Queries) │    │  (Pipeline: voice→LLM→out)│
│   50-node demo   │    │  Fallback: direct OpenAI  │
└─────────────────┘    └──────────────────────────┘
```

## Quick Start

```bash
cd kindred
pip install -r requirements.txt
# Set environment variables (see .env.example)
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

```
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
OPENAI_API_KEY=sk-...              # For Whisper + fallback LLM
ROCKETRIDE_URI=http://localhost:5565  # Optional: if RR engine running
```

## Team Roles

- **Backend Lead**: Neo4j AuraDB setup + seed data (`python -m seed_data.load`)
- **Intelligence Layer (Vaishnavi)**: This FastAPI app + RocketRide pipeline
- **PM/Frontend**: Next.js consuming the API endpoints above

## Demo Script (4:30 PM Golden Path)

1. Open app → select target "Nina"
2. GET `/api/recommend/nina` → shows warm path + serendipity score
3. Click record → POST `/api/voice-capture` with audio
4. App displays: icebreaker for Alex + 3 follow-up variants for Priya
