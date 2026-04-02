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
        Returns the shortest path from user to target through CONNECTED_TO
        or COLLABORATED_WITH edges, with trust scores.
        """
        query = """
        MATCH path = shortestPath(
            (a:Person {id: $user_id})-[:CONNECTED_TO|COLLABORATED_WITH*..5]-(b:Person {id: $target_id})
        )
        WITH path,
             [n IN nodes(path) | {id: n.id, name: n.name, role: n.role, company: n.company}] AS people,
             [r IN relationships(path) | {type: type(r), trust: coalesce(r.trust, 0.5)}] AS edges
        RETURN people, edges, length(path) AS hops
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, target_id=target_id)
            record = result.single()
            if not record:
                return {"path": [], "edges": [], "hops": -1}
            return {
                "path": record["people"],
                "edges": record["edges"],
                "hops": record["hops"],
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
                    points = int(rarity * 30)  # rarer = higher score
                    score += points
                    reasons.append(f"Both interested in {interest['name']}")

            for event in data.get("shared_events", []):
                if event:
                    score += 15
                    reasons.append(f"Both attended {event}")

            for item in data.get("b_can_help_a", []):
                if item:
                    score += 20
                    reasons.append(f"They can help you with: {item}")

            for item in data.get("a_can_help_b", []):
                if item:
                    score += 20
                    reasons.append(f"You can help them with: {item}")

            for uni in data.get("shared_universities", []):
                if uni:
                    score += 10
                    reasons.append(f"Both went to {uni}")

            for comm in data.get("shared_communities", []):
                if comm:
                    score += 12
                    reasons.append(f"Both in {comm} community")

            return {"score": min(score, 100), "reasons": reasons}

    # ------------------------------------------------------------------
    # 3. TRIANGULAR MATCH — 3-way ask/offer loops
    # ------------------------------------------------------------------
    def find_triangular_matches(self, user_id: str, max_size: int = 3) -> list:
        """
        Finds micro-circles where A needs what B offers, B needs what C offers,
        and C needs what A offers (or similar partial loops).
        """
        query = """
        MATCH (a:Person {id: $user_id})-[:ASKS_FOR]->(need1)
        MATCH (b:Person)-[:OFFERS]->(offer1)
        WHERE offer1.name = need1.name AND b.id <> a.id

        MATCH (b)-[:ASKS_FOR]->(need2)
        MATCH (c:Person)-[:OFFERS]->(offer2)
        WHERE offer2.name = need2.name AND c.id <> a.id AND c.id <> b.id

        // Bonus: check if C also needs something A offers
        OPTIONAL MATCH (c)-[:ASKS_FOR]->(need3)
        OPTIONAL MATCH (a)-[:OFFERS]->(offer3)
        WHERE offer3.name = need3.name

        WITH a, b, c,
             need1.name AS a_needs, offer1.name AS b_gives,
             need2.name AS b_needs, offer2.name AS c_gives,
             CASE WHEN offer3 IS NOT NULL THEN need3.name ELSE null END AS c_needs_from_a,
             CASE WHEN offer3 IS NOT NULL THEN 1.0 ELSE 0.5 END AS loop_strength

        RETURN
            {id: b.id, name: b.name, role: b.role} AS person_b,
            {id: c.id, name: c.name, role: c.role} AS person_c,
            a_needs, b_gives, b_needs, c_gives, c_needs_from_a,
            loop_strength
        ORDER BY loop_strength DESC
        LIMIT 5
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            circles = []
            for record in result:
                circles.append({
                    "person_b": dict(record["person_b"]),
                    "person_c": dict(record["person_c"]),
                    "flow": {
                        "you_need": record["a_needs"],
                        "b_provides": record["b_gives"],
                        "b_needs": record["b_needs"],
                        "c_provides": record["c_gives"],
                        "c_needs_from_you": record["c_needs_from_a"],
                    },
                    "is_full_loop": record["c_needs_from_a"] is not None,
                    "loop_strength": record["loop_strength"],
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
        """
        Rank all other attendees by combined score:
        complementarity + shared context + bridge value.
        """
        query = """
        MATCH (me:Person {id: $user_id})

        // Find all other people
        MATCH (other:Person)
        WHERE other.id <> me.id

        // Complementarity: they offer what I need
        OPTIONAL MATCH (me)-[:ASKS_FOR]->(need)<-[:OFFERS]-(other)
        WITH me, other, count(DISTINCT need) AS complementarity

        // Shared interests
        OPTIONAL MATCH (me)-[:INTERESTED_IN]->(t:Topic)<-[:INTERESTED_IN]-(other)
        WITH me, other, complementarity, count(DISTINCT t) AS shared_topics

        // Shared events
        OPTIONAL MATCH (me)-[:ATTENDED]->(e:PastEvent)<-[:ATTENDED]-(other)
        WITH me, other, complementarity, shared_topics, count(DISTINCT e) AS shared_events

        // Path distance (shorter = easier intro)
        OPTIONAL MATCH path = shortestPath((me)-[:CONNECTED_TO*..4]-(other))
        WITH me, other, complementarity, shared_topics, shared_events,
             CASE WHEN path IS NOT NULL THEN length(path) ELSE 99 END AS distance

        // Composite score
        WITH other,
             (complementarity * 25 + shared_topics * 15 + shared_events * 20 +
              CASE WHEN distance <= 2 THEN 30 WHEN distance <= 3 THEN 15 ELSE 0 END
             ) AS match_score,
             complementarity, shared_topics, shared_events, distance

        WHERE match_score > 0
        RETURN other.id AS id, other.name AS name, other.role AS role,
               other.company AS company, match_score,
               complementarity, shared_topics, shared_events, distance
        ORDER BY match_score DESC
        LIMIT $limit
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, limit=limit)
            return [dict(r) for r in result]
