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
Memory Server - Core memory management operations for Synapse.

This server handles all memory-related operations including reading, writing,
listing, and managing memory files in the Synapse system.
"""

from fastmcp import FastMCP
from typing import List, Optional
import os

# Local imports
from synapse.utils.helpers import get_db_instance, MemoryFileSystem

# Create Memory Server instance  
memory_server = FastMCP("Memory Synapse")

def get_memory_dir() -> str:
    """Get the configured memory directory."""
    from synapse.core.config import get_config
    return get_config("memory_dir", "memories")

@memory_server.tool()
def get_memory_list() -> List[str]:
    """Get a list of all memory files in Synapse."""
    try:
        db = get_db_instance()
        return db.list_memories()
    except Exception as e:
        return [f"Error listing memories: {str(e)}"]

@memory_server.tool()
def read_memory(file_name: str) -> str:
    """Read memory content from database or file system.
    
    Args:
        file_name: Name of the memory file to read
        
    Returns:
        Content of the memory file
    """
    try:
        # Try database first
        db = get_db_instance()
        content = db.load_memory(file_name)
        
        if content is not None:
            return content
            
        # Fallback to file system
        memory_dir = get_memory_dir()
        file_manager = MemoryFileSystem(memory_dir)
        content = file_manager.read_file(file_name)
        
        if content is not None:
            # Sync to database for future access
            db.save_memory(file_name, content)
            return content
            
        return f"Memory file '{file_name}' not found"
        
    except Exception as e:
        return f"Error reading memory '{file_name}': {str(e)}"

@memory_server.tool()
def write_memory(file_name: str, content: str) -> str:
    """Write memory content to database and file system.
    
    Args:
        file_name: Name of the memory file to write
        content: Content to write to the memory file
        
    Returns:
        Status message
    """
    try:
        # Save to database
        db = get_db_instance()
        success = db.save_memory(file_name, content)
        
        if not success:
            return f"Failed to save memory '{file_name}' to database"
            
        # Also save to file system for backup
        memory_dir = get_memory_dir()
        file_manager = MemoryFileSystem(memory_dir)
        file_manager.write_file(file_name, content)
        
        return f"Successfully saved memory '{file_name}'"
        
    except Exception as e:
        return f"Error writing memory '{file_name}': {str(e)}"

@memory_server.tool()  
def delete_memory(file_name: str) -> str:
    """Delete a memory file from database and file system.
    
    Args:
        file_name: Name of the memory file to delete
        
    Returns:
        Status message
    """
    try:
        # Delete from database
        db = get_db_instance()
        db_success = db.delete_memory(file_name)
        
        # Delete from file system
        memory_dir = get_memory_dir()
        file_manager = MemoryFileSystem(memory_dir)
        file_path = file_manager.memory_dir / file_name
        fs_success = False
        
        if file_path.exists():
            file_path.unlink()
            fs_success = True
            
        if db_success or fs_success:
            return f"Successfully deleted memory '{file_name}'"
        else:
            return f"Memory file '{file_name}' not found"
            
    except Exception as e:
        return f"Error deleting memory '{file_name}': {str(e)}"

@memory_server.tool()
def search_memories(query: str) -> List[str]:
    """Search through memory contents for a query string.
    
    Args:
        query: Search term to look for in memory content
        
    Returns:
        List of memory files containing the query
    """
    try:
        db = get_db_instance()
        results = db.search_memories(query)
        
        if results:
            return [f"{result['filename']}: {result.get('match_snippet', '')}" for result in results]
        else:
            return [f"No memories found containing '{query}'"]
            
    except Exception as e:
        return [f"Error searching memories: {str(e)}"]

# Export the server
__all__ = ["memory_server"] 