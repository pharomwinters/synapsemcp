"""
Constants for Synapse.

This module contains application-wide constants that are used throughout
the Synapse system. Having constants centralized makes them easier to
maintain and update.
"""

# File extensions
MEMORY_FILE_EXTENSION = ".md"
TEMPLATE_FILE_EXTENSION = ".md"

# Encoding
DEFAULT_ENCODING = "utf-8"

# Database types
SUPPORTED_DB_TYPES = ["sqlite", "duckdb", "mariadb", "mysql"]

# Default directories
DEFAULT_MEMORY_DIR = "memories"
DEFAULT_DOCUMENTS_DIR = "documents"
DEFAULT_TEMPLATES_DIR = "templates"
DEFAULT_CONFIG_DIR = "config"
DEFAULT_DATA_DIR = "data"

# File size limits (in bytes)
MAX_MEMORY_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_DOCUMENT_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# MCP related constants
MCP_TOOL_PREFIX = "synapse_"
MCP_SERVER_NAME = "Synapse MCP Platform"

# Logging
DEFAULT_LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Version
VERSION_MAJOR = 2
VERSION_MINOR = 0
VERSION_PATCH = 0

# Environment names
ENV_DEVELOPMENT = "development"
ENV_TESTING = "testing"
ENV_PRODUCTION = "production"

# Default ports
DEFAULT_HTTP_PORT = 8000
DEFAULT_MARIADB_PORT = 3306

# Template names
TEMPLATE_PROJECT_BRIEF = "projectbrief.md"
TEMPLATE_SYNAPSE_INSTRUCTIONS = "synapse_instructions.md"
TEMPLATE_TECH_CONTEXT = "tech_context.md"
TEMPLATE_SYSTEM_PATTERNS = "system_patterns.md" 