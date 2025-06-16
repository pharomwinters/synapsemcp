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
Configuration Server - Configuration management for Synapse.

This server handles configuration settings, system information, and 
environment management for the Synapse platform.
"""

from fastmcp import FastMCP
from typing import Dict, Any, Optional
import os
import sys
import platform
from datetime import datetime

# Local imports
from config import get_config, get_database_config, get_environment

# Create Config Server instance
config_server = FastMCP("Config Synapse")

@config_server.tool()
def get_configuration(key: Optional[str] = None) -> Dict[str, Any]:
    """Get Synapse configuration settings.
    
    Args:
        key: Optional configuration key to retrieve specific setting
        
    Returns:
        Configuration dictionary or specific value
    """
    try:
        if key:
            value = get_config(key)
            return {"key": key, "value": value}
        else:
            return get_config()
    except Exception as e:
        return {"error": f"Failed to get configuration: {str(e)}"}

@config_server.tool()
def get_environment_info() -> Dict[str, Any]:
    """Get information about current environment and system."""
    try:
        return {
            "environment": get_environment(),
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor()
            },
            "python": {
                "version": sys.version,
                "executable": sys.executable,
                "path": sys.path[:3]  # First 3 entries to avoid too much output
            },
            "process": {
                "pid": os.getpid(),
                "cwd": os.getcwd(),
                "user": os.environ.get("USER", os.environ.get("USERNAME", "unknown"))
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": f"Failed to get environment info: {str(e)}"}

@config_server.tool()
def validate_configuration() -> Dict[str, Any]:
    """Validate the current Synapse configuration."""
    try:
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        # Check database configuration
        try:
            db_config = get_database_config()
            db_type = db_config.get("type", "unknown")
            
            if db_type == "sqlite":
                db_path = db_config.get("db_path")
                if not db_path:
                    validation_results["errors"].append("SQLite database path not configured")
                    validation_results["valid"] = False
                else:
                    validation_results["info"].append(f"SQLite database configured: {db_path}")
                    
            elif db_type == "mariadb":
                required_fields = ["host", "port", "user", "database"]
                for field in required_fields:
                    if not db_config.get(field):
                        validation_results["errors"].append(f"MariaDB {field} not configured")
                        validation_results["valid"] = False
                        
                if validation_results["valid"]:
                    validation_results["info"].append("MariaDB configuration appears complete")
                    
            else:
                validation_results["errors"].append(f"Unknown database type: {db_type}")
                validation_results["valid"] = False
                
        except Exception as e:
            validation_results["errors"].append(f"Database configuration error: {str(e)}")
            validation_results["valid"] = False
            
        # Check memory directory
        memory_dir = get_config("memory_dir", "memories")
        if not memory_dir:
            validation_results["warnings"].append("Memory directory not configured, using default")
        else:
            validation_results["info"].append(f"Memory directory configured: {memory_dir}")
            
        # Check environment
        env = get_environment()
        if env not in ["development", "testing", "production"]:
            validation_results["warnings"].append(f"Unusual environment: {env}")
        else:
            validation_results["info"].append(f"Environment: {env}")
            
        return validation_results
        
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Configuration validation failed: {str(e)}"],
            "warnings": [],
            "info": []
        }

@config_server.tool()
def get_database_status() -> Dict[str, Any]:
    """Get the status of the database connection."""
    try:
        from utils import get_db_instance
        
        db_config = get_database_config()
        db_type = db_config.get("type", "unknown")
        
        status = {
            "type": db_type,
            "configuration": db_config,
            "connected": False,
            "error": None
        }
        
        try:
            db = get_db_instance()
            # Try a simple operation to test connectivity
            db.list_memories()
            status["connected"] = True
            status["message"] = "Database connection successful"
        except Exception as e:
            status["error"] = str(e)
            status["message"] = f"Database connection failed: {str(e)}"
            
        return status
        
    except Exception as e:
        return {
            "type": "unknown",
            "connected": False,
            "error": str(e),
            "message": f"Failed to check database status: {str(e)}"
        }

@config_server.tool()
def get_system_stats() -> Dict[str, Any]:
    """Get system statistics and resource usage."""
    try:
        import psutil
        
        stats = {
            "cpu": {
                "percent": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count(),
                "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent,
                "used": psutil.virtual_memory().used
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "used": psutil.disk_usage('/').used,
                "free": psutil.disk_usage('/').free,
                "percent": psutil.disk_usage('/').percent
            }
        }
        
        return stats
        
    except ImportError:
        return {"error": "psutil not installed - cannot get system stats"}
    except Exception as e:
        return {"error": f"Failed to get system stats: {str(e)}"}

# Export the server
__all__ = ["config_server"] 