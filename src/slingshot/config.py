"""Configuration management for Slingshot."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv


class Config:
    """Manages configuration for Cloudflare Workers deployment."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.

        Args:
            config_path: Path to .slingshot.json file. Defaults to current directory.
        """
        self.config_path = Path(config_path) if config_path else Path.cwd() / ".slingshot.json"
        self.config_data: Dict[str, Any] = {}

        # Load environment variables
        load_dotenv()

        # Load config file if it exists
        if self.config_path.exists():
            self.load()

    def load(self) -> Dict[str, Any]:
        """Load configuration from file.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        with open(self.config_path, 'r') as f:
            self.config_data = json.load(f)
        return self.config_data

    def save(self, data: Dict[str, Any]) -> None:
        """Save configuration to file.

        Args:
            data: Configuration dictionary to save
        """
        self.config_data = data
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value
        """
        return self.config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key
            value: Value to set
        """
        self.config_data[key] = value

    @property
    def account_id(self) -> Optional[str]:
        """Get Cloudflare account ID from environment."""
        return os.getenv("CLOUDFLARE_ACCOUNT_ID")

    @property
    def api_token(self) -> Optional[str]:
        """Get Cloudflare API token from environment."""
        return os.getenv("CLOUDFLARE_API_TOKEN")

    @property
    def worker_name(self) -> Optional[str]:
        """Get worker name from config."""
        return self.get("worker_name")

    @property
    def main_script(self) -> str:
        """Get main script path from config."""
        return self.get("main", "worker.js")

    @property
    def compatibility_date(self) -> str:
        """Get compatibility date from config."""
        return self.get("compatibility_date", "2024-01-01")

    def validate(self) -> tuple[bool, list[str]]:
        """Validate configuration.

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        if not self.account_id:
            errors.append("CLOUDFLARE_ACCOUNT_ID not set in environment")

        if not self.api_token:
            errors.append("CLOUDFLARE_API_TOKEN not set in environment")

        if not self.worker_name:
            errors.append("worker_name not set in config")

        main_path = Path.cwd() / self.main_script
        if not main_path.exists():
            errors.append(f"Main script not found: {self.main_script}")

        return len(errors) == 0, errors

    @classmethod
    def create_default(cls, worker_name: str, output_path: Optional[str] = None) -> "Config":
        """Create a default configuration file.

        Args:
            worker_name: Name of the worker
            output_path: Path to save config file

        Returns:
            Config instance
        """
        config = cls(output_path)
        default_data = {
            "worker_name": worker_name,
            "main": "worker.js",
            "compatibility_date": "2024-01-01",
            "routes": [],
            "kv_namespaces": [],
            "vars": {},
            "triggers": {
                "crons": []
            }
        }
        config.save(default_data)
        return config
