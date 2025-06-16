# MCP JSON Configuration Guide for Beginners

> **🎯 A beginner-friendly guide to configuring Synapse with your AI assistant**

## 🤔 What is MCP JSON Configuration?

Think of MCP JSON configuration like a **menu** you give to your AI assistant. This menu tells your AI assistant:
- What tools are available (like "Synapse")
- How to start those tools (like running a Python script)
- Where to find those tools (the folder path)

**Simple analogy:** It's like giving Claude a business card for Synapse with the address and phone number, so Claude knows how to contact it when needed.

## 📍 Where Do These Files Live?

### Claude Desktop
- **Windows:** `%appdata%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

### Cursor IDE
- Usually in your workspace settings (`.cursor/settings.json`)
- Or global Cursor settings

### Other AI Assistants
- Check their documentation for MCP configuration location
- Usually somewhere in their app data or settings folder

---

## 📋 Basic Structure Explained

Every MCP config file looks like this:

```json
{
  "mcpServers": {
    "your-tool-name": {
      "command": "how-to-start-it",
      "args": ["any-extra-options"],
      "cwd": "where-to-find-it"
    }
  }
}
```

**Breaking it down:**
- `mcpServers` - The list of all your AI tools
- `"your-tool-name"` - Any name you want (like "synapse" or "my-tools")
- `command` - What program to run (usually "python")
- `args` - Extra instructions for that program
- `cwd` - The folder path where your tool lives

---

## 🎯 Real Examples

### Example 1: Basic Synapse Setup (Claude Desktop)

```json
{
  "mcpServers": {
    "synapse": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "C:\\Users\\YourName\\Projects\\synapse"
    }
  }
}
```

**What this means:**
- **Name:** "synapse" (how Claude will refer to it)
- **Start it by:** Running `python main.py`
- `"cwd": "C:\\..."`: Where your Synapse project lives
- When Claude needs Synapse, it goes to that folder and runs that command

### Example 2: Multiple Tools Setup

```json
{
  "mcpServers": {
    "synapse": {
      "command": "python", 
      "args": ["main.py"],
      "cwd": "/Users/yourname/projects/synapse"
    },
    "other-tool": {
      "command": "node",
      "args": ["server.js"],
      "cwd": "/Users/yourname/projects/other-tool"
    }
  }
}
```

### Example 3: Synapse with Environment Variables

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

**What `env` does:**
- `"SYNAPSE_ENV": "development"` tells Synapse to run in development mode
- Environment variables are like settings you pass to the program
- Different tools use different environment variables

---

## ✅ Do's and Don'ts

### ✅ DO:
1. **✅ Use full absolute paths** 
   - Good: `"C:\\Users\\John\\projects\\synapse"`
   - Bad: `"../synapse"` or `"~/synapse"`

2. **✅ Use forward slashes OR double backslashes on Windows**
   - Good: `"C:/Users/John/synapse"` 
```json
{
  "mcp": {
    "servers": {
      "memory-bank": {
        "command": "python",
        "args": ["main.py"],
        "cwd": "${workspaceFolder}/memory_bank",
        "env": {
          "MEMORY_BANK_ENV": "development"
        }
      }
    }
  }
}
```

**Note:** Cursor uses `${workspaceFolder}` to refer to your current project folder.

## ✅ What SHOULD Be in Your MCP JSON

### Essential (You NEED these):
- `mcpServers` - The main section
- Server name (like `"memory-bank"`)
- `command` - How to run your tool
- `cwd` - Where your project files are

### Common and Useful:
- `args` - Command line arguments
- `env` - Environment variables for settings

### Example of Good Practice:
```json
{
  "mcpServers": {
    "memory-bank": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/Users/yourname/projects/memory_bank",
      "env": {
        "MEMORY_BANK_ENV": "development"
      }
    }
  }
}
```

## ❌ What Should NOT Be in Your MCP JSON

### Don't Include:
- **Passwords or API keys** (use environment variables instead)
- **Personal information** (names, emails, etc.)
- **Hardcoded sensitive paths** (like `/Users/john.doe/secret/`)
- **Overly complex configurations** (start simple!)

### Bad Example (Don't do this):
```json
{
  "mcpServers": {
    "memory-bank": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/Users/john.doe/secret-project/memory_bank",
      "env": {
        "DATABASE_PASSWORD": "my-secret-password123",
        "API_KEY": "sk-1234567890abcdef"
      }
    }
  }
}
```

### Better Approach:
```json
{
  "mcpServers": {
    "memory-bank": {
      "command": "python", 
      "args": ["main.py"],
      "cwd": "${HOME}/projects/memory_bank",
      "env": {
        "MEMORY_BANK_ENV": "development"
      }
    }
  }
}
```

## 🔧 Common Issues & Quick Fixes

### "Command not found"
**Problem:** Your computer can't find Python
**Solution:** Use full path to Python:
```json
"command": "C:\\Python312\\python.exe"
```

### "Path not found"  
**Problem:** Wrong project path
**Solution:** Double-check your `cwd` path. Use forward slashes `/` or double backslashes `\\`

### "Permission denied"
**Problem:** File permissions
**Solution:** Make sure your Python files are executable

## 🎯 Quick Start Checklist

1. **✅ Find your config file location** (Claude Desktop vs Cursor)
2. **✅ Copy the basic template** (from examples above)
3. **✅ Update the `cwd` path** to where your Memory Bank is
4. **✅ Test it** by asking Claude "What tools do you have?"
5. **✅ Start simple** - you can always add more later!

## 🚀 Testing Your Configuration

After setting up your MCP JSON:

1. **Restart Claude Desktop** or **Reload Cursor**
2. **Ask your AI**: "What MCP servers do you have available?"
3. **Try a simple command**: "List my memories" (if using Memory Bank)

If it works - congratulations! 🎉 If not, double-check:
- File paths (most common issue)
- JSON syntax (use a JSON validator online)
- Python installation

## 💡 Pro Tips for Beginners

1. **Start with the simplest configuration** - you can always add features later
2. **Use absolute paths** when you're learning (relative paths can be tricky)
3. **Keep a backup** of your working configuration
4. **Test each change** before adding more complexity
5. **Use environment variables** for anything that might change between computers

## 🆘 Need Help?

If you're stuck:
1. Check that Python is installed: `python --version`
2. Check that your Memory Bank project exists at the specified path
3. Validate your JSON syntax online
4. Start with the simplest possible configuration and build up

Remember: **Everyone starts as a beginner!** Don't be intimidated by complex configurations you see online - start simple and grow from there.

---

*Happy configuring! 🚀* 