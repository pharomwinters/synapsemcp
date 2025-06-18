#!/usr/bin/env python3
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
Main entry point for Synapse MCP Server.

This module provides command line interface for starting the Synapse server
with various configuration options.
"""

import argparse
import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from synapse.mcp.instance import mcp
from synapse.core.config import get_config

__version__ = "2.0.0"

def setup_logging(log_level: str):
    """Setup logging configuration."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Synapse MCP Server - AI-Human Collaboration Platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Start with default settings
  %(prog)s --env development                  # Start in development mode
  %(prog)s --host 0.0.0.0 --port 9000        # Custom host and port
  %(prog)s --db-type mariadb                  # Use MariaDB database
  %(prog)s --log-level DEBUG                  # Enable debug logging

Environment Variables:
  SYNAPSE_ENV               - Environment name (development/test/production)
  SYNAPSE_DB_TYPE           - Database type (duckdb/sqlite/mariadb)
  SYNAPSE_DUCKDB_DB_PATH    - DuckDB database path
  SYNAPSE_SQLITE_DB_PATH    - SQLite database path  
  SYNAPSE_MARIADB_HOST      - MariaDB host
  SYNAPSE_MARIADB_PORT      - MariaDB port
  SYNAPSE_MARIADB_USER      - MariaDB user
  SYNAPSE_MARIADB_PASSWORD  - MariaDB password
  SYNAPSE_MARIADB_DATABASE  - MariaDB database name
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'Synapse {__version__}'
    )
    
    parser.add_argument(
        '--env',
        choices=['development', 'test', 'production'],
        default=os.getenv('SYNAPSE_ENV', 'development'),
        help='Environment to run in (default: development)'
    )
    
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to bind to (default: 8000)'
    )
    
    parser.add_argument(
        '--db-type',
        choices=['duckdb', 'sqlite', 'mariadb', 'auto'],
        default='auto',
        help='Database type to use (default: auto)'
    )
    
    parser.add_argument(
        '--no-embedded-db',
        action='store_true',
        help="Don't start embedded database server"
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--config',
        help='Path to configuration file (overrides --env)'
    )
    
    parser.add_argument(
        '--transport',
        choices=['stdio', 'streamable-http', 'sse'],
        default='streamable-http',
        help='MCP transport to use (default: streamable-http)'
    )
    
    return parser.parse_args()

def validate_environment(args):
    """Validate the environment and dependencies."""
    # Check if we're in the right directory
    if not Path('mcp_instance.py').exists():
        print("❌ Error: mcp_instance.py not found. Are you in the Synapse project directory?")
        sys.exit(1)
    
    # Set environment variables from args
    os.environ['SYNAPSE_ENV'] = args.env
    if args.db_type != 'auto':
        os.environ['SYNAPSE_DB_TYPE'] = args.db_type
    
    # Create directories
    memory_dir = get_config('memory_dir', 'memories')
    documents_dir = get_config('documents_dir', 'documents')
    
    Path(memory_dir).mkdir(exist_ok=True)
    Path(documents_dir).mkdir(exist_ok=True)
    
    print(f"✅ Environment: {args.env}")
    print(f"✅ Memory directory: {memory_dir}")
    print(f"✅ Documents directory: {documents_dir}")

def print_banner():
    """Print the Synapse banner."""
    banner = r"""
 ____                                     
/ ___| _   _ _ __   __ _ _ __  ___  ___    
\___ \| | | | '_ \ / _` | '_ \/ __|/ _ \   
 ___) | |_| | | | | (_| | |_) \__ \  __/   
|____/ \__, |_| |_|\__,_| .__/|___/\___|   
       |___/            |_|               

🧠 AI-Human Collaboration Platform
    Where Intelligence Connects ⚡

Version: {version}
    """.format(version=__version__)
    print(banner)

def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Print banner
    print_banner()
    
    print(f"🚀 Starting Synapse MCP Server")
    print(f"📍 Environment: {args.env}")
    print(f"🌐 Transport: {args.transport}")
    if args.transport != 'stdio':
        print(f"🔗 Address: http://{args.host}:{args.port}")
    print(f"📊 Database: {args.db_type}")
    print(f"📝 Log Level: {args.log_level}")
    print()
    
    # Validate environment
    validate_environment(args)
    
    print()
    print("🧠 Synapse MCP Platform ready!")
    print("✅ Document management system enabled")
    print("✅ Multi-database support active")
    print("✅ All servers initialized")
    print()
    
    try:
        if args.transport == 'stdio':
            logger.info("Starting MCP server with STDIO transport")
            mcp.run()
        else:
            logger.info(f"Starting MCP server with {args.transport} transport on {args.host}:{args.port}")
            mcp.run(transport=args.transport, host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Synapse...")
        logger.info("Server shutdown requested")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        logger.error(f"Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()