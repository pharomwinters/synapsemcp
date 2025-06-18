"""
Database models and exceptions for Synapse.

This module contains data models, exceptions, and schemas used by the database layer.
"""

from ..core.exceptions import SynapseException


class DatabaseConnectionError(SynapseException):
    """Raised when database connection fails."""
    pass


class MemoryNotFoundError(SynapseException):
    """Raised when a memory is not found."""
    pass


class MemoryAlreadyExistsError(SynapseException):
    """Raised when trying to create a memory that already exists."""
    pass 