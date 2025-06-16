#
# This file is part of Synapse.
#
# Synapse is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Synapse is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Synapse.  If not, see <https://www.gnu.org/licenses/>.
#
"""
Guide Server - Documentation and help system for Synapse.

This server provides access to guides, documentation, and help resources
for the Synapse platform.
"""

from fastmcp import FastMCP
import os
from pathlib import Path
from typing import Dict, List, Optional

# Local imports
from guides.setup import GUIDE as SETUP_GUIDE
from guides.usage import GUIDE as USAGE_GUIDE
from guides.benefits import GUIDE as BENEFITS_GUIDE
from guides.structure import GUIDE as STRUCTURE_GUIDE

# Create Guide Server instance
guide_server = FastMCP("Guide Synapse")

# Available guides
GUIDES = {
    "setup": SETUP_GUIDE,
    "usage": USAGE_GUIDE,
    "benefits": BENEFITS_GUIDE,
    "structure": STRUCTURE_GUIDE
}

@guide_server.tool()
async def get_synapse_structure() -> str:
    """Get detailed description of Synapse file structure and organization."""
    
    return STRUCTURE_GUIDE

@guide_server.tool()
async def get_guide(guide_name: str) -> str:
    """
    Get a specific Synapse guide.
    
    Args:
        guide_name: Name of the guide (setup, usage, benefits, structure)
        
    Returns:
        Guide content as string
    """
    guide_modules = {
        "setup": "guides.setup",
        "usage": "guides.usage", 
        "benefits": "guides.benefits",
        "structure": "guides.structure"
    }
    
    if guide_name not in guide_modules:
        return f"Guide '{guide_name}' not found. Available guides: {', '.join(guide_modules.keys())}"
    
    try:
        module_name = guide_modules[guide_name]
        module = __import__(module_name, fromlist=['GUIDE'])
        return module.GUIDE
    except ImportError:
        return f"Guide module '{guide_name}' could not be loaded"

@guide_server.tool()
async def list_available_guides() -> List[str]:
    """List all available Synapse guides."""
    
    return [
        "setup - Getting started with Synapse",
        "usage - How to use Synapse effectively", 
        "benefits - Benefits of using Synapse",
        "structure - Synapse file structure and organization"
    ]

@guide_server.tool()
async def search_guides(query: str) -> List[Dict[str, str]]:
    """
    Search through guides for content matching the query.
    
    Args:
        query: Search term to look for in guide content
        
    Returns:
        List of matching guide sections with content
    """
    results = []
    guide_modules = ["setup", "usage", "benefits", "structure"]
    
    for guide_name in guide_modules:
        try:
            module_name = f"guides.{guide_name}"
            module = __import__(module_name, fromlist=['GUIDE'])
            guide_content = module.GUIDE
            
            if query.lower() in guide_content.lower():
                # Find lines containing the query
                lines = guide_content.split('\n')
                matching_lines = [line for line in lines if query.lower() in line.lower()]
                
                results.append({
                    "guide": guide_name,
                    "matches": matching_lines[:3],  # First 3 matches
                    "total_matches": len(matching_lines)
                })
        except ImportError:
            continue
    
    return results

@guide_server.tool()
async def get_quick_start() -> str:
    """Get quick start guide for Synapse."""
    
    return """## Synapse Quick Start

1. **Install**: `pip install -r requirements.txt`
2. **Run**: `python main.py`
3. **Configure**: Add to your AI assistant's MCP config
4. **Test**: Ask your AI assistant to list available tools

For detailed setup, use the 'setup' guide."""

@guide_server.tool()
async def get_troubleshooting() -> str:
    """Get troubleshooting help for common Synapse issues."""
    
    return """## Synapse Troubleshooting

**Server won't start:**
- Check Python version (3.12+)
- Verify dependencies installed
- Check configuration files

**Database errors:**
- Verify database configuration
- Check file permissions
- Ensure database server running (MariaDB)

**AI assistant can't connect:**
- Verify MCP configuration
- Check server path in config
- Restart AI assistant

**Auto-discovery not working:**
- Check SYNAPSE_AUTO_DISCOVER environment variable
- Verify tool decorators (@mcp_tool)
- Check file patterns

For more help, check the specific guides or documentation."""

# Define resource handler for dynamic guide access
@guide_server.resource("synapse_guide://{section}")
async def synapse_guide(section: str) -> tuple[str, str]:
    """Dynamic access to Synapse guides and documentation."""
    
    # Use the GUIDES dictionary directly instead of calling the get_guide tool
    if section in GUIDES:
        guide_content = GUIDES[section]
    else:
        guide_content = f"Guide '{section}' not found. Available guides: {', '.join(GUIDES.keys())}"
    
    return f"text/markdown", guide_content

# Export the server
__all__ = ["guide_server"] 