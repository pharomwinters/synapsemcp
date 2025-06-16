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
import os
import httpx
import argparse
from pathlib import Path
from typing import Any

from base import SynapseDatabase
from sqlite_db import SQLiteDatabase
from mariadb import MariaDBDatabase
from utils import (
    get_db_instance,
    migrate_files_to_db,
    read_memory_from_db_or_file,
    write_memory_to_db_and_file,
    list_all_memories
)
from config import get_config

from mcp_instance import mcp

def main():
    """Entry point for the application when run with uvx."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Synapse MCP Server")
    parser.add_argument(
        "--env", "--mode", 
        choices=["development", "production", "test"],
        default=None,
        help="Set the environment mode (development, production, test)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind the server to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to (default: 8000)"
    )
    
    args = parser.parse_args()
    
    # Load configuration from command line args, environment, or default to production
    if args.env:
        env = args.env
        os.environ["SYNAPSE_ENV"] = env
    else:
        env = os.environ.get("SYNAPSE_ENV", "production")
    
    # Enable auto-discovery for tools
    os.environ["SYNAPSE_AUTO_DISCOVER"] = "true"
    
    # Run the MCP server directly instead of FastAPI
    print(f"Starting Synapse MCP Server in {env} mode with auto-discovery enabled...")
    print(f"Server will be available at http://{args.host}:{args.port}")
    
    # Use StreamableHTTP
    mcp.run(transport="streamable-http", host=args.host, port=args.port)

if __name__ == "__main__":
    main()
