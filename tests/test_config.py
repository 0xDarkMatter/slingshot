"""Tests for config module."""

import json
import pytest
from pathlib import Path

from slingshot.config import Config


def test_config_create_default(temp_dir):
    """Test creating a default configuration."""
    config_path = temp_dir / ".slingshot.json"
    config = Config.create_default("my-worker", str(config_path))

    assert config_path.exists()
    assert config.worker_name == "my-worker"
    assert config.main_script == "worker.js"
    assert config.compatibility_date == "2024-01-01"


def test_config_load(temp_dir, sample_config):
    """Test loading configuration from file."""
    config_path = temp_dir / ".slingshot.json"
    with open(config_path, 'w') as f:
        json.dump(sample_config, f)

    config = Config(str(config_path))
    data = config.load()

    assert data["worker_name"] == "test-worker"
    assert data["main"] == "worker.js"


def test_config_save(temp_dir, sample_config):
    """Test saving configuration to file."""
    config_path = temp_dir / ".slingshot.json"
    config = Config(str(config_path))
    config.save(sample_config)

    assert config_path.exists()
    with open(config_path, 'r') as f:
        data = json.load(f)
    assert data["worker_name"] == "test-worker"


def test_config_get_set(temp_dir):
    """Test getting and setting configuration values."""
    config = Config.create_default("test-worker", str(temp_dir / ".slingshot.json"))

    config.set("test_key", "test_value")
    assert config.get("test_key") == "test_value"
    assert config.get("missing_key", "default") == "default"


def test_config_credentials(temp_dir, mock_env_credentials):
    """Test reading credentials from environment."""
    config = Config(str(temp_dir / ".slingshot.json"))

    assert config.account_id == "test_account_id"
    assert config.api_token == "test_api_token"


def test_config_validate_success(temp_dir, mock_env_credentials, sample_worker_script):
    """Test successful configuration validation."""
    config = Config.create_default("test-worker", str(temp_dir / ".slingshot.json"))

    # Create worker script
    worker_path = temp_dir / "worker.js"
    worker_path.write_text(sample_worker_script)

    # Change to temp directory for validation
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    try:
        is_valid, errors = config.validate()
        assert is_valid is True
        assert len(errors) == 0
    finally:
        os.chdir(original_cwd)


def test_config_validate_missing_credentials(temp_dir):
    """Test validation with missing credentials."""
    config = Config.create_default("test-worker", str(temp_dir / ".slingshot.json"))

    is_valid, errors = config.validate()
    assert is_valid is False
    assert any("CLOUDFLARE_ACCOUNT_ID" in error for error in errors)
    assert any("CLOUDFLARE_API_TOKEN" in error for error in errors)


def test_config_validate_missing_script(temp_dir, mock_env_credentials):
    """Test validation with missing worker script."""
    config = Config.create_default("test-worker", str(temp_dir / ".slingshot.json"))

    # Change to temp directory for validation
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    try:
        is_valid, errors = config.validate()
        assert is_valid is False
        assert any("worker.js" in error for error in errors)
    finally:
        os.chdir(original_cwd)
