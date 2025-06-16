#!/bin/bash
#
# Synapse Development Server Startup Script
# Enhanced version with config file support
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ENV="development"
HOST="127.0.0.1"
PORT="8000"
DB_TYPE="auto"
LOG_LEVEL="INFO"
NO_EMBEDDED_DB=false
CONFIG_FILE=""

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to show usage
show_usage() {
    cat << EOF
🧠 Synapse Development Server

Usage: $0 [OPTIONS]

OPTIONS:
    --env ENV           Environment (development, production, test) [default: development]
    --config FILE       Config file to use (overrides --env)
    --host HOST         Host to bind to [default: 127.0.0.1]
    --port PORT         Port to bind to [default: 8000]
    --db-type TYPE      Database type (duckdb, sqlite, mariadb, auto) [default: auto]
    --no-embedded-db    Don't start embedded MariaDB server
    --log-level LEVEL   Log level (DEBUG, INFO, WARNING, ERROR) [default: INFO]
    --help              Show this help message

EXAMPLES:
    # Start with default settings (DuckDB development)
    $0

    # Start with MariaDB development config
    $0 --config config.dev.mariadb.json

    # Start in production mode
    $0 --env production

    # Start with custom database type
    $0 --db-type mariadb

    # Start with debug logging
    $0 --log-level DEBUG

CONFIG FILES:
    config.dev.json           - DuckDB development (default)
    config.dev.mariadb.json   - MariaDB development
    config.test.json          - Testing environment
    config.prod.json          - Production environment
    config.local.json         - Local overrides (optional)

ENVIRONMENT VARIABLES:
    SYNAPSE_ENV               - Environment name
    SYNAPSE_DB_TYPE           - Database type
    SYNAPSE_DUCKDB_DB_PATH    - DuckDB database path
    SYNAPSE_SQLITE_DB_PATH    - SQLite database path (legacy)
    SYNAPSE_MARIADB_HOST      - MariaDB host
    SYNAPSE_MARIADB_PORT      - MariaDB port
    SYNAPSE_MARIADB_USER      - MariaDB user
    SYNAPSE_MARIADB_PASSWORD  - MariaDB password
    SYNAPSE_MARIADB_DATABASE  - MariaDB database name

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENV="$2"
            shift 2
            ;;
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --db-type)
            DB_TYPE="$2"
            shift 2
            ;;
        --no-embedded-db)
            NO_EMBEDDED_DB=true
            shift
            ;;
        --log-level)
            LOG_LEVEL="$2"
            shift 2
            ;;
        --help|-h)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Determine config file if not specified
determine_config_file() {
    if [[ -n "$CONFIG_FILE" ]]; then
        if [[ ! -f "$CONFIG_FILE" ]]; then
            print_error "Config file not found: $CONFIG_FILE"
            exit 1
        fi
        print_info "Using config file: $CONFIG_FILE"
    else
        # Use environment-based config
        case $ENV in
            "development")
                if [[ "$DB_TYPE" == "mariadb" ]]; then
                    CONFIG_FILE="config.dev.mariadb.json"
                else
                    CONFIG_FILE="config.dev.json"  # DuckDB default
                fi
                ;;
            "test")
                CONFIG_FILE="config.test.json"
                ;;
            "production")
                CONFIG_FILE="config.prod.json"
                ;;
            *)
                print_error "Unknown environment: $ENV"
                exit 1
                ;;
        esac
        
        print_info "Auto-selected config file: $CONFIG_FILE"
    fi
}

# Create default config files if they don't exist
create_default_configs() {
    # Create config.dev.json (DuckDB)
    if [[ ! -f "config.dev.json" ]]; then
        print_warning "config.dev.json not found, creating default..."
        cat > config.dev.json << 'EOF'
{
    "database": {
        "type": "duckdb",
        "duckdb": {
            "db_path": "synapse_dev.duckdb"
        }
    },
    "memory_dir": "memories_dev",
    "documents_dir": "documents_dev",
    "log_level": "DEBUG"
}
EOF
        print_success "Created config.dev.json"
    fi
    
    # Create config.dev.mariadb.json (MariaDB)
    if [[ ! -f "config.dev.mariadb.json" ]]; then
        print_warning "config.dev.mariadb.json not found, creating default..."
        cat > config.dev.mariadb.json << 'EOF'
{
    "database": {
        "type": "mariadb",
        "mariadb": {
            "host": "127.0.0.1",
            "port": 3307,
            "user": "synapse_user",
            "password": "synapse_pass_2024",
            "database": "synapse"
        }
    },
    "memory_dir": "memories_dev",
    "log_level": "DEBUG",
    "encoding": "utf-8",
    "embedded_mariadb": {
        "enabled": true,
        "auto_start": true,
        "data_directory": "synapse_mariadb_data",
        "port": 3307,
        "root_password": "synapse_root_2024",
        "database_name": "synapse",
        "user_name": "synapse_user",
        "user_password": "synapse_pass_2024"
    }
}
EOF
        print_success "Created config.dev.mariadb.json"
    fi
    
    # Create config.test.json
    if [[ ! -f "config.test.json" ]]; then
        print_warning "config.test.json not found, creating default..."
        cat > config.test.json << 'EOF'
{
    "database": {
        "type": "duckdb",
        "duckdb": {
            "db_path": "synapse_test.duckdb"
        }
    },
    "memory_dir": "memories_test",
    "documents_dir": "documents_test", 
    "log_level": "ERROR"
}
EOF
        print_success "Created config.test.json"
    fi
    
    # Create config.prod.json
    if [[ ! -f "config.prod.json" ]]; then
        print_warning "config.prod.json not found, creating default..."
        cat > config.prod.json << 'EOF'
{
    "database": {
        "type": "duckdb",
        "duckdb": {
            "db_path": "synapse.duckdb"
        }
    },
    "memory_dir": "memories",
    "documents_dir": "documents",
    "log_level": "WARNING"
}
EOF
        print_success "Created config.prod.json"
    fi
}

