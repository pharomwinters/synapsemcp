@echo off
REM Synapse Development Server Startup Script for Windows
REM Enhanced version with config file support

setlocal enabledelayedexpansion

REM Default values
set "ENV=development"
set "HOST=127.0.0.1"
set "PORT=8000"
set "DB_TYPE=auto"
set "LOG_LEVEL=INFO"
set "NO_EMBEDDED_DB=false"
set "CONFIG_FILE="

REM Parse command line arguments
:parse_args
if "%~1"=="" goto end_parse
if "%~1"=="--env" (
    set "ENV=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--config" (
    set "CONFIG_FILE=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--host" (
    set "HOST=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--port" (
    set "PORT=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--db-type" (
    set "DB_TYPE=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--no-embedded-db" (
    set "NO_EMBEDDED_DB=true"
    shift
    goto parse_args
)
if "%~1"=="--log-level" (
    set "LOG_LEVEL=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--help" goto show_help
if "%~1"=="-h" goto show_help
echo [ERROR] Unknown option: %~1
goto show_help

:end_parse

REM Function to print banner
call :show_banner

echo.
echo [INFO] Synapse Development Server Startup
echo [INFO] Environment: %ENV% ^| Database: %DB_TYPE% ^| Port: %PORT%
echo.

REM Check virtual environment
call :check_virtual_env
if errorlevel 1 exit /b 1

REM Check dependencies
call :check_dependencies
if errorlevel 1 exit /b 1

REM Pre-flight checks
call :pre_flight_checks
if errorlevel 1 exit /b 1

echo.
echo [SUCCESS] All checks passed! Starting server...
echo.

REM Start the server
call :start_server
goto :eof

REM Functions
:show_banner
echo  ____                                     
echo / ___^| _   _ _ __   __ _ _ __  ___  ___    
echo \___ \^| ^| ^| ^| '_ \ / _` ^| '_ \/ __^|/ _ \   
echo  ___) ^| ^|_^| ^| ^| ^| ^| (_` ^| ^|_) \__ \  __/   
echo ^|____/ \__, ^|_^| ^|_^\__,_^| .__/^|___/\___^|   
echo        ^|___/            ^|_^|               
echo.
echo 🧠 AI-Human Collaboration Platform
echo     Where Intelligence Connects ⚡
echo.
goto :eof

:show_help
echo 🧠 Synapse Development Server
echo.
echo Usage: %~0 [OPTIONS]
echo.
echo OPTIONS:
echo     --env ENV           Environment (development, production, test) [default: development]
echo     --config FILE       Config file to use (overrides --env)
echo     --host HOST         Host to bind to [default: 127.0.0.1]
echo     --port PORT         Port to bind to [default: 8000]
echo     --db-type TYPE      Database type (duckdb, sqlite, mariadb, auto) [default: auto]
echo     --no-embedded-db    Don't start embedded MariaDB server
echo     --log-level LEVEL   Log level (DEBUG, INFO, WARNING, ERROR) [default: INFO]
echo     --help              Show this help message
echo.
echo EXAMPLES:
echo     # Start with default settings (SQLite development)
echo     %~0
echo.
echo     # Start with MariaDB development config
echo     %~0 --config config.dev.mariadb.json
echo.
echo     # Start in production mode
echo     %~0 --env production
echo.
echo     # Start with custom database type
echo     %~0 --db-type mariadb
echo.
echo     # Start with debug logging
echo     %~0 --log-level DEBUG
echo.
echo CONFIG FILES:
echo     config.dev.json           - SQLite development (default)
echo     config.dev.mariadb.json   - MariaDB development
echo     config.test.json          - Testing environment
echo     config.prod.json          - Production environment
echo     config.local.json         - Local overrides (optional)
echo.
echo ENVIRONMENT VARIABLES:
echo     SYNAPSE_ENV               - Environment name
echo     SYNAPSE_DB_TYPE           - Database type
echo     SYNAPSE_MARIADB_HOST      - MariaDB host
echo     SYNAPSE_MARIADB_PORT      - MariaDB port
echo     SYNAPSE_MARIADB_USER      - MariaDB user
echo     SYNAPSE_MARIADB_PASSWORD  - MariaDB password
echo     SYNAPSE_MARIADB_DATABASE  - MariaDB database name
echo.
exit /b 0

:determine_config_file
if not "%CONFIG_FILE%"=="" (
    if not exist "%CONFIG_FILE%" (
        echo [ERROR] Config file not found: %CONFIG_FILE%
        exit /b 1
    )
    echo [INFO] Using config file: %CONFIG_FILE%
    goto :eof
)

REM Use environment-based config
if "%ENV%"=="development" (
    if "%DB_TYPE%"=="mariadb" (
        set "CONFIG_FILE=config.dev.mariadb.json"
    ) else (
        set "CONFIG_FILE=config.dev.json"
    )
) else if "%ENV%"=="test" (
    set "CONFIG_FILE=config.test.json"
) else if "%ENV%"=="production" (
    set "CONFIG_FILE=config.prod.json"
) else (
    echo [ERROR] Unknown environment: %ENV%
    exit /b 1
)

echo [INFO] Auto-selected config file: %CONFIG_FILE%
goto :eof

:create_default_configs
REM Create config.dev.json (DuckDB)
if not exist config.dev.json (
    echo [WARNING] config.dev.json not found, creating default...
    (
        echo {
        echo     "database": {
        echo         "type": "duckdb",
        echo         "duckdb": {
        echo             "db_path": "synapse_dev.duckdb"
        echo         }
        echo     },
        echo     "memory_dir": "memories_dev",
        echo     "documents_dir": "documents_dev",
        echo     "log_level": "DEBUG"
        echo }
    ) > config.dev.json
    echo [SUCCESS] Created config.dev.json
)

REM Create config.dev.mariadb.json (MariaDB)
if not exist config.dev.mariadb.json (
    echo [WARNING] config.dev.mariadb.json not found, creating default...
    (
        echo {
        echo     "database": {
        echo         "type": "mariadb",
        echo         "mariadb": {
        echo             "host": "127.0.0.1",
        echo             "port": 3307,
        echo             "user": "synapse_user",
        echo             "password": "synapse_pass_2024",
        echo             "database": "synapse"
        echo         }
        echo     },
        echo     "memory_dir": "memories_dev",
        echo     "log_level": "DEBUG",
        echo     "encoding": "utf-8",
        echo     "embedded_mariadb": {
        echo         "enabled": true,
        echo         "auto_start": true,
        echo         "data_directory": "synapse_mariadb_data",
        echo         "port": 3307,
        echo         "root_password": "synapse_root_2024",
        echo         "database_name": "synapse",
        echo         "user_name": "synapse_user",
        echo         "user_password": "synapse_pass_2024"
        echo     }
        echo }
    ) > config.dev.mariadb.json
    echo [SUCCESS] Created config.dev.mariadb.json
)

REM Create config.test.json
if not exist config.test.json (
    echo [WARNING] config.test.json not found, creating default...
    (
        echo {
        echo     "database": {
        echo         "type": "duckdb",
        echo         "duckdb": {
        echo             "db_path": "synapse_test.duckdb"
        echo         }
        echo     },
        echo     "memory_dir": "memories_test",
        echo     "documents_dir": "documents_test",
        echo     "log_level": "ERROR"
        echo }
    ) > config.test.json
    echo [SUCCESS] Created config.test.json
)

REM Create config.prod.json
if not exist config.prod.json (
    echo [WARNING] config.prod.json not found, creating default...
    (
        echo {
        echo     "database": {
        echo         "type": "duckdb",
        echo         "duckdb": {
        echo             "db_path": "synapse.duckdb"
        echo         }
        echo     },
        echo     "memory_dir": "memories",
        echo     "documents_dir": "documents",
        echo     "log_level": "WARNING"
        echo }
    ) > config.prod.json
    echo [SUCCESS] Created config.prod.json
)

goto :eof

:check_virtual_env
if "%VIRTUAL_ENV%"=="" (
    echo [WARNING] Not in a virtual environment!
    echo [INFO] It's recommended to use a virtual environment:
    echo [INFO]   python -m venv .venv
    echo [INFO]   .venv\Scripts\activate
    echo.
    set /p "continue=Continue anyway? (y/N): "
    if /i not "!continue!"=="y" exit /b 1
) else (
    echo [SUCCESS] Virtual environment detected: %VIRTUAL_ENV%
)
goto :eof

:check_dependencies
echo [INFO] Checking dependencies...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.12+.
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python version: %PYTHON_VERSION%

REM Check if requirements are installed
python -c "import fastmcp" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] FastMCP not found. Installing dependencies...
    if exist requirements.txt (
        pip install -r requirements.txt
        if errorlevel 1 (
            echo [ERROR] Failed to install dependencies.
            exit /b 1
        )
    ) else (
        echo [ERROR] requirements.txt not found. Please install dependencies manually.
        exit /b 1
    )
)

REM Check MariaDB if needed
if "%DB_TYPE%"=="mariadb" goto check_mariadb
if "%DB_TYPE%"=="auto" goto check_mariadb
goto skip_mariadb_check

:check_mariadb
if "%NO_EMBEDDED_DB%"=="true" goto skip_mariadb_check

mysqld --version >nul 2>&1
if errorlevel 1 (
    mariadbd --version >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] MariaDB/MySQL server not found.
        echo [INFO] Installing MariaDB is recommended for development.
        echo [INFO] Download from: https://mariadb.org/download/
        echo [INFO] Or use SQLite config: %~0 --config config.dev.json
        echo.
        set /p "continue=Continue with SQLite fallback? (y/N): "
        if /i "!continue!"=="y" (
            set "CONFIG_FILE=config.dev.json"
            set "DB_TYPE=sqlite"
            echo [INFO] Switched to SQLite configuration
        ) else (
            exit /b 1
        )
    ) else (
        echo [SUCCESS] MariaDB server found
    )
) else (
    echo [SUCCESS] MySQL server found
)

:skip_mariadb_check
goto :eof

:pre_flight_checks
echo [INFO] Running pre-flight checks...

REM Check if main.py exists
if not exist main.py (
    echo [ERROR] main.py not found. Are you in the Synapse project directory?
    exit /b 1
)

REM Create default config files
call :create_default_configs

REM Determine which config file to use
call :determine_config_file
if errorlevel 1 exit /b 1

REM Create memories directory based on environment
set "memory_dir=memories_dev"
if "%ENV%"=="test" set "memory_dir=memories_test"
if "%ENV%"=="production" set "memory_dir=memories"

if not exist "%memory_dir%" (
    mkdir "%memory_dir%"
    echo [SUCCESS] Created %memory_dir% directory
)

echo [SUCCESS] Pre-flight checks completed
goto :eof

:start_server
echo [INFO] Starting Synapse MCP Server...
echo.
echo [INFO] Configuration:
echo [INFO]   Config File: %CONFIG_FILE%
echo [INFO]   Environment: %ENV%
echo [INFO]   Host: %HOST%
echo [INFO]   Port: %PORT%
echo [INFO]   Database: %DB_TYPE%
echo [INFO]   Log Level: %LOG_LEVEL%
if "%NO_EMBEDDED_DB%"=="true" echo [INFO]   Embedded DB: disabled
echo.

REM Build command arguments
set "CMD_ARGS=--env %ENV% --host %HOST% --port %PORT% --db-type %DB_TYPE% --log-level %LOG_LEVEL%"
if "%NO_EMBEDDED_DB%"=="true" set "CMD_ARGS=%CMD_ARGS% --no-embedded-db"

echo [SUCCESS] 🚀 Starting server with: python main.py %CMD_ARGS%
echo.

REM Start the server with proper error handling
python main.py %CMD_ARGS%
if errorlevel 1 (
    echo.
    echo [ERROR] Server failed to start. Check the error messages above.
    pause
    exit /b 1
)

goto :eof