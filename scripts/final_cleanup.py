#!/usr/bin/env python3
"""
Final cleanup script to handle remaining miscellaneous files and organize project structure.
"""

import os
import shutil
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalCleanup:
    def __init__(self):
        self.root_dir = Path(".")
        
        # Files to move to better locations
        self.file_moves = {
            # MCP config file
            "mcp/mcp.json": "config/mcp.json",
            
            # MariaDB manager
            "mariadb_server_manager.py": "src/synapse/database/mariadb_server_manager.py",
            
            # Instructions file
            "synapse_instructions.py": "docs/synapse_instructions.py",
            
            # Commit message (temporary file)
            "COMMIT_MESSAGE.txt": None,  # Delete
        }
        
        # Directories to organize
        self.directory_cleanup = {
            # Remove empty mcp directory after moving files
            "mcp/": None,  # Will be removed if empty
        }

    def move_files(self):
        """Move files to better locations"""
        logger.info("Moving remaining files to proper locations...")
        
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
                # Backup existing and move
                backup_path = str(new_file) + ".backup"
                shutil.move(str(new_file), backup_path)
                logger.info(f"Backed up existing {new_path}")
            
            # Move file to new location
            shutil.move(str(old_file), str(new_file))
            logger.info(f"Moved {old_path} to {new_path}")

    def cleanup_empty_directories(self):
        """Remove empty directories"""
        logger.info("Cleaning up empty directories...")
        
        for dir_path in ["mcp"]:
            dir_obj = Path(dir_path)
            if dir_obj.exists() and dir_obj.is_dir():
                try:
                    # Check if directory is empty
                    if not any(dir_obj.iterdir()):
                        dir_obj.rmdir()
                        logger.info(f"Removed empty directory: {dir_path}")
                    else:
                        logger.info(f"Directory not empty, keeping: {dir_path}")
                except OSError as e:
                    logger.warning(f"Could not remove directory {dir_path}: {e}")

    def create_config_directory(self):
        """Ensure config directory exists and is properly organized"""
        logger.info("Organizing config directory...")
        
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        
        # Move config files to config directory if they're in root
        config_files = [
            "config.dev.json",
            "config.test.json", 
            "config.prod.json",
            "config.dev.mariadb.json"
        ]
        
        for config_file in config_files:
            root_config = Path(config_file)
            target_config = config_dir / config_file
            
            if root_config.exists() and not target_config.exists():
                shutil.move(str(root_config), str(target_config))
                logger.info(f"Moved {config_file} to config/ directory")

    def run_cleanup(self):
        """Run the final cleanup process"""
        logger.info("Starting final cleanup...")
        
        try:
            # Create and organize config directory
            self.create_config_directory()
            
            # Move remaining files
            self.move_files()
            
            # Clean up empty directories
            self.cleanup_empty_directories()
            
            logger.info("✅ Final cleanup completed successfully!")
            
            # Show current root directory status
            logger.info("\n📁 Current root directory contents:")
            for item in sorted(self.root_dir.iterdir()):
                if item.is_dir():
                    logger.info(f"  [DIR]  {item.name}/")
                else:
                    size = item.stat().st_size / 1024  # KB
                    logger.info(f"  [FILE] {item.name} ({size:.1f} KB)")
            
        except Exception as e:
            logger.error(f"❌ Final cleanup failed: {e}")
            raise

if __name__ == "__main__":
    cleanup = FinalCleanup()
    cleanup.run_cleanup() 