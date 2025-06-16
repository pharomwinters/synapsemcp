#
# Synapse Development Server Startup Script for Windows PowerShell
# Enhanced version with config file support
#

param(
    [string]$Env = "development",
    [string]$Config = "",
    [string]$HostName = "127.0.0.1",
    [int]$Port = 8000,
    [string]$DbType = "auto",
    [switch]$NoEmbeddedDb,
    [string]$LogLevel = "INFO",
    [switch]$Help
)

# Colors for output
$Script:Colors = @{
    Info = "Cyan"
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor $Script:Colors.Info
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor $Script:Colors.Success
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor $Script:Colors.Warning
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor $Script:Colors.Error
}

function Show-Banner {
    Write-Host @"
 ____                                     
/ ___| _   _ _ __   __ _ _ __  ___  ___    
\___ \| | | | '_ \ / _` | '_ \/ __|/ _ \   
 ___) | |_| | | | | (_| | |_) \__ \  __/   
|____/ \__, |_| |_|\__,_| .__/|___/\___|   
       |___/            |_|               

🧠 AI-Human Collaboration Platform
    Where Intelligence Connects ⚡

"@ -ForegroundColor Magenta
}

function Show-Help {
    Write-Host @"
🧠 Synapse Development Server

Usage: .\synapse-dev.ps1 [OPTIONS]

OPTIONS:
    -Env ENV            Environment (development, production, test) [default: development]
    -Config FILE        Config file to use (overrides -Env)
    -Host HOST          Host to bind to [default: 127.0.0.1]
    -Port PORT          Port to bind to [default: 8000]
    -DbType TYPE        Database type (duckdb, sqlite, mariadb, auto) [default: auto]
    -NoEmbeddedDb       Don't start embedded MariaDB server
    -LogLevel LEVEL     Log level (DEBUG, INFO, WARNING, ERROR) [default: INFO]
    -Help               Show this help message

EXAMPLES:
    # Start with default settings (SQLite development)
    .\synapse-dev.ps1

    # Start with MariaDB development config
    .\synapse-dev.ps1 -Config config.dev.mariadb.json

    # Start in production mode
    .\synapse-dev.ps1 -Env production

    # Start with custom database type
    .\synapse-dev.ps1 -DbType mariadb

    # Start with debug logging
    .\synapse-dev.ps1 -LogLevel DEBUG

CONFIG FILES:
    config.dev.json           - SQLite development (default)
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

"@
}

function Test-VirtualEnvironment {
    if (-not $env:VIRTUAL_ENV) {
        Write-Warning "Not in a virtual environment!"
        Write-Info "It's recommended to use a virtual environment:"
        Write-Info "  python -m venv .venv"
        Write-Info "  .venv\Scripts\Activate.ps1"
        Write-Host ""
        
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            exit 1
        }
    } else {
        Write-Success "Virtual environment detected: $env:VIRTUAL_ENV"
    }
}

function Test-Dependencies {
    Write-Info "Checking dependencies..."
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python not found"
        }
        Write-Success "Python version: $($pythonVersion -replace 'Python ', '')"
    }
    catch {
        Write-Error "Python not found. Please install Python 3.12+."
        exit 1
    }
    
    # Check if requirements are installed
    try {
        python -c "import fastmcp" 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "FastMCP not found"
        }
    }
    catch {
        Write-Warning "FastMCP not found. Installing dependencies..."
        if (Test-Path "requirements.txt") {
            pip install -r requirements.txt
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Failed to install dependencies."
                exit 1
            }
        } else {
            Write-Error "requirements.txt not found. Please install dependencies manually."
            exit 1
        }
    }
    
    # Check MariaDB if needed
    if (($DbType -eq "mariadb" -or $DbType -eq "auto") -and -not $NoEmbeddedDb) {
        $mariadbFound = $false
        
        try {
            mysqld --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                $mariadbFound = $true
                Write-Success "MySQL server found"
            }
        } catch {}
        
        if (-not $mariadbFound) {
            try {
                mariadbd --version 2>$null
                if ($LASTEXITCODE -eq 0) {
                    $mariadbFound = $true
                    Write-Success "MariaDB server found"
                }
            } catch {}
        }
        
        if (-not $mariadbFound) {
            Write-Warning "MariaDB/MySQL server not found."
            Write-Info "Installing MariaDB is recommended for development."
            Write-Info "Download from: https://mariadb.org/download/"
            Write-Info "Or use DuckDB config: .\synapse-dev.ps1 -Config config.dev.json"
            Write-Host ""
            
            $continue = Read-Host "Continue with DuckDB fallback? (y/N)"
            if ($continue -eq "y" -or $continue -eq "Y") {
                $Script:Config = "config.dev.json"
                $Script:DbType = "duckdb"
                Write-Info "Switched to DuckDB configuration"
            } else {
                exit 1
            }
        }
    }
}

