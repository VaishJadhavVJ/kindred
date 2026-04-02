import os
import logging
from dotenv import load_dotenv

load_dotenv()

class Settings:
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "password")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    rocketride_uri: str = os.getenv("ROCKETRIDE_URI", "")

def get_settings():
    return Settings()

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
