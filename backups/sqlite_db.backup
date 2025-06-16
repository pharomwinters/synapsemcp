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
SQLite database implementation for Synapse.
This module provides SQLite-specific functionality for storing and retrieving synapse data.
"""
import os
import sqlite3
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime

from base import SynapseDatabase, MemoryRecord, DatabaseConnectionError, MemoryNotFoundError


class SQLiteDatabase(SynapseDatabase):
    """SQLite implementation of Synapse database operations."""

    def __init__(self, db_path: str = "synapse.db"):
        """
        Initialize SQLite database connection.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def initialize_database(self) -> None:
        """Initialize the database schema."""
        if not self.conn:
            self.connect()
        self.create_tables()

    def connect(self) -> None:
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            self.cursor = self.conn.cursor()
            assert self.conn is not None
            assert self.cursor is not None
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Error connecting to SQLite database: {e}")

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def create_tables(self) -> None:
        """Create necessary tables if they don't exist."""
        if not self.conn or not self.cursor:
            self.connect()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                version INTEGER DEFAULT 1
            )
            ''')
            
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Error creating tables: {e}")

    def save_memory(self, filename: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Save memory content to database."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            metadata_json = None
            if metadata:
                import json
                metadata_json = json.dumps(metadata)

            # Check if memory already exists
            self.cursor.execute("SELECT id, version FROM memories WHERE filename = ?", (filename,))
            result = self.cursor.fetchone()

            if result:
                # Save to history before updating
                old_version = result['version']
                self.cursor.execute(
                    "INSERT INTO memory_history (filename, content, version, metadata) "
                    "SELECT filename, content, version, metadata FROM memories WHERE filename = ?",
                    (filename,)
                )
                
                # Update existing memory
                self.cursor.execute(
                    "UPDATE memories SET content = ?, updated_at = CURRENT_TIMESTAMP, metadata = ?, version = ? WHERE filename = ?",
                    (content, metadata_json, old_version + 1, filename)
                )
            else:
                # Insert new memory
                self.cursor.execute(
                    "INSERT INTO memories (filename, content, metadata) VALUES (?, ?, ?)",
                    (filename, content, metadata_json)
                )
                
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            raise Exception(f"Error saving memory: {e}")

    def load_memory(self, filename: str) -> Optional[str]:
        """Load memory content from database."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute("SELECT content FROM memories WHERE filename = ?", (filename,))
            result = self.cursor.fetchone()
            return result['content'] if result else None
        except sqlite3.Error as e:
            raise Exception(f"Error loading memory: {e}")

    def list_memories(self) -> List[str]:
        """List all memory filenames."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute("SELECT filename FROM memories ORDER BY filename")
            results = self.cursor.fetchall()
            return [result['filename'] for result in results]
        except sqlite3.Error as e:
            raise Exception(f"Error listing memories: {e}")

    def delete_memory(self, filename: str) -> bool:
        """Delete memory from database."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            # Also delete history
            self.cursor.execute("DELETE FROM memory_history WHERE filename = ?", (filename,))
            self.cursor.execute("DELETE FROM memories WHERE filename = ?", (filename,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            raise Exception(f"Error deleting memory: {e}")

    def get_memory_metadata(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific memory."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute("SELECT metadata, created_at, updated_at, version FROM memories WHERE filename = ?", (filename,))
            result = self.cursor.fetchone()
            
            if result:
                metadata = {}
                if result['metadata']:
                    import json
                    metadata = json.loads(result['metadata'])
                
                metadata.update({
                    'created_at': result['created_at'],
                    'updated_at': result['updated_at'],
                    'version': result['version']
                })
                return metadata
            return None
        except sqlite3.Error as e:
            raise Exception(f"Error getting metadata: {e}")

    def search_memories(self, query: str) -> List[Dict[str, Any]]:
        """Search memories by content."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute(
                "SELECT filename, content FROM memories WHERE content LIKE ? ORDER BY filename",
                (f"%{query}%",)
            )
            results = self.cursor.fetchall()
            return [{'filename': r['filename'], 'content': r['content']} for r in results]
        except sqlite3.Error as e:
            raise Exception(f"Error searching memories: {e}")

    def get_memory_history(self, filename: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get revision history for a memory."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute(
                "SELECT version, created_at, metadata FROM memory_history WHERE filename = ? "
                "ORDER BY version DESC LIMIT ?",
                (filename, limit)
            )
            results = self.cursor.fetchall()
            
            history = []
            for result in results:
                metadata = {}
                if result['metadata']:
                    import json
                    metadata = json.loads(result['metadata'])
                
                history.append({
                    'version': result['version'],
                    'created_at': result['created_at'],
                    'metadata': metadata
                })
            return history
        except sqlite3.Error as e:
            raise Exception(f"Error getting memory history: {e}")

    # Legacy methods for compatibility
    def store_memory(self, file_name: str, content: str) -> None:
        """Legacy method - use save_memory instead."""
        self.save_memory(file_name, content)

    def get_memory(self, file_name: str) -> Optional[str]:
        """Legacy method - use load_memory instead."""
        return self.load_memory(file_name)

    def update_memory(self, file_name: str, content: str) -> bool:
        """Legacy method - use save_memory instead."""
        return self.save_memory(file_name, content)
