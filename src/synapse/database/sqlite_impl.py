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

from synapse.database.base import SynapseDatabase, MemoryRecord, DatabaseConnectionError, MemoryNotFoundError


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
        try:
            # Ensure directory exists
            db_dir = os.path.dirname(os.path.abspath(self.db_path))
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                
            # Connect and create tables
            self.connect()
            self.create_tables()
            
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to initialize SQLite database: {e}")

    def connect(self) -> None:
        """Connect to the SQLite database."""
        try:
            # Close existing connection if any
            if self.conn:
                self.conn.close()
                
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            self.cursor = self.conn.cursor()
            
            # Verify connection
            self.cursor.execute("SELECT 1")
            
            assert self.conn is not None
            assert self.cursor is not None
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Error connecting to SQLite database: {e}")

    def disconnect(self) -> None:
        """Disconnect from the database."""
        self.close()

    def close(self) -> None:
        """Close database connection."""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            if self.conn:
                self.conn.close()
                self.conn = None
        except sqlite3.Error as e:
            # Log warning but don't raise exception on close
            print(f"Warning: Error closing SQLite connection: {e}")

    def create_tables(self) -> None:
        """Create necessary tables if they don't exist."""
        if not self.conn or not self.cursor:
            self.connect()
        assert self.conn is not None
        assert self.cursor is not None
            
        try:
            # Create memories table
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
            
            # Create memory history table
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
            
            # Create documents table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_name TEXT UNIQUE NOT NULL,
                original_filename TEXT NOT NULL,
                file_extension TEXT NOT NULL,
                file_type TEXT NOT NULL,
                mime_type TEXT,
                file_size INTEGER NOT NULL,
                file_hash TEXT UNIQUE NOT NULL,
                stored_filename TEXT NOT NULL,
                stored_path TEXT NOT NULL,
                original_path TEXT NOT NULL,
                extracted_text TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
            ''')
            
            # Create document_tags table for better tag management
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_name TEXT NOT NULL,
                tag TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(document_name, tag)
            )
            ''')
            
            # Create indexes for better performance
            self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_memories_filename 
            ON memories(filename)
            ''')
            
            self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_memory_history_filename 
            ON memory_history(filename, version)
            ''')
            
            self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_documents_name 
            ON documents(document_name)
            ''')
            
            self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_documents_hash 
            ON documents(file_hash)
            ''')
            
            self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_documents_extension 
            ON documents(file_extension)
            ''')
            
            self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_document_tags_name 
            ON document_tags(document_name)
            ''')
            
            self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_document_tags_tag 
            ON document_tags(tag)
            ''')
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            raise DatabaseConnectionError(f"Error creating tables: {e}")

    def save_memory(self, filename: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Save memory content to database."""
        if not self.conn or not self.cursor:
            self.connect()
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
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Error saving memory: {e}")

    def load_memory(self, filename: str) -> Optional[str]:
        """Load memory content from database."""
        if not self.conn or not self.cursor:
            self.connect()
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
            self.connect()
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
            self.connect()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            # Also delete history
            self.cursor.execute("DELETE FROM memory_history WHERE filename = ?", (filename,))
            self.cursor.execute("DELETE FROM memories WHERE filename = ?", (filename,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Error deleting memory: {e}")

    def get_memory_metadata(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific memory."""
        if not self.conn or not self.cursor:
            self.connect()
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
            self.connect()
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
            self.connect()
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
        success = self.save_memory(file_name, content)
        if not success:
            raise Exception(f"Failed to store memory: {file_name}")

    def get_memory(self, file_name: str) -> Optional[str]:
        """Legacy method - use load_memory instead."""
        return self.load_memory(file_name)

    def update_memory(self, file_name: str, content: str) -> bool:
        """Legacy method - use save_memory instead."""
        return self.save_memory(file_name, content)
    
    # Document management methods
    def store_document(self, document_name: str, document_metadata: Dict[str, Any]) -> bool:
        """Store document metadata in database."""
        if not self.conn or not self.cursor:
            self.connect()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            import json
            
            # Check if document already exists
            self.cursor.execute("SELECT id FROM documents WHERE document_name = ?", (document_name,))
            result = self.cursor.fetchone()
            
            if result:
                # Update existing document
                self.cursor.execute('''
                UPDATE documents SET 
                    original_filename = ?, file_extension = ?, file_type = ?, mime_type = ?,
                    file_size = ?, file_hash = ?, stored_filename = ?, stored_path = ?,
                    original_path = ?, extracted_text = ?, tags = ?, updated_at = CURRENT_TIMESTAMP,
                    metadata = ?
                WHERE document_name = ?
                ''', (
                    document_metadata.get('original_filename'),
                    document_metadata.get('file_extension'),
                    document_metadata.get('file_type'),
                    document_metadata.get('mime_type'),
                    document_metadata.get('file_size'),
                    document_metadata.get('file_hash'),
                    document_metadata.get('stored_filename'),
                    document_metadata.get('stored_path'),
                    document_metadata.get('original_path'),
                    document_metadata.get('extracted_text'),
                    json.dumps(document_metadata.get('tags', [])),
                    json.dumps(document_metadata),
                    document_name
                ))
            else:
                # Insert new document
                self.cursor.execute('''
                INSERT INTO documents (
                    document_name, original_filename, file_extension, file_type, mime_type,
                    file_size, file_hash, stored_filename, stored_path, original_path,
                    extracted_text, tags, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    document_name,
                    document_metadata.get('original_filename'),
                    document_metadata.get('file_extension'),
                    document_metadata.get('file_type'),
                    document_metadata.get('mime_type'),
                    document_metadata.get('file_size'),
                    document_metadata.get('file_hash'),
                    document_metadata.get('stored_filename'),
                    document_metadata.get('stored_path'),
                    document_metadata.get('original_path'),
                    document_metadata.get('extracted_text'),
                    json.dumps(document_metadata.get('tags', [])),
                    json.dumps(document_metadata)
                ))
            
            # Update tags table
            self.cursor.execute("DELETE FROM document_tags WHERE document_name = ?", (document_name,))
            for tag in document_metadata.get('tags', []):
                self.cursor.execute('''
                INSERT INTO document_tags (document_name, tag) VALUES (?, ?)
                ''', (document_name, tag))
            
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Error storing document: {e}")

    def get_document(self, document_name: str) -> Optional[Dict[str, Any]]:
        """Get document metadata from database."""
        if not self.conn or not self.cursor:
            self.connect()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute('''
            SELECT original_filename, file_extension, file_type, mime_type, file_size,
                   file_hash, stored_filename, stored_path, original_path, extracted_text,
                   tags, created_at, updated_at, metadata
            FROM documents WHERE document_name = ?
            ''', (document_name,))
            result = self.cursor.fetchone()
            
            if not result:
                return None
            
            import json
            metadata = json.loads(result[13]) if result[13] else {}
            tags = json.loads(result[10]) if result[10] else []
            
            return {
                'document_name': document_name,
                'original_filename': result[0],
                'file_extension': result[1],
                'file_type': result[2],
                'mime_type': result[3],
                'file_size': result[4],
                'file_hash': result[5],
                'stored_filename': result[6],
                'stored_path': result[7],
                'original_path': result[8],
                'extracted_text': result[9],
                'tags': tags,
                'created_at': result[11],
                'updated_at': result[12],
                **metadata
            }
            
        except sqlite3.Error as e:
            raise Exception(f"Error getting document: {e}")

    def list_documents(self) -> List[str]:
        """List all document names."""
        if not self.conn or not self.cursor:
            self.connect()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute("SELECT document_name FROM documents ORDER BY document_name")
            results = self.cursor.fetchall()
            return [result[0] for result in results]
        except sqlite3.Error as e:
            raise Exception(f"Error listing documents: {e}")

    def delete_document(self, document_name: str) -> bool:
        """Delete document from database."""
        if not self.conn or not self.cursor:
            self.connect()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            # Delete tags first
            self.cursor.execute("DELETE FROM document_tags WHERE document_name = ?", (document_name,))
            
            # Delete document
            self.cursor.execute("DELETE FROM documents WHERE document_name = ?", (document_name,))
            rows_affected = self.cursor.rowcount
            
            self.conn.commit()
            return rows_affected > 0
            
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Error deleting document: {e}")

    def search_documents_by_content(self, query: str) -> List[str]:
        """Search documents by content."""
        if not self.conn or not self.cursor:
            self.connect()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute('''
            SELECT document_name FROM documents 
            WHERE extracted_text LIKE ? OR document_name LIKE ?
            ORDER BY document_name
            ''', (f'%{query}%', f'%{query}%'))
            results = self.cursor.fetchall()
            return [result[0] for result in results]
        except sqlite3.Error as e:
            raise Exception(f"Error searching documents: {e}")