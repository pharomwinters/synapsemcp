# Synapse Server Architecture

## Overview

The Synapse project uses a **Hard-Coded Tool Architecture** with **Server Composition** for reliable and predictable tool management.

### Key Benefits
- **Reliability**: Hard-coded tools ensure consistent behavior across environments
- **Modularity**: Each server handles a specific domain (memory, documents, templates, config, guides)
- **Performance**: No runtime discovery overhead, immediate tool availability
- **Maintainability**: Individual servers can be developed, tested, and updated independently
- **Predictability**: All tools are registered at startup with known capabilities

## Architecture Diagram

```
Synapse MCP Platform (Main)
├── Memory Synapse      - Core memory operations (CRUD)
├── Document Synapse    - Document processing & management
├── Template Synapse    - Template generation & analysis
├── Config Synapse      - Configuration & system management
└── Guide Synapse       - Documentation & help resources
```

## Server Composition Structure

```
synapse/
├── mcp_instance.py            # Main composed server
├── servers/                   # Individual specialized servers
│   ├── memory_server.py      # Memory operations
│   ├── document_server.py    # Document processing & management
│   ├── template_server.py    # Template generation
│   ├── config_server.py      # Configuration management
│   └── guide_server.py       # Documentation & guides
├── startup_scripts/          # Cross-platform startup automation
├── docs/                     # Comprehensive documentation
├── duckdb_db.py             # DuckDB database implementation
├── mariadb_server_manager.py # Embedded MariaDB management
└── utils.py                  # Database and utility functions
```

## Server Responsibilities

### Memory Synapse (`memory_server.py`)
**Purpose**: Core memory management operations

**Tools Provided**:
- `get_memory_list()` - List all memory files
- `read_memory(file_name)` - Read memory content
- `write_memory(file_name, content)` - Write memory content
- `delete_memory(file_name)` - Delete memory files
- `search_memories(query)` - Search memory content

**Key Features**:
- Database integration (DuckDB/MariaDB/SQLite)
- File system fallback
- Automatic synchronization between database and filesystem

### Document Synapse (`document_server.py`)
**Purpose**: Document processing and management operations

**Tools Provided**:
- `store_document(file_path, document_name, tags)` - Store and process documents
- `get_document(document_name)` - Retrieve document information
- `list_documents(tag_filter)` - List all documents with optional filtering
- `search_documents(query, search_content)` - Search document names and content
- `delete_document(document_name, delete_file)` - Delete documents
- `get_supported_formats()` - Get supported file format information
- `add_document_tags(document_name, tags)` - Add tags to documents

**Key Features**:
- Multi-format document support (PDF, Office, LibreOffice, plain text)
- Text extraction for searchability
- Tag-based organization
- Full-text search capabilities
- Metadata management
- File hash verification

### Template Synapse (`template_server.py`)
**Purpose**: Template generation and project analysis

**Tools Provided**:
- `generate_synapse_template(file_name)` - Generate templates
- `list_available_templates()` - List template library
- `analyze_project_summary(summary)` - Project analysis
- `create_project_structure(project_name)` - Complete project setup

**Key Features**:
- Pre-built template library
- Dynamic project analysis
- Template customization
- Project scaffolding

### Config Synapse (`config_server.py`)
**Purpose**: Configuration and system management

**Tools Provided**:
- `get_configuration(key)` - Get config settings
- `get_environment_info()` - System information
- `validate_configuration()` - Config validation
- `get_database_status()` - Database connectivity
- `get_system_stats()` - System resource usage

**Key Features**:
- Multi-environment support (dev/test/prod)
- Database configuration management
- System health monitoring
- Configuration validation

### Guide Synapse (`guide_server.py`)
**Purpose**: Documentation and help resources

**Tools Provided**:
- `get_synapse_structure()` - File structure guide
- `get_guide(guide_name)` - Specific guides
- `list_available_guides()` - Available documentation
- `search_guides(query)` - Search documentation
- `get_quick_start()` - Quick start guide
- `get_troubleshooting()` - Troubleshooting help

**Resources Provided**:
- `synapse_guide://{section}` - Dynamic guide access

**Key Features**:
- Comprehensive documentation system
- Context-sensitive help
- Troubleshooting guides
- Quick start resources

## Database Configuration

