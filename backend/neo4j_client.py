"""
Neo4j graph queries for Project Kindred.
All the "graph magic" lives here.
"""

from typing import Optional
from neo4j import GraphDatabase


class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # ------------------------------------------------------------------
    # 1. WARM INTRO PATH — shortest trust-weighted path between two people
    # ------------------------------------------------------------------
    def find_warm_path(self, user_id: str, target_id: str) -> dict:
        """
        Returns structured path from user to target with relationship metadata.
        """
        query = """
        MATCH path = shortestPath(
            (a:Person {id: $user_id})-[:CONNECTED_TO|COLLABORATED_WITH*..5]-(b:Person {id: $target_id})
        )
        RETURN 
            [n IN nodes(path) | {id: n.id, name: n.name, role: n.role}] AS nodes,
            [r IN relationships(path) | {type: type(r), trust: coalesce(r.trust, 1.0), context: coalesce(r.project, r.context)}] AS edges,
            length(path) AS hops
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, target_id=target_id)
            record = result.single()
            if not record:
                return {"nodes": [], "edges": [], "hops": -1, "strength_score": 0.0}
            
            # Calculate strength: product of trust scores along the path
            edges = record["edges"]
            strength = 1.0
            for e in edges:
                strength *= e.get("trust", 1.0)

            return {
                "nodes": record["nodes"],
                "edges": edges,
                "hops": record["hops"],
                "strength_score": round(strength, 2)
            }

    # ------------------------------------------------------------------
    # 2. SERENDIPITY SCORE — hidden/niche overlap between two people
    # ------------------------------------------------------------------
    def compute_serendipity(self, user_id: str, target_id: str) -> dict:
        """
        Finds non-obvious overlap: shared niche interests, same obscure
        past events, complementary asks/offers, or shared communities
        that aren't the top-5 most common.
        """
        query = """
        MATCH (a:Person {id: $user_id}), (b:Person {id: $target_id})

        // Shared interests (weighted by rarity)
        OPTIONAL MATCH (a)-[:INTERESTED_IN]->(i:Topic)<-[:INTERESTED_IN]-(b)
        WITH a, b, collect(DISTINCT {name: i.name, rarity: coalesce(i.rarity, 0.5)}) AS shared_interests

        // Shared past events
        OPTIONAL MATCH (a)-[:ATTENDED]->(e:PastEvent)<-[:ATTENDED]-(b)
        WITH a, b, shared_interests,
             collect(DISTINCT e.name) AS shared_events

        // Complementary ask/offer
        OPTIONAL MATCH (a)-[:ASKS_FOR]->(need)<-[:OFFERS]-(b)
        WITH a, b, shared_interests, shared_events,
             collect(DISTINCT need.name) AS b_can_help_a

        OPTIONAL MATCH (b)-[:ASKS_FOR]->(need2)<-[:OFFERS]-(a)
        WITH a, b, shared_interests, shared_events, b_can_help_a,
             collect(DISTINCT need2.name) AS a_can_help_b

        // Shared universities
        OPTIONAL MATCH (a)-[:WENT_TO]->(u:University)<-[:WENT_TO]-(b)
        WITH a, b, shared_interests, shared_events, b_can_help_a, a_can_help_b,
             collect(DISTINCT u.name) AS shared_universities

        // Shared communities
        OPTIONAL MATCH (a)-[:MEMBER_OF]->(c:Community)<-[:MEMBER_OF]-(b)

        RETURN shared_interests,
               shared_events,
               b_can_help_a,
               a_can_help_b,
               shared_universities,
               collect(DISTINCT c.name) AS shared_communities
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, target_id=target_id)
            record = result.single()
            if not record:
                return {"score": 0, "reasons": []}

            data = dict(record)

            # Calculate serendipity score
            reasons = []
            score = 0

            # Rare shared interests are worth more
            for interest in data.get("shared_interests", []):
                if interest.get("name"):
                    rarity = interest.get("rarity", 0.5)
                    points = int(rarity * 35)  # rarer = higher score
                    score += points
                    reasons.append(f"Both interested in {interest['name']}")

            for event in data.get("shared_events", []):
                if event:
                    score += 15
                    reasons.append(f"Both attended {event}")

            complementarity_found = False
            for item in data.get("b_can_help_a", []):
                if item:
                    score += 30
                    reasons.append(f"They can help you with: {item}")
                    complementarity_found = True

            for item in data.get("a_can_help_b", []):
                if item:
                    score += 30
                    reasons.append(f"You can help them with: {item}")
                    complementarity_found = True

            for uni in data.get("shared_universities", []):
                if uni:
                    score += 15
                    reasons.append(f"Both went to {uni}")

            for comm in data.get("shared_communities", []):
                if comm:
                    score += 12
                    reasons.append(f"Both in {comm} community")

            return {
                "score": min(score, 100), 
                "reasons": reasons, 
                "primary_reason": reasons[0] if reasons else "No obvious overlap found",
                "complementarity_found": complementarity_found
            }

    # ------------------------------------------------------------------
    # 3. TRIANGULAR MATCH — 3-way ask/offer loops
    # ------------------------------------------------------------------
    def find_triangular_matches(self, user_id: str, max_size: int = 3) -> list:
        """
        Finds 3-person cycles where needs are met in a loop: A -> B -> C -> A.
        """
        query = """
        MATCH (a:Person {id: $user_id})-[:ASKS_FOR]->(n1)<-[:OFFERS]-(b:Person)
        WHERE b.id <> a.id
        
        MATCH (b)-[:ASKS_FOR]->(n2)<-[:OFFERS]-(c:Person)
        WHERE c.id <> a.id AND c.id <> b.id
        
        MATCH (c)-[:ASKS_FOR]->(n3)<-[:OFFERS]-(a)
        
        WITH a, b, c, n1, n2, n3
        
        // Loop Strength: base 1.0, + shared communities
        OPTIONAL MATCH (a)-[:MEMBER_OF]->(comm)<-[:MEMBER_OF]-(b)
        OPTIONAL MATCH (b)-[:MEMBER_OF]->(comm2)<-[:MEMBER_OF]-(c)
        OPTIONAL MATCH (c)-[:MEMBER_OF]->(comm3)<-[:MEMBER_OF]-(a)
        
        WITH a, b, c, n1, n2, n3,
             count(DISTINCT comm) + count(DISTINCT comm2) + count(DISTINCT comm3) AS common_comms
             
        RETURN 
            [{id: a.id, name: a.name, role: a.role, contribution: n3.name},
             {id: b.id, name: b.name, role: b.role, contribution: n1.name},
             {id: c.id, name: c.name, role: c.role, contribution: n2.name}] AS members,
            "Value Loop: " + n3.name + " -> " + n1.name + " -> " + n2.name AS why,
            1.0 + (common_comms * 0.1) AS strength,
            "You receive expertise in " + n3.name + " from " + c.name AS direct,
            "You provide " + n3.name + " utility to the group" AS indirect
        ORDER BY strength DESC
        LIMIT 5
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            circles = []
            for record in result:
                circles.append({
                    "members": record["members"],
                    "why_this_circle": record["why"],
                    "loop_strength": round(record["strength"], 2),
                    "direct_value": record["direct"],
                    "indirect_value": record["indirect"]
                })
            return circles

    # ------------------------------------------------------------------
    # 4. PERSON CONTEXT — pull all context about a person for LLM prompts
    # ------------------------------------------------------------------
    def get_person_context(self, person_id: str) -> dict:
        """Get rich context about a person for icebreaker/follow-up generation."""
        query = """
        MATCH (p:Person {id: $person_id})
        OPTIONAL MATCH (p)-[:HAS_SKILL]->(s:Skill)
        OPTIONAL MATCH (p)-[:INTERESTED_IN]->(t:Topic)
        OPTIONAL MATCH (p)-[:WORKS_AT]->(co:Company)
        OPTIONAL MATCH (p)-[:LOOKING_FOR]->(g:Goal)
        OPTIONAL MATCH (p)-[:ASKS_FOR]->(ask)
        OPTIONAL MATCH (p)-[:OFFERS]->(offer)
        OPTIONAL MATCH (p)-[:WENT_TO]->(u:University)
        OPTIONAL MATCH (p)-[:ATTENDED]->(ev:PastEvent)
        RETURN p.id AS id, p.name AS name, p.role AS role, p.bio AS bio,
               collect(DISTINCT s.name) AS skills,
               collect(DISTINCT t.name) AS interests,
               collect(DISTINCT co.name) AS companies,
               collect(DISTINCT g.name) AS goals,
               collect(DISTINCT ask.name) AS asks,
               collect(DISTINCT offer.name) AS offers,
               collect(DISTINCT u.name) AS universities,
               collect(DISTINCT ev.name) AS past_events
        """
        with self.driver.session() as session:
            result = session.run(query, person_id=person_id)
            record = result.single()
            if not record:
                return {}
            return dict(record)

    # ------------------------------------------------------------------
    # 5. TOP RECOMMENDATIONS — personalized PageRank-style ranking
    # ------------------------------------------------------------------
    def get_top_recommendations(self, user_id: str, limit: int = 5) -> list:
        """Rank all other attendees by strategic graph alignment."""
        query = """
        MATCH (me:Person {id: $user_id})
        MATCH (other:Person) WHERE other.id <> me.id

        // Signal 1: Complementarity (Asks/Offers)
        OPTIONAL MATCH (me)-[:ASKS_FOR]->(need)<-[:OFFERS]-(other)
        WITH me, other, collect(DISTINCT need.name) AS needs
        
        // Signal 2: Topics
        OPTIONAL MATCH (me)-[:INTERESTED_IN]->(t:Topic)<-[:INTERESTED_IN]-(other)
        WITH me, other, needs, collect(DISTINCT t.name) AS topics
        
        // Signal 3: Events
        OPTIONAL MATCH (me)-[:ATTENDED]->(e:PastEvent)<-[:ATTENDED]-(other)
        WITH me, other, needs, topics, collect(DISTINCT e.name) AS events
        
        // Signal 4: Universities
        OPTIONAL MATCH (me)-[:WENT_TO]->(u:University)<-[:WENT_TO]-(other)
        WITH me, other, needs, topics, events, collect(DISTINCT u.name) AS unis
        
        // Signal 5: Communities
        OPTIONAL MATCH (me)-[:MEMBER_OF]->(c:Community)<-[:MEMBER_OF]-(other)
        WITH me, other, needs, topics, events, unis, collect(DISTINCT c.name) AS comms
        
        // Signal 6: Path Distance
        OPTIONAL MATCH path = shortestPath((me)-[:CONNECTED_TO*..4]-(other))
        WITH me, other, needs, topics, events, unis, comms,
             CASE WHEN path IS NOT NULL THEN length(path) ELSE 99 END AS dist
        
        // Final Scoring logic
        WITH other,
             (size(needs) * 30 + size(topics) * 15 + size(events) * 10 + 
              size(unis) * 20 + size(comms) * 12 +
              CASE WHEN dist <= 2 THEN 35 WHEN dist <= 3 THEN 15 ELSE 0 END
             ) AS score,
             needs, topics, events, unis, comms, dist
        
        WHERE score > 0
        RETURN other.id AS id, other.name AS name, other.role AS role, 
               other.company AS company, score AS match_score,
               size(needs) AS complementarity, size(topics) AS shared_topics,
               size(events) AS shared_events, size(unis) AS shared_universities,
               size(comms) AS shared_communities, dist AS distance,
               CASE 
                 WHEN size(needs) > 0 THEN "Offers exactly what you need"
                 WHEN dist = 2 THEN "Intro possible via mutual connection"
                 WHEN size(unis) > 0 THEN "Fellow " + unis[0] + " alumni"
                 WHEN size(topics) > 0 THEN "Shared interest in " + topics[0]
                 WHEN size(events) > 0 THEN "Both attended " + events[0]
                 WHEN size(comms) > 0 THEN "Part of " + comms[0]
                 ELSE "Strong serendipity signal"
               END AS short_reason
        ORDER BY match_score DESC
        LIMIT $limit
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, limit=limit)
            return [dict(r) for r in result]
