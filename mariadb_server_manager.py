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
MariaDB Server Manager for Synapse

Automatically starts and manages a local MariaDB instance when the MCP server starts.
This is perfect for development and testing environments.
Cross-platform compatible: Windows, Linux, macOS.
"""

import os
import sys
import subprocess
import time
import signal
import atexit
import logging
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import threading
import socket

logger = logging.getLogger(__name__)


class MariaDBServerManager:
    """Manages a local MariaDB server instance for Synapse."""
    
    def __init__(self, 
                 data_dir: Optional[str] = None,
                 port: int = 3306,
                 root_password: str = "synapse_root",
                 database_name: str = "synapse",
                 user_name: str = "synapse_user",
                 user_password: str = "synapse_pass"):
        """
        Initialize MariaDB server manager.
        
        Args:
            data_dir: Directory to store database files (None = temp directory)
            port: Port for MariaDB server
            root_password: Root user password
            database_name: Name of the Synapse database
            user_name: Synapse application user name
            user_password: Synapse application user password
        """
        self.port = port
        self.root_password = root_password
        self.database_name = database_name
        self.user_name = user_name
        self.user_password = user_password
        
        # Set up directories
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path(tempfile.mkdtemp(prefix="synapse_mariadb_"))
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.socket_file = self.data_dir / "mysql.sock"
        self.pid_file = self.data_dir / "mysql.pid"
        self.log_file = self.data_dir / "mysql.log"
        self.config_file = self.data_dir / "my.cnf"
        
        # Server process
        self.server_process: Optional[subprocess.Popen] = None
        self.is_running = False
        
        # Register cleanup on exit
        atexit.register(self.stop)
        
        # Handle signals for graceful shutdown (Unix only)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self._signal_handler)
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down MariaDB...")
        self.stop()
        sys.exit(0)

    def _find_mariadb_binary(self) -> Optional[str]:
        """Find MariaDB server binary - Windows compatible version."""
        possible_paths = [
            "mysqld",
            "mariadbd",
            # Windows-specific paths
            "C:\\Program Files\\MariaDB 10.11\\bin\\mysqld.exe",
            "C:\\Program Files\\MariaDB 10.10\\bin\\mysqld.exe",
            "C:\\Program Files\\MariaDB 10.9\\bin\\mysqld.exe",
            "C:\\Program Files\\MariaDB 10.8\\bin\\mysqld.exe",
            "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqld.exe",
            "C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysqld.exe",
            "C:\\xampp\\mysql\\bin\\mysqld.exe",
            "C:\\wamp64\\bin\\mysql\\mysql8.0.31\\bin\\mysqld.exe",
            # Unix/Linux paths
            "/usr/sbin/mysqld",
            "/usr/local/mysql/bin/mysqld",
            "/opt/homebrew/bin/mysqld",
            "/usr/bin/mysqld",
            "/usr/sbin/mariadbd",
            "/usr/local/bin/mariadbd"
        ]
        
        for path in possible_paths:
            if shutil.which(path) or (os.path.isfile(path) and os.access(path, os.X_OK)):
                return path
                
        return None

    def _find_mysql_install_db(self) -> Optional[str]:
        """Find mysql_install_db or mariadb-install-db binary - Windows compatible."""
        possible_paths = [
            "mysql_install_db",
            "mariadb-install-db",
            # Windows-specific paths
            "C:\\Program Files\\MariaDB 10.11\\bin\\mysql_install_db.exe",
            "C:\\Program Files\\MariaDB 10.10\\bin\\mysql_install_db.exe",
            "C:\\Program Files\\MariaDB 10.9\\bin\\mysql_install_db.exe",
            "C:\\Program Files\\MariaDB 10.8\\bin\\mysql_install_db.exe",
            "C:\\xampp\\mysql\\bin\\mysql_install_db.exe",
            # Unix/Linux paths
            "/usr/bin/mysql_install_db",
            "/usr/bin/mariadb-install-db",
            "/usr/local/bin/mysql_install_db",
            "/usr/local/bin/mariadb-install-db",
            "/opt/homebrew/bin/mysql_install_db"
        ]
        
        for path in possible_paths:
            if shutil.which(path) or (os.path.isfile(path) and os.access(path, os.X_OK)):
                return path
                
        return None

    def _is_port_available(self, port: int) -> bool:
        """Check if a port is available."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return True
        except OSError:
            return False

    def _wait_for_port(self, port: int, timeout: int = 30) -> bool:
        """Wait for a port to become available."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('localhost', port))
                    return True
            except OSError:
                time.sleep(0.5)
        return False

    def _create_config_file(self):
        """Create MariaDB configuration file - Windows compatible."""
        # Use forward slashes even on Windows (MySQL/MariaDB accepts them)
        data_dir_path = str(self.data_dir).replace('\\', '/')
        socket_file_path = str(self.socket_file).replace('\\', '/')
        pid_file_path = str(self.pid_file).replace('\\', '/')
        log_file_path = str(self.log_file).replace('\\', '/')
        
        config_content = f"""[mysqld]
