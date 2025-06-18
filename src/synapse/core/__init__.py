"""
Core functionality for Synapse.

This package contains the fundamental components that all other parts of
Synapse depend on, including configuration, exceptions, and constants.
"""

from .config import Config, get_config, ConfigurationError
from .exceptions import SynapseException
from .constants import *

__all__ = [
    "Config",
    "get_config",
    "ConfigurationError", 
    "SynapseException",
] 