#!/usr/bin/env python3
"""
Migration script to refactor Synapse to the new package structure.

This script automates the process of moving files to their new locations
and updating import statements throughout the codebase.
"""

import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Tuple


class SynapseRefactorer:
    """Handles the refactoring of Synapse to the new package structure."""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.src_dir = self.root_dir / "src" / "synapse"
        
        # Define file mappings: old_path -> new_path
        self.file_mappings = {
            # Core files
            "config.py": "src/synapse/core/config.py",
            
            # Database files  
            "base.py": "src/synapse/database/base.py",
            "sqlite_db.py": "src/synapse/database/sqlite.py",
            "duckdb_db.py": "src/synapse/database/duckdb.py", 
            "mariadb.py": "src/synapse/database/mariadb.py",
            
            # Utility files
            "utils.py": "src/synapse/utils/helpers.py",
            
            # MCP files
            "mcp_instance.py": "src/synapse/mcp/instance.py",
            
            # CLI files
            "main.py": "src/synapse/cli/main.py",
            
            # Tools
            "tools/advanced_tools.py": "src/synapse/mcp/tools/advanced.py",
        }
        
        # Import mappings: old_import -> new_import
        self.import_mappings = {
            "from synapse.core.config import": "from synapse.core.config import",
            "from synapse.database.base import": "from synapse.database.base import", 
            "from synapse.utils.helpers import": "from synapse.utils.helpers import",
            "from synapse.mcp.instance import": "from synapse.mcp.instance import",
            "from synapse.core import config": "from synapse.core from synapse.core import config",
            "from synapse.database import base": "from synapse.database from synapse.database import base",
            "from synapse.utils import helpers": "from synapse.utils import helpers",
        }
    
    def create_directory_structure(self):
        """Create the new directory structure."""
        print("📁 Creating new directory structure...")
        
        directories = [
            "src/synapse/core",
            "src/synapse/database", 
            "src/synapse/mcp/tools",
            "src/synapse/mcp/servers",
            "src/synapse/storage",
            "src/synapse/services",
            "src/synapse/cli/commands",
            "src/synapse/web",
            "src/synapse/utils",
            "tests/unit/database",
            "tests/unit/mcp", 
            "tests/unit/services",
            "tests/integration",
            "tests/fixtures",
            "config",
            "data/memories",
            "data/documents",
            "data/templates"
        ]
        
        for directory in directories:
            dir_path = self.root_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {directory}")
    
    def move_files(self):
        """Move files to their new locations."""
        print("\n📄 Moving files to new locations...")
        
        for old_path, new_path in self.file_mappings.items():
            old_file = self.root_dir / old_path
            new_file = self.root_dir / new_path
            
            if old_file.exists():
                # Create parent directory if it doesn't exist
                new_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file (don't move yet, in case we need to rollback)
                shutil.copy2(old_file, new_file)
                print(f"  ✅ Copied: {old_path} -> {new_path}")
            else:
                print(f"  ⚠️  Not found: {old_path}")
    
    def update_imports(self):
        """Update import statements in all Python files."""
        print("\n🔄 Updating import statements...")
        
        python_files = list(self.root_dir.rglob("*.py"))
        
        for file_path in python_files:
            if self.should_skip_file(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply import mappings
                for old_import, new_import in self.import_mappings.items():
                    content = content.replace(old_import, new_import)
                
                # Write back if changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  ✅ Updated imports in: {file_path.relative_to(self.root_dir)}")
                    
            except Exception as e:
                print(f"  ❌ Error updating {file_path}: {e}")
    
    def should_skip_file(self, file_path: Path) -> bool:
        """Check if a file should be skipped during import updates."""
        skip_patterns = [
            ".venv/",
            "__pycache__/", 
            ".git/",
            "build/",
            "dist/",
            ".pytest_cache/",
            "node_modules/"
        ]
        
        file_str = str(file_path)
        return any(pattern in file_str for pattern in skip_patterns)
    
    def create_init_files(self):
        """Create __init__.py files for all packages."""
        print("\n📝 Creating __init__.py files...")
        
        # Already created the main ones, let's create the remaining ones
        init_files = [
            "src/synapse/database/__init__.py",
            "src/synapse/mcp/__init__.py", 
            "src/synapse/mcp/tools/__init__.py",
            "src/synapse/mcp/servers/__init__.py",
            "src/synapse/storage/__init__.py",
            "src/synapse/services/__init__.py",
            "src/synapse/cli/__init__.py",
            "src/synapse/cli/commands/__init__.py",
            "src/synapse/web/__init__.py",
            "src/synapse/utils/__init__.py",
            "tests/__init__.py",
            "tests/unit/__init__.py",
            "tests/unit/database/__init__.py",
            "tests/unit/mcp/__init__.py",
            "tests/unit/services/__init__.py",
            "tests/integration/__init__.py",
        ]
        
        for init_file in init_files:
            init_path = self.root_dir / init_file
            if not init_path.exists():
                init_path.touch()
                print(f"  ✅ Created: {init_file}")
    
    def update_pyproject_toml(self):
        """Update pyproject.toml for the new package structure."""
        print("\n⚙️  Updating pyproject.toml...")
        
        pyproject_path = self.root_dir / "pyproject.toml"
        if not pyproject_path.exists():
            print("  ⚠️  pyproject.toml not found")
            return
        
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Update package configuration
        content = re.sub(
            r'\[project\.scripts\]\nsynapse = "main:main"',
            '[project.scripts]\nsynapse = "synapse.cli.main:main"',
            content
        )
        
        # Update hatch version path
        content = re.sub(
            r'\[tool\.hatch\.version\]\npath = "main\.py"',
            '[tool.hatch.version]\npath = "src/synapse/__version__.py"',
            content 
        )
        
        with open(pyproject_path, 'w') as f:
            f.write(content)
        
        print("  ✅ Updated pyproject.toml")
    
    def move_config_files(self):
        """Move configuration files to the config directory."""
        print("\n🔧 Moving configuration files...")
        
        config_files = [
            "config.dev.json",
            "config.test.json", 
            "config.prod.json",
            "config.dev.mariadb.json"
        ]
        
        for config_file in config_files:
            old_path = self.root_dir / config_file
            new_name = config_file.replace("config.", "").replace(".json", ".json")
            new_path = self.root_dir / "config" / new_name
            
            if old_path.exists():
                shutil.copy2(old_path, new_path)
                print(f"  ✅ Copied: {config_file} -> config/{new_name}")
    
    def run_migration(self):
        """Run the complete migration process."""
        print("🚀 Starting Synapse refactoring migration...\n")
        
        try:
            self.create_directory_structure()
            self.move_files()
            self.create_init_files()
            self.move_config_files()
            self.update_pyproject_toml()
            self.update_imports()
            
            print("\n✅ Migration completed successfully!")
            print("\n📋 Next steps:")
            print("1. Test the new structure: python -m pytest tests/")
            print("2. Run the application: python -m synapse.cli.main")
            print("3. Update any remaining import issues")
            print("4. Remove old files after testing")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            raise


if __name__ == "__main__":
    import sys
    
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    refactorer = SynapseRefactorer(root_dir)
    refactorer.run_migration() 