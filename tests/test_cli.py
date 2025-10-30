"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner
from pathlib import Path

from slingshot.cli import main


@pytest.fixture
def cli_runner():
    """Create a CLI test runner."""
    return CliRunner()


def test_cli_version(cli_runner):
    """Test --version flag."""
    result = cli_runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert '0.1.0' in result.output


def test_cli_help(cli_runner):
    """Test --help flag."""
    result = cli_runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'CFWorker' in result.output
    assert 'deploy' in result.output
    assert 'init' in result.output


def test_init_command(cli_runner, temp_dir):
    """Test init command."""
    with cli_runner.isolated_filesystem(temp=temp_dir):
        result = cli_runner.invoke(main, ['init', 'test-worker', '--template', 'api'])

        assert result.exit_code == 0
        assert Path('.slingshot.json').exists()
        assert Path('worker.js').exists()
        assert 'Created .slingshot.json' in result.output
        assert 'Created worker.js' in result.output


def test_init_command_force_overwrite(cli_runner, temp_dir):
    """Test init command with --force flag."""
    with cli_runner.isolated_filesystem(temp=temp_dir):
        # Create files first
        Path('.slingshot.json').write_text('{}')
        Path('worker.js').write_text('test')

        # Try without --force (should fail)
        result = cli_runner.invoke(main, ['init', 'test-worker'])
        assert result.exit_code != 0
        assert 'already exists' in result.output

        # Try with --force (should succeed)
        result = cli_runner.invoke(main, ['init', 'test-worker', '--force'])
        assert result.exit_code == 0


def test_init_templates(cli_runner, temp_dir):
    """Test different templates."""
    templates = ['api', 'static', 'edge']

    for template in templates:
        with cli_runner.isolated_filesystem(temp=temp_dir):
            result = cli_runner.invoke(main, ['init', 'test-worker', '--template', template])
            assert result.exit_code == 0

            worker_content = Path('worker.js').read_text()
            assert len(worker_content) > 0
            assert 'export default' in worker_content


def test_deploy_missing_config(cli_runner, temp_dir):
    """Test deploy command without config file."""
    with cli_runner.isolated_filesystem(temp=temp_dir):
        result = cli_runner.invoke(main, ['deploy'])
        # Should fail because config doesn't exist
        assert result.exit_code != 0


def test_deploy_dry_run(cli_runner, temp_dir, mock_env_credentials, sample_worker_script, sample_config):
    """Test deploy with --dry-run flag."""
    import json

    with cli_runner.isolated_filesystem(temp=temp_dir):
        # Setup config and worker
        Path('.slingshot.json').write_text(json.dumps(sample_config))
        Path('worker.js').write_text(sample_worker_script)

        result = cli_runner.invoke(main, ['deploy', '--dry-run'])
        assert result.exit_code == 0
        assert 'Validation successful' in result.output
