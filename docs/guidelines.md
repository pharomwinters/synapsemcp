# Synapse Development Guidelines

This document provides essential information for developers working on the Synapse project. It includes build/configuration instructions, testing information, and development guidelines.

## Quick Start

### Prerequisites
- Python 3.12+
- Virtual environment (recommended)
- Git

### Setup
```bash
# Clone repository
git clone <repository-url>
cd synapse

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Unix/macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Configuration

The Synapse application uses environment-based configuration. Configuration files:

- `config.dev.json` - Development settings
- `config.test.json` - Testing settings  
- `config.prod.json` - Production settings
- `config.local.json` - Local overrides (not in version control)

Environment variables:
- `SYNAPSE_ENV` - Environment (development/testing/production)
- `SYNAPSE_AUTO_DISCOVER` - Enable auto-discovery on startup
- `SYNAPSE_DB_TYPE` - Database type (duckdb/sqlite/mariadb)
- `SYNAPSE_DUCKDB_DB_PATH` - DuckDB database path (default)
- `SYNAPSE_SQLITE_DB_PATH` - SQLite database path (legacy)

## Testing

### Running Tests
```bash
# Run all tests
cd tests
python -m unittest discover

# Run specific test
python test_database.py

# Test with coverage (if installed)
coverage run -m unittest discover
coverage report
```

### Test Structure
```
tests/
├── test_config.py           # Configuration tests
├── test_database.py         # Database tests
├── test_memory_server.py    # Memory server tests
├── test_template_server.py  # Template server tests
├── test_config_server.py    # Config server tests
└── test_guide_server.py     # Guide server tests
```

### Example Test
```python
import unittest
from pathlib import Path
from duckdb_db import DuckDBDatabase

class TestDuckDBDatabase(unittest.TestCase):
    def setUp(self):
        self.db_path = Path("test_synapse.duckdb")
        self.db = DuckDBDatabase(str(self.db_path))
        self.db.initialize_database()

    def test_save_and_load_memory(self):
        # Test implementation
        pass

    def tearDown(self):
        self.db.close()
```

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Include docstrings for public functions
- Keep functions focused and atomic

### Architecture
The Synapse project follows a modular architecture:

- `main.py`: Application entry point
- `mcp_instance.py`: Sets up the MCP server and defines tools for interacting with Synapse
- `config.py`: Configuration management system
- `servers/`: Individual specialized servers (memory, templates, config, guides)
- `utils.py`: Utility functions and auto-discovery system
- `base.py`: Abstract base classes
- `duckdb_db.py`, `sqlite_db.py`, `mariadb.py`: Database implementations

### Adding New Features

#### Adding a New Server
1. Create new server file in `servers/` directory
2. Follow naming convention: `{domain}_server.py`
3. Use FastMCP for server creation
4. Define tools with `@server.tool()` decorators
5. Export server instance in `__all__`
6. Mount in `mcp_instance.py` with appropriate prefix
7. Add tests in `tests/`
8. Update documentation

#### Adding New Tools
1. Use `@mcp_tool` decorator for auto-discovery
2. Place in `tools/` for general tools or `plugins/` for plugin tools
3. Follow naming conventions for parameters and returns
4. Include comprehensive docstrings
5. Add tests for the new functionality

### Database Development

#### DuckDB (Default)
- Used for most deployments due to high performance
- Database file is created automatically
- No additional setup required
- Optimized for analytical workloads

#### SQLite (Legacy)
- Available for compatibility with existing setups
- Database file is created automatically
- Simple file-based database

#### MariaDB (Production)
- Requires MariaDB server installation
- Configuration through environment variables or config files
- Better for production environments

#### Adding Database Operations
1. Add method to base class (`base.py`)
2. Implement in DuckDB (`duckdb_db.py`), SQLite (`sqlite_db.py`) and MariaDB (`mariadb.py`)
3. Test all implementations
4. Update utilities as needed

## Deployment

### Development
```bash
export SYNAPSE_ENV=development
python main.py
```

### Production
```bash
export SYNAPSE_ENV=production
export SYNAPSE_AUTO_DISCOVER=true
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker (Future)
```bash
# Build image
docker build -t synapse .

# Run container
docker run -p 8000:8000 -e SYNAPSE_ENV=production synapse
```

## Troubleshooting

### Common Issues

**Database connection failed**
- Check database configuration in config files
- Verify database server is running (MariaDB)
- Check file permissions (DuckDB/SQLite)

**Import errors**
- Verify virtual environment is activated
- Check all dependencies are installed
- Verify Python version compatibility

**Auto-discovery not working**
- Check `SYNAPSE_AUTO_DISCOVER` environment variable
- Verify tools are decorated with `@mcp_tool`
- Check file patterns and directories

**Configuration errors**
- Validate JSON syntax in config files
- Check environment variable names
- Verify file paths and permissions

### Debug Mode
```bash
export SYNAPSE_ENV=development
export SYNAPSE_LOG_LEVEL=DEBUG
python main.py
```

## Contributing

### Pull Request Process
1. Create feature branch from main
2. Make changes following coding standards
3. Add tests for new functionality
4. Update documentation as needed
5. Ensure all tests pass
6. Submit pull request with clear description

### Documentation
- Update README.md for major changes
- Add docstrings to new functions
- Update architecture docs for structural changes
- Include examples in documentation

### Version Control
- Use meaningful commit messages
- Keep commits atomic and focused
- Reference issues in commit messages
- Use conventional commit format where possible

## Performance

### Database Performance
- Use database indexes for frequently queried fields
- Implement connection pooling for high-load scenarios
- Consider read replicas for scaling

### Memory Usage
- Monitor memory usage in production
- Implement cleanup for temporary files
- Use generators for large data sets

### Monitoring
- Log important operations
- Monitor database connection health
- Track auto-discovery performance
- Monitor server composition overhead

## Security

### Database Security
- Use environment variables for sensitive configuration
- Implement proper database user permissions
- Use connection encryption in production

### File Security
- Validate file paths to prevent directory traversal
- Sanitize user input
- Implement proper access controls

This document should be updated as the project evolves to maintain accuracy and usefulness for developers. 