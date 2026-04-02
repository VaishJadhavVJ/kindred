"""
Seed Data Loader for Project Kindred
=====================================
Creates ~50 Person nodes + supporting nodes (Topics, Skills, Events, etc.)
with rich relationships that make the demo look incredible.

Run with: python -m seed_data.load

The demo Golden Path:
  - "you" (user) → Sam → Nina (warm path)
  - Nina has serendipity score ~88 via hidden overlap (Vintage Synthesizers)
  - Priya introduced you to Alex (voice capture scenario)
  - Triangular match: you need funding advice, B knows fundraising + needs AI talent, C is AI + needs startup team
"""

import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


def clear_database(session):
    session.run("MATCH (n) DETACH DELETE n")
    print("  Cleared existing data.")


def create_constraints(session):
    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (e:PastEvent) REQUIRE e.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (u:University) REQUIRE u.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Community) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (co:Company) REQUIRE co.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (g:Goal) REQUIRE g.name IS UNIQUE",
    ]
    for c in constraints:
        session.run(c)
    print("  Constraints created.")


def seed_nodes(session):
    """Create all supporting nodes (topics, skills, events, etc.)."""

    # Topics (with rarity scores — higher = more niche = more serendipity points)
    topics = [
        ("Machine Learning", 0.2), ("AI Agents", 0.3), ("Knowledge Graphs", 0.5),
        ("Rust Programming", 0.6), ("Healthcare AI", 0.5), ("Vector Search", 0.5),
        ("Compliance Workflows", 0.7), ("Vintage Synthesizers", 0.95),
        ("Retro Computing", 0.85), ("AI Safety", 0.4), ("RL for Robotics", 0.6),
        ("Options Trading", 0.5), ("Open Source Security", 0.6),
        ("Enterprise RAG", 0.5), ("Biomedical Search", 0.6),
        ("Supply Chain AI", 0.5), ("EdTech", 0.4), ("FinTech", 0.5),
        ("Crypto Infrastructure", 0.6), ("Climate Tech", 0.5),
        ("Prompt Engineering", 0.3), ("MLOps", 0.4), ("Data Privacy", 0.4),
        ("Collaborative Worldbuilding", 0.9), ("Mechanical Keyboards", 0.8),
    ]
    for name, rarity in topics:
        session.run(
            "MERGE (t:Topic {name: $name}) SET t.rarity = $rarity",
            name=name, rarity=rarity,
        )

    # Skills
    skills = [
        "Python", "Rust", "TypeScript", "Go", "React", "Neo4j", "PyTorch",
        "FastAPI", "Docker", "Kubernetes", "Prompt Engineering", "Data Pipelines",
        "System Design", "Frontend", "Backend", "ML Engineering", "DevOps",
        "Product Management", "UX Research", "Technical Writing",
    ]
    for s in skills:
        session.run("MERGE (:Skill {name: $name})", name=s)

    # Past Events
    events = [
        "GenAI Infra Summit 2025", "ChicagoHacks 2025", "UIC ML Symposium",
        "Neo4j GraphDay Chicago", "AI Safety Meetup March 2026",
        "DemonHacks 2025", "HackWithChicago 2.0", "PyCon US 2025",
        "Startup Grind Chicago", "Google DevFest Chicago",
    ]
    for e in events:
        session.run("MERGE (:PastEvent {name: $name})", name=e)

    # Universities
    for u in ["UIC", "Northwestern", "UChicago", "IIT", "DePaul", "MIT", "Stanford", "Georgia Tech"]:
        session.run("MERGE (:University {name: $name})", name=u)

    # Communities
    for c in ["GDSC UIC", "Chicago AI Builders", "Neo4j Community", "Indie Hackers Chicago",
              "Women in AI Chicago", "YC Startup School", "Rust Chicago"]:
        session.run("MERGE (:Community {name: $name})", name=c)

    # Companies
    for co in ["Google", "Anthropic", "Neo4j", "Stripe", "Citadel", "Akuna Capital",
               "Cohere", "Scale AI", "Hugging Face", "IBM", "Jump Trading",
               "Gelber Group", "Tempus AI", "Relativity", "Grubhub"]:
        session.run("MERGE (:Company {name: $name})", name=co)

    # Goals (for Ask/Offer matching)
    goals = [
        "Find internship", "Find cofounder", "Get funding advice",
        "Learn MLOps", "Hire AI engineers", "Find mentor",
        "Break into healthcare AI", "Recruit for startup",
        "Find open source collaborators", "Learn graph databases",
    ]
    for g in goals:
        session.run("MERGE (:Goal {name: $name})", name=g)

    print("  Supporting nodes created.")


