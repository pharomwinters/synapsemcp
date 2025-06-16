🪟 Synapse Windows Setup Guide
🚀 Quick Start for Windows Users
Option 1: Command Prompt / Batch Script (Recommended)
cmd
# Save as synapse-dev.bat in your Synapse folder
# Double-click to run, or use from command prompt:
synapse-dev.bat

# With options:
synapse-dev.bat --config config.dev.mariadb.json
synapse-dev.bat --env production --db-type duckdb
synapse-dev.bat --log-level DEBUG
Option 2: PowerShell Script (Advanced Users)
powershell
# Save as synapse-dev.ps1 in your Synapse folder
# Run from PowerShell:
.\synapse-dev.ps1

# With options:
.\synapse-dev.ps1 -Config config.dev.mariadb.json
.\synapse-dev.ps1 -Env production -DbType duckdb
.\synapse-dev.ps1 -LogLevel DEBUG
📋 Prerequisites
1. Python 3.12+
Download from: https://www.python.org/downloads/

✅ Important: Check "Add Python to PATH" during installation
✅ Choose "Install for all users" if you have admin rights
2. Git (Optional but recommended)
Download from: https://git-scm.com/download/win

3. MariaDB (Optional - for development with real database)
Download from: https://mariadb.org/download/

✅ Choose "MSI Package" for easy installation
✅ Remember the root password you set during installation
🛠️ Installation Steps
Step 1: Get Synapse
cmd
# Option A: Clone with Git
git clone https://github.com/your-repo/synapse.git
cd synapse

# Option B: Download ZIP
# Download ZIP from GitHub, extract to a folder, open Command Prompt in that folder
Step 2: Set Up Virtual Environment
cmd
# Create virtual environment
python -m venv .venv

# Activate it (Command Prompt)
.venv\Scripts\activate

# OR Activate it (PowerShell)
.venv\Scripts\Activate.ps1
Step 3: Install Dependencies
cmd
# Install Synapse dependencies
pip install -r requirements.txt
Step 4: Choose Your Startup Method
Method A: Batch Script (Easiest)
Save the enhanced batch script as synapse-dev.bat
Double-click synapse-dev.bat to start with defaults
Or run from Command Prompt with options
Method B: PowerShell Script (More Features)
Save the PowerShell script as synapse-dev.ps1
You may need to enable script execution:
powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Run: .\synapse-dev.ps1
Method C: Manual (Direct Control)
cmd
python main.py --env development --db-type auto
🎯 Usage Examples
Basic Usage (DuckDB - Default High-Performance Database)

# Start with DuckDB (recommended - works out of the box)
python main.py

# Or explicitly specify DuckDB
python main.py --db-type duckdb

# With development mode and DuckDB
python main.py --env development --db-type duckdb
Advanced Usage (MariaDB Development)
cmd
# Requires MariaDB installed
synapse-dev.bat --db-type mariadb

# Or use specific config file
synapse-dev.bat --config config.dev.mariadb.json
Production Mode
cmd
synapse-dev.bat --env production
Debug Mode
cmd
synapse-dev.bat --log-level DEBUG
🔧 Configuration Files
The scripts will automatically create these config files:

config.dev.json (DuckDB - Default)
```json
{
    "database": {
        "type": "duckdb",
        "duckdb": {
            "db_path": "synapse_dev.duckdb"
        }
    },
    "memory_dir": "memories_dev",
    "log_level": "DEBUG"
}
config.dev.mariadb.json (MariaDB Development)
json
{
    "database": {
        "type": "mariadb",
        "mariadb": {
            "host": "127.0.0.1",
            "port": 3307,
            "user": "synapse_user",
            "password": "synapse_pass_2024",
            "database": "synapse"
        }
    },
    "memory_dir": "memories_dev",
    "log_level": "DEBUG",
    "embedded_mariadb": {
        "enabled": true,
        "auto_start": true,
        "data_directory": "synapse_mariadb_data",
        "port": 3307
    }
}
🚨 Troubleshooting
Python Issues
Problem: 'python' is not recognized Solution:

Reinstall Python with "Add to PATH" checked
Or use full path: C:\Python312\python.exe
Virtual Environment Issues
Problem: cannot be loaded because running scripts is disabled Solution: Run PowerShell as Administrator and execute:

powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
MariaDB Issues
Problem: MariaDB server not found Solutions:

Install MariaDB from https://mariadb.org/download/
Or use DuckDB: synapse-dev.bat --db-type duckdb
Or use DuckDB config: synapse-dev.bat --config config.dev.json
Permission Issues
Problem: Access denied errors Solutions:

Run Command Prompt as Administrator
Check antivirus software isn't blocking Python
Make sure you have write permissions in the Synapse folder
Port Already in Use
Problem: Port 8000 already in use Solution: Use a different port:

cmd
synapse-dev.bat --port 9000
🎉 Success Indicators
When everything is working, you should see:

🧠 AI-Human Collaboration Platform
    Where Intelligence Connects ⚡

[INFO] Synapse Development Server Startup
[SUCCESS] Virtual environment detected: C:\path\to\synapse\.venv
[SUCCESS] Python version: 3.12.x
[SUCCESS] Pre-flight checks completed
[SUCCESS] All checks passed! Starting server...
[SUCCESS] 🚀 Starting server with: python main.py --env development ...
🚀 Starting Synapse MCP Server in development mode...
✅ Database connection successful! Found 0 existing memories.
🧠 Synapse MCP Platform ready with hard-coded tools
Server will be available at http://127.0.0.1:8000
🔗 Connecting to Your AI Assistant
After Synapse starts, add this to your AI assistant's MCP configuration:

For Claude Desktop:
File location: %APPDATA%\Claude\claude_desktop_config.json

json
{
  "mcpServers": {
    "synapse": {
      "command": "python",
      "args": ["main.py", "--env", "development"],
      "cwd": "C:\\path\\to\\your\\synapse\\folder"
    }
  }
}
For Cursor:
Add to your workspace settings:

json
{
  "mcp": {
    "servers": {
      "synapse": {
        "command": "python",
        "args": ["main.py", "--env", "development"],
        "cwd": "C:\\path\\to\\your\\synapse\\folder"
      }
    }
  }
}
🎯 Quick Test
Once everything is running:

Ask your AI assistant: "List my available tools"
You should see Synapse memory tools listed
Try: "Save this to my memories: 'Windows setup completed successfully!'"
Then: "List my memories"
If these work, you're all set! 🎉

💡 Pro Tips for Windows Users
Use Windows Terminal: Much better than Command Prompt
Install from Microsoft Store
Supports multiple tabs and better colors
Pin to Taskbar: Right-click synapse-dev.bat → "Pin to taskbar"
Create Desktop Shortcut: Right-click synapse-dev.bat → "Send to" → "Desktop"
Use PowerShell ISE: For editing PowerShell scripts with syntax highlighting
Windows Defender: Add Synapse folder to exclusions for better performance
🆘 Getting Help
If you're still having issues:

Check the logs: Look at the console output for error messages
Try DuckDB first: Use --db-type duckdb to rule out MariaDB issues
Test Python: Run python --version to make sure Python works
Check paths: Make sure you're in the right folder with dir command
Run diagnostics: Create and run the database test script
Remember: Start simple with DuckDB, then move to MariaDB once basic functionality works!

