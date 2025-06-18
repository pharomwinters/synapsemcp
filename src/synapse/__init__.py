"""
Synapse - AI-Human Collaboration Platform

A sophisticated MCP (Model Context Protocol) platform for AI-human collaboration
with advanced memory management, document processing, and template generation.
"""

from .__version__ import __version__

__author__ = "Synapse Team"
__email__ = "team@synapse-platform.org"
__license__ = "GPL-3.0-or-later"

# Core exports
from .core.config import Config, get_config
from .core.exceptions import SynapseException

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__license__",
    "Config",
    "get_config", 
    "SynapseException",
] 