@echo off
REM Deploy latest libraries to target Unreal project

echo.
echo ====================================================================
echo DEPLOY LATEST LIBRARIES
echo ====================================================================
echo.

if "%~1"=="" (
    echo Usage: deploy.bat "path\to\target\project"
    echo.
    echo Example:
    echo   deploy.bat "C:\Users\cwood\Documents\Unreal Projects\Test1"
    echo   deploy.bat "..\Test1"
    echo.
    pause
    exit /b 1
)

REM Run deploy script
python "%~dp0deploy.py" "%~1"

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Deployment completed successfully!
) else (
    echo.
    echo [FAILED] Deployment encountered errors
)

echo.
pause
