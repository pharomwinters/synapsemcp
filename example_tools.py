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
# example_tools.py - Example of using auto-discovery for MCP tools

from utils import mcp_tool
import asyncio

# Example tools using the @mcp_tool decorator for auto-discovery

@mcp_tool
def calculate_sum(a: float, b: float) -> float:
    """Calculate the sum of two numbers."""
    return a + b

@mcp_tool
def calculate_product(a: float, b: float) -> float:
    """Calculate the product of two numbers."""
    return a * b

@mcp_tool
async def async_greeting(name: str) -> str:
    """Generate an async greeting."""
    await asyncio.sleep(0.1)  # Simulate async work
    return f"Hello, {name}! (from async function)"

@mcp_tool
def get_system_info() -> dict:
    """Get basic system information."""
    import platform
    return {
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "machine": platform.machine()
    }

# This function won't be registered (no @mcp_tool decorator)
def internal_helper():
    """This won't be auto-discovered."""
    return "internal"

# Neither will this (starts with underscore)
def _private_function():
    """This won't be auto-discovered either."""
    return "private"


# Example usage in main file:
"""
from mcp.server.fastmcp import FastMCP
from utils import auto_discover_tools

mcp = FastMCP("Auto-Discovery Demo")

# Auto-discover tools from this module
tools_registered = auto_discover_tools(mcp, 'example_tools', verbose=True)
print(f"Registered {tools_registered} tools automatically")

# Or discover from multiple modules with prefixes
auto_discover_tools(mcp, 'database_tools', prefix='db_')
auto_discover_tools(mcp, 'api_tools', prefix='api_')
""" 