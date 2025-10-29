@echo off
REM Setup Unreal Engine Project for Python Remote Execution
REM This is a convenience wrapper for setup_unreal_remote.py

echo ============================================================
echo Unreal Engine Python Remote Execution Setup
echo ============================================================
echo.

cd /d "%~dp0.."

REM Check if project path is provided
if "%~1"=="" (
    echo Usage: setup_unreal_remote.bat "C:\Path\To\Project.uproject"
    echo.
    echo This script will:
    echo   1. Enable required plugins
    echo   2. Configure remote execution
    echo   3. Create init_unreal.py startup script
    echo   4. Setup scripts directory with .env file
    echo   5. Copy unreallib, examples, and remotecontrol modules
    echo.
    pause
    exit /b 1
)

REM Run the Python setup script
python env_setup\setup_unreal_remote.py --project "%~1"

pause
