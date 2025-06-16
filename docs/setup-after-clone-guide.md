# Setup Guide: Getting Started After Cloning Synapse

> **🎯 Just cloned the Synapse repository? This guide will get you running in 10 minutes!**

📚 **Platform-Specific Guides:**
- 🪟 **Windows Users:** See the [Windows Setup Guide](windows-setup-guide.md) for automated setup scripts
- 🍎🐧 **Mac/Linux Users:** See the [Mac/Linux Setup Guide](mac-linux-setup-guide.md) for Unix-specific instructions

## ⚡ Quick Setup (TL;DR)

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it (Windows)
.venv\Scripts\activate
# OR Unix/Mac:
source .venv/bin/activate

# 3. Install everything Synapse needs
pip install -r requirements.txt

# 4. Test that it works
python main.py

# Or test with development mode
python main.py --env development
```

## 🎯 Detailed Setup

### Step 1: Virtual Environment

**Why?** This keeps Synapse's dependencies separate from your system Python.

```bash
# Create the environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate

# Unix/Mac:
source .venv/bin/activate

# You should see (.venv) in your terminal now
```

**Without it:** Installing Synapse might conflict with other Python projects
**With it:** Synapse gets its own space, nothing conflicts

### Step 2: Install Dependencies

The `requirements.txt` file lists everything Synapse needs:

```bash
pip install -r requirements.txt
```

This installs:
- FastMCP (for AI assistant connections)
- MariaDB connector (database support)
- DuckDB (high-performance analytical database)
- psutil (system monitoring)

### Step 3: Configuration (Optional)

For basic usage, defaults work fine. For customization:

```bash
# Copy the development config
cp config.dev.json config.local.json

# Edit with your preferences
notepad config.local.json  # Windows
nano config.local.json     # Unix/Mac
```

### Step 4: First Run

```bash
# Run Synapse to see if it works (production mode)
python main.py

# Or run in development mode
python main.py --env development

# See all available options
python main.py --help
```

**Success looks like:** 
- Server starts without errors
- Shows "Starting Synapse MCP Server in [mode] mode with auto-discovery enabled..."
- Shows "Server will be available at http://127.0.0.1:8000"

### Step 5: Connect to Your AI Assistant

1. **Find your AI assistant's MCP config file**
2. **Get the full path** to your Synapse folder
3. **Add Synapse to your config:**

**Option A: STDIO Mode (Traditional)**
```json
{
  "mcpServers": {
    "synapse": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/full/path/to/your/synapse/folder"
    }
  }
}
```

**Option B: HTTP Mode (Streamable - Recommended)**
```json
{
  "mcpServers": {
    "synapse": {
      "command": "python",
      "args": ["main.py", "--env", "development"],
      "cwd": "/full/path/to/your/synapse/folder"
    }
  }
}
```

> **💡 Pro Tip:** HTTP mode (Option B) provides better performance and is supported by more AI assistants.

## 🚀 Command Line Options

Synapse now supports flexible command line configuration:

```bash
# Basic usage
python main.py                    # Production mode on 127.0.0.1:8000

# Environment control
python main.py --env development  # Development mode
python main.py --env production   # Production mode (default)
python main.py --env test         # Test mode

# Network configuration
python main.py --host 0.0.0.0     # Bind to all interfaces
python main.py --port 9000        # Use custom port

# Combined options
python main.py --env development --host 0.0.0.0 --port 9000

# Get help
python main.py --help
```

**Why use command line options?**
- **Flexibility:** Easy to switch between environments
- **Deployment:** Simple configuration for different hosts/ports
- **Testing:** Quick mode switching without config file changes
- **Streamable HTTP:** Better compatibility with modern AI assistants

## 🔄 Auto-Start Service Setup (Recommended for Beginners)

**Why set up as a service?**
- ✅ **Always available** - Synapse starts when your computer boots
- ✅ **No manual startup** - Just open your AI assistant and it works
- ✅ **Runs in background** - Doesn't clutter your terminal
- ✅ **Beginner friendly** - Set it once, forget about it

### Windows (Task Scheduler)

1. **Create a batch file** `start-synapse.bat`:
```batch
@echo off
cd /d "C:\path\to\your\synapse\folder"
.venv\Scripts\activate
python main.py --env production
```

2. **Open Task Scheduler** (`Win + R`, type `taskschd.msc`)
3. **Create Basic Task**:
   - Name: "Synapse MCP Server"
   - Trigger: "When the computer starts"
   - Action: "Start a program"
   - Program: `C:\path\to\your\synapse\folder\start-synapse.bat`

### macOS (launchd)

1. **Create launch agent** `~/Library/LaunchAgents/com.synapse.mcp.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.synapse.mcp</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/your/synapse/.venv/bin/python</string>
        <string>/path/to/your/synapse/main.py</string>
        <string>--env</string>
        <string>production</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/your/synapse</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

2. **Load the service**:
```bash
launchctl load ~/Library/LaunchAgents/com.synapse.mcp.plist
launchctl start com.synapse.mcp
```

### Linux (systemd)

