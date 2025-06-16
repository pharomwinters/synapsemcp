# Synapse Tools Reference

> **Complete guide to all available tools in the Synapse system**

## 🧠 Overview

Synapse provides a comprehensive set of tools for memory management, document processing, database configuration, project analysis, and workflow automation. All tools are hard-coded for maximum reliability and predictability.

---

## 📋 Core Memory Tools

### `memory_get_memory_list`
**Description:** Get a list of all memory files in the Synapse system.

**Usage:** 
```
Ask your AI assistant: "List all my memories" or "Show me my memory files"
```

**Returns:** List of memory file names
**Example Output:**
```
- project_notes.md
- meeting_summary.md
- research_findings.md
```

---

### `memory_read_memory`
**Description:** Read the content of a specific memory file.

**Parameters:**
- `file_name` (required): Name of the memory file to read

**Usage:**
```
Ask your AI assistant: "Read my project_notes.md memory" or "Show me the content of meeting_summary.md"
```

**Returns:** Full content of the memory file
**Example:** Retrieves the complete text content of the specified memory file

---

### `memory_write_memory`
**Description:** Write or update content in a memory file.

**Parameters:**
- `file_name` (required): Name of the memory file to write
- `content` (required): Content to write to the memory file

**Usage:**
```
Ask your AI assistant: "Save this to my project_notes.md: [your content]" or "Update meeting_summary.md with: [new content]"
```

**Returns:** Success confirmation message
**Example:** "Successfully saved memory 'project_notes.md'"

---

### `memory_delete_memory`
**Description:** Delete a memory file from both database and file system.

**Parameters:**
- `file_name` (required): Name of the memory file to delete

**Usage:**
```
Ask your AI assistant: "Delete my old_notes.md memory" or "Remove the file draft_ideas.md"
```

**Returns:** Success/failure confirmation
**Example:** "Successfully deleted memory 'old_notes.md'"

---

### `memory_search_memories`
**Description:** Search through all memory contents for specific text.

**Parameters:**
- `query` (required): Search term to look for in memory content

**Usage:**
```
Ask your AI assistant: "Search my memories for 'API design'" or "Find memories containing 'budget'"
```

**Returns:** List of memory files containing the search term with snippets
**Example:**
```
- project_notes.md: "API design patterns for microservices..."
- meeting_summary.md: "Discussed API design decisions..."
```

---

## 📄 Document Management Tools

These tools handle document storage, text extraction, and management operations for various file formats.

### `document_store_document`
**Description:** Store and process a document in the Synapse system with text extraction and metadata management.

**Parameters:**
- `file_path` (required): Path to the document file to store
- `document_name` (optional): Custom name for the document (defaults to filename)
- `tags` (optional): List of tags to associate with the document

**Usage:**
```
Ask your AI assistant: "Store this document: /path/to/file.pdf" or "Add document report.docx with tags ['project', 'quarterly']"
```

**Returns:** Document storage confirmation with metadata
**Supported Formats:** PDF, DOCX, XLSX, ODT, TXT, MD, RTF, CSV, HTML

---

### `document_get_document`
**Description:** Retrieve document information and metadata.

**Parameters:**
- `document_name` (required): Name of the document to retrieve

**Usage:**
```
Ask your AI assistant: "Get document info for report.pdf" or "Show me details of my_document"
```

**Returns:** Complete document metadata including extracted text, file info, and tags

---

### `document_list_documents`
**Description:** List all documents in the system with optional tag filtering.

**Parameters:**
- `tag_filter` (optional): Filter documents by specific tag

**Usage:**
```
Ask your AI assistant: "List all documents" or "Show documents tagged with 'project'"
```

**Returns:** List of documents with basic metadata

---

### `document_search_documents`
**Description:** Search through document names and content.

**Parameters:**
- `query` (required): Search term to look for
- `search_content` (optional): Whether to search document content (default: true)

**Usage:**
```
Ask your AI assistant: "Search documents for 'budget analysis'" or "Find documents about 'API design'"
```

**Returns:** List of matching documents with relevance information

---

### `document_delete_document`
**Description:** Delete a document from the system.

**Parameters:**
- `document_name` (required): Name of the document to delete
- `delete_file` (optional): Whether to delete the original file (default: false)

**Usage:**
```
Ask your AI assistant: "Delete document old_report.pdf" or "Remove document draft.docx and delete file"
```

**Returns:** Deletion confirmation

---

### `document_get_supported_formats`
**Description:** Get information about supported document formats and processing capabilities.

**Usage:**
```
Ask your AI assistant: "What document formats are supported?" or "Show document processing capabilities"
```

**Returns:** List of supported file formats with descriptions and processing status

---

