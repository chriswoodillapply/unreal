@echo off
REM Python Environment Setup for Unreal Remote Control
REM Creates virtual environment and installs dependencies

echo ============================================================
echo Python Environment Setup
echo ============================================================
echo.

cd /d "%~dp0.."

REM Check if virtual environment exists
IF EXIST "venv\" (
    echo Virtual environment already exists.
    echo To recreate it, delete the venv folder first.
    echo.
    choice /C YN /M "Do you want to use the existing environment"
    if errorlevel 2 exit /b 0
) ELSE (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Error: Failed to create virtual environment
        echo Make sure Python 3.10+ is installed and in PATH
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install requirements
echo.
echo Installing required packages...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo [SUCCESS] Python environment setup complete!
    echo ============================================================
    echo.
    echo Installed packages:
    echo   - upyrc (Unreal Python Remote Control^)
    echo   - pytest (testing framework^)
    echo   - python-dotenv (environment configuration^)
    echo.
    echo Virtual environment location: venv\
    echo.
    echo To activate in future sessions:
    echo   venv\Scripts\activate.bat
    echo.
    echo To deactivate:
    echo   deactivate
    echo.
    pause
    exit /b 0
) else (
    echo.
    echo ============================================================
    echo [ERROR] Installation failed
    echo ============================================================
    echo.
    echo Please check:
    echo   - Internet connection
    echo   - No proxy/firewall blocking pip
    echo   - Python version is 3.10 or higher
    echo.
    pause
    exit /b 1
)
