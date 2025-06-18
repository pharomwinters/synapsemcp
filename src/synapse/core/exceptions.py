"""
Exception classes for Synapse.

This module defines all custom exceptions used throughout the Synapse system.
Having centralized exception handling makes error management more consistent
and easier to maintain.
"""


class SynapseException(Exception):
    """Base exception for all Synapse-related errors."""
    pass


class DatabaseError(SynapseException):
    """Raised when database operations fail."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when database connection fails."""
    pass


class MemoryNotFoundError(SynapseException):
    """Raised when a requested memory file is not found."""
    pass


class DocumentError(SynapseException):
    """Raised when document operations fail."""
    pass


class DocumentNotFoundError(DocumentError):
    """Raised when a requested document is not found."""
    pass


class TemplateError(SynapseException):
    """Raised when template operations fail."""
    pass


class ConfigurationError(SynapseException):
    """Raised when configuration is invalid or missing."""
    pass


class ValidationError(SynapseException):
    """Raised when data validation fails."""
    pass


class ServiceError(SynapseException):
    """Raised when service operations fail."""
    pass 