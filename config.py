#
# This file is part of Synapse.
#
# Synapse is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Synapse is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Synapse.  If not, see <https://www.gnu.org/licenses/>.
#
"""
Configuration management for Synapse.

This module handles loading and managing configuration settings for the Synapse system.
It supports different environments (development, testing, production) and can load
settings from JSON files or environment variables.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration structure
DEFAULT_CONFIG = {
    "database": {
        "type": "sqlite",
        "sqlite": {
            "db_path": "synapse.db"
        },
        "mariadb": {
            "host": "localhost",
            "port": 3306,
            "user": "synapse_user",
            "database": "synapse"
        }
    },
    "memory_dir": "memories",
    "encoding": "utf-8",
    "log_level": "INFO"
}

class ConfigurationError(Exception):
    """Raised when there's an error with configuration."""
    pass

class Config:
    """Configuration manager for Synapse.
    
    Loads configuration from JSON files and environment variables.
    Supports different environments: development, testing, production.
    
    Environment files:
    - config.dev.json: Development settings
    - config.test.json: Testing settings  
    - config.prod.json: Production settings
    - config.local.json: Local overrides (not in version control)
    
    Environment variables take precedence over file settings.
    """
    
    def __init__(self):
        self._config = DEFAULT_CONFIG.copy()
        self._loaded_env = None
    
    def load(self, environment: Optional[str] = None) -> None:
        """Load configuration for the specified environment.
        
        Args:
            environment: Environment name (development/testing/production).
                        If None, uses the SYNAPSE_ENV environment variable or defaults to 'development'
        """
        if environment is None:
            env = os.environ.get("SYNAPSE_ENV", "development")
        else:
            env = environment
            
        self._loaded_env = env
        
        # Load base configuration from file
        config_file = f"config.{env}.json"
        if Path(config_file).exists():
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self._merge_config(file_config)
        
        # Try to load local overrides
        local_config_file = "config.local.json"
        if Path(local_config_file).exists():
            with open(local_config_file, 'r') as f:
                local_config = json.load(f)
                self._merge_config(local_config)
        
        # Override with environment variables
        self._load_from_environment()
    
    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """Merge new configuration into existing config."""
        def merge_dict(base: Dict, new: Dict) -> Dict:
            result = base.copy()
            for key, value in new.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dict(result[key], value)
                else:
                    result[key] = value
            return result
        
        self._config = merge_dict(self._config, new_config)
    
    def _load_from_environment(self) -> None:
        """Load configuration overrides from environment variables."""
        # Database configuration
        if "SYNAPSE_DB_TYPE" in os.environ:
            self._config["database"]["type"] = os.environ["SYNAPSE_DB_TYPE"]
        
        # SQLite configuration
        if "SYNAPSE_SQLITE_DB_PATH" in os.environ:
            self._config["database"]["sqlite"]["db_path"] = os.environ["SYNAPSE_SQLITE_DB_PATH"]
        
        # MariaDB configuration
        if "SYNAPSE_MARIADB_HOST" in os.environ:
            self._config["database"]["mariadb"]["host"] = os.environ["SYNAPSE_MARIADB_HOST"]
        
        if "SYNAPSE_MARIADB_PORT" in os.environ:
            try:
                self._config["database"]["mariadb"]["port"] = int(os.environ["SYNAPSE_MARIADB_PORT"])
            except ValueError:
                raise ConfigurationError(f"Invalid port number: {os.environ['SYNAPSE_MARIADB_PORT']}")
        
        if "SYNAPSE_MARIADB_USER" in os.environ:
            self._config["database"]["mariadb"]["user"] = os.environ["SYNAPSE_MARIADB_USER"]
        
        if "SYNAPSE_MARIADB_PASSWORD" in os.environ:
            self._config["database"]["mariadb"]["password"] = os.environ["SYNAPSE_MARIADB_PASSWORD"]
        
        if "SYNAPSE_MARIADB_DATABASE" in os.environ:
            self._config["database"]["mariadb"]["database"] = os.environ["SYNAPSE_MARIADB_DATABASE"]
        
        # Other configuration
        if "SYNAPSE_MEMORY_DIR" in os.environ:
            self._config["memory_dir"] = os.environ["SYNAPSE_MEMORY_DIR"]
        
        if "SYNAPSE_ENCODING" in os.environ:
            self._config["encoding"] = os.environ["SYNAPSE_ENCODING"]
        
        if "SYNAPSE_LOG_LEVEL" in os.environ:
            self._config["log_level"] = os.environ["SYNAPSE_LOG_LEVEL"]
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key path.
        
        Args:
            key: Configuration key (supports dot notation like 'database.type')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        try:
            keys = key.split('.')
            value = self._config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration for the current database type."""
        db_type = self.get("database.type", "sqlite")
        db_config = self.get(f"database.{db_type}", {})
        return {"type": db_type, **db_config}
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration as a dictionary."""
        return self._config.copy()
    
    def get_environment(self) -> Optional[str]:
        """Get the currently loaded environment name."""
        return self._loaded_env
    
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self._loaded_env == "development"
    
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self._loaded_env == "testing"
    
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self._loaded_env == "production"

# Global configuration instance
config = Config()

# Convenience functions
def get_config(key: Optional[str] = None, default: Any = None) -> Any:
    """Get configuration value. If key is None, returns all config."""
    if key is None:
        return config.get_all()
    return config.get(key, default)

def get_database_config() -> Dict[str, Any]:
    """Get database configuration."""
    return config.get_database_config()

def load_config(environment: Optional[str] = None) -> None:
    """Load configuration for specified environment."""
    config.load(environment)

def get_environment() -> Optional[str]:
    """Get current environment."""
    return config.get_environment()

# Auto-load configuration on import
if not config.get_environment():
    config.load()