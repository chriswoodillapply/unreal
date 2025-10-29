# Environment Setup Scripts

This directory contains scripts to set up your development environment for Unreal Engine Python remote execution.

## 🚀 Quick Setup (First Time)

### Step 1: Python Environment

Setup Python virtual environment and install dependencies:

```batch
env_setup\setup_python_env.bat
```

This will:
- Create a Python virtual environment in `venv/`
- Install upyrc, pytest, python-dotenv, and other dependencies
- Activate the virtual environment

### Step 2: Unreal Project Configuration

Configure your Unreal Engine project for remote execution:

```batch
env_setup\setup_unreal_remote.bat "C:\Path\To\YourProject.uproject"
```

Or using Python directly:

```batch
python env_setup\setup_unreal_remote.py --project "C:\Path\To\YourProject.uproject"
```

This will:
- Enable required plugins (PythonScriptPlugin, RemoteControl, etc.)
- Configure DefaultEngine.ini for remote execution
- Create `Content/Python/init_unreal.py` startup script
- Setup `scripts/` directory with `.env` configuration file
- Copy `unreallib/`, `examples/`, and `remotecontrol/` modules to your project

## 📁 Scripts Overview

### `setup_python_env.bat`
**Purpose**: Initialize Python virtual environment  
**What it does**:
- Creates `venv/` virtual environment
- Upgrades pip
- Installs all requirements from `requirements.txt`
- Activates the environment

**Usage**:
```batch
env_setup\setup_python_env.bat
```

---

### `setup_unreal_remote.bat`
**Purpose**: Configure Unreal project for remote execution  
**What it does**:
- Modifies `.uproject` to enable plugins
- Updates `Config/DefaultEngine.ini` with remote execution settings
- Creates `Content/Python/init_unreal.py` startup script
- Creates `scripts/.env` configuration
- Copies `unreallib/`, `examples/`, and `remotecontrol/` to project scripts folder

**Usage**:
```batch
env_setup\setup_unreal_remote.bat "C:\Path\To\Project.uproject"
```

---

### `setup_unreal_remote.py`
**Purpose**: Python implementation of Unreal project setup  
**What it does**: Same as the batch file, but with more options

**Usage**:
```batch
python env_setup\setup_unreal_remote.py --project "C:\Path\To\Project.uproject"
```

**Options**:
- `--project PATH` - Path to .uproject file (required)
- `--multicast-host IP` - Multicast IP (default: 239.0.0.1)
- `--multicast-port PORT` - Multicast port (default: 6766)
- `--web-port PORT` - HTTP port for WebRemoteControl (default: 30010)
- `--no-backup` - Skip creating backup files

**Example with custom ports**:
```batch
python env_setup\setup_unreal_remote.py ^
    --project "C:\MyProject\MyProject.uproject" ^
    --multicast-port 7777 ^
    --web-port 30020
```

## 🔧 What Gets Modified

### 1. YourProject.uproject
Adds/enables these plugins:
- `PythonScriptPlugin` - Python scripting support
- `PythonFoundationPackages` - Python standard libraries
- `PythonAutomationTest` - Python testing support
- `RemoteControl` - Remote control API

**Backup created**: `YourProject.uproject.backup`

### 2. Config/DefaultEngine.ini
Adds these sections:

```ini
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
bRemoteExecution=True
RemoteExecutionMulticastGroupEndpoint=239.0.0.1:6766
RemoteExecutionMulticastBindAddress=0.0.0.0
RemoteExecutionSendBufferSizeBytes=2097152
RemoteExecutionReceiveBufferSizeBytes=2097152
RemoteExecutionMulticastTtl=0

[/Script/WebRemoteControl.WebRemoteControlSettings]
bServerStartByDefault=True
RemoteControlHttpServerPort=30010
+RemoteControlAllowlist=/Script/PythonScriptPlugin.PythonScriptLibrary
```

