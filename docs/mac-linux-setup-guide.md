🍎🐧 Synapse Mac/Linux Setup Guide
🚀 Quick Start for Mac and Linux Users

## Option 1: Bash Script (Recommended)
```bash
# Save as synapse-dev.sh in your Synapse folder
# Make it executable and run:
chmod +x synapse-dev.sh
./synapse-dev.sh

# With options:
./synapse-dev.sh --config config.dev.mariadb.json
./synapse-dev.sh --env production --db-type duckdb
./synapse-dev.sh --log-level DEBUG
```

## Option 2: Manual Setup (Direct Control)
```bash
# Activate virtual environment
source .venv/bin/activate

# Run Synapse
python main.py --env development --db-type auto
```

---

## 📋 Prerequisites

### 1. Python 3.12+
**macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.12

# Or download from: https://www.python.org/downloads/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip

# For older Ubuntu versions, use deadsnakes PPA:
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

**Linux (CentOS/RHEL/Fedora):**
```bash
# CentOS/RHEL 8+
sudo dnf install python3.12 python3.12-pip

# Fedora
sudo dnf install python3.12 python3.12-pip python3.12-devel
```

### 2. Git (Usually pre-installed)
**macOS:**
```bash
# Usually comes with Xcode Command Line Tools
xcode-select --install

# Or via Homebrew
brew install git
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install git

# CentOS/RHEL/Fedora
sudo dnf install git
```

### 3. MariaDB (Optional - for production database)
**macOS:**
```bash
# Using Homebrew
brew install mariadb
brew services start mariadb

# Secure installation
sudo mysql_secure_installation
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install mariadb-server mariadb-client
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Secure installation
sudo mysql_secure_installation
```

**Linux (CentOS/RHEL/Fedora):**
```bash
sudo dnf install mariadb-server mariadb
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Secure installation
sudo mysql_secure_installation
```

---

## 🛠️ Installation Steps

### Step 1: Get Synapse
```bash
# Option A: Clone with Git
git clone https://github.com/your-repo/synapse.git
cd synapse

# Option B: Download and extract ZIP
# wget https://github.com/your-repo/synapse/archive/main.zip
# unzip main.zip && cd synapse-main
```

### Step 2: Set Up Virtual Environment
```bash
# Create virtual environment
python3.12 -m venv .venv

# Activate it
source .venv/bin/activate

# Verify activation (you should see (.venv) in your prompt)
which python
```

### Step 3: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install Synapse dependencies
pip install -r requirements.txt
```

### Step 4: Choose Your Startup Method

#### Method A: Bash Script (Recommended)
```bash
# Make the script executable
chmod +x startup_scripts/synapse-dev.sh

# Copy to project root for convenience
cp startup_scripts/synapse-dev.sh ./

# Run with defaults (DuckDB development)
./synapse-dev.sh

# Or with options
./synapse-dev.sh --config config.dev.mariadb.json
```

#### Method B: Direct Python (Full Control)
```bash
# Basic startup
python main.py

# Development mode
python main.py --env development

# With custom database
python main.py --env development --db-type mariadb

# Custom host/port
python main.py --host 0.0.0.0 --port 9000
```

---

## 🎯 Usage Examples

### Basic Usage (DuckDB - Default High-Performance Database)
```bash
# Start with DuckDB (recommended - works out of the box)
python main.py

# Or explicitly specify DuckDB
python main.py --db-type duckdb

# With development mode and DuckDB
python main.py --env development --db-type duckdb
```

### Advanced Usage (MariaDB Development)
```bash
# Requires MariaDB installed
./synapse-dev.sh --db-type mariadb

# Or use specific config file
./synapse-dev.sh --config config.dev.mariadb.json

# Manual start with MariaDB
python main.py --env development --db-type mariadb
```

### Production Mode
```bash
./synapse-dev.sh --env production

# Or manual
python main.py --env production --host 0.0.0.0 --port 8000
```

### Debug Mode
```bash
./synapse-dev.sh --log-level DEBUG

# Or manual
python main.py --env development --log-level DEBUG
```

---

## 🔧 Configuration Files

The scripts will automatically create these config files:

### config.dev.json (DuckDB - Default)
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
```

### config.dev.mariadb.json (MariaDB Development)
```json
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
```

---

## 🚨 Troubleshooting

### Python Issues
**Problem:** `python3.12: command not found`
**Solutions:**
```bash
# Try alternative commands
python3 --version
python --version

# Install Python 3.12 using your system's package manager
# macOS: brew install python@3.12
# Ubuntu: sudo apt install python3.12
```

### Virtual Environment Issues
**Problem:** Virtual environment not activating
**Solutions:**
```bash
# Ensure you're in the right directory
pwd

# Try recreating the virtual environment
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
```

### MariaDB Issues
**Problem:** MariaDB server not found
**Solutions:**
```bash
# Check if MariaDB is installed
which mysqld
which mariadbd

# Install MariaDB
# macOS: brew install mariadb
# Ubuntu: sudo apt install mariadb-server
# CentOS: sudo dnf install mariadb-server

# Or use DuckDB instead
./synapse-dev.sh --db-type duckdb
```