function New-DefaultConfigs {
    # Create config.dev.json (DuckDB)
    if (-not (Test-Path "config.dev.json")) {
        Write-Warning "config.dev.json not found, creating default..."
        
        $config = @{
            database = @{
                type = "duckdb"
                duckdb = @{
                    db_path = "synapse_dev.duckdb"
                }
            }
            memory_dir = "memories_dev"
            documents_dir = "documents_dev"
            log_level = "DEBUG"
        }
        
        $config | ConvertTo-Json -Depth 10 | Out-File -FilePath "config.dev.json" -Encoding UTF8
        Write-Success "Created config.dev.json"
    }
    
    # Create config.dev.mariadb.json (MariaDB)
    if (-not (Test-Path "config.dev.mariadb.json")) {
        Write-Warning "config.dev.mariadb.json not found, creating default..."
        
        $config = @{
            database = @{
                type = "mariadb"
                mariadb = @{
                    host = "127.0.0.1"
                    port = 3307
                    user = "synapse_user"
                    password = "synapse_pass_2024"
                    database = "synapse"
                }
            }
            memory_dir = "memories_dev"
            log_level = "DEBUG"
            encoding = "utf-8"
            embedded_mariadb = @{
                enabled = $true
                auto_start = $true
                data_directory = "synapse_mariadb_data"
                port = 3307
                root_password = "synapse_root_2024"
                database_name = "synapse"
                user_name = "synapse_user"
                user_password = "synapse_pass_2024"
            }
        }
        
        $config | ConvertTo-Json -Depth 10 | Out-File -FilePath "config.dev.mariadb.json" -Encoding UTF8
        Write-Success "Created config.dev.mariadb.json"
    }
    
    # Create config.test.json
    if (-not (Test-Path "config.test.json")) {
        Write-Warning "config.test.json not found, creating default..."
        
        $config = @{
            database = @{
                type = "duckdb"
                duckdb = @{
                    db_path = "synapse_test.duckdb"
                }
            }
            memory_dir = "memories_test"
            documents_dir = "documents_test"
            log_level = "ERROR"
        }
        
        $config | ConvertTo-Json -Depth 10 | Out-File -FilePath "config.test.json" -Encoding UTF8
        Write-Success "Created config.test.json"
    }
    
    # Create config.prod.json
    if (-not (Test-Path "config.prod.json")) {
        Write-Warning "config.prod.json not found, creating default..."
        
        $config = @{
            database = @{
                type = "duckdb"
                duckdb = @{
                    db_path = "synapse.duckdb"
                }
            }
            memory_dir = "memories"
            documents_dir = "documents"
            log_level = "WARNING"
        }
        
        $config | ConvertTo-Json -Depth 10 | Out-File -FilePath "config.prod.json" -Encoding UTF8
        Write-Success "Created config.prod.json"
    }
}

function Get-ConfigFile {
    if ($Config) {
        if (-not (Test-Path $Config)) {
            Write-Error "Config file not found: $Config"
            exit 1
        }
        Write-Info "Using config file: $Config"
        return $Config
    }
    
    # Use environment-based config
    switch ($Env) {
        "development" {
            if ($DbType -eq "mariadb") {
                $configFile = "config.dev.mariadb.json"
            } else {
                $configFile = "config.dev.json"
            }
        }
        "test" {
            $configFile = "config.test.json"
        }
        "production" {
            $configFile = "config.prod.json"
        }
        default {
            Write-Error "Unknown environment: $Env"
            exit 1
        }
    }
    
    Write-Info "Auto-selected config file: $configFile"
    return $configFile
}

function Invoke-PreFlightChecks {
    Write-Info "Running pre-flight checks..."
    
    # Check if main.py exists
    if (-not (Test-Path "main.py")) {
        Write-Error "main.py not found. Are you in the Synapse project directory?"
        exit 1
    }
    
    # Create default config files
    New-DefaultConfigs
    
    # Determine which config file to use
    $Script:Config = Get-ConfigFile
    
    # Create memories directory based on environment
    $memoryDir = switch ($Env) {
        "test" { "memories_test" }
        "production" { "memories" }
        default { "memories_dev" }
    }
    
    if (-not (Test-Path $memoryDir)) {
        New-Item -ItemType Directory -Path $memoryDir | Out-Null
        Write-Success "Created $memoryDir directory"
    }
    
    Write-Success "Pre-flight checks completed"
}

function Start-Server {
    Write-Info "Starting Synapse MCP Server..."
    Write-Host ""
    Write-Info "Configuration:"
    Write-Info "  Config File: $Config"
    Write-Info "  Environment: $Env"
    Write-Info "  Host: $Host"
    Write-Info "  Port: $Port"
    Write-Info "  Database: $DbType"
    Write-Info "  Log Level: $LogLevel"
    if ($NoEmbeddedDb) {
        Write-Info "  Embedded DB: disabled"
    }
    Write-Host ""
    
    # Build command arguments
    $cmdArgs = @(
        "--env", $Env,
        "--host", $Host,
        "--port", $Port,
        "--db-type", $DbType,
        "--log-level", $LogLevel
    )
    
    if ($NoEmbeddedDb) {
        $cmdArgs += "--no-embedded-db"
    }
    
    Write-Success "🚀 Starting server with: python main.py $($cmdArgs -join ' ')"
    Write-Host ""
    
    # Start the server
    try {
        python main.py @cmdArgs
    }
    catch {
        Write-Host ""
        Write-Error "Server failed to start. Check the error messages above."
        Read-Host "Press Enter to continue..."
        exit 1
    }
}

# Main execution
function Main {
    if ($Help) {
        Show-Help
        return
    }
    
    Show-Banner
    
    Write-Info "Synapse Development Server Startup"
    Write-Info "Environment: $Env | Database: $DbType | Port: $Port"
    Write-Host ""
    
    Test-VirtualEnvironment
    Test-Dependencies
    Invoke-PreFlightChecks
    
    Write-Host ""
    Write-Success "All checks passed! Starting server..."
    Write-Host ""
    
    Start-Server
}

# Handle Ctrl+C gracefully
$null = Register-EngineEvent PowerShell.Exiting -Action {
    Write-Info "Shutting down..."
}

# Run main function
try {
    Main
}
catch {
    Write-Error "An unexpected error occurred: $_"
    Read-Host "Press Enter to exit..."
    exit 1
}