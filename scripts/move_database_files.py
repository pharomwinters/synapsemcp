#!/usr/bin/env python3
"""
Script to move database files to the data directory and update configuration.
"""

import os
import shutil
from pathlib import Path
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseFileMover:
    def __init__(self):
        self.root_dir = Path(".")
        self.data_dir = Path("data")
        
        # Database files to move
        self.db_files = {
            "synapse.db": "data/synapse.db",
            "synapse.duckdb": "data/synapse.duckdb"
        }
        
        # Config files to update
        self.config_files = [
            "config/config.dev.json",
            "config/config.test.json", 
            "config/config.prod.json"
        ]

    def create_data_directory(self):
        """Ensure data directory exists"""
        self.data_dir.mkdir(exist_ok=True)
        logger.info(f"Ensured data directory exists: {self.data_dir}")

    def move_database_files(self):
        """Move database files to data directory"""
        logger.info("Moving database files to data directory...")
        
        for old_path, new_path in self.db_files.items():
            old_file = Path(old_path)
            new_file = Path(new_path)
            
            if old_file.exists():
                if new_file.exists():
                    # Backup existing file in data directory
                    backup_path = str(new_file) + ".backup"
                    shutil.move(str(new_file), backup_path)
                    logger.info(f"Backed up existing file: {new_path}")
                
                # Move file
                shutil.move(str(old_file), str(new_file))
                logger.info(f"✅ Moved {old_path} → {new_path}")
            else:
                logger.info(f"File not found: {old_path}")

    def update_config_files(self):
        """Update configuration files to point to new database locations"""
        logger.info("Updating configuration files...")
        
        for config_file_path in self.config_files:
            config_file = Path(config_file_path)
            
            if not config_file.exists():
                logger.info(f"Config file not found: {config_file_path}")
                continue
            
            try:
                # Load existing config
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                # Update database paths
                updated = False
                if "database" in config:
                    if "duckdb" in config["database"] and "db_path" in config["database"]["duckdb"]:
                        if config["database"]["duckdb"]["db_path"] == "synapse.duckdb":
                            config["database"]["duckdb"]["db_path"] = "data/synapse.duckdb"
                            updated = True
                    
                    if "sqlite" in config["database"] and "db_path" in config["database"]["sqlite"]:
                        if config["database"]["sqlite"]["db_path"] == "synapse.db":
                            config["database"]["sqlite"]["db_path"] = "data/synapse.db"
                            updated = True
                
                # Write back if updated
                if updated:
                    with open(config_file, 'w') as f:
                        json.dump(config, f, indent=2)
                    logger.info(f"✅ Updated database paths in {config_file_path}")
                else:
                    logger.info(f"No updates needed for {config_file_path}")
                    
            except Exception as e:
                logger.error(f"Failed to update {config_file_path}: {e}")

    def update_default_config(self):
        """Update the default configuration in the source code"""
        logger.info("Updating default configuration in source code...")
        
        config_py_path = Path("src/synapse/core/config.py")
        if config_py_path.exists():
            try:
                # Read the file
                content = config_py_path.read_text()
                
                # Update the default paths
                updated_content = content.replace(
                    '"db_path": "synapse.duckdb"',
                    '"db_path": "data/synapse.duckdb"'
                ).replace(
                    '"db_path": "synapse.db"',
                    '"db_path": "data/synapse.db"'
                )
                
                # Write back if changed
                if content != updated_content:
                    config_py_path.write_text(updated_content)
                    logger.info("✅ Updated default database paths in config.py")
                else:
                    logger.info("Default config already correct")
                    
            except Exception as e:
                logger.error(f"Failed to update config.py: {e}")

    def create_gitignore_entry(self):
        """Add data directory to .gitignore if not already present"""
        gitignore_path = Path(".gitignore")
        
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            
            # Check if data directory is already ignored
            if "data/" not in content and "/data/" not in content:
                # Add data directory to gitignore
                with open(gitignore_path, 'a') as f:
                    f.write("\n# Database files\ndata/\n")
                logger.info("✅ Added data/ directory to .gitignore")
            else:
                logger.info("data/ directory already in .gitignore")

    def run(self):
        """Run the complete database file migration"""
        logger.info("🚀 Starting database file migration...")
        
        try:
            # Create data directory
            self.create_data_directory()
            
            # Move database files
            self.move_database_files()
            
            # Update configuration files
            self.update_config_files()
            
            # Update default configuration in source
            self.update_default_config()
            
            # Update .gitignore
            self.create_gitignore_entry()
            
            logger.info("✅ Database file migration completed successfully!")
            logger.info("📁 Database files are now in: data/")
            logger.info("⚙️  Configuration updated to use new paths")
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            raise

if __name__ == "__main__":
    mover = DatabaseFileMover()
    mover.run() 