# Check if we're in a virtual environment
check_virtual_env() {
    if [[ -z "$VIRTUAL_ENV" ]]; then
        print_warning "Not in a virtual environment!"
        print_info "It's recommended to use a virtual environment:"
        print_info "  python -m venv .venv"
        print_info "  source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows"
        echo
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "Virtual environment detected: $VIRTUAL_ENV"
    fi
}

# Check dependencies
check_dependencies() {
    print_info "Checking dependencies..."
    
    # Check Python
    if ! command -v python &> /dev/null; then
        print_error "Python not found. Please install Python 3.12+."
        exit 1
    fi
    
    python_version=$(python --version 2>&1 | cut -d' ' -f2)
    print_success "Python version: $python_version"
    
    # Check if requirements are installed
    if ! python -c "import fastmcp" &> /dev/null; then
        print_warning "FastMCP not found. Installing dependencies..."
        if [[ -f "requirements.txt" ]]; then
            pip install -r requirements.txt
        else
            print_error "requirements.txt not found. Please install dependencies manually."
            exit 1
        fi
    fi
    
    # Check MariaDB if needed
    if [[ "$DB_TYPE" == "mariadb" || "$DB_TYPE" == "auto" ]] && [[ "$NO_EMBEDDED_DB" == false ]]; then
        if ! command -v mysqld &> /dev/null && ! command -v mariadbd &> /dev/null; then
            print_warning "MariaDB/MySQL server not found."
            print_info "Installing MariaDB is recommended for development:"
            print_info "  # Ubuntu/Debian:"
            print_info "  sudo apt-get install mariadb-server mariadb-client"
            print_info "  # macOS:"
            print_info "  brew install mariadb"
            print_info "  # Or use DuckDB config: $0 --config config.dev.json"
            echo
            read -p "Continue with DuckDB fallback? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                CONFIG_FILE="config.dev.json"
                DB_TYPE="duckdb"
                print_info "Switched to DuckDB configuration"
            else
                exit 1
            fi
        else
            print_success "MariaDB/MySQL server found"
        fi
    fi
}

# Pre-flight checks
pre_flight_checks() {
    print_info "Running pre-flight checks..."
    
    # Check if main.py exists
    if [[ ! -f "main.py" ]]; then
        print_error "main.py not found. Are you in the Synapse project directory?"
        exit 1
    fi
    
    # Create default config files
    create_default_configs
    
    # Determine which config file to use
    determine_config_file
    
    # Create memories directory if it doesn't exist
    memory_dir="memories_dev"
    if [[ "$ENV" == "test" ]]; then
        memory_dir="memories_test"
    elif [[ "$ENV" == "production" ]]; then
        memory_dir="memories"
    fi
    
    if [[ ! -d "$memory_dir" ]]; then
        mkdir -p "$memory_dir"
        print_success "Created $memory_dir directory"
    fi
    
    print_success "Pre-flight checks completed"
}

# Start the server
start_server() {
    print_info "Starting Synapse MCP Server..."
    echo
    print_info "Configuration:"
    print_info "  Config File: $CONFIG_FILE"
    print_info "  Environment: $ENV"
    print_info "  Host: $HOST"
    print_info "  Port: $PORT"
    print_info "  Database: $DB_TYPE"
    print_info "  Log Level: $LOG_LEVEL"
    if [[ "$NO_EMBEDDED_DB" == true ]]; then
        print_info "  Embedded DB: disabled"
    fi
    echo
    
    # Build command arguments
    CMD_ARGS=(
        "--env" "$ENV"
        "--host" "$HOST"
        "--port" "$PORT"
        "--db-type" "$DB_TYPE"
        "--log-level" "$LOG_LEVEL"
    )
    
    if [[ "$NO_EMBEDDED_DB" == true ]]; then
        CMD_ARGS+=("--no-embedded-db")
    fi
    
    # Start the server
    print_success "🚀 Starting server with: python main.py ${CMD_ARGS[*]}"
    echo
    
    # Handle Ctrl+C gracefully
    trap 'print_info "Shutting down..."; exit 0' INT
    
    exec python main.py "${CMD_ARGS[@]}"
}

# Show banner
show_banner() {
    cat << 'EOF'
 ____                                     
/ ___| _   _ _ __   __ _ _ __  ___  ___    
\___ \| | | | '_ \ / _` | '_ \/ __|/ _ \   
 ___) | |_| | | | | (_| | |_) \__ \  __/   
|____/ \__, |_| |_|\__,_| .__/|___/\___|   
       |___/            |_|               

🧠 AI-Human Collaboration Platform
    Where Intelligence Connects ⚡

EOF
}

# Main execution
main() {
    show_banner
    
    print_info "Synapse Development Server Startup"
    print_info "Environment: $ENV | Database: $DB_TYPE | Port: $PORT"
    echo
    
    check_virtual_env
    check_dependencies
    pre_flight_checks
    
    echo
    print_success "All checks passed! Starting server..."
    echo
    
    start_server
}

# Run main function
main