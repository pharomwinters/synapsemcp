#!/usr/bin/env python3
"""Test file to debug import issues."""

try:
    print("Testing basic imports...")
    from src.synapse.core.config import get_config
    print("✅ Config import works")
    
    from src.synapse.utils.helpers import MemoryFileSystem
    print("✅ Utils import works")
    
    print("Attempting MCP import...")
    from src.synapse.mcp import mcp
    print("✅ MCP import works")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc() 