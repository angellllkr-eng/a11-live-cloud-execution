"""
A11 Platform Configuration
Production-grade config with environment-based overrides.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Platform settings with environment override support."""
    
    # Environment
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"
    
    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/a11"
    )
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    
    # Google Cloud
    GCP_PROJECT: str = os.getenv("GCP_PROJECT", "a11-platform")
    GCP_REGION: str = os.getenv("GCP_REGION", "us-central1")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # BigQuery (Evidence Log)
    BIGQUERY_DATASET: str = os.getenv("BIGQUERY_DATASET", "a11_evidence")
    BIGQUERY_EVIDENCE_TABLE: str = os.getenv("BIGQUERY_EVIDENCE_TABLE", "evidence_log")
    BIGQUERY_GOVERNANCE_TABLE: str = os.getenv("BIGQUERY_GOVERNANCE_TABLE", "governance_events")
    
    # Embedding Service (Gemini)
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "768"))
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # LLM Models (Multi-model routing)
    PRIMARY_MODEL: str = os.getenv("PRIMARY_MODEL", "gemini-3.7")
    FALLBACK_MODEL: str = os.getenv("FALLBACK_MODEL", "grok-6")
    TERTIARY_MODEL: str = os.getenv("TERTIARY_MODEL", "gpt-4-turbo")
    
    # Model Configuration
    MODEL_TEMPERATURE: float = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
    MODEL_MAX_TOKENS: int = int(os.getenv("MODEL_MAX_TOKENS", "2048"))
    MODEL_TIMEOUT: int = int(os.getenv("MODEL_TIMEOUT", "30"))
    
    # Search Configuration
    SEARCH_TOP_K: int = int(os.getenv("SEARCH_TOP_K", "10"))
    BM25_WEIGHT: float = float(os.getenv("BM25_WEIGHT", "0.3"))
    VECTOR_WEIGHT: float = float(os.getenv("VECTOR_WEIGHT", "0.7"))
    
    # Ingestion Pipeline (Halo)
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    MAX_DOCUMENT_SIZE: int = int(os.getenv("MAX_DOCUMENT_SIZE", "10485760"))  # 10MB
    BATCH_EMBEDDING_SIZE: int = int(os.getenv("BATCH_EMBEDDING_SIZE", "100"))
    
    # Cloud Tasks (Async Queue)
    CLOUD_TASKS_QUEUE: str = os.getenv("CLOUD_TASKS_QUEUE", "a11-ingestion-queue")
    CLOUD_TASKS_TTL: int = int(os.getenv("CLOUD_TASKS_TTL", "86400"))  # 24 hours
    
    # Governance Rules
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    ESCALATION_ENABLED: bool = os.getenv("ESCALATION_ENABLED", "true").lower() == "true"
    ESCALATION_SLACK_WEBHOOK: Optional[str] = os.getenv("ESCALATION_SLACK_WEBHOOK")
    
    # Evidence Signing
    SIGNING_KEY_PATH: Optional[str] = os.getenv("SIGNING_KEY_PATH")
    SIGNING_ALGORITHM: str = os.getenv("SIGNING_ALGORITHM", "ed25519")
    
    # Caching
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_QUERIES_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_QUERIES_PER_MINUTE", "60"))
    RATE_LIMIT_INGEST_PER_HOUR: int = int(os.getenv("RATE_LIMIT_INGEST_PER_HOUR", "100"))
    
    # Monitoring + Observability
    ENABLE_PROMETHEUS: bool = os.getenv("ENABLE_PROMETHEUS", "true").lower() == "true"
    ENABLE_CLOUD_TRACE: bool = os.getenv("ENABLE_CLOUD_TRACE", "true").lower() == "true"
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = int(os.getenv("JWT_EXPIRY_HOURS", "24"))
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "https://a11-live-cloud-execution.vercel.app",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_database_url(self) -> str:
        """Return database URL with connection pooling settings."""
        return self.DATABASE_URL
    
    def get_bigquery_table_id(self, table_name: str) -> str:
        """Get full BigQuery table ID."""
        return f"{self.GCP_PROJECT}.{self.BIGQUERY_DATASET}.{table_name}"


# Singleton instance
settings = Settings()

# Export for easy access
__all__ = ["settings", "Settings"]
