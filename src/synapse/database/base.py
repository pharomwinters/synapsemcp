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
Base database interface for Synapse.

This module defines the abstract base class for all database implementations.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


class SynapseDatabase(ABC):
    """Base class for Synapse database operations."""
    
    @abstractmethod
    def __init__(self, **kwargs):
        """Initialize the database connection."""
        pass
    
    @abstractmethod
    def initialize_database(self) -> None:
        """Initialize the database schema."""
        pass
    
    @abstractmethod
    def save_memory(self, filename: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Save memory content to database."""
        pass
    
    @abstractmethod
    def load_memory(self, filename: str) -> Optional[str]:
        """Load memory content from database."""
        pass
    
    @abstractmethod
    def list_memories(self) -> List[str]:
        """List all memory filenames."""
        pass
    
    @abstractmethod
    def delete_memory(self, filename: str) -> bool:
        """Delete memory from database."""
        pass
    
    @abstractmethod
    def get_memory_metadata(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific memory."""
        pass
    
    @abstractmethod
    def search_memories(self, query: str) -> List[Dict[str, Any]]:
        """Search memories by content."""
        pass
    
    @abstractmethod
    def get_memory_history(self, filename: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get revision history for a memory."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close database connection."""
        pass

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def create_tables(self) -> None:
        pass

    @abstractmethod
    def store_memory(self, file_name: str, content: str) -> None:
        pass

    @abstractmethod
    def get_memory(self, file_name: str) -> Optional[str]:
        pass


@dataclass
class MemoryRecord:
    """Data structure for memory records."""
    filename: str
    content: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None
    version: int = 1


class SynapseException(Exception):
    """Base exception for synapse operations."""
    pass


class DatabaseConnectionError(SynapseException):
    """Raised when database connection fails."""
    pass


class MemoryNotFoundError(SynapseException):
    """Raised when a memory is not found."""
    pass


class MemoryAlreadyExistsError(SynapseException):
    """Raised when trying to create a memory that already exists."""
    pass