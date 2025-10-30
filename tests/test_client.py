"""Tests for Cloudflare API client."""

import pytest
import responses
from slingshot.client import CloudflareClient, CloudflareAPIError


@pytest.fixture
def client():
    """Create a test Cloudflare client."""
    return CloudflareClient(
        account_id="test_account_id",
        api_token="test_api_token"
    )


def test_client_initialization(client):
    """Test client initialization."""
    assert client.account_id == "test_account_id"
    assert client.api_token == "test_api_token"
    assert "Bearer test_api_token" in client.session.headers["Authorization"]


@responses.activate
def test_verify_token_success(client):
    """Test successful token verification."""
    responses.add(
        responses.GET,
        "https://api.cloudflare.com/client/v4/user/tokens/verify",
        json={"success": True, "result": {"status": "active"}},
        status=200
    )

    assert client.verify_token() is True


@responses.activate
def test_verify_token_failure(client):
    """Test failed token verification."""
    responses.add(
        responses.GET,
        "https://api.cloudflare.com/client/v4/user/tokens/verify",
        json={"success": False, "errors": [{"message": "Invalid token"}]},
        status=403
    )

    assert client.verify_token() is False


@responses.activate
def test_upload_worker_success(client):
    """Test successful worker upload."""
    responses.add(
        responses.PUT,
        "https://api.cloudflare.com/client/v4/accounts/test_account_id/workers/scripts/test-worker",
        json={"success": True, "result": {"id": "test-worker"}},
        status=200
    )

    result = client.upload_worker(
        worker_name="test-worker",
        script_content="export default { async fetch() {} };"
    )

    assert result["id"] == "test-worker"


@responses.activate
def test_api_error_handling(client):
    """Test API error handling."""
    responses.add(
        responses.GET,
        "https://api.cloudflare.com/client/v4/accounts/test_account_id/workers/scripts",
        json={
            "success": False,
            "errors": [{"message": "Authentication error"}]
        },
        status=403
    )

    with pytest.raises(CloudflareAPIError) as exc_info:
        client.list_workers()

    assert "Authentication error" in str(exc_info.value)
    assert exc_info.value.status_code == 403


@responses.activate
def test_list_workers(client):
    """Test listing workers."""
    responses.add(
        responses.GET,
        "https://api.cloudflare.com/client/v4/accounts/test_account_id/workers/scripts",
        json={
            "success": True,
            "result": [
                {"id": "worker-1", "created_on": "2024-01-01"},
                {"id": "worker-2", "created_on": "2024-01-02"}
            ]
        },
        status=200
    )

    workers = client.list_workers()
    assert len(workers) == 2
    assert workers[0]["id"] == "worker-1"


@responses.activate
def test_delete_worker(client):
    """Test deleting a worker."""
    responses.add(
        responses.DELETE,
        "https://api.cloudflare.com/client/v4/accounts/test_account_id/workers/scripts/test-worker",
        json={"success": True, "result": None},
        status=200
    )

    result = client.delete_worker("test-worker")
    assert result is not None
