import os
from pathlib import Path

from dotenv import load_dotenv

SERVICE_ROOT = Path(__file__).resolve().parents[1]
env_file = next(
    (path for path in (SERVICE_ROOT / ".env", SERVICE_ROOT.parent / ".env") if path.is_file()),
    None,
)
if env_file:
    load_dotenv(env_file, override=False)


class Settings:
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8085"))
    APP_NAME: str = os.getenv("APP_NAME", "llm-spring-ai")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "https://ollama.com")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "gemma4:31b")
    OLLAMA_TEMPERATURE: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
    OLLAMA_API_KEY: str = os.getenv("OLLAMA_API_KEY", "")


settings = Settings()
