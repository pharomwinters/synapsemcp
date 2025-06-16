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
# servers/__init__.py
"""
Synapse MCP Servers Package

This package contains all the specialized servers that are composed together
to create the complete Synapse functionality.

Each server handles a specific domain:
- Memory Synapse: Core memory operations (CRUD)
- Template Synapse: Template generation and project analysis
- Config Synapse: Configuration and system management  
- Guide Synapse: Documentation and help resources

The servers are composed together in mcp_instance.py to create the full
Synapse MCP platform.
"""

__version__ = "2.0.0"

from .memory_server import memory_server
from .template_server import template_server
from .config_server import config_server
from .guide_server import guide_server

__all__ = [
    "memory_server",
    "template_server", 
    "config_server",
    "guide_server"
] 