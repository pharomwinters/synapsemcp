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
    from utils import get_db_instance, MemoryFileSystem, write_memory_to_db_and_file
    from config import config
    from typing import List
    
    def get_memory_dir() -> str:
        """Get the configured memory directory."""
        return config.get("memory_dir", "memories")

    @mcp.tool()
    def memory_get_memory_list() -> List[str]:
        """Get a list of all memory files in Synapse."""
        try:
            db = get_db_instance()
            return db.list_memories()
        except Exception as e:
            logger.error(f"Error listing memories: {e}")
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
            logger.debug(f"Attempting to read memory: {file_name}")
            
            # Try database first
            db = get_db_instance()
            content = db.load_memory(file_name)
            
            if content is not None:
                logger.debug(f"Successfully read {file_name} from database")
                return content
                
            # Fallback to file system
            memory_dir = get_memory_dir()
            file_manager = MemoryFileSystem(memory_dir)
            content = file_manager.read_file(file_name)
            
            if content is not None:
                # Sync to database for future access
                db.save_memory(file_name, content)
                logger.debug(f"Successfully read {file_name} from file system and synced to database")
                return content
                
            return f"❌ Memory file '{file_name}' not found"
            
        except Exception as e:
            error_msg = f"Error reading memory '{file_name}': {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"

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
            logger.info(f"Attempting to write memory: {file_name}")
            
            # Get memory directory from config
            memory_dir = get_memory_dir()
            
            # Use the improved write function
            success = write_memory_to_db_and_file(file_name, content, memory_dir)
            
            if success:
                logger.info(f"Successfully saved memory '{file_name}'")
                return f"✅ Successfully saved memory '{file_name}'"
            else:
                logger.error(f"Failed to save memory '{file_name}'")
                return f"❌ Failed to save memory '{file_name}' - check logs for details"
                
        except Exception as e:
            error_msg = f"Error writing memory '{file_name}': {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"

    @mcp.tool()
    def memory_delete_memory(file_name: str) -> str:
        """Delete a memory file from database and file system.
        
        Args:
            file_name: Name of the memory file to delete
            
        Returns:
            Status message
        """
        try:
            logger.info(f"Attempting to delete memory: {file_name}")
            
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
                logger.debug(f"Deleted {file_name} from file system")
                
            if db_success or fs_success:
                logger.info(f"Successfully deleted memory '{file_name}'")
                return f"✅ Successfully deleted memory '{file_name}'"
            else:
                return f"❌ Memory file '{file_name}' not found"
                
        except Exception as e:
            error_msg = f"Error deleting memory '{file_name}': {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"

    @mcp.tool()
    def memory_search_memories(query: str) -> List[str]:
        """Search through memory contents for a query string.
        
        Args:
            query: Search term to look for in memory content
            
        Returns:
            List of memory files containing the query
        """
        try:
            logger.debug(f"Searching memories for: {query}")
            
            db = get_db_instance()
            results = db.search_memories(query)
            
            if results:
                search_results = []
                for result in results:
                    # Truncate content for display
                    content_preview = result.get('content', '')[:100]
                    if len(content_preview) == 100:
                        content_preview += "..."
                    search_results.append(f"📄 {result['filename']}: {content_preview}")
                
                logger.debug(f"Found {len(results)} memories containing '{query}'")
                return search_results
            else:
                return [f"🔍 No memories found containing '{query}'"]
                
        except Exception as e:
            error_msg = f"Error searching memories: {str(e)}"
            logger.error(error_msg)
            return [f"❌ {error_msg}"]
    
    logger.info("✅ Memory tools registered!")
    
    # Document management tools
    try:
        from servers.document_server import (
            store_document as _store_document,
            get_document as _get_document,
            list_documents as _list_documents,
            search_documents as _search_documents,
            delete_document as _delete_document,
            get_supported_formats as _get_supported_formats,
            add_document_tags as _add_document_tags
        )
        
        @mcp.tool()
        def documents_store_document(file_path: str, document_name: str = None, tags: List[str] = None) -> str:
            """Store a document in the Synapse document management system.
            
            Args:
                file_path: Full path to the document file to store
                document_name: Optional custom name for the document (defaults to filename)
                tags: Optional list of tags to associate with the document
            """
            try:
                result = _store_document(file_path, document_name, tags)
                if result["success"]:
                    return f"📄 Document stored successfully: {result['document_name']}\n" \
                           f"Type: {result['file_type']}\n" \
                           f"Size: {result['file_size']} bytes\n" \
                           f"Preview: {result['text_preview']}"
                else:
                    return f"❌ Error: {result['error']}"
            except Exception as e:
                return f"❌ Error storing document: {str(e)}"
        
        @mcp.tool() 
        def documents_get_document(document_name: str) -> str:
            """Retrieve document metadata and content.
            
            Args:
                document_name: Name of the document to retrieve
            """
            try:
                result = _get_document(document_name)
                if result["success"]:
                    doc = result["document"]
                    return f"📄 {doc['document_name']}\n" \
                           f"Original: {doc['original_filename']}\n" \
                           f"Type: {doc['file_type']}\n" \
                           f"Size: {doc['file_size']} bytes\n" \
                           f"Tags: {', '.join(doc['tags'])}\n" \
                           f"Created: {doc['created_at']}\n" \
                           f"Text: {doc['extracted_text'][:500]}{'...' if len(doc['extracted_text']) > 500 else ''}"
                else:
                    return f"❌ Error: {result['error']}"
            except Exception as e:
                return f"❌ Error retrieving document: {str(e)}"
        
        @mcp.tool()
        def documents_list_documents(tag_filter: str = None) -> str:
            """List all stored documents.
            
            Args:
                tag_filter: Optional tag to filter documents by
            """
            try:
                result = _list_documents(tag_filter)
                if result["success"]:
                    if result["count"] == 0:
                        return "📁 No documents found"
                    
                    docs_list = []
                    for doc in result["documents"]:
                        tags_str = f" [{', '.join(doc['tags'])}]" if doc['tags'] else ""
                        docs_list.append(f"📄 {doc['document_name']}{tags_str} - {doc['file_type']}")
                    
                    return f"📁 Documents ({result['count']}):\n" + "\n".join(docs_list)
                else:
                    return f"❌ Error: {result['error']}"
            except Exception as e:
                return f"❌ Error listing documents: {str(e)}"
        
        @mcp.tool()
        def documents_search_documents(query: str, search_content: bool = True) -> str:
            """Search documents by name, tags, or content.
            
            Args:
                query: Search query string
                search_content: Whether to search document content (extracted text)
            """
            try:
                result = _search_documents(query, search_content)
                if result["success"]:
                    if result["count"] == 0:
                        return f"🔍 No documents found matching '{query}'"
                    
                    matches = []
                    for doc in result["matches"]:
                        match_info = f"Score: {doc['match_score']}, Reasons: {', '.join(doc['match_reasons'])}"
                        matches.append(f"📄 {doc['document_name']} ({match_info})\n   Preview: {doc['content_preview']}")
                    
                    return f"🔍 Search results for '{query}' ({result['count']}):\n" + "\n\n".join(matches)
                else:
                    return f"❌ Error: {result['error']}"
            except Exception as e:
                return f"❌ Error searching documents: {str(e)}"
        
        @mcp.tool()
        def documents_delete_document(document_name: str, delete_file: bool = False) -> str:
            """Delete a document from the system.
            
            Args:
                document_name: Name of the document to delete
                delete_file: Whether to also delete the stored file
            """
            try:
                result = _delete_document(document_name, delete_file)
                if result["success"]:
                    file_status = "and file" if result["file_deleted"] else "(metadata only)"
                    return f"🗑️ Document '{document_name}' deleted {file_status}"
                else:
                    return f"❌ Error: {result['error']}"
            except Exception as e:
                return f"❌ Error deleting document: {str(e)}"
        
        @mcp.tool()
        def documents_get_supported_formats() -> str:
            """Get list of supported document formats and their availability."""
            try:
                result = _get_supported_formats()
                if result["success"]:
                    formats = []
                    for ext, desc in result["supported_extensions"].items():
                        formats.append(f"{ext}: {desc}")
                    
                    capabilities = []
                    for capability, available in result["processing_capabilities"].items():
                        status = "✅" if available else "❌"
                        capabilities.append(f"{status} {capability}")
                    
                    missing = "\n".join(result["missing_dependencies"]) if result["missing_dependencies"] else "All dependencies available"
                    
                    return f"📄 Supported Formats:\n" + "\n".join(formats) + \
                           f"\n\n🔧 Processing Capabilities:\n" + "\n".join(capabilities) + \
                           f"\n\n📦 Missing Dependencies:\n{missing}"
                else:
                    return f"❌ Error: {result['error']}"
            except Exception as e:
                return f"❌ Error getting supported formats: {str(e)}"
        
        @mcp.tool()
        def documents_add_tags(document_name: str, tags: List[str]) -> str:
            """Add tags to an existing document.
            
            Args:
                document_name: Name of the document
                tags: List of tags to add
            """
            try:
                result = _add_document_tags(document_name, tags)
                if result["success"]:
                    added = ", ".join(result["added_tags"]) if result["added_tags"] else "none (already present)"
                    all_tags = ", ".join(result["all_tags"]) if result["all_tags"] else "none"
                    return f"🏷️ Tags added to '{document_name}'\n" \
                           f"Added: {added}\n" \
                           f"All tags: {all_tags}"
                else:
                    return f"❌ Error: {result['error']}"
            except Exception as e:
                return f"❌ Error adding tags: {str(e)}"
        
        logger.info("✅ Document management tools registered!")
        
    except ImportError as e:
        logger.warning(f"⚠️ Could not import document management tools: {e}")
    except Exception as e:
        logger.error(f"❌ Failed to register document management tools: {e}")
    
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
        "documents_store_document",
        "documents_get_document",
        "documents_list_documents",
        "documents_search_documents",
        "documents_delete_document",
        "documents_get_supported_formats",
        "documents_add_tags",
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
        db_type: Type of database ('duckdb', 'sqlite', 'mariadb')
        db_path: Optional database path for DuckDB/SQLite or connection details
        
    Returns:
        Status message confirming the database configuration
    """
    try:
        import os
        
        # Validate database type
        valid_types = ['duckdb', 'sqlite', 'mariadb']
        if db_type.lower() not in valid_types:
            return f"❌ Invalid database type '{db_type}'. Valid types: {', '.join(valid_types)}"
        
        # Set environment variables to override config
        os.environ["SYNAPSE_DB_TYPE"] = db_type.lower()
        
        if db_path:
            if db_type.lower() == 'duckdb':
                os.environ["SYNAPSE_DUCKDB_DB_PATH"] = db_path
            elif db_type.lower() == 'sqlite':
                os.environ["SYNAPSE_SQLITE_DB_PATH"] = db_path
            elif db_type.lower() == 'mariadb':
                return f"ℹ️ For MariaDB, please set individual environment variables: SYNAPSE_MARIADB_HOST, SYNAPSE_MARIADB_USER, etc."
        
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
**Type**: {db_config.get('type', 'duckdb')}
**Memory Directory**: {memory_dir}

**Current Database Settings**:
"""
        
        # Add specific database settings
        if db_config.get('type') == 'duckdb':
            info += f"• DuckDB Path: {db_config.get('db_path', 'synapse.duckdb')}\n"
        elif db_config.get('type') == 'sqlite':
            info += f"• SQLite Path: {db_config.get('db_path', 'synapse.db')}\n"
        elif db_config.get('type') == 'mariadb':
            info += f"• Host: {db_config.get('host', 'localhost')}\n"
            info += f"• Port: {db_config.get('port', 3306)}\n"
            info += f"• Database: {db_config.get('database', 'synapse')}\n"
            info += f"• User: {db_config.get('user', 'synapse_user')}\n"
        
        info += """
**Supported Types**:
• duckdb - DuckDB database (default)
• sqlite - Local SQLite database
• mariadb - MariaDB/MySQL database

**Usage**: Use config_set_database_type to change database backend
**Environment Variables**: SYNAPSE_DB_TYPE, SYNAPSE_DUCKDB_DB_PATH, SYNAPSE_SQLITE_DB_PATH, etc.
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
• Document Server - Document storage and text extraction (PDF, Office, LibreOffice)
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