**Backup created**: `DefaultEngine.ini.backup`

### 3. Content/Python/init_unreal.py
Creates startup script that:
- Adds `scripts/` folder to Python path (enables `import unreallib`)
- Starts file-based command watcher
- Monitors `.unreal_command.py` for external commands
- Initializes remote execution listener
- Logs startup information to Output Log

**Backup created**: `init_unreal.py.backup` (if file exists)

### 4. scripts/.env
Creates configuration file with project-specific settings:

```env
# Project Configuration
UNREAL_PROJECT_PATH=C:/Path/To/YourProject.uproject
UNREAL_ENGINE_PATH=C:/Program Files/Epic Games/UE_5.6

# Remote Control
UNREAL_REMOTE_PORT=6766
UNREAL_MULTICAST_GROUP=239.0.0.1
UNREAL_MULTICAST_TTL=1

# Scene Configuration
CLEAR_SCENE_BEFORE_POPULATE=false
DEFAULT_ACTOR_SCALE=1.0
```

**Backup created**: `.env.backup` (if file exists)

## 🧪 Verify Setup

After running setup, verify everything works:

### 1. Start Unreal Editor
Open your project. You should see in the Output Log:
```
LogPython: ✓ Added to Python path: C:/YourProject/scripts
LogPython: Python Command Watcher started
LogPython: Watching: C:/YourProject/scripts/.unreal_command.py
LogPython: Remote Execution (upyre) started:
LogPython:   Multicast: 239.0.0.1:6766
```

### 2. Test Python Environment
```batch
cd scripts
venv\Scripts\activate
python -c "import unreal; import upyrc; print('✓ Environment OK')"
```

### 3. Test Remote Execution
```batch
python -m remotecontrol examples/spawn_shapes.py --method=file
```

You should see shapes spawn in your Unreal level!

## 🔄 Re-running Setup

### To update an existing project:
Just run the setup again. Backups will be created before modifying any files.

### To reset everything:
1. Delete backups: `*.backup` files
2. Remove `Content/Python/init_unreal.py`
3. Manually remove added sections from `Config/DefaultEngine.ini`
4. Manually remove plugins from `.uproject`

### To recreate Python environment:
```batch
rmdir /s /q venv
env_setup\setup_python_env.bat
```

## 📚 Next Steps

After setup is complete:

1. **Review Configuration**: Check `scripts/.env` and adjust paths if needed
2. **Install Dependencies**: Make sure `pip install -r requirements.txt` completed
3. **Read Documentation**: See `docs/README_CLEAN.md` for complete guide
4. **Try Examples**: Run example scripts from `examples/` directory
5. **Run Tests**: Execute `pytest tests/` to verify everything works

## 🐛 Troubleshooting

### "Virtual environment creation failed"
- Ensure Python 3.10+ is installed
- Check Python is in system PATH
- Try: `python --version`

### "Project file not found"
- Use absolute path to .uproject file
- Ensure path is in quotes if it contains spaces
- Check file extension is exactly `.uproject`

### "Permission denied" errors
- Run as Administrator
- Close Unreal Editor before modifying project files
- Check file permissions on project directory

### "Module 'unreal' not found"
- Only import `unreal` inside functions that run in Unreal
- Use lazy imports: `import unreal` inside `execute()` methods
- Check init_unreal.py was created and loads on startup

### "Remote execution not working"
- Check Output Log for startup messages
- Verify firewall isn't blocking ports 6766, 30010
- Try `--method=file` instead of upyrc
- Check `scripts/.unreal_command.py` exists and is writable

## 📞 Support

For more help:
- **Quick Start Guide**: `docs/QUICKSTART.md`
- **upyrc Setup Guide**: `docs/QUICKSTART_UPYRC.md`
- **Testing Guide**: `docs/TESTING_CHECKLIST.md`
- **Complete Documentation**: `docs/README_CLEAN.md`
