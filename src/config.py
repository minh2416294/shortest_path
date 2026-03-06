from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ShortestPath"
    DATA_PATH: str = "src/data"
    PLACE_NAME: str = "Hoan Kiem District, Hanoi, Vietnam"

    # Development variables
    APP_ENV: str = "development"
    DEBUG: bool = True

    # --- Server Configuration ---
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

@lru_cache
def get_settings() -> Settings:
    return Settings()