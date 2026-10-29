import os
import pytest

@pytest.fixture(autouse=True)
def mock_env_keys(monkeypatch):
    """Ensure dummy API keys are present for all tests so imports and models initialize."""
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_test_gemini_key")
    monkeypatch.setenv("GOOGLE_API_KEY", "dummy_test_google_key")
    monkeypatch.setenv("TAVILY_API_KEY", "dummy_test_tavily_key")

