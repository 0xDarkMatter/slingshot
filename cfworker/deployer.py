"""Worker deployment logic."""

from pathlib import Path
from typing import Dict, Any, Optional

from .client import CloudflareClient
from .config import Config


class DeploymentError(Exception):
    """Exception raised for deployment errors."""
    pass


class WorkerDeployer:
    """Handles deployment of Cloudflare Workers."""

    def __init__(self, config: Config):
        """Initialize deployer.

        Args:
            config: Configuration instance
        """
        self.config = config

        # Validate configuration
        is_valid, errors = config.validate()
        if not is_valid:
            raise DeploymentError(f"Invalid configuration:\n" + "\n".join(f"  - {e}" for e in errors))

        # Initialize Cloudflare client
        self.client = CloudflareClient(
            account_id=config.account_id,
            api_token=config.api_token
        )

    def read_script(self, script_path: Optional[str] = None) -> str:
        """Read worker script from file.

        Args:
            script_path: Path to script file. Defaults to config main script.

        Returns:
            Script content

        Raises:
            DeploymentError: If script file cannot be read
        """
        path = Path(script_path) if script_path else Path.cwd() / self.config.main_script

        if not path.exists():
            raise DeploymentError(f"Script file not found: {path}")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise DeploymentError(f"Failed to read script file: {e}")

    def prepare_metadata(self) -> Dict[str, Any]:
        """Prepare worker metadata from configuration.

        Returns:
            Metadata dictionary
        """
        metadata = {
            "main_module": self.config.main_script,
            "compatibility_date": self.config.compatibility_date,
        }

        # Add bindings if configured
        bindings = []

        # Environment variables
        vars_config = self.config.get("vars", {})
        for key, value in vars_config.items():
            bindings.append({
                "type": "plain_text",
                "name": key,
                "text": value
            })

        # KV namespaces
        kv_namespaces = self.config.get("kv_namespaces", [])
        for kv in kv_namespaces:
            bindings.append({
                "type": "kv_namespace",
                "name": kv.get("binding"),
                "namespace_id": kv.get("id")
            })

        if bindings:
            metadata["bindings"] = bindings

        return metadata

    def deploy(self, script_path: Optional[str] = None, dry_run: bool = False) -> Dict[str, Any]:
        """Deploy worker to Cloudflare.

        Args:
            script_path: Path to script file. Defaults to config main script.
            dry_run: If True, validate but don't actually deploy

        Returns:
            Deployment result

        Raises:
            DeploymentError: If deployment fails
        """
        worker_name = self.config.worker_name

        # Read script
        script_content = self.read_script(script_path)

        # Prepare metadata
        metadata = self.prepare_metadata()

        if dry_run:
            return {
                "worker_name": worker_name,
                "script_size": len(script_content),
                "metadata": metadata,
                "status": "dry_run"
            }

        # Deploy to Cloudflare
        try:
            result = self.client.upload_worker(
                worker_name=worker_name,
                script_content=script_content,
                metadata=metadata
            )

            return {
                "worker_name": worker_name,
                "script_size": len(script_content),
                "deployed": True,
                "result": result
            }
        except Exception as e:
            raise DeploymentError(f"Failed to deploy worker: {e}")

    def delete(self) -> Dict[str, Any]:
        """Delete worker from Cloudflare.

        Returns:
            Deletion result

        Raises:
            DeploymentError: If deletion fails
        """
        worker_name = self.config.worker_name

        try:
            result = self.client.delete_worker(worker_name)
            return {
                "worker_name": worker_name,
                "deleted": True,
                "result": result
            }
        except Exception as e:
            raise DeploymentError(f"Failed to delete worker: {e}")

    def get_info(self) -> Dict[str, Any]:
        """Get information about deployed worker.

        Returns:
            Worker information

        Raises:
            DeploymentError: If worker info cannot be retrieved
        """
        worker_name = self.config.worker_name

        try:
            result = self.client.get_worker(worker_name)
            return result
        except Exception as e:
            raise DeploymentError(f"Failed to get worker info: {e}")

    def list_workers(self) -> Dict[str, Any]:
        """List all workers in the account.

        Returns:
            List of workers
        """
        try:
            workers = self.client.list_workers()
            return {"workers": workers, "count": len(workers)}
        except Exception as e:
            raise DeploymentError(f"Failed to list workers: {e}")

    def verify_connection(self) -> bool:
        """Verify connection to Cloudflare API.

        Returns:
            True if connection is valid

        Raises:
            DeploymentError: If connection verification fails
        """
        try:
            return self.client.verify_token()
        except Exception as e:
            raise DeploymentError(f"Failed to verify connection: {e}")
