# servers/guide_server.py
"""
Guide Server - Documentation and guides for Synapse.

Handles guides, documentation resources, and help content.
"""

from mcp.server.fastmcp import FastMCP
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from guides.setup import GUIDE as SETUP_GUIDE
from guides.usage import GUIDE as USAGE_GUIDE
from guides.benefits import GUIDE as BENEFITS_GUIDE
from guides.structure import GUIDE as STRUCTURE_GUIDE

# Create the guide server
guide_server = FastMCP("Synapse-Guides")

GUIDES = {
    "setup": SETUP_GUIDE,
    "usage": USAGE_GUIDE,
    "benefits": BENEFITS_GUIDE,
    "structure": STRUCTURE_GUIDE
}


@guide_server.tool()
async def get_memory_bank_structure() -> str:
    """Get a detailed description of the Synapse file structure."""
    return GUIDES["structure"]


@guide_server.tool()
async def get_guide(guide_name: str) -> str:
    """Get a specific Synapse guide.
    
    Args:
        guide_name: Name of the guide (setup, usage, benefits, structure)
    """
    if guide_name in GUIDES:
        return f"# Synapse Guide: {guide_name.title()}\n\n{GUIDES[guide_name]}"
    else:
        available_guides = ", ".join(GUIDES.keys())
        return f"Guide '{guide_name}' not found. Available guides: {available_guides}"


@guide_server.tool()
async def list_available_guides() -> dict:
    """List all available Synapse guides."""
    guide_descriptions = {
        "setup": "Instructions for setting up and configuring Synapse",
        "usage": "How to use Synapse effectively in your workflow",
        "benefits": "Benefits and advantages of using Synapse",
        "structure": "Detailed explanation of Synapse file structure and organization"
    }
    
    return {
        "available_guides": list(GUIDES.keys()),
        "descriptions": guide_descriptions,
        "total_count": len(GUIDES)
    }


@guide_server.tool()
async def search_guides(query: str) -> dict:
    """Search through all guides for content matching the query.
    
    Args:
        query: Search term to look for in guide content
    """
    results = {}
    query_lower = query.lower()
    
    for guide_name, guide_content in GUIDES.items():
        if query_lower in guide_content.lower():
            # Find the context around the match
            lines = guide_content.split('\n')
            matching_lines = []
            
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    # Add some context around the match
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context = '\n'.join(lines[start:end])
                    matching_lines.append({
                        "line_number": i + 1,
                        "context": context
                    })
            
            if matching_lines:
                results[guide_name] = {
                    "matches": len(matching_lines),
                    "contexts": matching_lines[:3]  # Limit to first 3 matches
                }
    
    return {
        "query": query,
        "total_guides_searched": len(GUIDES),
        "guides_with_matches": len(results),
        "results": results
    }


# Add resources for guide access
@guide_server.resource("memory_bank_guide://{section}")
async def memory_bank_guide(section: str) -> tuple[str, str]:
    """Provide guidance on Synapse setup and usage.

    Args:
        section: The section of the guide to retrieve
    """
    if section in GUIDES:
        content = f"# Synapse Guide: {section}\n\n{GUIDES[section]}"
        return content, "text/markdown"
    else:
        available_guides = ", ".join(GUIDES.keys())
        return f"Guide for {section} not found. Available guides: {available_guides}", "text/plain"


# For standalone testing
if __name__ == "__main__":
    guide_server.run() 