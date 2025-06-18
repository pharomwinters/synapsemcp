"""
Database layer for Synapse.

This package contains all database-related functionality including:
- Abstract base classes for database operations
- Concrete implementations for SQLite, DuckDB, and MariaDB
- Data models and schemas
- Database factory functions
"""

from .base import SynapseDatabase, MemoryRecord
from .models import DatabaseConnectionError, MemoryNotFoundError

from typing import Dict, Type, Any
from ..core.config import get_config
from ..core.exceptions import ConfigurationError

# Database implementation registry (populated dynamically)
DATABASE_REGISTRY: Dict[str, Type[SynapseDatabase]] = {}

def create_database(db_config: Dict[str, Any] = None) -> SynapseDatabase:
    """
    Create a database instance based on configuration.
    
    Args:
        db_config: Database configuration dict. If None, uses global config.
        
    Returns:
        Configured database instance
        
    Raises:
        ConfigurationError: If database type is not supported
    """
    if db_config is None:
        from ..core.config import get_database_config
        db_config = get_database_config()
    
    db_type = db_config.get("type", "duckdb")
    
    # Dynamic import of database class
    if db_type == "sqlite":
        from .sqlite import SQLiteDatabase
        return SQLiteDatabase(**db_config)
    elif db_type == "duckdb":
        from .duckdb import DuckDBDatabase
        return DuckDBDatabase(**db_config)
    elif db_type in ["mariadb", "mysql"]:
        from .mariadb import MariaDBDatabase
        return MariaDBDatabase(**db_config)
    else:
        raise ConfigurationError(f"Unsupported database type: {db_type}")

def get_database_instance() -> SynapseDatabase:
    """Get a database instance using the global configuration."""
    return create_database()

__all__ = [
    "SynapseDatabase",
    "MemoryRecord", 
    "DatabaseConnectionError",
    "MemoryNotFoundError",
    "SQLiteDatabase",
    "DuckDBDatabase", 
    "MariaDBDatabase",
    "create_database",
    "get_database_instance",
    "DATABASE_REGISTRY",
] 