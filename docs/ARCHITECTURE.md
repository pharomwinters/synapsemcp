# Synapse Server Architecture

## Overview

The Synapse project has been refactored to use **Server Composition** architecture with **Auto-Discovery** capabilities for scalable tool management.

### Key Benefits
- **Modularity**: Each server handles a specific domain (memory, templates, config, guides)
- **Scalability**: New servers can be added without modifying existing code
- **Maintainability**: Individual servers can be developed, tested, and updated independently
- **Auto-Discovery**: Tools can be dynamically loaded from plugins and extensions

## Architecture Diagram

```
Synapse MCP Platform (Main)
├── Memory Synapse      - Core memory operations (CRUD)
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
│   ├── template_server.py    # Template generation
│   ├── config_server.py      # Configuration management
│   └── guide_server.py       # Documentation & guides
├── tools/                    # Auto-discoverable tools
├── plugins/                  # Plugin-style tools
└── utils.py                  # Auto-discovery utilities
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
- Database integration (SQLite/MariaDB)
- File system fallback
- Automatic synchronization between database and filesystem

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

## Auto-Discovery System

### Overview
The auto-discovery system allows new tools to be automatically detected and registered without modifying the main server code.

### Discovery Patterns
- `tools/*.py` - General purpose tools
- `plugins/*_plugin.py` - Plugin-style tools

### Tool Registration
Tools are registered using the `@mcp_tool` decorator:

```python
from utils import mcp_tool

@mcp_tool
def my_custom_tool(data: str) -> str:
    """My custom analysis tool."""
    return f"Processed: {data}"
```

### Auto-Discovery Configuration
```bash
# Enable auto-discovery on startup
export SYNAPSE_AUTO_DISCOVER=true
python main.py
```

### Manual Discovery
```python
# Trigger discovery manually
result = await discover_tools(verbose=True)
```

## Tool Naming Convention

Tools are prefixed by their server when mounted:
- **memory_*** - Memory operations (memory_read_memory, memory_write_memory)
- **templates_*** - Template operations (templates_generate_synapse_template)
- **config_*** - Configuration operations (config_get_configuration)
- **guides_*** - Documentation operations (guides_get_guide)

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
- `SYNAPSE_DB_TYPE` - Database type (sqlite/mariadb)
- `SYNAPSE_SQLITE_DB_PATH` - SQLite database path
- `SYNAPSE_MARIADB_*` - MariaDB connection settings

### Configuration Files
- `config.dev.json` - Development settings
- `config.test.json` - Testing settings
- `config.prod.json` - Production settings
- `config.local.json` - Local overrides (not in version control)

This architecture provides a robust foundation for the Synapse system while maintaining flexibility for future growth. 