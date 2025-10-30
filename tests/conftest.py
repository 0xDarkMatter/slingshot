"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import tempfile
import os


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_worker_script():
    """Sample worker JavaScript code."""
    return '''export default {
  async fetch(request, env, ctx) {
    return new Response('Hello, World!');
  },
};'''


@pytest.fixture
def sample_config():
    """Sample worker configuration."""
    return {
        "worker_name": "test-worker",
        "main": "worker.js",
        "compatibility_date": "2024-01-01",
        "routes": [],
        "kv_namespaces": [],
        "vars": {},
        "triggers": {
            "crons": []
        }
    }


@pytest.fixture
def mock_env_credentials(monkeypatch):
    """Mock Cloudflare credentials in environment."""
    monkeypatch.setenv("CLOUDFLARE_ACCOUNT_ID", "test_account_id")
    monkeypatch.setenv("CLOUDFLARE_API_TOKEN", "test_api_token")


@pytest.fixture
def mock_env_file(temp_dir):
    """Create a mock .env file."""
    env_file = temp_dir / ".env"
    env_file.write_text(
        "CLOUDFLARE_ACCOUNT_ID=test_account_id\n"
        "CLOUDFLARE_API_TOKEN=test_api_token\n"
    )
    return env_file
