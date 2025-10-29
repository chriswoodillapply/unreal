@echo off
REM Main setup script - delegates to env_setup scripts
REM This provides a simple entry point for new users

echo ============================================================
echo Unreal Engine Python Remote Control - Setup
echo ============================================================
echo.
echo This setup will:
echo   1. Create Python virtual environment
echo   2. Install required packages
echo.
echo For Unreal project configuration, use:
echo   env_setup\setup_unreal_remote.bat "path\to\project.uproject"
echo.
echo ============================================================
echo.

REM Run Python environment setup
call env_setup\setup_python_env.bat

echo.
echo ============================================================
echo Main Setup Complete
echo ============================================================
echo.
echo Next steps:
echo.
echo 1. Configure your Unreal project:
echo    env_setup\setup_unreal_remote.bat "C:\Path\To\Project.uproject"
echo.
echo 2. Open your project in Unreal Editor
echo.
echo 3. Test remote execution:
echo    python -m remotecontrol examples\spawn_shapes.py --method=file
echo.
echo For detailed documentation, see:
echo    docs\README.md
echo    docs\QUICKSTART.md
echo.
pause