### `document_add_document_tags`
**Description:** Add additional tags to an existing document.

**Parameters:**
- `document_name` (required): Name of the document
- `tags` (required): List of tags to add

**Usage:**
```
Ask your AI assistant: "Add tags ['important', 'review'] to report.pdf"
```

**Returns:** Updated tag information

---

## ⚙️ Database Configuration Tools

These tools allow you to configure and manage the database backend for Synapse.

### `config_set_database_type`
**Description:** Configure the database type for Synapse memory storage.

**Parameters:**
- `db_type` (required): Type of database ('duckdb', 'sqlite', 'mariadb')
- `db_path` (optional): Database path for DuckDB/SQLite or connection details

**Usage:**
```
Ask your AI assistant: "Set database to DuckDB with path custom.duckdb" or "Configure MariaDB database"
```

**Returns:** Status message confirming the database configuration
**Example:** "✅ Database type set to 'duckdb' with path: custom_synapse.duckdb"

**Notes:**
- DuckDB is the default and recommended for most use cases
- SQLite is available for legacy compatibility
- MariaDB requires additional environment variables for connection details

---

### `config_get_database_info`
**Description:** Get current database configuration information.

**Usage:**
```
Ask your AI assistant: "Show database configuration" or "What database am I using?"
```

**Returns:** Comprehensive database configuration including:
- Current environment (development/testing/production)
- Database type and specific settings
- Memory directory location
- Supported database types
- Configuration guidance

**Example Output:**
```
🗄️ Database Configuration
        
**Environment**: development
**Type**: duckdb
**Memory Directory**: memories_dev

**Current Database Settings**:
• DuckDB Path: synapse_dev.duckdb

**Supported Types**:
• duckdb - DuckDB database (default)
• sqlite - Local SQLite database (legacy)
• mariadb - MariaDB/MySQL database
```

---

## 🔧 Advanced Analysis Tools

These tools provide sophisticated project analysis and file management capabilities.

### `analyze_project_structure`
**Description:** Analyze the structure of a project directory and provide comprehensive insights.

**Parameters:**
- `directory_path` (optional): Path to analyze (defaults to current directory)

**Usage:**
```
Ask your AI assistant: "Analyze my project structure" or "What's in my current directory?"
```

**Returns:** Detailed analysis including:
- Total files and directories
- File type breakdown
- Largest files
- Synapse-specific files
- Recently modified files

**Example Output:**
```json
{
  "total_files": 45,
  "total_directories": 8,
  "file_types": {".py": 12, ".md": 8, ".json": 3},
  "largest_files": [...],
  "synapse_files": ["projectbrief.md", "requirements.md"],
  "recent_files": [...]
}
```

---

### `generate_file_checksum`
**Description:** Generate cryptographic checksums for files to verify integrity.

**Parameters:**
- `file_path` (required): Path to the file
- `algorithm` (optional): Hash algorithm (md5, sha1, sha256, sha512) - defaults to sha256

**Usage:**
```
Ask your AI assistant: "Generate checksum for main.py" or "Get SHA256 hash of config.json"
```

**Returns:** Checksum information including:
- File path and size
- Generated checksum
- File modification time
- Generation timestamp

**Example:** Useful for verifying file integrity, detecting changes, or creating file signatures.

---

### `search_text_in_files`
**Description:** Search for text across multiple files in a directory with context.

**Parameters:**
- `search_term` (required): Text to search for
- `directory_path` (optional): Directory to search in (defaults to current)
- `file_extensions` (optional): File types to include (defaults to common text files)
- `case_sensitive` (optional): Case sensitive search (defaults to false)

**Usage:**
```
Ask your AI assistant: "Search for 'TODO' in all Python files" or "Find 'database' in my project files"
```

**Returns:** Comprehensive search results with:
- Files searched and total matches
- Line numbers and content
- Context lines before and after matches
- Match statistics

**Example Use Cases:**
- Finding TODO comments
- Locating API references
- Searching for configuration values
- Code review assistance

---

### `compare_synapse_templates`
**Description:** Compare existing files with Synapse templates and suggest improvements.

**Parameters:**
- `template_name` (required): Name of template to compare (e.g., "projectbrief.md", "requirements.md")

**Usage:**
```
Ask your AI assistant: "Compare my projectbrief.md with the template" or "Check if my requirements.md follows the template"
```

**Returns:** Comparison analysis including:
- File existence and sizes
- Missing or extra sections
- Content freshness recommendations
- Template compliance score

**Available Templates:**
- `projectbrief.md` - Project overview and goals
- `requirements.md` - Functional and technical requirements

**Example:** Helps ensure project documentation follows best practices and includes all recommended sections.

---