### Permission Issues
**Problem:** Permission denied errors
**Solutions:**
```bash
# Make script executable
chmod +x synapse-dev.sh

# Check file permissions
ls -la synapse-dev.sh

# Fix ownership if needed
sudo chown $USER:$USER synapse-dev.sh
```

### Port Already in Use
**Problem:** Port 8000 already in use
**Solutions:**
```bash
# Use a different port
./synapse-dev.sh --port 9000

# Or find what's using the port
lsof -i :8000

# Kill the process if safe to do so
sudo kill -9 <PID>
```

### Package Installation Issues
**Problem:** pip install failures
**Solutions:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install build tools if needed (Linux)
sudo apt install build-essential python3.12-dev  # Ubuntu
sudo dnf install gcc python3.12-devel           # Fedora

# macOS: Install Xcode Command Line Tools
xcode-select --install

# Clear pip cache
pip cache purge
```

---

## 🎉 Success Indicators

When everything is working, you should see:

```
 ____                                     
/ ___| _   _ _ __   __ _ _ __  ___  ___    
\___ \| | | | '_ \ / _` | '_ \/ __|/ _ \   
 ___) | |_| | | | | (_| | |_) \__ \  __/   
|____/ \__, |_| |_|\__,_| .__/|___/\___|   
       |___/            |_|               

🧠 AI-Human Collaboration Platform
    Where Intelligence Connects ⚡

[INFO] Synapse Development Server Startup
[SUCCESS] Virtual environment detected: /path/to/synapse/.venv
[SUCCESS] Python version: 3.12.x
[SUCCESS] Pre-flight checks completed
[SUCCESS] All checks passed! Starting server...
[SUCCESS] 🚀 Starting server with: python main.py --env development ...
🚀 Starting Synapse MCP Server in development mode...
✅ Database connection successful! Found 0 existing memories.
🧠 Synapse MCP Platform ready with hard-coded tools
Server will be available at http://127.0.0.1:8000
```

---

## 🔗 Connecting to Your AI Assistant

After Synapse starts, add this to your AI assistant's MCP configuration:

### For Claude Desktop:
**Config file location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "synapse": {
      "command": "python",
      "args": ["main.py", "--env", "development"],
      "cwd": "/absolute/path/to/your/synapse/folder"
    }
  }
}
```

### For Cursor:
Add to your workspace settings:

```json
{
  "mcp": {
    "synapse": {
      "command": "python",
      "args": ["main.py", "--env", "development"],
      "cwd": "/absolute/path/to/your/synapse/folder"
    }
  }
}
```

---

## 🔄 Service Setup (Auto-Start on Boot)

### macOS (launchd)
Create `~/Library/LaunchAgents/com.synapse.mcp.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.synapse.mcp</string>
    <key>ProgramArguments</key>
    <array>
        <string>/absolute/path/to/synapse/.venv/bin/python</string>
        <string>/absolute/path/to/synapse/main.py</string>
        <string>--env</string>
        <string>production</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/absolute/path/to/synapse</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/synapse.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/synapse.error.log</string>
</dict>
</plist>
```

Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.synapse.mcp.plist
launchctl start com.synapse.mcp
```

### Linux (systemd)
Create `/etc/systemd/system/synapse.service`:

```ini
[Unit]
Description=Synapse MCP Server
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/absolute/path/to/synapse
Environment=PATH=/absolute/path/to/synapse/.venv/bin
ExecStart=/absolute/path/to/synapse/.venv/bin/python main.py --env production
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable synapse.service
sudo systemctl start synapse.service
sudo systemctl status synapse.service
```

---

## 📱 Platform-Specific Tips

### macOS Specific
- Use Homebrew for package management: `brew install python@3.12 mariadb`
- TextEdit creates rich text files by default - use `nano` or `vim` for plain text
- Spotlight can find your Synapse folder quickly: `Cmd+Space`, type "synapse"

### Linux Specific
- Package names vary by distribution - use your distro's package manager
- Some distributions require separate `-dev` packages for Python development
- Use `systemctl` for service management in modern Linux distributions
- Consider using `screen` or `tmux` for persistent sessions

### Both Platforms
- The tilde (`~`) represents your home directory
- Use `which python` to find your Python installation
- Environment variables can be set in `~/.bashrc`, `~/.zshrc`, or `~/.profile`
- Use absolute paths in service configurations for reliability

---

## 🎯 Quick Reference Commands

```bash
# Essential commands for daily use
source .venv/bin/activate          # Activate virtual environment
./synapse-dev.sh                   # Start Synapse (recommended)
python main.py --help              # See all options
./synapse-dev.sh --config config.dev.mariadb.json  # MariaDB mode
python main.py --env production    # Production mode
pip install -r requirements.txt    # Install/update dependencies
git pull origin main              # Update Synapse code
```

---

This guide covers everything needed to get Synapse running smoothly on Mac and Linux systems. For additional help, refer to the [main documentation](../README.md) or check the [troubleshooting guide](./setup-after-clone-guide.md). 