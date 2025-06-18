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
MariaDB implementation for Synapse.
This module provides MariaDB-specific functionality for storing and retrieving synapse data.
"""
from typing import List, Optional, Dict, Any, cast, Union
from datetime import datetime
from synapse.database.base import SynapseDatabase, MemoryRecord, DatabaseConnectionError, MemoryNotFoundError

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    raise ImportError("mysql-connector-python package is required for MariaDB support. Install it with 'pip install mysql-connector-python'")


class MariaDBDatabase(SynapseDatabase):
    """MariaDB implementation of Synapse database operations."""

    def __init__(self, host: str = "localhost", port: int = 3306, 
                 user: str = "root", password: str = "", 
                 database: str = "synapse"):
        """
        Initialize MariaDB database connection.

        Args:
            host: MariaDB server host
            port: MariaDB server port
            user: MariaDB username
            password: MariaDB password
            database: MariaDB database name
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def initialize_database(self) -> None:
        """Initialize the database schema."""
        if not self.conn:
            self.connect()
        self.create_tables()

    def connect(self) -> None:
        """Connect to the MariaDB database."""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor(dictionary=True)  # Enable dictionary cursor
            assert self.conn is not None
            assert self.cursor is not None
        except MySQLError as e:
            raise DatabaseConnectionError(f"Error connecting to MariaDB: {e}")

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
            # Create database if it doesn't exist
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.cursor.execute(f"USE {self.database}")

            # Create memories table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                metadata JSON,
                version INT DEFAULT 1
            )
            ''')
            
            # Create memory history table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                version INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON
            )
            ''')
            
            self.conn.commit()
        except MySQLError as e:
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
            self.cursor.execute("SELECT id, version FROM memories WHERE filename = %s", (filename,))
            result = self.cursor.fetchone()

            if result:
                # Save to history before updating
                result_dict = cast(Dict[str, Any], result)
                old_version = int(result_dict.get('version', 1))
                self.cursor.execute(
                    "INSERT INTO memory_history (filename, content, version, metadata) "
                    "SELECT filename, content, version, metadata FROM memories WHERE filename = %s",
                    (filename,)
                )
                
                # Update existing memory
                self.cursor.execute(
                    "UPDATE memories SET content = %s, metadata = %s, version = %s WHERE filename = %s",
                    (content, metadata_json, old_version + 1, filename)
                )
            else:
                # Insert new memory
                self.cursor.execute(
                    "INSERT INTO memories (filename, content, metadata) VALUES (%s, %s, %s)",
                    (filename, content, metadata_json)
                )
                
            self.conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error saving memory: {e}")

    def load_memory(self, filename: str) -> Optional[str]:
        """Load memory content from database."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute("SELECT content FROM memories WHERE filename = %s", (filename,))
            result = self.cursor.fetchone()
            if result:
                result_dict = cast(Dict[str, Any], result)
                return cast(str, result_dict.get('content'))
            return None
        except MySQLError as e:
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
            memory_list: List[str] = []
            for result in results:
                result_dict = cast(Dict[str, Any], result)
                if 'filename' in result_dict:
                    memory_list.append(cast(str, result_dict['filename']))
            return memory_list
        except MySQLError as e:
            raise Exception(f"Error listing memories: {e}")

    def delete_memory(self, filename: str) -> bool:
        """Delete memory from database."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            # Also delete history
            self.cursor.execute("DELETE FROM memory_history WHERE filename = %s", (filename,))
            self.cursor.execute("DELETE FROM memories WHERE filename = %s", (filename,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except MySQLError as e:
            raise Exception(f"Error deleting memory: {e}")

    def get_memory_metadata(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific memory."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute("SELECT metadata, created_at, updated_at, version FROM memories WHERE filename = %s", (filename,))
            result = self.cursor.fetchone()
            
            if result:
                result_dict = cast(Dict[str, Any], result)
                metadata: Dict[str, Any] = {}
                
                if result_dict.get('metadata'):
                    import json
                    metadata_str = cast(str, result_dict.get('metadata'))
                    metadata = json.loads(metadata_str)
                
                created_at = result_dict.get('created_at')
                updated_at = result_dict.get('updated_at')
                
                metadata.update({
                    'created_at': created_at.isoformat() if created_at and hasattr(created_at, 'isoformat') else created_at,
                    'updated_at': updated_at.isoformat() if updated_at and hasattr(updated_at, 'isoformat') else updated_at,
                    'version': result_dict.get('version')
                })
                return metadata
            return None
        except MySQLError as e:
            raise Exception(f"Error getting metadata: {e}")

    def search_memories(self, query: str) -> List[Dict[str, Any]]:
        """Search memories by content."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute(
                "SELECT filename, content FROM memories WHERE content LIKE %s ORDER BY filename",
                (f"%{query}%",)
            )
            results = self.cursor.fetchall()
            search_results: List[Dict[str, Any]] = []
            
            for r in results:
                r_dict = cast(Dict[str, Any], r)
                if 'filename' in r_dict and 'content' in r_dict:
                    search_results.append({
                        'filename': cast(str, r_dict['filename']), 
                        'content': cast(str, r_dict['content'])
                    })
            
            return search_results
        except MySQLError as e:
            raise Exception(f"Error searching memories: {e}")

    def get_memory_history(self, filename: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get revision history for a memory."""
        if not self.conn or not self.cursor:
            self.initialize_database()
        assert self.conn is not None
        assert self.cursor is not None

        try:
            self.cursor.execute(
                "SELECT version, created_at, metadata FROM memory_history WHERE filename = %s "
                "ORDER BY version DESC LIMIT %s",
                (filename, limit)
            )
            results = self.cursor.fetchall()
            
            history: List[Dict[str, Any]] = []
            for result in results:
                result_dict = cast(Dict[str, Any], result)
                metadata: Dict[str, Any] = {}
                
                if result_dict.get('metadata'):
                    import json
                    metadata_str = cast(str, result_dict.get('metadata'))
                    metadata = json.loads(metadata_str)
                
                created_at = result_dict.get('created_at')
                
                history.append({
                    'version': result_dict.get('version'),
                    'created_at': created_at.isoformat() if created_at and hasattr(created_at, 'isoformat') else created_at,
                    'metadata': metadata
                })
            return history
        except MySQLError as e:
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