def seed_people(session):
    """Create ~50 Person nodes with rich attributes."""

    people = [
        # === DEMO GOLDEN PATH PEOPLE ===
        {"id": "you", "name": "Vaishnavi", "role": "MS CS Student / Builder",
         "company": "UIC", "bio": "First-year MS CS at UIC. Backend/ML. Building things."},
        {"id": "sam", "name": "Sam Chen", "role": "Senior Engineer",
         "company": "Anthropic", "bio": "Works on AI safety tooling. Connector."},
        {"id": "nina", "name": "Nina Patel", "role": "Healthcare AI Lead",
         "company": "Tempus AI", "bio": "Runs healthcare AI products. Secret synth collector."},
        {"id": "priya", "name": "Priya Sharma", "role": "AI Research Engineer",
         "company": "Cohere", "bio": "NLP and retrieval systems. Hackathon regular."},
        {"id": "alex", "name": "Alex Rivera", "role": "Founding Engineer",
         "company": "Scale AI", "bio": "Building AI data infra. Looking for Rust devs."},

        # === BRIDGE CONNECTORS ===
        {"id": "omar", "name": "Omar Hassan", "role": "Engineering Manager",
         "company": "Citadel", "bio": "Manages quant infra team. Knows everyone in Chicago finance."},
        {"id": "lena", "name": "Lena Kim", "role": "VP Engineering",
         "company": "Relativity", "bio": "Hiring AI/ML engineers. eDiscovery + AI."},
        {"id": "raj", "name": "Raj Mehta", "role": "Founder",
         "company": "Indie Hackers Chicago", "bio": "Serial founder. Mentors students."},
        {"id": "maya", "name": "Maya Johnson", "role": "Product Manager",
         "company": "Stripe", "bio": "FinTech PM. Speaker at multiple conferences."},
        {"id": "jordan", "name": "Jordan Lee", "role": "ML Engineer",
         "company": "Jump Trading", "bio": "ML for trading systems. AI safety side projects."},

        # === FOUNDERS / INVESTORS ===
        {"id": "rhea", "name": "Rhea Gupta", "role": "Founder & CEO",
         "company": "FinLit AI", "bio": "Building financial literacy platform. Raised pre-seed."},
        {"id": "derek", "name": "Derek Wu", "role": "Partner",
         "company": "Hyde Park Ventures", "bio": "Invests in Midwest B2B SaaS + AI."},
        {"id": "tanya", "name": "Tanya Brooks", "role": "Founder",
         "company": "GraphHealth", "bio": "Knowledge graphs for clinical trials."},
        {"id": "carlos", "name": "Carlos Mendez", "role": "CTO",
         "company": "DataVault", "bio": "Data privacy startup. Ex-Google."},

        # === STUDENTS / EARLY CAREER ===
        {"id": "madhu", "name": "Madhumitha Seshaiah", "role": "MS CS Student",
         "company": "UIC", "bio": "ML research. Working on PRM verification."},
        {"id": "kevin", "name": "Kevin Park", "role": "CS Senior",
         "company": "Northwestern", "bio": "Full-stack dev. Looking for startup roles."},
        {"id": "aisha", "name": "Aisha Williams", "role": "PhD Student",
         "company": "UChicago", "bio": "Computational biology + ML. TA for intro CS."},
        {"id": "tom", "name": "Tom Zhang", "role": "MS DS Student",
         "company": "IIT", "bio": "Data science. Kaggle competitor."},
        {"id": "sarah", "name": "Sarah Chen", "role": "CS Junior",
         "company": "DePaul", "bio": "Frontend dev. React and design systems."},

        # === INDUSTRY ENGINEERS ===
        {"id": "mike", "name": "Mike O'Brien", "role": "Staff Engineer",
         "company": "Google", "bio": "Search infrastructure. 10 years at Google."},
        {"id": "elena", "name": "Elena Volkov", "role": "Senior ML Engineer",
         "company": "Hugging Face", "bio": "Open source ML models. Conference speaker."},
        {"id": "david", "name": "David Kim", "role": "Backend Engineer",
         "company": "Grubhub", "bio": "Distributed systems. Looking to move into AI."},
        {"id": "lisa", "name": "Lisa Tanaka", "role": "DevOps Lead",
         "company": "Neo4j", "bio": "Graph database internals. Community organizer."},
        {"id": "ben", "name": "Ben Foster", "role": "Security Engineer",
         "company": "Cloudflare", "bio": "Web security. Open source contributor."},

        # === RECRUITERS / HIRING ===
        {"id": "rachel", "name": "Rachel Adams", "role": "Technical Recruiter",
         "company": "Anthropic", "bio": "Hiring for AI safety and infrastructure."},
        {"id": "james", "name": "James Wright", "role": "Talent Lead",
         "company": "Scale AI", "bio": "Building the AI ops team."},
        {"id": "nadia", "name": "Nadia Hassan", "role": "University Recruiting",
         "company": "Citadel", "bio": "Campus recruiting for quant roles."},

        # === MENTORS / SPEAKERS ===
        {"id": "prof_liu", "name": "Prof. Wei Liu", "role": "Associate Professor",
         "company": "UIC", "bio": "Teaches ML and AI ethics. PhD advisor."},
        {"id": "arjun", "name": "Arjun Reddy", "role": "Distinguished Engineer",
         "company": "IBM", "bio": "AI systems architecture. 20 year veteran."},
        {"id": "kate", "name": "Kate Morrison", "role": "Director of Engineering",
         "company": "Tempus AI", "bio": "Engineering leadership. Healthcare AI."},

        # === MORE DIVERSE PROFILES ===
        {"id": "zara", "name": "Zara Ahmed", "role": "UX Researcher",
         "company": "Stripe", "bio": "Human-centered AI design."},
        {"id": "leo", "name": "Leo Garcia", "role": "Data Engineer",
         "company": "Akuna Capital", "bio": "Real-time data pipelines for trading."},
        {"id": "mia", "name": "Mia Thompson", "role": "Technical Writer",
         "company": "Anthropic", "bio": "AI documentation. Ex-journalist."},
        {"id": "chris", "name": "Chris Nakamura", "role": "iOS Engineer",
         "company": "Duolingo", "bio": "Mobile ML. Gamification expert."},
        {"id": "diana", "name": "Diana Reyes", "role": "Climate Data Scientist",
         "company": "Argonne Lab", "bio": "Climate modeling with ML. Open datasets."},
        {"id": "frank", "name": "Frank Osei", "role": "Blockchain Engineer",
         "company": "Coinbase", "bio": "Crypto infrastructure. DeFi protocols."},
        {"id": "grace", "name": "Grace Park", "role": "Product Designer",
         "company": "Figma", "bio": "Design systems. Accessibility advocate."},
        {"id": "henry", "name": "Henry Liu", "role": "Quant Researcher",
         "company": "Jump Trading", "bio": "Statistical arbitrage. PhD in physics."},
        {"id": "iris", "name": "Iris Mendoza", "role": "Community Manager",
         "company": "Neo4j", "bio": "Developer relations. Event organizer."},
        {"id": "jake", "name": "Jake Robinson", "role": "Startup Advisor",
         "company": "Techstars Chicago", "bio": "Advises early-stage startups. Angel investor."},
        {"id": "luna", "name": "Luna Nguyen", "role": "NLP Researcher",
         "company": "Toyota Research", "bio": "Conversational AI for autonomous vehicles."},
        {"id": "nick", "name": "Nick Petrova", "role": "Platform Engineer",
         "company": "Shopify", "bio": "Ecommerce infrastructure. Ruby to Rust migration."},
        {"id": "olivia", "name": "Olivia Chen", "role": "AI Ethics Researcher",
         "company": "UChicago", "bio": "AI fairness and accountability."},
        {"id": "pablo", "name": "Pablo Santos", "role": "Robotics Engineer",
         "company": "Boston Dynamics", "bio": "RL for robot locomotion."},
        {"id": "quinn", "name": "Quinn Taylor", "role": "Growth Lead",
         "company": "Notion", "bio": "PLG strategy. Community-driven growth."},
        {"id": "rita", "name": "Rita Patel", "role": "Healthcare Data Analyst",
         "company": "Tempus AI", "bio": "Clinical data pipelines. Bioinformatics."},
        {"id": "steve", "name": "Steve Kim", "role": "Venture Scout",
         "company": "a16z", "bio": "Scouting AI startups in Midwest."},
        {"id": "uma", "name": "Uma Krishnan", "role": "Research Scientist",
         "company": "Google DeepMind", "bio": "Reinforcement learning. Published 20+ papers."},
        {"id": "victor", "name": "Victor Huang", "role": "SRE Lead",
         "company": "Cloudflare", "bio": "Infrastructure reliability. Open source."},
        {"id": "wendy", "name": "Wendy Zhao", "role": "Startup Founder",
         "company": "MeetGraph", "bio": "Building networking tools. Graph enthusiast."},
    ]

    for p in people:
        session.run(
            """
            MERGE (person:Person {id: $id})
            SET person.name = $name,
                person.role = $role,
                person.company = $company,
                person.bio = $bio
            """,
            **p,
        )

    print(f"  Created {len(people)} people.")


