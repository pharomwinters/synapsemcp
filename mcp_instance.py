# mcp_instance.py - Composed Synapse MCP Server
"""
Main Synapse MCP Server with Hard-Coded Tools.

This module creates a unified MCP server with all tools explicitly defined:
- Memory Server: Core memory management
- Template Server: Template generation and analysis  
- Config Server: Configuration and system management
- Guide Server: Documentation and help resources

All tools are hard-coded for reliability and predictability.
Tool categories:
- memory_* tools for memory management
- Meta tools for system information and introspection
- Advanced tools for project analysis and file operations
"""

import os
import logging
from fastmcp import FastMCP
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create main MCP instance
mcp = FastMCP("Synapse MCP Platform")

logger.info("Starting Synapse MCP server initialization...")

# Import and define core tools
logger.info("Creating Synapse tools...")
try:
    # Import utility functions directly
    from utils import get_db_instance, MemoryFileSystem
    from typing import List
    
    def get_memory_dir() -> str:
        """Get the configured memory directory."""
        from config import get_config
        return get_config("memory_dir", "memories")

    @mcp.tool()
    def memory_get_memory_list() -> List[str]:
        """Get a list of all memory files in Synapse."""
        try:
            db = get_db_instance()
            return db.list_memories()
        except Exception as e:
            return [f"Error listing memories: {str(e)}"]

    @mcp.tool()
    def memory_read_memory(file_name: str) -> str:
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

    @mcp.tool()
    def memory_write_memory(file_name: str, content: str) -> str:
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

    @mcp.tool()
    def memory_delete_memory(file_name: str) -> str:
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

    @mcp.tool()
    def memory_search_memories(query: str) -> List[str]:
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
    
    logger.info("✅ Memory tools registered!")
    
except ImportError as e:
    logger.error(f"❌ Failed to import dependencies: {e}")
    logger.info("Creating basic MCP server instead...")
except Exception as e:
    logger.error(f"❌ Failed to create tools: {e}")
    logger.info("Creating basic MCP server instead...")

# Meta-tools for system information
@mcp.tool()
def list_available_tools() -> str:
    """List all available tools in the Synapse system."""
    tools = [
        "memory_get_memory_list",
        "memory_read_memory", 
        "memory_write_memory",
        "memory_delete_memory",
        "memory_search_memories",
        "config_set_database_type",
        "config_get_database_info",
        "list_available_tools",
        "get_synapse_info",
        "analyze_project_structure",
        "analyze_synapse_health",
        "compare_synapse_templates", 
        "generate_file_checksum",
        "search_text_in_files"
    ]
    return f"Available tools ({len(tools)}):\n" + "\n".join(f"• {tool}" for tool in sorted(tools))

@mcp.tool()
def config_set_database_type(db_type: str, db_path: str = "") -> str:
    """Configure the database type for Synapse memory storage.
    
    Args:
        db_type: Type of database ('sqlite', 'mariadb')
        db_path: Optional database path for SQLite or connection details
        
    Returns:
        Status message confirming the database configuration
    """
    try:
        import os
        
        # Validate database type
        valid_types = ['sqlite', 'mariadb']
        if db_type.lower() not in valid_types:
            return f"Invalid database type '{db_type}'. Valid types: {', '.join(valid_types)}"
        
        # Set environment variables to override config
        os.environ["SYNAPSE_DB_TYPE"] = db_type.lower()
        
        if db_path:
            if db_type.lower() == 'sqlite':
                os.environ["SYNAPSE_SQLITE_DB_PATH"] = db_path
            elif db_type.lower() == 'mariadb':
                return f"For MariaDB, please set individual environment variables: SYNAPSE_MARIADB_HOST, SYNAPSE_MARIADB_USER, etc."
        
        # Reload config to pick up changes
        from config import load_config
        load_config()
        
        return f"✅ Database type set to '{db_type}'" + (f" with path: {db_path}" if db_path else "") + "\n⚠️ Restart may be required for changes to take effect."
        
    except Exception as e:
        return f"❌ Error setting database type: {str(e)}"

@mcp.tool()
def config_get_database_info() -> str:
    """Get current database configuration information.
    
    Returns:
        Current database type and connection details
    """
    try:
        from config import get_config, get_database_config
        
        db_config = get_database_config()
        memory_dir = get_config("memory_dir", "memories")
        environment = get_config("environment", "development")
        
        info = f"""🗄️ **Database Configuration**
        
**Environment**: {environment}
**Type**: {db_config.get('type', 'sqlite')}
**Memory Directory**: {memory_dir}

**Current Database Settings**:
"""
        
        # Add specific database settings
        if db_config.get('type') == 'sqlite':
            info += f"• SQLite Path: {db_config.get('db_path', 'synapse.db')}\n"
        elif db_config.get('type') == 'mariadb':
            info += f"• Host: {db_config.get('host', 'localhost')}\n"
            info += f"• Port: {db_config.get('port', 3306)}\n"
            info += f"• Database: {db_config.get('database', 'synapse')}\n"
            info += f"• User: {db_config.get('user', 'synapse_user')}\n"
        
        info += """
**Supported Types**:
• sqlite - Local SQLite database (default)
• mariadb - MariaDB/MySQL database

**Usage**: Use config_set_database_type to change database backend
**Environment Variables**: SYNAPSE_DB_TYPE, SYNAPSE_SQLITE_DB_PATH, etc.
        """
        
        return info.strip()
        
    except Exception as e:
        return f"❌ Error getting database info: {str(e)}"

@mcp.tool()
def get_synapse_info() -> str:
    """Get information about the Synapse system."""
    return """🧠 Synapse - AI Memory Bank & Workflow Management System

**Architecture**: Hard-Coded Tool Registration
**Components**:
• Memory Server - Core memory management (CRUD operations)
• Template Server - Template generation and project analysis  
• Config Server - Configuration and system management
• Guide Server - Documentation and help system

**Tools**: All tools are explicitly defined for maximum reliability
**Usage**: Use the list_available_tools command to see all available operations.
"""

# Hard-coded advanced tools registration
try:
    from tools.advanced_tools import (
        analyze_project_structure as _analyze_project_structure,
        analyze_synapse_health as _analyze_synapse_health, 
        compare_synapse_templates as _compare_synapse_templates,
        generate_file_checksum as _generate_file_checksum,
        search_text_in_files as _search_text_in_files
    )
    
    # Register advanced tools directly with FastMCP
    mcp.tool(name="analyze_project_structure")(_analyze_project_structure)
    mcp.tool(name="analyze_synapse_health")(_analyze_synapse_health)
    mcp.tool(name="compare_synapse_templates")(_compare_synapse_templates)
    mcp.tool(name="generate_file_checksum")(_generate_file_checksum)
    mcp.tool(name="search_text_in_files")(_search_text_in_files)
    
    logger.info("✅ Advanced tools registered!")
    
except ImportError as e:
    logger.warning(f"⚠️ Could not import advanced tools: {e}")
except Exception as e:
    logger.error(f"❌ Failed to register advanced tools: {e}")

logger.info("🧠 Synapse MCP Platform ready with hard-coded tools")
logger.info("✅ Server composition complete!")

# Export the configured MCP instance
__all__ = ["mcp"]
