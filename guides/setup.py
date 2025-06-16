"""Setup guide for Synapse."""

GUIDE = """## Setting Up Synapse

### 1. Installation
1. Clone the Synapse repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment
4. Install dependencies: `pip install -r requirements.txt`

### 2. Configuration
1. Copy `config.dev.json` to `config.local.json`
2. Modify database settings if needed
3. Set environment variables:
   - `SYNAPSE_ENV` - Environment (development/testing/production)
   - `SYNAPSE_AUTO_DISCOVER` - Enable auto-discovery on startup

### 3. Database Setup
The system supports DuckDB (default) and MariaDB:

**DuckDB (Recommended for most use cases):**
- No additional setup required
- Database file created automatically
- High-performance analytical database
- Optimized for OLAP workloads

**SQLite (Legacy compatibility):**
- No additional setup required
- Database file created automatically
- Simple file-based database

**MariaDB (For production):**
- Install MariaDB server
- Create database and user
- Update configuration with connection details

### 4. First Run
1. Run `python main.py` to start the server
2. Test basic functionality with MCP client
3. Create your first synapse files

### 5. MCP Client Configuration
Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "synapse": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/synapse",
      "env": {
        "SYNAPSE_ENV": "development"
      }
    }
  }
}
```

### 6. Verification
- List available tools to verify connection
- Try creating a memory file
- Check that database is working
- Verify auto-discovery if enabled

Your Synapse system is now ready for AI-human collaboration!""" 