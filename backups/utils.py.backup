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
Utility functions for Synapse database operations.

This module provides utility functions for database operations, file management,
auto-discovery of tools, and other common tasks used throughout the Synapse system.
"""

import os
import sys
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union, cast
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)


class SynapseException(Exception):
    """Base exception for synapse operations."""
    pass


from contextlib import contextmanager
from typing import Iterator

from base import SynapseDatabase
from mariadb import MariaDBDatabase
from sqlite_db import SQLiteDatabase
from config import config, ConfigurationError

MEMORY_FILE_EXTENSION = ".md"
ENCODING = config.get("encoding", "utf-8")
SUPPORTED_DB_TYPES = {
    "sqlite": SQLiteDatabase,
    "mariadb": MariaDBDatabase,
    "mysql": MariaDBDatabase
}


# Auto-discovery functions for MCP tools
def mcp_tool(func):
    """Decorator to mark functions as MCP tools for auto-discovery."""
    func._is_mcp_tool = True
    return func


def auto_discover_tools(mcp_instance, module_or_path: Union[str, object], 
                       prefix: str = "", verbose: bool = False) -> int:
    """
    Auto-discover and register MCP tools from a module.
    
    Args:
        mcp_instance: The FastMCP instance to register tools with
        module_or_path: Module object or import path (e.g., 'myproject.tools')
        prefix: Optional prefix for tool names
        verbose: Print registration details
        
    Returns:
        Number of tools registered
        
    Example:
        # In your tools module
        @mcp_tool
        def my_function():
            return "Hello"
            
        # In your main file
        from utils import auto_discover_tools
        auto_discover_tools(mcp, 'myproject.tools', prefix='db_')
    """
    # Import module if string path provided
    if isinstance(module_or_path, str):
        try:
            module = importlib.import_module(module_or_path)
        except ImportError as e:
            raise SynapseException(f"Failed to import module '{module_or_path}': {e}")
    else:
        module = module_or_path
    
    registered_count = 0
    
    # Scan module for marked functions
    for name in dir(module):
        if name.startswith('_'):
            continue
            
        func = getattr(module, name)
        
        # Check if it's a callable function marked as MCP tool
        if (callable(func) and 
            hasattr(func, '_is_mcp_tool') and 
            func._is_mcp_tool):
            
            try:
                # Generate tool name with optional prefix
                tool_name = f"{prefix}{name}" if prefix else name
                
                # Register with FastMCP (works for both sync and async)
                mcp_instance.tool(name=tool_name)(func)
                
                if verbose:
                    func_type = "async" if inspect.iscoroutinefunction(func) else "sync"
                    print(f"Registered {func_type} tool: {tool_name}")
                
                registered_count += 1
                
            except Exception as e:
                if verbose:
                    print(f"Failed to register tool '{name}': {e}")
    
    return registered_count


def discover_tools_from_pattern(mcp_instance, pattern: str = "tools_*.py", 
                               base_path: str = ".", verbose: bool = False) -> int:
    """
    Auto-discover tools from files matching a pattern.
    
    Args:
        mcp_instance: The FastMCP instance
        pattern: File pattern to match (e.g., "tools_*.py", "*_tools.py")
        base_path: Base directory to search
        verbose: Print discovery details
        
    Returns:
        Total number of tools registered
    """
    from pathlib import Path
    import sys
    
    base_path_path = Path(base_path)
    total_registered = 0
    
    for file_path in base_path_path.glob(pattern):
        if file_path.is_file() and file_path.suffix == '.py':
            # Convert file path to module name
            module_name = file_path.stem
            
            try:
                # Add to Python path if needed
                if str(base_path_path) not in sys.path:
                    sys.path.insert(0, str(base_path_path))
                
                # Import and register tools
                registered = auto_discover_tools(mcp_instance, module_name, verbose=verbose)
                total_registered += registered
                
                if verbose:
                    print(f"Found {registered} tools in {file_path}")
                    
            except Exception as e:
                if verbose:
                    print(f"Error processing {file_path}: {e}")
    
    return total_registered


class MemoryFileSystem:
    """Handles file system operations for memory files."""

    def __init__(self, memory_dir: Optional[Union[str, Path]] = None):
        """
        Initialize the memory file system.

        Args:
            memory_dir: The directory where memory files are stored
                       If None, uses the directory from configuration
        """
        if memory_dir is None:
            memory_dir = config.get("memory_dir", "memories")
        self.memory_dir = Path(str(memory_dir))

    def ensure_directory_exists(self) -> None:
        """Create memory directory if it doesn't exist."""
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def read_file(self, file_name: str) -> Optional[str]:
        """
        Read content from a memory file.

        Args:
            file_name: The name of the memory file to read

        Returns:
            The content of the memory file or None if not found

        Raises:
            SynapseException: If there is an error reading the file
        """
        file_path = self.memory_dir / file_name
        try:
            return file_path.read_text(encoding=ENCODING) if file_path.is_file() else None
        except Exception as e:
            raise SynapseException(f"Error reading file {file_name}: {e}")

    def write_file(self, file_name: str, content: str) -> None:
        """
        Write content to a memory file.

        Args:
            file_name: The name of the memory file to write
            content: The content to write to the file

        Raises:
            SynapseException: If there is an error writing the file
        """
        self.ensure_directory_exists()
        file_path = self.memory_dir / file_name
        try:
            file_path.write_text(content, encoding=ENCODING)
        except Exception as e:
            raise SynapseException(f"Error writing file {file_name}: {e}")

    def list_files(self) -> List[str]:
        """
        List all memory files in the directory.

        Returns:
            A list of memory file names
        """
        return [f.name for f in self.memory_dir.glob(f"*{MEMORY_FILE_EXTENSION}")]


