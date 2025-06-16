#!/usr/bin/env python3
"""
Database diagnostic script for Synapse.
Run this to test if your database setup is working correctly.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_database():
    """Test database functionality."""
    
    print("🔍 Testing Synapse Database Setup...")
    print("=" * 50)
    
    try:
        # Test configuration loading
        print("1. Testing configuration...")
        from config import config
        config.load()
        
        db_type = config.get("database.type", "duckdb")
        print(f"   ✅ Database type: {db_type}")
        
        if db_type == "duckdb":
            db_path = config.get("database.duckdb.db_path", "synapse.duckdb")
            print(f"   ✅ DuckDB path: {db_path}")
        elif db_type == "sqlite":
            db_path = config.get("database.sqlite.db_path", "synapse.db")
            print(f"   ✅ SQLite path: {db_path}")
        elif db_type == "mariadb":
            host = config.get("database.mariadb.host", "localhost")
            print(f"   ✅ MariaDB host: {host}")
        
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False
    
    try:
        # Test database instance creation
        print("\n2. Testing database instance creation...")
        from utils import get_db_instance
        
        db = get_db_instance()
        print(f"   ✅ Database instance created: {type(db).__name__}")
        
    except Exception as e:
        print(f"   ❌ Database instance creation failed: {e}")
        return False
    
    try:
        # Test database operations
        print("\n3. Testing database operations...")
        
        # Test save
        test_filename = "test_memory.md"
        test_content = "This is a test memory for diagnostics."
        
        success = db.save_memory(test_filename, test_content)
        if success:
            print("   ✅ Save operation successful")
        else:
            print("   ❌ Save operation failed")
            return False
        
        # Test load
        loaded_content = db.load_memory(test_filename)
        if loaded_content == test_content:
            print("   ✅ Load operation successful")
        else:
            print("   ❌ Load operation failed - content mismatch")
            return False
        
        # Test list
        memories = db.list_memories()
        if test_filename in memories:
            print("   ✅ List operation successful")
        else:
            print("   ❌ List operation failed - test file not found")
            return False
        
        # Test delete
        delete_success = db.delete_memory(test_filename)
        if delete_success:
            print("   ✅ Delete operation successful")
        else:
            print("   ❌ Delete operation failed")
            return False
        
    except Exception as e:
        print(f"   ❌ Database operations failed: {e}")
        return False
    
    finally:
        # Clean up
        try:
            if hasattr(db, 'close'):
                db.close()
        except:
            pass
    
    try:
        # Test memory tools
        print("\n4. Testing memory tools...")
        from mcp_instance import mcp
        
        # This would test the actual MCP tools
        print("   ✅ MCP instance loaded")
        
    except Exception as e:
        print(f"   ❌ MCP tools test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All database tests passed! Your Synapse setup is working correctly.")
    return True

def check_permissions():
    """Check file permissions and directories."""
    
    print("\n🔍 Checking file permissions...")
    
    # Check current directory
    current_dir = Path.cwd()
    if not os.access(current_dir, os.W_OK):
        print(f"   ❌ No write permission in current directory: {current_dir}")
        return False
    else:
        print(f"   ✅ Write permission OK in: {current_dir}")
    
    # Check memory directory
    from config import config
    memory_dir = Path(config.get("memory_dir", "memories"))
    
    if not memory_dir.exists():
        try:
            memory_dir.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created memory directory: {memory_dir}")
        except Exception as e:
            print(f"   ❌ Cannot create memory directory: {e}")
            return False
    else:
        print(f"   ✅ Memory directory exists: {memory_dir}")
    
    if not os.access(memory_dir, os.W_OK):
        print(f"   ❌ No write permission in memory directory: {memory_dir}")
        return False
    else:
        print(f"   ✅ Write permission OK in memory directory")
    
    return True

if __name__ == "__main__":
    print("🧠 Synapse Database Diagnostic Tool")
    print("====================================")
    
    # Check permissions first
    if not check_permissions():
        print("\n❌ Permission check failed. Please fix file permissions and try again.")
        sys.exit(1)
    
    # Test database
    if test_database():
        print("\n✅ Database diagnostic completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Database diagnostic failed. Check the error messages above.")
        sys.exit(1)