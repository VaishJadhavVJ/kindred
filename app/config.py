import os
import logging
from pydantic import BaseModel
from functools import lru_cache
from dotenv import load_dotenv

class Settings(BaseModel):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    rocketride_uri: str
    openai_api_key: str | None = None
    log_level: str = "INFO"

@lru_cache()
def get_settings() -> Settings:
    """Load settings from environment variables with safe defaults."""
    load_dotenv()
    return Settings(
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "password"),
        rocketride_uri=os.getenv("ROCKETRIDE_URI", "http://localhost:5565"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )

def setup_logging():
    """Configure standard application logging."""
    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # Reduce noise from chatty dependencies
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("neo4j").setLevel(logging.WARNING)