### Multi-Database Support
Synapse supports three database backends with automatic selection:

- **DuckDB** - High-performance analytical database (default)
- **MariaDB** - Production-ready relational database with embedded server
- **SQLite** - Lightweight database for backward compatibility

### Environment Variables
Configuration can be controlled via environment variables:

- `SYNAPSE_ENV` - Environment (development/test/production)
- `SYNAPSE_DB_TYPE` - Database type (duckdb/mariadb/sqlite/auto)
- `SYNAPSE_DUCKDB_DB_PATH` - DuckDB database path
- `SYNAPSE_SQLITE_DB_PATH` - SQLite database path (legacy)
- `SYNAPSE_MARIADB_HOST` - MariaDB host
- `SYNAPSE_MARIADB_PORT` - MariaDB port
- `SYNAPSE_MARIADB_USER` - MariaDB user
- `SYNAPSE_MARIADB_PASSWORD` - MariaDB password
- `SYNAPSE_MARIADB_DATABASE` - MariaDB database name

### Configuration Files
Environment-specific JSON configuration files:
- `config.dev.json` - Development (DuckDB default)
- `config.dev.mariadb.json` - Development with MariaDB
- `config.test.json` - Testing environment
- `config.prod.json` - Production environment

## Tool Naming Convention

Tools are prefixed by their server when mounted:
- **memory_*** - Memory operations (memory_read_memory, memory_write_memory)
- **document_*** - Document operations (document_store_document, document_search_documents)
- **template_*** - Template operations (template_generate_synapse_template)
- **config_*** - Configuration operations (config_get_configuration)
- **guide_*** - Documentation operations (guide_get_guide)

## Composition Benefits

### 1. Separation of Concerns
Each server handles a specific domain, making the codebase more organized and maintainable.

### 2. Independent Development
Servers can be developed, tested, and deployed independently without affecting others.

### 3. Scalability
New servers can be added to handle additional domains (analysis, workflows, etc.).

### 4. Tool Organization
Tools are logically grouped by prefix, making them easier to discover and use.

### 5. Plugin Architecture
The auto-discovery system enables a plugin ecosystem for extending functionality.

## Future Extensions

The architecture supports easy extension with additional servers:

```
Synapse MCP Platform (Future)
├── Memory Synapse      - Core memory operations
├── Template Synapse    - Template generation & analysis
├── Config Synapse      - Configuration & system management
├── Guide Synapse       - Documentation & help resources
├── Analysis Synapse    - Data analysis workflows
├── Document Synapse    - Pharom XML integration
├── Journal Synapse     - Personal reflection & tracking
└── Creative Synapse    - Writing & creative workflows
```

## Development Guidelines

### Adding New Servers
1. Create new server file in `servers/` directory
2. Follow naming convention: `{domain}_server.py`
3. Use FastMCP for server creation
4. Export server instance in `__all__`
5. Mount in `mcp_instance.py` with appropriate prefix

### Adding New Tools
1. Use `@mcp_tool` decorator for auto-discovery
2. Place in `tools/` for general tools or `plugins/` for plugin tools
3. Follow naming conventions for parameters and returns
4. Include comprehensive docstrings

### Testing Servers
Each server can be run independently for testing:
```bash
python servers/memory_server.py
python servers/template_server.py
python servers/config_server.py
python servers/guide_server.py
```

## Configuration

### Environment Variables
- `SYNAPSE_ENV` - Environment (development/testing/production)
- `SYNAPSE_AUTO_DISCOVER` - Enable auto-discovery on startup
- `SYNAPSE_DB_TYPE` - Database type (duckdb/mariadb/sqlite)
- `SYNAPSE_DUCKDB_DB_PATH` - DuckDB database path (default)
- `SYNAPSE_SQLITE_DB_PATH` - SQLite database path (legacy)
- `SYNAPSE_MARIADB_*` - MariaDB connection settings

### Configuration Files
- `config.dev.json` - Development settings
- `config.test.json` - Testing settings
- `config.prod.json` - Production settings
- `config.local.json` - Local overrides (not in version control)

**Note:** As of the latest version, Synapse has upgraded from SQLite to DuckDB as the default database for improved performance and analytical capabilities. SQLite remains supported for legacy compatibility.

This architecture provides a robust foundation for the Synapse system while maintaining flexibility for future growth. 