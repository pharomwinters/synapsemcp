#!/usr/bin/env python3
"""
Cleanup script to move remaining files from root directory to proper locations
and remove duplicates after the main refactoring.
"""

import os
import shutil
from pathlib import Path
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CleanupManager:
    def __init__(self):
        self.root_dir = Path(".")
        self.src_dir = Path("src/synapse")
        
        # Files to move from root to their proper locations
        self.file_moves = {
            # Database files
            "duckdb_db.py": "src/synapse/database/duckdb_impl.py",
            "sqlite_db.py": "src/synapse/database/sqlite_impl.py", 
            "mariadb.py": "src/synapse/database/mariadb_impl.py",
            "base.py": "src/synapse/database/base.py",  # Only if different from existing
            
            # MCP files
            "mcp_instance.py": "src/synapse/mcp/instance.py",
            
            # Utils files
            "utils.py": "src/synapse/utils/helpers.py",
            
            # Config file (old one)
            "config.py": None,  # Delete - we have the new one
            
            # Server files
            "server.py": "src/synapse/web/server.py",
            
            # Tools
            "example_tools.py": "src/synapse/mcp/tools/example_tools.py",
            
            # CLI
            "main.py": "src/synapse/cli/main.py",
            
            # Test files
            "test_database.py": "tests/unit/test_database.py",
            "test_import.py": "tests/unit/test_import.py",
        }
        
        # Directories to move
        self.dir_moves = {
            "servers/": "src/synapse/services/",
            "tools/": "src/synapse/mcp/tools/",
        }
        
        # Files to delete (duplicates or no longer needed)
        self.files_to_delete = [
            "config.prod.json",  # We have these in root already
            "config.dev.json",
            "config.test.json",
        ]
        
        # Config directory cleanup
        self.config_cleanup = {
            "config/dev.json": "config.dev.json",
            "config/test.json": "config.test.json", 
            "config/prod.json": "config.prod.json",
            "config/dev.mariadb.json": "config.dev.mariadb.json"
        }

    def cleanup_config_files(self):
        """Clean up config file duplicates"""
        logger.info("Cleaning up config files...")
        
        # Move config/ files to root if they're newer/different
        for old_path, new_path in self.config_cleanup.items():
            old_file = Path(old_path)
            new_file = Path(new_path)
            
            if old_file.exists():
                if not new_file.exists():
                    logger.info(f"Moving {old_path} to {new_path}")
                    shutil.move(str(old_file), str(new_file))
                else:
                    # Check if they're different
                    if self._files_different(old_file, new_file):
                        logger.warning(f"Config files differ: {old_path} vs {new_path}")
                        logger.warning("Keeping root version and removing config/ version")
                    os.remove(old_file)
                    logger.info(f"Removed duplicate: {old_path}")
        
        # Remove empty config directory
        config_dir = Path("config")
        if config_dir.exists() and not any(config_dir.iterdir()):
            config_dir.rmdir()
            logger.info("Removed empty config/ directory")

    def _files_different(self, file1: Path, file2: Path) -> bool:
        """Check if two files are different"""
        try:
            if file1.suffix == '.json' and file2.suffix == '.json':
                with open(file1) as f1, open(file2) as f2:
                    return json.load(f1) != json.load(f2)
            else:
                return file1.read_text() != file2.read_text()
        except Exception:
            return True

    def move_files(self):
        """Move individual files to their new locations"""
        logger.info("Moving files to proper locations...")
        
        for old_path, new_path in self.file_moves.items():
            old_file = Path(old_path)
            
            if not old_file.exists():
                continue
                
            if new_path is None:
                # Delete file
                os.remove(old_file)
                logger.info(f"Deleted: {old_path}")
                continue
            
            new_file = Path(new_path)
            
            # Create parent directories if they don't exist
            new_file.parent.mkdir(parents=True, exist_ok=True)
            
            if new_file.exists():
                # Check if files are different
                if not self._files_different(old_file, new_file):
                    # Files are the same, just remove the old one
                    os.remove(old_file)
                    logger.info(f"Removed duplicate: {old_path}")
                else:
                    # Files are different, backup the new one and move
                    backup_path = str(new_file) + ".backup"
                    shutil.move(str(new_file), backup_path)
                    shutil.move(str(old_file), str(new_file))
                    logger.info(f"Moved {old_path} to {new_path} (backed up existing)")
            else:
                # Move file to new location
                shutil.move(str(old_file), str(new_file))
                logger.info(f"Moved {old_path} to {new_path}")

    def move_directories(self):
        """Move directories to their new locations"""
        logger.info("Moving directories...")
        
        for old_dir, new_dir in self.dir_moves.items():
            old_path = Path(old_dir)
            new_path = Path(new_dir)
            
            if not old_path.exists():
                continue
            
            # Create parent directory if it doesn't exist
            new_path.parent.mkdir(parents=True, exist_ok=True)
            
            if new_path.exists():
                # Merge directories
                self._merge_directories(old_path, new_path)
                # Remove old directory if empty
                try:
                    old_path.rmdir()
                    logger.info(f"Removed empty directory: {old_dir}")
                except OSError:
                    logger.warning(f"Directory not empty, keeping: {old_dir}")
            else:
                # Move entire directory
                shutil.move(str(old_path), str(new_path))
                logger.info(f"Moved directory {old_dir} to {new_dir}")

    def _merge_directories(self, src_dir: Path, dst_dir: Path):
        """Merge contents of src_dir into dst_dir"""
        for item in src_dir.iterdir():
            dst_item = dst_dir / item.name
            
            if item.is_file():
                if dst_item.exists():
                    if not self._files_different(item, dst_item):
                        # Same file, remove source
                        os.remove(item)
                        logger.info(f"Removed duplicate file: {item}")
                    else:
                        # Different files, backup and move
                        backup_path = str(dst_item) + ".backup"
                        shutil.move(str(dst_item), backup_path)
                        shutil.move(str(item), str(dst_item))
                        logger.info(f"Merged {item} to {dst_item} (backed up existing)")
                else:
                    shutil.move(str(item), str(dst_item))
                    logger.info(f"Moved {item} to {dst_item}")
            elif item.is_dir():
                if dst_item.exists():
                    self._merge_directories(item, dst_item)
                else:
                    shutil.move(str(item), str(dst_item))
                    logger.info(f"Moved directory {item} to {dst_item}")

    def delete_unnecessary_files(self):
        """Delete files that are no longer needed"""
        logger.info("Deleting unnecessary files...")
        
        for file_path in self.files_to_delete:
            file = Path(file_path)
            if file.exists():
                os.remove(file)
                logger.info(f"Deleted: {file_path}")

    def cleanup_empty_directories(self):
        """Remove empty directories"""
        logger.info("Cleaning up empty directories...")
        
        # List of directories to check
        check_dirs = ["servers", "tools", "config", "__pycache__"]
        
        for dir_name in check_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists() and dir_path.is_dir():
                try:
                    # Remove __pycache__ directories recursively
                    if dir_name == "__pycache__":
                        shutil.rmtree(dir_path)
                        logger.info(f"Removed directory tree: {dir_name}")
                    else:
                        # Try to remove if empty
                        dir_path.rmdir()
                        logger.info(f"Removed empty directory: {dir_name}")
                except OSError:
                    logger.info(f"Directory not empty, keeping: {dir_name}")

    def run_cleanup(self):
        """Run the complete cleanup process"""
        logger.info("Starting cleanup of remaining files...")
        
        try:
            # Clean up config files first
            self.cleanup_config_files()
            
            # Move individual files
            self.move_files()
            
            # Move directories
            self.move_directories()
            
            # Delete unnecessary files
            self.delete_unnecessary_files()
            
            # Clean up empty directories
            self.cleanup_empty_directories()
            
            logger.info("✅ Cleanup completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
            raise

if __name__ == "__main__":
    cleanup_manager = CleanupManager()
    cleanup_manager.run_cleanup() 