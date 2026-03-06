from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ShortestPath"
    DATA_PATH: str = "src/data"
    NODES_DATA_PATH: str = "src/data/nodes.json"
    EDGES_DATA_PATH: str = "src/data/edges.json"
    PLACE_NAME: str = "Hoan Kiem District, Hanoi, Vietnam"

    # Development variables
    APP_ENV: str = "development"
    DEBUG: bool = True

@lru_cache
def get_settings() -> Settings:
    return Settings()