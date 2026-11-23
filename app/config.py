from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """App settings. Any of these can be overridden in .env."""

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    anthropic_api_key: str = ""
    llm_model: str = "claude-haiku-5-5"  # Fast and inexpensive.
    llm_effort: str = "low"  # low, medium, high, xhigh or max. Higher costs more.
    llm_max_tokens: int = 16000

    data_dir: Path = BASE_DIR / "data"
    database_url: str = f"sqlite:///{(BASE_DIR / 'data' / 'support.db').as_posix()}"

    chroma_db_path: str = str(BASE_DIR / "chroma_db")
    chroma_collection: str = "support_docs"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 800
    chunk_overlap: int = 100

    retrieval_top_k: int = 5  # Chunks returned to the caller.
    retrieval_candidates: int = 20  # Chunks each search passes to fusion.
    rrf_k: int = 60  # Standard reciprocal rank fusion constant.

    structured_search_limit: int = 3  # Error codes and known issues returned.
    structured_min_matches: int = 2  # Shared words needed to count as a match.

    # API
    max_question_length: int = 2000  # Characters; longer questions are rejected with 422.
    rate_limit_per_minute: int = Field(default=10, ge=1)  # Questions per visitor, per server process.
    rate_limit_per_day: int = Field(default=100, ge=1)
    # Proxies in front of the app that append to X-Forwarded-For: 1 on Cloud Run, 0 when run directly.
    trusted_proxy_hops: int = Field(default=0, ge=0)


settings = Settings()