datadir = {data_dir_path}
socket = {socket_file_path}
pid-file = {pid_file_path}
log-error = {log_file_path}
port = {self.port}
bind-address = 127.0.0.1

# Performance settings for development
innodb_buffer_pool_size = 64M
innodb_log_file_size = 16M
innodb_flush_log_at_trx_commit = 2
sync_binlog = 0

# Security settings
skip-networking = 0
skip-name-resolve = 1

# Character set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4

[client]
default-character-set = utf8mb4
port = {self.port}
socket = {socket_file_path}
"""
        
        with open(self.config_file, 'w') as f:
            f.write(config_content)

    def initialize_database(self) -> bool:
        """Initialize the MariaDB database - Windows compatible."""
        logger.info("Initializing MariaDB database...")
        
        install_db_cmd = self._find_mysql_install_db()
        if not install_db_cmd:
            logger.error("mysql_install_db or mariadb-install-db not found")
            return False
        
        try:
            # Build initialization command
            cmd = [
                install_db_cmd,
                f"--datadir={self.data_dir}",
            ]
            
            # Add basedir only on Unix systems (Windows MariaDB doesn't usually need it)
            if not sys.platform.startswith('win'):
                cmd.append("--basedir=/usr")
            
            # Add auth method (newer MariaDB versions)
            cmd.append("--auth-root-authentication-method=normal")
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=120)
            
            if result.returncode != 0:
                logger.error(f"Database initialization failed: {result.stderr}")
                return False
                
            logger.info("✅ Database initialized successfully")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("Database initialization timed out")
            return False
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            return False

    def start(self) -> bool:
        """Start the MariaDB server."""
        if self.is_running:
            logger.info("MariaDB server is already running")
            return True
            
        logger.info("Starting MariaDB server...")
        
        # Check if port is already in use
        if not self._is_port_available(self.port):
            logger.error(f"Port {self.port} is already in use")
            return False
        
        # Find MariaDB binary
        mysqld_path = self._find_mariadb_binary()
        if not mysqld_path:
            logger.error("MariaDB server binary not found. Please install MariaDB/MySQL.")
            return False
            
        logger.info(f"Found MariaDB binary: {mysqld_path}")
        
        # Create config file
        self._create_config_file()
        
        # Initialize database if it doesn't exist
        if not (self.data_dir / "mysql").exists():
            if not self.initialize_database():
                return False
        
        try:
            # Build command - fixed for cross-platform compatibility
            cmd = [
                mysqld_path,
                f"--defaults-file={self.config_file}",
            ]
            
            # Add user parameter only on Unix-like systems and only if running as root
            try:
                # Check if we're on a Unix-like system and running as root
                if hasattr(os, 'geteuid') and os.geteuid() == 0:
                    cmd.append("--user=mysql")
            except (AttributeError, OSError):
                # On Windows or if geteuid() fails, skip the --user parameter
                pass
            
            logger.info(f"Starting MariaDB with command: {' '.join(cmd)}")
            
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.data_dir)
            )
            
            # Wait for server to start
            if self._wait_for_port(self.port, timeout=30):
                self.is_running = True
                logger.info(f"✅ MariaDB server started on port {self.port}")
                
                # Set up database and user
                time.sleep(2)  # Give server time to fully start
                if self._setup_database():
                    logger.info("✅ Database and user setup complete")
                    return True
                else:
                    logger.warning("⚠️ Server started but database setup failed")
                    return True  # Server is still running
            else:
                logger.error("❌ MariaDB server failed to start within timeout")
                self.stop()
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to start MariaDB server: {e}")
            return False

    def _setup_database(self) -> bool:
        """Set up the Synapse database and user."""
        try:
            import mysql.connector
            
            # Connect as root to set up database
            conn = mysql.connector.connect(
                host='127.0.0.1',
                port=self.port,
                user='root',
                password='',  # No password initially
                auth_plugin='mysql_native_password'
            )
            
            cursor = conn.cursor()
            
            # Set root password
            cursor.execute(f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{self.root_password}'")
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
            # Create user
            cursor.execute(f"CREATE USER IF NOT EXISTS '{self.user_name}'@'localhost' IDENTIFIED BY '{self.user_password}'")
            cursor.execute(f"CREATE USER IF NOT EXISTS '{self.user_name}'@'127.0.0.1' IDENTIFIED BY '{self.user_password}'")
            
            # Grant privileges
            cursor.execute(f"GRANT ALL PRIVILEGES ON {self.database_name}.* TO '{self.user_name}'@'localhost'")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {self.database_name}.* TO '{self.user_name}'@'127.0.0.1'")
            
            # Flush privileges
            cursor.execute("FLUSH PRIVILEGES")
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            return False

    def stop(self):
        """Stop the MariaDB server."""
        if not self.is_running:
            return
            
        logger.info("Stopping MariaDB server...")
        
        if self.server_process:
            try:
                # Try graceful shutdown first
                self.server_process.terminate()
                
                # Wait for process to end
                try:
                    self.server_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't stop gracefully
                    logger.warning("Force killing MariaDB server...")
                    self.server_process.kill()
                    self.server_process.wait()
                    
                logger.info("✅ MariaDB server stopped")
                
            except Exception as e:
                logger.error(f"Error stopping MariaDB server: {e}")
            finally:
                self.server_process = None
                self.is_running = False
        
        # Clean up PID file
        if self.pid_file.exists():
            try:
                self.pid_file.unlink()
            except:
                pass

    def get_connection_config(self) -> Dict[str, Any]:
        """Get connection configuration for Synapse."""
        return {
            "host": "127.0.0.1",
            "port": self.port,
            "user": self.user_name,
            "password": self.user_password,
            "database": self.database_name
        }

    def is_server_running(self) -> bool:
        """Check if the server is currently running."""
        if not self.is_running or not self.server_process:
            return False
            
        # Check if process is still alive
        poll_result = self.server_process.poll()
        if poll_result is not None:
            # Process has terminated
            self.is_running = False
            return False
            
        return True

    def get_status(self) -> Dict[str, Any]:
        """Get detailed server status."""
        return {
            "running": self.is_server_running(),
            "port": self.port,
            "data_dir": str(self.data_dir),
            "database": self.database_name,
            "user": self.user_name,
            "pid": self.server_process.pid if self.server_process else None,
            "log_file": str(self.log_file),
            "platform": sys.platform
        }


# Global server instance
_mariadb_server: Optional[MariaDBServerManager] = None


def start_mariadb_server(auto_start: bool = True) -> Optional[MariaDBServerManager]:
    """Start MariaDB server for Synapse development."""
    global _mariadb_server
    
    if not auto_start:
        return None
        
    if _mariadb_server and _mariadb_server.is_server_running():
        return _mariadb_server
    
    try:
        logger.info("🚀 Starting embedded MariaDB server for Synapse...")
        
        _mariadb_server = MariaDBServerManager(
            data_dir="synapse_mariadb_data",  # Persistent data directory
            port=3307,  # Use different port to avoid conflicts
            root_password="synapse_root_2024",
            database_name="synapse",
            user_name="synapse_user",
            user_password="synapse_pass_2024"
        )
        
        if _mariadb_server.start():
            # Update environment variables for Synapse to use
            config = _mariadb_server.get_connection_config()
            os.environ["SYNAPSE_DB_TYPE"] = "mariadb"
            os.environ["SYNAPSE_MARIADB_HOST"] = config["host"]
            os.environ["SYNAPSE_MARIADB_PORT"] = str(config["port"])
            os.environ["SYNAPSE_MARIADB_USER"] = config["user"]
            os.environ["SYNAPSE_MARIADB_PASSWORD"] = config["password"]
            os.environ["SYNAPSE_MARIADB_DATABASE"] = config["database"]
            
            logger.info("✅ MariaDB server started and configured for Synapse")
            logger.info(f"   📍 Connection: {config['host']}:{config['port']}")
            logger.info(f"   🗄️ Database: {config['database']}")
            logger.info(f"   👤 User: {config['user']}")
            logger.info(f"   🖥️ Platform: {sys.platform}")
            
            return _mariadb_server
        else:
            logger.error("❌ Failed to start MariaDB server")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error starting MariaDB server: {e}")
        return None


def stop_mariadb_server():
    """Stop the MariaDB server."""
    global _mariadb_server
    if _mariadb_server:
        _mariadb_server.stop()


def get_mariadb_status() -> Optional[Dict[str, Any]]:
    """Get MariaDB server status."""
    global _mariadb_server
    if _mariadb_server:
        return _mariadb_server.get_status()
    return None


# For standalone testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🧪 Testing MariaDB Server Manager...")
    print(f"🖥️ Platform: {sys.platform}")
    
    server = start_mariadb_server(auto_start=True)
    if server:
        print("✅ Server started successfully!")
        status = server.get_status()
        print(f"Status: {status}")
        
        # Test connection
        try:
            import mysql.connector
            config = server.get_connection_config()
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Connection test successful: {result}")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
        
        # Keep running for testing
        try:
            input("Press Enter to stop the server...")
        except KeyboardInterrupt:
            pass
        
        server.stop()
        print("✅ Server stopped")
    else:
        print("❌ Failed to start server")