@contextmanager
def db_connection(db: SynapseDatabase) -> Iterator[SynapseDatabase]:
    """Context manager for database connections."""
    try:
        db.connect()
        yield db
    finally:
        db.disconnect()


def get_db_instance(db_type: Optional[str] = None, **kwargs) -> SynapseDatabase:
    """
    Get a database instance based on the specified type.

    Args:
        db_type: The database type to use (sqlite, mariadb, mysql)
                If None, uses the type from configuration
        **kwargs: Additional parameters to pass to the database constructor
                  These override any values from configuration

    Returns:
        A database instance of the specified type

    Raises:
        SynapseException: If the database type is not supported
    """
    # Use configuration if db_type is not specified
    if db_type is None:
        db_type = config.get("database.type", "sqlite")
    
    # Ensure db_type is a string before calling lower()
    db_type_str = str(db_type)
    db_class = SUPPORTED_DB_TYPES.get(db_type_str.lower())
    
    if not db_class:
        raise SynapseException(f"Unsupported database type: {db_type}")

    # Get database configuration and override with kwargs
    db_config = get_db_config_from_config()
    db_config.update(kwargs)

    return db_class(**db_config)


def get_db_config_from_config() -> Dict[str, Any]:
    """
    Extract database configuration from the global config.
    
    Returns:
        A dictionary with database configuration parameters
    """
    db_config = {
        "host": config.get("database.host", "localhost"),
        "port": config.get("database.port", 3306),
        "user": config.get("database.user", "root"),
        "password": config.get("database.password", ""),
        "database": config.get("database.name", "synapse"),
        "db_path": config.get("database.path", "synapse.db")
    }
    return db_config


def migrate_files_to_db(memory_dir: Optional[Union[str, Path]] = None, db: Optional[SynapseDatabase] = None) -> Dict[str, bool]:
    """
    Migrate memory files from the filesystem to the database.

    Args:
        memory_dir: The directory where memory files are stored
                   If None, uses the directory from configuration
        db: The database instance to use
            If None, creates a new instance using configuration

    Returns:
        A dictionary mapping file names to success status
    """
    fs = MemoryFileSystem(memory_dir)
    results = {}

    # Create database instance if not provided
    if db is None:
        db = get_db_instance()

    with db_connection(db) as connected_db:
        connected_db.create_tables()
        for file_name in fs.list_files():
            try:
                content = fs.read_file(file_name)
                if content:
                    connected_db.store_memory(file_name, content)
                    results[file_name] = True
            except Exception as e:
                print(f"Error migrating {file_name}: {e}")
                results[file_name] = False

    return results


def read_memory_from_db_or_file(file_name: str, memory_dir: Optional[Union[str, Path]] = None,
                                db: Optional[SynapseDatabase] = None) -> Optional[str]:
    """
    Read memory content from the database or file system.

    Args:
        file_name: The name of the memory file to read
        memory_dir: The directory where memory files are stored
                   If None, uses the directory from configuration
        db: The database instance to use
            If None, creates a new instance using configuration

    Returns:
        The content of the memory file or None if not found
    """
    # Create database instance if not provided
    if db is None:
        db = get_db_instance()

    try:
        with db_connection(db) as connected_db:
            content = connected_db.get_memory(file_name)
            if content:
                return content
    except Exception as e:
        print(f"Error reading from database: {e}")

    fs = MemoryFileSystem(memory_dir)
    return fs.read_file(file_name)


def write_memory_to_db_and_file(file_name: str, content: str,
                                memory_dir: Optional[Union[str, Path]] = None,
                                db: Optional[SynapseDatabase] = None) -> bool:
    """
    Write memory content to both the database and file system.

    Args:
        file_name: The name of the memory file to write
        content: The content to write to the file
        memory_dir: The directory where memory files are stored
                   If None, uses the directory from configuration
        db: The database instance to use
            If None, creates a new instance using configuration

    Returns:
        True if both operations succeeded, False otherwise
    """
    success = True
    fs = MemoryFileSystem(memory_dir)

    # Create database instance if not provided
    if db is None:
        db = get_db_instance()

    try:
        fs.write_file(file_name, content)
    except Exception as e:
        print(f"Error writing to file: {e}")
        success = False

    try:
        with db_connection(db) as connected_db:
            connected_db.store_memory(file_name, content)
    except Exception as e:
        print(f"Error writing to database: {e}")
        success = False

    return success


def list_all_memories(memory_dir: Optional[Union[str, Path]] = None, db: Optional[SynapseDatabase] = None) -> List[str]:
    """
    List all memory files from both the database and file system.

    Args:
        memory_dir: The directory where memory files are stored
                   If None, uses the directory from configuration
        db: The database instance to use
            If None, creates a new instance using configuration

    Returns:
        A sorted list of all memory file names
    """
    memories = set()
    fs = MemoryFileSystem(memory_dir)

    # Create database instance if not provided
    if db is None:
        db = get_db_instance()

    try:
        with db_connection(db) as connected_db:
            memories.update(connected_db.list_memories())
    except Exception as e:
        print(f"Error listing memories from database: {e}")

    memories.update(fs.list_files())
    return sorted(list(memories))