1. **Create service file** `/etc/systemd/system/synapse-mcp.service`:
```ini
[Unit]
Description=Synapse MCP Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/your/synapse
ExecStart=/path/to/your/synapse/.venv/bin/python main.py --env production
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

2. **Enable and start**:
```bash
sudo systemctl enable synapse-mcp.service
sudo systemctl start synapse-mcp.service
```

### MCP Configuration for Service Mode

When Synapse runs as a service, your AI assistant connects to the **already running server**:

```json
{
  "mcpServers": {
    "synapse": {
      "url": "http://127.0.0.1:8000"
    }
  }
}
```

That's it! No `command`, `args`, or `cwd` needed - just point to the URL.

### Troubleshooting Service Setup

**Check if service is running:**
- Windows: Task Manager → Services tab → Look for your task
- macOS: `launchctl list | grep synapse`
- Linux: `systemctl status synapse-mcp`

**View logs:**
- Windows: Check the folder where you put the batch file
- macOS: `tail -f /var/log/system.log | grep synapse`
- Linux: `journalctl -u synapse-mcp -f`

**Test the connection:**
```bash
curl http://127.0.0.1:8000
# Should return MCP server info
```

## ✅ Quick Verification Checklist

- [ ] **Virtual environment created** (`.venv` folder exists)
- [ ] **Dependencies installed** (`pip install -r requirements.txt` worked)
- [ ] **Synapse runs** (`python main.py` doesn't crash)
- [ ] **Auto-discovery enabled** (see "with auto-discovery enabled" in output)
- [ ] **AI assistant configured** (added to MCP config)
- [ ] **Test with AI assistant** (try "List available tools")

---

## ❓ Frequently Asked Questions

### 1. **Do I need to start my MCP Server before running my AI assistant?**

**It depends on the mode:**

**STDIO Mode (Traditional):** **No!** 
- The AI assistant automatically starts Synapse when needed
- Your MCP config tells it how to start Synapse
- No manual server management required

**HTTP Mode (Streamable):** **Multiple options!**
- **Service mode (recommended):** Set up Synapse to auto-start with your computer
- **Manual start:** Run `python main.py` when you need it
- **Auto-start:** Let the AI assistant start it automatically (same as STDIO mode)

**Think of it like this:**
- Your MCP config is like giving your AI assistant a "recipe" for starting Synapse
- HTTP mode adds options: "pre-cook" (service), "cook when needed" (manual), or "follow recipe" (auto-start)

### 2. **Why use a virtual environment?**

**Problem without virtual environment:**
- Cleanup: Hard to remove Synapse cleanly later
- Conflicts: Different projects might need different package versions
- System pollution: Installs packages globally

**Benefits with virtual environment:**
- Clean: Each project has its own space
- Safe: Won't break other Python projects
- Portable: Easy to recreate on other machines

### 3. **What if I get installation errors?**

**Windows users:** You might need Visual Studio Build Tools for some packages (though Synapse tries to avoid this)

**Common fixes:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

### 4. **How do I know if my dependencies installed correctly?**

```bash
# Check if key packages are there
python -c "import fastmcp; print('FastMCP installed')"
python -c "import mariadb; print('MariaDB connector installed')"
```

### 5. **Where does Synapse store my data?**

**Files created automatically:**
- **Memory directory:** `memories` (for storing AI memory files)
- **DuckDB database:** `synapse.duckdb` (created automatically)
- **Configuration:** Uses `config.prod.json` by default

### 6. **How do I know if Synapse is working with my AI assistant?**

1. Start your AI assistant normally
2. It should connect to Synapse automatically when needed
3. Try: *"List my memories"* or *"What Synapse tools do you have?"*

**If it's not working:**
- Verify the `cwd` path points to your Synapse folder
- Check that `python main.py` works when run manually

### 7. **Can I use Synapse with multiple AI assistants at once?**

**Yes!** Each AI assistant can connect to the same Synapse instance. They'll share the same memory/data.

**Setup:** Add the same Synapse configuration to each AI assistant's MCP config.

**Benefits:** Consistent memory across all your AI tools.

### 8. **What if I want to move Synapse to a different folder later?**

1. Move the entire folder
2. Update the `cwd` path in your AI assistant's MCP config
3. Done! (The database and memory files move with the folder)

**Note:** Don't just move some files - move the whole project folder.

### 9. **Should I set up Synapse as a service?**

**For beginners: YES!** It's the easiest way to use Synapse.

**Service benefits:**
- ✅ **No remembering** to start Synapse manually
- ✅ **Always available** when you open your AI assistant
- ✅ **Runs quietly** in the background
- ✅ **Survives reboots** - starts automatically

**When NOT to use service mode:**
- You only use Synapse occasionally
- You want to see server logs in your terminal
- You're actively developing/debugging

**Service vs Manual startup:**
- **Service:** `{"url": "http://127.0.0.1:8000"}` (simple!)
- **Manual:** Full command/args config (more complex)

### 10. **Do I need to understand MCP to use Synapse?**

**No!** Think of MCP as the "plumbing" that connects Synapse to your AI assistant. You don't need to understand plumbing to use a faucet.

**What you need to know:**
- How to edit a JSON config file ✅
- How to ask your AI assistant to use Synapse tools ✅

**What you don't need to know:**
- MCP protocol details ❌
- Server implementation ❌
- Database management ❌

### 10. **What's the difference between development and production mode?**

**Development mode** (default):
- More verbose logging
- SQLite database (simpler)
- Auto-reloads on changes
- Better for testing

**Production mode:**
```bash
export SYNAPSE_ENV=production
python main.py
```
- Optimized performance
- Can use MariaDB
- Suitable for team/server deployment

---

## 🎉 You're Ready!

If you've completed the checklist above:
- ✅ Synapse is installed and configured
- ✅ Your AI assistant can use Synapse tools
- ✅ You understand the basic workflow

**Next steps:**
- Try creating your first memory: *"Store this as a memory file..."*
- Explore Synapse's templates: *"What templates are available?"*
- Check system status: *"Show me Synapse configuration"*

**Welcome to the Synapse community!** 🚀 

**Synapse (This Project):**
- Memory management ✅
- Template generation ✅
- Project analysis ✅
- Database management ✅
- DuckDB database (high-performance)
- AI assistant integration ✅ 