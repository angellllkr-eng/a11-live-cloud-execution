"""Tests for configuration module."""

from config import settings, Settings


def test_settings_loads():
    """Test that settings loads with expected types."""
    assert isinstance(settings, Settings)
    assert isinstance(settings.ENV, str)
    assert isinstance(settings.API_PORT, int)
    assert isinstance(settings.CHUNK_SIZE, int)
    assert isinstance(settings.MODEL_TEMPERATURE, float)


def test_settings_defaults():
    """Test that settings have sensible defaults."""
    assert settings.ENV == "development"
    assert settings.API_PORT == 8000
    assert settings.CHUNK_SIZE == 512
    assert settings.EMBEDDING_DIMENSION == 768
    assert 0 < settings.CONFIDENCE_THRESHOLD < 1.0


def test_get_database_url():
    """Test database URL getter."""
    url = settings.get_database_url()
    assert isinstance(url, str)
    assert "postgresql" in url


def test_get_bigquery_table_id():
    """Test BigQuery table ID generation."""
    table_id = settings.get_bigquery_table_id("test_table")
    assert isinstance(table_id, str)
    assert "a11" in table_id
    assert "test_table" in table_id
