# ARCHIVED: This test file is archived due to incompatibility with the current implementation (missing memory_exists method, etc.).
# To restore, update the tests and implementation to match current codebase.
import os
import sys
import unittest
import tempfile
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlite_db import SynapseDatabase

class TestSynapseDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_synapse.db"
        self.db = SynapseDatabase(str(self.db_path))
        self.db.initialize_database()

    def tearDown(self):
        # Clean up after the test
        if hasattr(self.db, 'close'):
            self.db.close()
        self.temp_dir.cleanup()
    
    def test_initialize_database(self):
        # Test that the database was created
        self.assertTrue(self.db_path.exists())
        
        # Test that the table was created
        memories = self.db.list_memories()
        self.assertIsInstance(memories, list)
    
    def test_save_and_load_memory(self):
        # Test storing and retrieving a memory
        test_file_name = "test_memory.md"
        test_content = "This is a test memory content for Synapse."
        
        # Store the memory
        self.db.save_memory(test_file_name, test_content)
        
        # Retrieve the memory
        retrieved_content = self.db.load_memory(test_file_name)
        
        # Assert that the retrieved content matches the original
        self.assertEqual(retrieved_content, test_content)
    
    def test_list_memories(self):
        # Test listing memories
        memories = self.db.list_memories()
        initial_count = len(memories)
        
        # Add a memory
        self.db.save_memory("test_list.md", "Test content")
        
        # Check that the list now contains the new memory
        memories = self.db.list_memories()
        self.assertEqual(len(memories), initial_count + 1)
        self.assertIn("test_list.md", memories)
    
    def test_memory_exists(self):
        # Test checking if a memory exists
        test_file_name = "test_exists.md"
        
        # Initially, the memory should not exist
        self.assertFalse(self.db.memory_exists(test_file_name))
        
        # After saving, it should exist
        self.db.save_memory(test_file_name, "Test content")
        self.assertTrue(self.db.memory_exists(test_file_name))
    
    def test_delete_memory(self):
        # Test deleting a memory
        test_file_name = "test_delete.md"
        
        # Save a memory
        self.db.save_memory(test_file_name, "Content to delete")
        self.assertTrue(self.db.memory_exists(test_file_name))
        
        # Delete the memory
        self.db.delete_memory(test_file_name)
        self.assertFalse(self.db.memory_exists(test_file_name))
    
    def test_search_memories(self):
        # Test searching memories
        test_memories = [
            ("python_guide.md", "Python is a programming language"),
            ("javascript_guide.md", "JavaScript is used for web development"),
            ("database_guide.md", "SQL databases store data in tables")
        ]
        
        # Save test memories
        for file_name, content in test_memories:
            self.db.save_memory(file_name, content)
        
        # Search for memories
        results = self.db.search_memories("programming")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["file_name"], "python_guide.md")
        
        results = self.db.search_memories("guide")
        self.assertEqual(len(results), 3)
        
        # Case insensitive search
        results = self.db.search_memories("PYTHON")
        self.assertEqual(len(results), 1)
    
    def test_load_nonexistent_memory(self):
        # Test loading a memory that doesn't exist
        with self.assertRaises(Exception):
            self.db.load_memory("nonexistent.md")
    
    def test_delete_nonexistent_memory(self):
        # Test deleting a memory that doesn't exist
        with self.assertRaises(Exception):
            self.db.delete_memory("nonexistent.md")
    
    def test_update_memory(self):
        # Test updating an existing memory
        test_file_name = "test_update.md"
        original_content = "Original content"
        updated_content = "Updated content"
        
        # Save original content
        self.db.save_memory(test_file_name, original_content)
        self.assertEqual(self.db.load_memory(test_file_name), original_content)
        
        # Update the memory
        self.db.save_memory(test_file_name, updated_content)
        self.assertEqual(self.db.load_memory(test_file_name), updated_content)
    
    def test_empty_content(self):
        # Test saving empty content
        test_file_name = "empty_test.md"
        empty_content = ""
        
        self.db.save_memory(test_file_name, empty_content)
        retrieved_content = self.db.load_memory(test_file_name)
        self.assertEqual(retrieved_content, empty_content)
    
    def test_special_characters(self):
        # Test handling special characters in content
        test_file_name = "special_chars.md"
        special_content = "Content with special chars: áéíóú ñ ¿¡ 中文 🎉"
        
        self.db.save_memory(test_file_name, special_content)
        retrieved_content = self.db.load_memory(test_file_name)
        self.assertEqual(retrieved_content, special_content)

if __name__ == '__main__':
    unittest.main()
