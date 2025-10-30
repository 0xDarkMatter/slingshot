"""Cloudflare API client wrapper."""

from typing import Any, Dict, List, Optional
import requests


class CloudflareAPIError(Exception):
    """Exception raised for Cloudflare API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, errors: Optional[List] = None):
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(self.message)


class CloudflareClient:
    """Client for interacting with Cloudflare API."""

    BASE_URL = "https://api.cloudflare.com/client/v4"

    def __init__(self, account_id: str, api_token: str):
        """Initialize Cloudflare client.

        Args:
            account_id: Cloudflare account ID
            api_token: Cloudflare API token
        """
        self.account_id = account_id
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make a request to the Cloudflare API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: JSON data to send
            files: Files to upload
            params: Query parameters

        Returns:
            API response data

        Raises:
            CloudflareAPIError: If the API request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"

        # Handle file uploads differently
        headers = None
        if files:
            headers = {"Authorization": f"Bearer {self.api_token}"}
            response = self.session.request(
                method,
                url,
                data=data,
                files=files,
                params=params,
                headers=headers
            )
        else:
            response = self.session.request(
                method,
                url,
                json=data,
                params=params
            )

        # Parse response
        try:
            result = response.json()
        except ValueError:
            raise CloudflareAPIError(
                f"Invalid JSON response from API: {response.text}",
                status_code=response.status_code
            )

        # Check for errors
        if not result.get("success", False):
            errors = result.get("errors", [])
            error_messages = [e.get("message", str(e)) for e in errors]
            raise CloudflareAPIError(
                f"API request failed: {', '.join(error_messages)}",
                status_code=response.status_code,
                errors=errors
            )

        return result.get("result", {})

    def list_workers(self) -> List[Dict[str, Any]]:
        """List all workers in the account.

        Returns:
            List of worker scripts
        """
        return self._request("GET", f"accounts/{self.account_id}/workers/scripts")

    def get_worker(self, worker_name: str) -> Dict[str, Any]:
        """Get details of a specific worker.

        Args:
            worker_name: Name of the worker

        Returns:
            Worker details
        """
        return self._request("GET", f"accounts/{self.account_id}/workers/scripts/{worker_name}")

    def upload_worker(
        self,
        worker_name: str,
        script_content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Upload or update a worker script.

        Args:
            worker_name: Name of the worker
            script_content: JavaScript/TypeScript worker code
            metadata: Worker metadata (bindings, vars, etc.)

        Returns:
            Upload response
        """
        # Prepare multipart form data
        files = {
            "script": ("worker.js", script_content, "application/javascript+module")
        }

        # Add metadata if provided
        data = {}
        if metadata:
            import json
            data["metadata"] = json.dumps(metadata)

        return self._request(
            "PUT",
            f"accounts/{self.account_id}/workers/scripts/{worker_name}",
            data=data,
            files=files
        )

    def delete_worker(self, worker_name: str) -> Dict[str, Any]:
        """Delete a worker script.

        Args:
            worker_name: Name of the worker to delete

        Returns:
            Delete response
        """
        return self._request(
            "DELETE",
            f"accounts/{self.account_id}/workers/scripts/{worker_name}"
        )

    def get_worker_routes(self, zone_id: str) -> List[Dict[str, Any]]:
        """Get routes for a zone.

        Args:
            zone_id: Cloudflare zone ID

        Returns:
            List of routes
        """
        return self._request("GET", f"zones/{zone_id}/workers/routes")

    def create_worker_route(
        self,
        zone_id: str,
        pattern: str,
        worker_name: str
    ) -> Dict[str, Any]:
        """Create a route for a worker.

        Args:
            zone_id: Cloudflare zone ID
            pattern: Route pattern (e.g., "example.com/*")
            worker_name: Name of the worker to route to

        Returns:
            Route creation response
        """
        return self._request(
            "POST",
            f"zones/{zone_id}/workers/routes",
            data={"pattern": pattern, "script": worker_name}
        )

    def list_kv_namespaces(self) -> List[Dict[str, Any]]:
        """List all KV namespaces in the account.

        Returns:
            List of KV namespaces
        """
        return self._request("GET", f"accounts/{self.account_id}/storage/kv/namespaces")

    def create_kv_namespace(self, title: str) -> Dict[str, Any]:
        """Create a KV namespace.

        Args:
            title: Namespace title

        Returns:
            Namespace creation response
        """
        return self._request(
            "POST",
            f"accounts/{self.account_id}/storage/kv/namespaces",
            data={"title": title}
        )

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information.

        Returns:
            Account details
        """
        return self._request("GET", f"accounts/{self.account_id}")

    def verify_token(self) -> bool:
        """Verify that the API token is valid.

        Returns:
            True if token is valid, False otherwise
        """
        try:
            self._request("GET", "user/tokens/verify")
            return True
        except CloudflareAPIError:
            return False
