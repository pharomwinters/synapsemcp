# servers/config_server.py
"""
Configuration Server - Configuration management for Synapse.

Handles configuration retrieval, system information, and settings management.
"""

from mcp.server.fastmcp import FastMCP
from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config

# Create the configuration server
config_server = FastMCP("Synapse-Config")


@config_server.tool()
async def get_configuration(key: str = None) -> Dict[str, Any]:
    """Get Synapse configuration settings.

    Args:
        key: The configuration key to retrieve (dot notation for nested keys)
             If None, returns all configuration settings
    """
    if key:
        value = config.get(key)
        return {key: value}
    else:
        # Return a simplified view of the configuration
        return {
            "database": {
                "type": config.get("database.type"),
                "sqlite": {
                    "db_path": config.get("database.sqlite.db_path")
                },
                "mariadb": {
                    "host": config.get("database.mariadb.host"),
                    "port": config.get("database.mariadb.port"),
                    "database": config.get("database.mariadb.database")
                }
            },
            "memory_dir": config.get("memory_dir"),
            "encoding": config.get("encoding"),
            "log_level": config.get("log_level"),
            "environment": config.get("environment")
        }


@config_server.tool()
async def get_environment_info() -> Dict[str, Any]:
    """Get information about the current environment and system."""
    import platform
    import sys
    
    return {
        "environment": config.get("environment", "unknown"),
        "python_version": sys.version,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor()
        },
        "memory_bank": {
            "database_type": config.get("database.type"),
            "memory_directory": config.get("memory_dir"),
            "encoding": config.get("encoding")
        }
    }


@config_server.tool()
async def validate_configuration() -> Dict[str, Any]:
    """Validate the current Synapse configuration."""
    validation_results = {
        "valid": True,
        "issues": [],
        "warnings": []
    }
    
    # Check database configuration
    db_type = config.get("database.type")
    if not db_type:
        validation_results["valid"] = False
        validation_results["issues"].append("Database type not configured")
    
    if db_type == "sqlite":
        db_path = config.get("database.sqlite.db_path")
        if not db_path:
            validation_results["valid"] = False
            validation_results["issues"].append("SQLite database path not configured")
    elif db_type in ["mariadb", "mysql"]:
        host = config.get("database.mariadb.host")
        if not host:
            validation_results["valid"] = False
            validation_results["issues"].append("MariaDB host not configured")
    
    # Check memory directory
    memory_dir = config.get("memory_dir")
    if not memory_dir:
        validation_results["warnings"].append("Memory directory not configured, using default")
    
    # Check environment
    env = config.get("environment")
    if env not in ["development", "testing", "production"]:
        validation_results["warnings"].append(f"Unknown environment: {env}")
    
    return validation_results


@config_server.tool()
async def get_database_status() -> Dict[str, Any]:
    """Get the status of the database connection."""
    from utils import get_db_instance
    
    try:
        db = get_db_instance()
        # Test connection
        with db:
            db.connect()
            
        return {
            "status": "connected",
            "database_type": config.get("database.type"),
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "error",
            "database_type": config.get("database.type"),
            "message": f"Database connection failed: {str(e)}"
        }


# For standalone testing
if __name__ == "__main__":
    config_server.run() 