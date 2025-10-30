"""Tests for worker deployer."""

import pytest
from pathlib import Path
from cfworker.deployer import WorkerDeployer, DeploymentError
from cfworker.config import Config


def test_deployer_initialization(temp_dir, mock_env_credentials, sample_worker_script):
    """Test deployer initialization."""
    config = Config.create_default("test-worker", str(temp_dir / ".cfworker.json"))

    # Create worker script
    worker_path = temp_dir / "worker.js"
    worker_path.write_text(sample_worker_script)

    # Change to temp directory
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    try:
        deployer = WorkerDeployer(config)
        assert deployer.config == config
        assert deployer.client.account_id == "test_account_id"
    finally:
        os.chdir(original_cwd)


def test_deployer_invalid_config(temp_dir):
    """Test deployer with invalid configuration."""
    config = Config.create_default("test-worker", str(temp_dir / ".cfworker.json"))

    with pytest.raises(DeploymentError) as exc_info:
        WorkerDeployer(config)

    assert "Invalid configuration" in str(exc_info.value)


def test_read_script(temp_dir, mock_env_credentials, sample_worker_script):
    """Test reading worker script."""
    config = Config.create_default("test-worker", str(temp_dir / ".cfworker.json"))
    worker_path = temp_dir / "worker.js"
    worker_path.write_text(sample_worker_script)

    import os
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    try:
        deployer = WorkerDeployer(config)
        script = deployer.read_script()
        assert script == sample_worker_script
    finally:
        os.chdir(original_cwd)


def test_read_script_not_found(temp_dir, mock_env_credentials, sample_worker_script):
    """Test reading non-existent script."""
    config = Config.create_default("test-worker", str(temp_dir / ".cfworker.json"))
    worker_path = temp_dir / "worker.js"
    worker_path.write_text(sample_worker_script)

    import os
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    try:
        deployer = WorkerDeployer(config)
        with pytest.raises(DeploymentError) as exc_info:
            deployer.read_script("nonexistent.js")
        assert "not found" in str(exc_info.value)
    finally:
        os.chdir(original_cwd)


def test_prepare_metadata(temp_dir, mock_env_credentials, sample_worker_script):
    """Test preparing worker metadata."""
    config = Config.create_default("test-worker", str(temp_dir / ".cfworker.json"))
    worker_path = temp_dir / "worker.js"
    worker_path.write_text(sample_worker_script)

    # Add some vars to config
    config.set("vars", {"API_KEY": "secret", "ENV": "test"})

    import os
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    try:
        deployer = WorkerDeployer(config)
        metadata = deployer.prepare_metadata()

        assert metadata["main_module"] == "worker.js"
        assert metadata["compatibility_date"] == "2024-01-01"
        assert "bindings" in metadata
        assert len(metadata["bindings"]) == 2
    finally:
        os.chdir(original_cwd)


def test_deploy_dry_run(temp_dir, mock_env_credentials, sample_worker_script):
    """Test dry-run deployment."""
    config = Config.create_default("test-worker", str(temp_dir / ".cfworker.json"))
    worker_path = temp_dir / "worker.js"
    worker_path.write_text(sample_worker_script)

    import os
    original_cwd = os.getcwd()
    os.chdir(temp_dir)

    try:
        deployer = WorkerDeployer(config)
        result = deployer.deploy(dry_run=True)

        assert result["worker_name"] == "test-worker"
        assert result["status"] == "dry_run"
        assert result["script_size"] == len(sample_worker_script)
    finally:
        os.chdir(original_cwd)