### `analyze_synapse_health`
**Description:** Analyze the health and completeness of your Synapse setup.

**Parameters:** None

**Usage:**
```
Ask your AI assistant: "Check my Synapse health" or "How complete is my Synapse setup?"
```

**Returns:** Comprehensive health report including:
- Overall health score (excellent/good/fair/poor)
- Core files status and presence
- Context files availability
- Specific recommendations for improvement
- Completion statistics

**Health Categories:**
- **Core Files:** Essential Synapse files (synapse_instructions.md, projectbrief.md, etc.)
- **Context Files:** Optional documentation (timeline.md, meeting_notes.md, etc.)

**Example:** Identifies missing documentation and suggests improvements for optimal Synapse functionality.

---

## 🔍 Meta Tools

These tools help you work with the Synapse system itself.

### `list_available_tools`
**Description:** List all available tools in the Synapse system.

**Usage:**
```
Ask your AI assistant: "What tools do you have?" or "List available Synapse tools"
```

**Returns:** Complete list of all registered tools with descriptions.

---

### `get_synapse_info`
**Description:** Get comprehensive information about the Synapse system.

**Usage:**
```
Ask your AI assistant: "Tell me about Synapse" or "What is this system?"
```

**Returns:** System information including:
- Architecture overview
- Component descriptions
- Usage instructions
- Feature highlights

---

## 🚀 Usage Patterns

### Basic Memory Operations
```
# Store information
"Save this to project_notes.md: [your content]"

# Retrieve information  
"Read my project_notes.md"

# Find information
"Search my memories for 'API design'"

# Organize information
"List all my memories"
```

### Project Analysis
```
# Understand project structure
"Analyze my project structure"

# Find specific content
"Search for 'TODO' in all Python files"

# Check file integrity
"Generate checksum for main.py"

# Verify documentation
"Check my Synapse health"
```

### Template Compliance
```
# Compare with templates
"Compare my projectbrief.md with the template"

# Get recommendations
"How can I improve my project documentation?"

# Check completeness
"What Synapse files am I missing?"
```

---

## 🔧 Hard-Coded Tool Architecture

Synapse uses a hard-coded tool architecture for maximum reliability and predictability:

- ✅ **All tools are explicitly defined** in `mcp_instance.py`
- ✅ **No dynamic tool discovery** - eliminates runtime surprises
- ✅ **Predictable tool availability** - consistent across restarts
- ✅ **Easy debugging** - clear visibility of all available tools

### Adding Custom Tools

To add new tools to Synapse:

1. **Define the tool function** in `mcp_instance.py`
2. **Add the `@mcp.tool()` decorator**
3. **Update the tool list** in `list_available_tools()`
4. **Restart Synapse** to load the new tool

**Example:**
```python
@mcp.tool()
def my_custom_tool(input_text: str) -> str:
    """Description of what this tool does."""
    return f"Processed: {input_text}"
```

---

## 📊 Tool Categories Summary

| Category | Tools | Purpose |
|----------|-------|---------|
| **Memory** | 5 tools | Store, retrieve, manage persistent information |
| **Config** | 2 tools | Database configuration and system settings |
| **Analysis** | 5 tools | Analyze projects, files, and structures |
| **Meta** | 2 tools | System information and tool listing |

---

## 💡 Tips for Effective Use

### 1. **Natural Language**
- Use conversational language with your AI assistant
- Be specific about what you want to accomplish
- Combine tools for complex workflows

### 2. **Memory Management**
- Use descriptive file names (e.g., `meeting_2024_01_15.md`)
- Store related information together
- Use search to find information quickly

### 3. **Project Analysis**
- Run health checks regularly
- Use structure analysis for new projects
- Compare with templates for consistency

### 4. **Workflow Integration**
- Chain tools together for complex tasks
- Use search to find relevant existing information
- Leverage auto-discovery for custom workflows

---

## 🆘 Troubleshooting

### Tool Not Found
- Verify tool is defined in `mcp_instance.py`
- Check if tool is in `list_available_tools()` list
- Ensure `@mcp.tool()` decorator is used
- Restart Synapse server

### Database Configuration Issues
- Use `config_get_database_info` to check current settings
- Ensure database file permissions are correct (DuckDB/SQLite)
- Check database file permissions (DuckDB/SQLite)
- Verify MariaDB server is running and accessible (if using MariaDB)

### Permission Errors
- Check file permissions
- Verify directory access
- Ensure proper file paths
- Check memory directory permissions

### Memory Operations
- Verify database connection using `config_get_database_info`
- Check file system permissions
- Ensure memory directory exists
- Test with different database types if needed

---

**Synapse Tools Reference** - *Making AI-Human Collaboration Seamless* 🧠⚡ 