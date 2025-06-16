# Synapse 🧠⚡

> *AI-Human Collaboration Platform - Where Intelligence Connects*

**AI and humans will always need to work together.**

Synapse is the bridge that connects artificial and human intelligence, creating a collaborative partnership where both minds contribute their unique strengths. Like neural synapses that strengthen connections between neurons, our platform strengthens the connection between AI and human intelligence.

## 📚 Table of Contents

- [🌟 The Vision](#-the-vision)
- [🏗️ Architecture](#️-architecture)
  - [Server Composition with Auto-Discovery](#server-composition-with-auto-discovery)
  - [🔧 Technical Foundation](#-technical-foundation)
- [🚀 Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage Options](#usage-options)
  - [MCP Configuration](#mcp-configuration)
- [💡 Core Capabilities](#-core-capabilities)
  - [🧠 Memory Operations](#-memory-operations)
  - [📝 Template Generation](#-template-generation)
  - [⚙️ Configuration Management](#️-configuration-management)
  - [📚 Documentation System](#-documentation-system)
- [🎯 Real-World Applications](#-real-world-applications)
  - [Development Teams](#development-teams)
  - [Content Creators](#content-creators)
  - [Researchers](#researchers)
- [🏆 Benefits](#-benefits)
  - [For Humans](#for-humans)
  - [For AI Assistants](#for-ai-assistants)
  - [For Teams](#for-teams)
- [🔧 Advanced Features](#-advanced-features)
  - [Auto-Discovery System](#auto-discovery-system)
  - [Multi-Database Support](#multi-database-support)
  - [Server Composition](#server-composition)
- [📈 Roadmap](#-roadmap)
  - [Phase 1: Foundation ✅](#phase-1-foundation-)
  - [Phase 2: Intelligence 🔄](#phase-2-intelligence-)
  - [Phase 3: Collaboration 🔮](#phase-3-collaboration-)
- [🤝 Community](#-community)
  - [Contributing](#contributing)
  - [Getting Help](#getting-help)
- [📖 Documentation & Guides](#-documentation--guides)
  - [📚 Tools Reference](docs/tools-reference.md) - Complete guide to all Synapse tools
  - [🚀 Setup After Clone Guide](docs/setup-after-clone-guide.md) - Get started in 10 minutes
  - [⚙️ MCP Configuration Guide](docs/mcp-json-configuration-guide.md) - AI assistant setup
  - [🏗️ Architecture Guide](docs/ARCHITECTURE.md) - Technical architecture details
  - [📋 Guidelines](docs/guidelines.md) - Development and usage guidelines
- [📄 License](#-license)

---

## 🌟 The Vision

Synapse isn't about AI replacing humans—it's about AI amplifying human potential. We believe the future belongs to collaborative intelligence where:

- **AI provides processing power** while **humans provide wisdom**
- **AI handles routine tasks** while **humans drive creativity**  
- **AI offers instant recall** while **humans provide context**
- **AI scales globally** while **humans ensure relevance**

---

## 🏗️ Architecture

### Hard-Coded Tool Architecture

```
Synapse MCP Platform
├── Memory Tools        - Core memory operations (CRUD)
├── Config Tools        - Database & system configuration
├── Advanced Tools      - Project analysis & file operations
└── Meta Tools          - System information & introspection
```

### 🔧 Technical Foundation

- **MCP (Model Context Protocol)** - Seamless AI assistant integration
- **Hard-Coded Tools** - Reliable, predictable tool registration
- **Multi-Database Support** - SQLite (default) + MariaDB (production)
- **Configuration Management** - Environment-based settings
- **Cross-Platform** - Windows, macOS, Linux

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/synapse-platform/synapse.git
cd synapse

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Synapse
python main.py

# Or with custom options
python main.py --env development --host 0.0.0.0 --port 9000
```

### Usage Options

```bash
# Production mode (default)
python main.py

# Development mode
python main.py --env development

# Custom host and port
python main.py --host 0.0.0.0 --port 9000

# Show help
python main.py --help
```

### MCP Configuration

**Option 1: STDIO Mode (Traditional)**
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

**Option 2: HTTP Mode (Streamable)**
```json
{
  "mcpServers": {
    "synapse": {
      "command": "python",
      "args": ["main.py", "--env", "development"],
      "cwd": "/path/to/synapse"
    }
  }
}
```

> **Note:** Streamable HTTP mode is supported by more AI assistants and provides better performance for large operations.

---

## 💡 Core Capabilities

### 🧠 Memory Operations
- **Store & Retrieve** - Persistent memory across AI sessions
- **Search & Discovery** - Find information instantly
- **Auto-Sync** - Database + file system synchronization

### 📝 Template Generation
- **Smart Templates** - Context-aware document generation
- **Project Analysis** - Intelligent project insights
- **Custom Templates** - Tailored to your workflow

### ⚙️ Configuration Management
- **Multi-Environment** - Development, testing, production
- **Database Configuration** - Runtime database type switching
- **Health Monitoring** - System status and diagnostics
- **Environment Variables** - SYNAPSE_* configuration overrides

### 📚 Documentation System
- **Interactive Guides** - Step-by-step assistance
- **Dynamic Help** - Context-sensitive support
- **Searchable Docs** - Find answers quickly

---

## 🎯 Real-World Applications

### Development Teams
```python
# Store project decisions
ai_assistant.store_memory("architecture_decision.md", """
# Why We Chose FastAPI
- Performance requirements
- Team expertise
- Ecosystem compatibility
""")

# Generate project templates
ai_assistant.generate_template("api_endpoint.py", {
    "endpoint": "/users",
    "method": "POST"
})
```

### Content Creators
```python
# Track content ideas
ai_assistant.store_memory("content_calendar.md", """
# Q1 2024 Content Plan
- AI collaboration series
- Technical deep dives
- Community spotlights
""")

# Analyze content performance
ai_assistant.analyze_project("blog_performance.md")
```

### Researchers
```python
# Store research findings
ai_assistant.store_memory("research_notes.md", """
# Study: AI-Human Collaboration
- Findings show 40% productivity increase
- Key factors: trust, communication, tool quality
""")

# Search across research
results = ai_assistant.search_memories("productivity increase")
```

---

## 🏆 Benefits

### For Humans
- **🧠 Enhanced Memory** - Never lose important information
- **⚡ Faster Onboarding** - Get up to speed instantly
- **🎯 Better Decisions** - Access to complete context
- **🔄 Consistent Quality** - Standardized processes

### For AI Assistants
- **📊 Persistent Context** - Remember across sessions
- **🔍 Rich Information** - Access to detailed project history
- **🎨 Better Outputs** - Generate more relevant responses
- **🚀 Improved Efficiency** - Reduce repetitive explanations

### For Teams
- **👥 Shared Knowledge** - Everyone works from same information
- **📈 Scalable Growth** - Onboard new members quickly
- **🔄 Process Improvement** - Learn from past decisions
- **🛡️ Knowledge Preservation** - Prevent information loss

---

## 🔧 Advanced Features

### Database Configuration Tools
```python
# Configure database type at runtime
config_set_database_type("sqlite", "custom_synapse.db")
config_set_database_type("mariadb")

# Get current database information
config_get_database_info()
```

### Multi-Database Support
```bash
# SQLite for development (default)
export SYNAPSE_DB_TYPE=sqlite
export SYNAPSE_SQLITE_DB_PATH=synapse.db

# MariaDB for production
export SYNAPSE_DB_TYPE=mariadb
export SYNAPSE_MARIADB_HOST=localhost
export SYNAPSE_MARIADB_USER=synapse_user
export SYNAPSE_MARIADB_PASSWORD=password
export SYNAPSE_MARIADB_DATABASE=synapse
```

### Hard-Coded Tool Architecture
```python
# All tools are explicitly defined for reliability
tools = [
    "memory_get_memory_list", "memory_read_memory", 
    "memory_write_memory", "memory_delete_memory",
    "memory_search_memories", "config_set_database_type",
    "config_get_database_info", # ... and more
]
```

---

## 📈 Roadmap

### Phase 1: Foundation ✅
- [x] Core memory operations
- [x] Template system
- [x] Configuration management
- [x] Documentation system

### Phase 2: Intelligence 🔄
- [ ] Data analysis workflows
- [ ] Advanced search capabilities
- [ ] ML-powered insights
- [ ] Automated optimization

### Phase 3: Collaboration 🔮
- [ ] Multi-user support
- [ ] Real-time synchronization
- [ ] Team workflows
- [ ] Enterprise features

---

## 🤝 Community

### Contributing
We welcome contributions from developers, researchers, and users who share our vision of AI-human collaboration.

- **Developers** - Build new servers, tools, and integrations
- **Researchers** - Study AI-human collaboration patterns
- **Users** - Share feedback and use cases
- **Contributors** - Everyone who helps improve Synapse

### Getting Help
- 📖 **Documentation** - [docs.synapse-platform.org](https://docs.synapse-platform.org)
- 💬 **Community** - [Discord](https://discord.gg/synapse)
- 🐛 **Issues** - [GitHub Issues](https://github.com/synapse-platform/synapse/issues)
- 💡 **Ideas** - [GitHub Discussions](https://github.com/synapse-platform/synapse/discussions)

---

## 📖 Documentation & Guides

### Essential Guides
- **[📚 Tools Reference](docs/tools-reference.md)** - Complete guide to all available Synapse tools with usage examples
- **[🚀 Setup After Clone Guide](docs/setup-after-clone-guide.md)** - Get Synapse running in 10 minutes with step-by-step instructions
- **[⚙️ MCP Configuration Guide](docs/mcp-json-configuration-guide.md)** - Configure your AI assistant to work with Synapse

### Technical Documentation
- **[🏗️ Architecture Guide](docs/ARCHITECTURE.md)** - Deep dive into Synapse's technical architecture and design decisions
- **[📋 Guidelines](docs/guidelines.md)** - Development guidelines, coding standards, and best practices

### Additional Resources
- **[📝 Tasks & Development](docs/tasks.md)** - Current development tasks and project management
- **[🎯 Project Vision](docs/project-name-synapse.md)** - The story behind the Synapse name and vision

> 💡 **New to Synapse?** Start with the [Setup Guide](docs/setup-after-clone-guide.md), then explore the [Tools Reference](docs/tools-reference.md) to see what's possible!

---

## 📄 License

This project is licensed under the GNU General Public License v3.0 (GPLv3).

You are free to use, modify, and distribute this software under the terms of the GPLv3. See the LICENSE file in the project root for the full license text and your rights and obligations.

*Note: This project was previously licensed under the MIT License. As of [date], it is now licensed under GPL v3.0 for stronger copyleft and future flexibility.*

---

**Synapse** - *Where Intelligence Connects* 🧠⚡ 