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
cp .env.example .env
# Edit .env with your credentials (Neo4j, OpenAI)
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

```
# Neo4j AuraDB (free tier) - Required
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# RocketRide Engine (Docker on localhost) - Optional layer
ROCKETRIDE_URI=http://localhost:5565

# OpenAI Fallback - Required if RocketRide is offline
OPENAI_API_KEY=sk-...

# Application Settings
LOG_LEVEL=INFO
```

## Seeding the Database (Demo Graph)
The project comes with a highly realistic 50-person graph (connected via Topics, Events, Roles, and Asks/Offers). To populate your Neo4j database:

```bash
python3 -m seed_data.load
```
*Note: This command will cleanly clear the existing database, create constraints, and generate roughly 50 connected nodes with detailed serendipity mappings.*

## Testing & Reliability
The project includes a full test suite for reliability:

### 1. Unit & API Tests (Mocked)
Fast, stable tests that verify logic and routing without needing external services:
```bash
pytest tests/
```

### 2. Integration Tests (Real Data)
Verifies the end-to-end product flow against your seeded Neo4j instance:
```bash
python3 test_integration.py
```

## The 5-Minute Backend Demo

Kindred is a "Product-First" engine. You can run a full narrative demo that simulates a real event journey (Vaishnavi's arrival at the UIC ML Symposium) without needing a frontend:

1.  **Seed the Graph**:
    ```bash
    python3 -m seed_data.load
    ```
2.  **Run the Narrative Demo**:
    ```bash
    python3 scripts/demo_engine.py
    ```

### What the Demo Exercises:
- **Step 1: Health Check**: Verifies Neo4j connectivity and Intelligence Mode (RocketRide vs. OpenAI Fallback).
- **Step 2: Recommendation**: Ranks the top 5 strategic matches for Vaishnavi based on her "Asks" (e.g., *Find cofounder*).
- **Step 3: Targeted Match**: Finds a **Warm Intro Path** and **Serendipity Score** for Nina Patel.
- **Step 4: Grounded Icebreaker**: Synthesizes a fact-grounded greeting for Nina based on shared interests in *Knowledge Graphs*.
- **Step 5: Micro-Circle Discovery**: Finds a 3-person "Value Loop" between Vaishnavi, Raj, and Alex.
- **Step 6: Smart Follow-ups**: Generates professional and casual follow-up variants for the morning after.

## Reliability & Verification

The engine is protected by 21+ automated tests covering graph logic, prompt grounding, and API contracts:

```bash
pytest tests/
```

## Team Integration

- **Backend / Graph**: Managed via `app/neo4j_client.py` and `seed_data/load.py`.
- **Intelligence Layer**: Orchestrated by `app/intelligence.py` using RocketRide or OpenAI.
- **Frontend (Next.js)**: Consumes the REST API defined in `app/main.py` using the schemas in `app/schemas.py`.