def seed_relationships(session):
    """Create all the rich relationships that make the demo shine."""

    # ---- INTEREST relationships ----
    interests = {
        "you": ["Machine Learning", "AI Agents", "Options Trading", "Collaborative Worldbuilding",
                "Vintage Synthesizers", "Prompt Engineering", "Knowledge Graphs"],
        "sam": ["AI Safety", "AI Agents", "Open Source Security", "Vintage Synthesizers"],
        "nina": ["Healthcare AI", "Knowledge Graphs", "Vintage Synthesizers", "Biomedical Search",
                 "Mechanical Keyboards"],
        "priya": ["Machine Learning", "Enterprise RAG", "AI Agents", "Prompt Engineering"],
        "alex": ["Rust Programming", "AI Agents", "MLOps", "Open Source Security"],
        "omar": ["FinTech", "Machine Learning", "Options Trading"],
        "lena": ["Machine Learning", "Data Privacy", "AI Safety"],
        "raj": ["EdTech", "FinTech", "AI Agents"],
        "maya": ["FinTech", "Compliance Workflows", "Vector Search"],
        "jordan": ["AI Safety", "Machine Learning", "RL for Robotics"],
        "rhea": ["FinTech", "EdTech", "Options Trading"],
        "derek": ["FinTech", "Supply Chain AI", "Climate Tech"],
        "tanya": ["Healthcare AI", "Knowledge Graphs", "Biomedical Search"],
        "carlos": ["Data Privacy", "Crypto Infrastructure", "AI Safety"],
        "madhu": ["Machine Learning", "AI Safety", "Prompt Engineering"],
        "elena": ["Machine Learning", "MLOps", "AI Agents"],
        "lisa": ["Knowledge Graphs", "AI Agents", "Retro Computing"],
        "uma": ["RL for Robotics", "AI Safety", "Machine Learning"],
        "wendy": ["Knowledge Graphs", "AI Agents", "EdTech"],
    }
    for person_id, topics in interests.items():
        for t in topics:
            session.run(
                "MATCH (p:Person {id: $pid}), (t:Topic {name: $topic}) MERGE (p)-[:INTERESTED_IN]->(t)",
                pid=person_id, topic=t,
            )

    # ---- SKILL relationships ----
    skills = {
        "you": ["Python", "PyTorch", "FastAPI", "React", "Docker"],
        "sam": ["Python", "Rust", "System Design"],
        "nina": ["Python", "PyTorch", "Product Management"],
        "priya": ["Python", "PyTorch", "ML Engineering"],
        "alex": ["Rust", "Go", "System Design", "DevOps"],
        "omar": ["Python", "System Design", "Backend"],
        "lena": ["System Design", "ML Engineering", "Backend"],
        "madhu": ["Python", "PyTorch", "ML Engineering"],
        "elena": ["Python", "PyTorch", "ML Engineering", "Technical Writing"],
        "lisa": ["Neo4j", "Docker", "Kubernetes", "DevOps"],
        "kevin": ["TypeScript", "React", "Frontend"],
        "sarah": ["React", "Frontend", "TypeScript"],
    }
    for person_id, sk_list in skills.items():
        for s in sk_list:
            session.run(
                "MATCH (p:Person {id: $pid}), (s:Skill {name: $skill}) MERGE (p)-[:HAS_SKILL]->(s)",
                pid=person_id, skill=s,
            )

    # ---- UNIVERSITY relationships ----
    universities = {
        "you": "UIC", "madhu": "UIC", "prof_liu": "UIC",
        "kevin": "Northwestern", "aisha": "UChicago", "olivia": "UChicago",
        "tom": "IIT", "sarah": "DePaul",
        "sam": "MIT", "uma": "Stanford", "henry": "MIT",
    }
    for pid, uni in universities.items():
        session.run(
            "MATCH (p:Person {id: $pid}), (u:University {name: $uni}) MERGE (p)-[:WENT_TO]->(u)",
            pid=pid, uni=uni,
        )

    # ---- WORKS_AT relationships ----
    companies = {
        "sam": "Anthropic", "rachel": "Anthropic", "mia": "Anthropic",
        "nina": "Tempus AI", "kate": "Tempus AI", "rita": "Tempus AI",
        "priya": "Cohere", "alex": "Scale AI", "james": "Scale AI",
        "omar": "Citadel", "nadia": "Citadel",
        "lena": "Relativity", "maya": "Stripe", "zara": "Stripe",
        "jordan": "Jump Trading", "henry": "Jump Trading",
        "mike": "Google", "uma": "Google",
        "elena": "Hugging Face", "david": "Grubhub",
        "lisa": "Neo4j", "iris": "Neo4j",
        "ben": "Cloudflare", "victor": "Cloudflare",
        "arjun": "IBM", "leo": "Akuna Capital",
        "derek": "Hyde Park Ventures",
    }
    for pid, co in companies.items():
        session.run(
            "MATCH (p:Person {id: $pid}), (c:Company {name: $co}) MERGE (p)-[:WORKS_AT]->(c)",
            pid=pid, co=co,
        )

    # ---- PAST EVENT attendance ----
    events = {
        "you": ["DemonHacks 2025", "HackWithChicago 2.0", "GenAI Infra Summit 2025", "UIC ML Symposium"],
        "sam": ["GenAI Infra Summit 2025", "AI Safety Meetup March 2026"],
        "nina": ["GenAI Infra Summit 2025", "Neo4j GraphDay Chicago"],
        "priya": ["HackWithChicago 2.0", "ChicagoHacks 2025", "GenAI Infra Summit 2025"],
        "alex": ["ChicagoHacks 2025", "PyCon US 2025"],
        "omar": ["Startup Grind Chicago"],
        "lisa": ["Neo4j GraphDay Chicago", "Google DevFest Chicago"],
        "madhu": ["DemonHacks 2025", "UIC ML Symposium"],
        "elena": ["PyCon US 2025", "GenAI Infra Summit 2025"],
        "jordan": ["AI Safety Meetup March 2026", "GenAI Infra Summit 2025"],
    }
    for pid, ev_list in events.items():
        for ev in ev_list:
            session.run(
                "MATCH (p:Person {id: $pid}), (e:PastEvent {name: $event}) MERGE (p)-[:ATTENDED]->(e)",
                pid=pid, event=ev,
            )

    # ---- CONNECTED_TO (social graph with trust weights) ----
    connections = [
        # The golden path: you → sam → nina
        ("you", "sam", 0.8),
        ("sam", "nina", 0.9),
        ("sam", "alex", 0.7),
        # You know Priya
        ("you", "priya", 0.85),
        ("priya", "alex", 0.75),
        # Bridge connections
        ("you", "madhu", 0.95),
        ("sam", "rachel", 0.8),
        ("sam", "jordan", 0.7),
        ("omar", "jordan", 0.8),
        ("omar", "henry", 0.85),
        ("omar", "nadia", 0.9),
        ("omar", "lena", 0.6),
        ("lena", "kate", 0.7),
        ("nina", "kate", 0.9),
        ("nina", "tanya", 0.8),
        ("nina", "rita", 0.7),
        ("raj", "derek", 0.8),
        ("raj", "rhea", 0.85),
        ("raj", "jake", 0.9),
        ("derek", "steve", 0.7),
        ("maya", "zara", 0.8),
        ("lisa", "iris", 0.9),
        ("elena", "uma", 0.7),
        ("mike", "uma", 0.75),
        ("ben", "victor", 0.85),
        ("alex", "ben", 0.7),
        ("priya", "elena", 0.6),
        ("kevin", "sarah", 0.7),
        ("you", "raj", 0.5),
        ("you", "lisa", 0.4),
        ("wendy", "lisa", 0.8),
        ("wendy", "iris", 0.7),
    ]
    for src, tgt, trust in connections:
        session.run(
            """
            MATCH (a:Person {id: $src}), (b:Person {id: $tgt})
            MERGE (a)-[r:CONNECTED_TO]-(b)
            SET r.trust = $trust
            """,
            src=src, tgt=tgt, trust=trust,
        )

    # ---- COLLABORATED_WITH (stronger than CONNECTED_TO) ----
    collabs = [
        ("sam", "alex", "open-source security project 2024"),
        ("priya", "you", "HackWithChicago 2.0 team"),
        ("madhu", "you", "CS 517 course project"),
        ("nina", "tanya", "healthcare knowledge graph research"),
        ("jordan", "sam", "AI safety paper review"),
    ]
    for src, tgt, project in collabs:
        session.run(
            """
            MATCH (a:Person {id: $src}), (b:Person {id: $tgt})
            MERGE (a)-[r:COLLABORATED_WITH]-(b)
            SET r.project = $project, r.trust = 0.95
            """,
            src=src, tgt=tgt, project=project,
        )

    # ---- COMMUNITY membership ----
    communities = {
        "you": ["GDSC UIC", "Chicago AI Builders", "YC Startup School"],
        "sam": ["Chicago AI Builders"],
        "alex": ["YC Startup School", "Chicago AI Builders"],
        "priya": ["Chicago AI Builders", "Women in AI Chicago"],
        "lisa": ["Neo4j Community", "Chicago AI Builders"],
        "raj": ["Indie Hackers Chicago", "YC Startup School"],
        "madhu": ["GDSC UIC"],
        "nina": ["Women in AI Chicago"],
        "wendy": ["Neo4j Community", "Indie Hackers Chicago"],
    }
    for pid, comms in communities.items():
        for c in comms:
            session.run(
                "MATCH (p:Person {id: $pid}), (c:Community {name: $comm}) MERGE (p)-[:MEMBER_OF]->(c)",
                pid=pid, comm=c,
            )

    # ---- ASK / OFFER (for triangular matching) ----
    asks = {
        "you": ["Find internship", "Get funding advice", "Find cofounder"],
        "rhea": ["Hire AI engineers", "Get funding advice"],
        "raj": ["Find open source collaborators"],
        "alex": ["Learn MLOps"],
        "kevin": ["Find internship"],
        "david": ["Learn MLOps"],
        "tom": ["Find internship", "Find mentor"],
        "tanya": ["Hire AI engineers", "Get funding advice"],
        "lena": ["Hire AI engineers"],
    }
    for pid, ask_list in asks.items():
        for a in ask_list:
            session.run(
                "MATCH (p:Person {id: $pid}) MERGE (g:Goal {name: $goal}) MERGE (p)-[:ASKS_FOR]->(g)",
                pid=pid, goal=a,
            )

    offers = {
        "you": ["Learn graph databases", "Learn MLOps"],  # you can teach these
        "sam": ["Find internship", "Find mentor"],  # sam can help with internships
        "omar": ["Get funding advice", "Find internship"],
        "derek": ["Get funding advice"],
        "raj": ["Find cofounder", "Find mentor", "Get funding advice"],
        "elena": ["Learn MLOps"],
        "lisa": ["Learn graph databases"],
        "rachel": ["Find internship", "Hire AI engineers"],
        "arjun": ["Find mentor"],
        "jake": ["Get funding advice", "Find cofounder"],
        "lena": ["Find internship"],
        "alex": ["Find open source collaborators"],
    }
    for pid, offer_list in offers.items():
        for o in offer_list:
            session.run(
                "MATCH (p:Person {id: $pid}) MERGE (g:Goal {name: $goal}) MERGE (p)-[:OFFERS]->(g)",
                pid=pid, goal=o,
            )

    print("  All relationships created.")


def main():
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    print(f"Connecting to Neo4j at {uri}...")
    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        print("Step 1: Clearing database...")
        clear_database(session)

        print("Step 2: Creating constraints...")
        create_constraints(session)

        print("Step 3: Creating supporting nodes...")
        seed_nodes(session)

        print("Step 4: Creating people...")
        seed_people(session)

        print("Step 5: Creating relationships...")
        seed_relationships(session)

    driver.close()
    print("\nDone! 50-node demo graph is ready.")
    print("Golden Path test: GET /api/recommend/you?target_id=nina")


if __name__ == "__main__":
    main()
