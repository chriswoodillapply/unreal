"""
Setup Unreal Remote Control for a new project

This script:
1. Enables required plugins in .uproject file
2. Configures remote execution in DefaultEngine.ini
3. Creates init_unreal.py startup script
4. Creates .env configuration file
"""

import sys
import json
import shutil
from pathlib import Path
from typing import Optional
import argparse


def setup_project(
    project_path: Path,
    multicast_host: str = '239.0.0.1',
    multicast_port: int = 6766,
    web_remote_port: int = 30010,
    backup: bool = True
) -> bool:
    """
    Setup remote control for an Unreal project
    
    Args:
        project_path: Path to .uproject file
        multicast_host: Multicast group IP for upyrc
        multicast_port: Multicast port for upyrc
        web_remote_port: HTTP port for WebRemoteControl
        backup: Create backups of modified files
    
    Returns:
        True if successful
    """
    project_path = Path(project_path)
    
    if not project_path.exists():
        print(f"✗ Error: Project file not found: {project_path}")
        return False
    
    if project_path.suffix != '.uproject':
        print(f"✗ Error: Not a .uproject file: {project_path}")
        return False
    
    project_dir = project_path.parent
    project_name = project_path.stem
    
    print(f"\n{'='*60}")
    print(f"Setting up Unreal Remote Control")
    print(f"{'='*60}")
    print(f"Project: {project_name}")
    print(f"Path: {project_dir}")
    print(f"\n")
    
    # Step 1: Enable plugins in .uproject
    success = _setup_uproject(project_path, backup)
    if not success:
        return False
    
    # Step 2: Configure DefaultEngine.ini
    config_dir = project_dir / 'Config'
    engine_ini = config_dir / 'DefaultEngine.ini'
    success = _setup_engine_ini(
        engine_ini,
        multicast_host,
        multicast_port,
        web_remote_port,
        backup
    )
    if not success:
        return False
    
    # Step 3: Create init_unreal.py startup script
    python_dir = project_dir / 'Content' / 'Python'
    init_script = python_dir / 'init_unreal.py'
    success = _create_init_script(init_script, project_dir, backup)
    if not success:
        return False
    
    # Step 4: Create scripts folder and .env
    scripts_dir = project_dir / 'scripts'
    scripts_dir.mkdir(exist_ok=True)
    env_file = scripts_dir / '.env'
    success = _create_env_file(
        env_file,
        project_name,
        project_dir,
        multicast_host,
        multicast_port,
        web_remote_port,
        backup
    )
    if not success:
        return False
    
    # Step 5: Copy required libraries and examples
    success = _copy_libraries(scripts_dir)
    if not success:
        return False
    
    print(f"\n{'='*60}")
    print("✓ Setup Complete!")
    print(f"{'='*60}")
    print("\nNext steps:")
    print("1. Open the project in Unreal Editor")
    print("2. Check Output Log for 'Remote Execution (upyre) started'")
    print("3. Test with a simple command:")
    print(f"   cd {scripts_dir}")
    print("   python -m remotecontrol --method file \"import unreal; unreal.log('Hello!')\"")
    print("4. Try the examples:")
    print("   python -m remotecontrol examples/spawn_shapes.py --method file")
    print("")
    
    return True


def _setup_uproject(project_path: Path, backup: bool) -> bool:
    """Enable required plugins in .uproject"""
    print("Step 1: Enabling plugins in .uproject...")
    
    try:
        # Backup if requested
        if backup and project_path.exists():
            backup_path = project_path.with_suffix('.uproject.backup')
            shutil.copy2(project_path, backup_path)
            print(f"  Created backup: {backup_path.name}")
        
        # Read current project file
        with open(project_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        # Ensure Plugins section exists
        if 'Plugins' not in project_data:
            project_data['Plugins'] = []
        
        # Required plugins
        required_plugins = [
            'PythonScriptPlugin',
            'PythonFoundationPackages',
            'PythonAutomationTest',
            'RemoteControl'
        ]
        
        # Add missing plugins
        existing_plugins = {p['Name'] for p in project_data['Plugins'] if 'Name' in p}
        
        for plugin_name in required_plugins:
            if plugin_name not in existing_plugins:
                project_data['Plugins'].append({
                    'Name': plugin_name,
                    'Enabled': True
                })
                print(f"  + Added plugin: {plugin_name}")
            else:
                # Make sure it's enabled
                for plugin in project_data['Plugins']:
                    if plugin.get('Name') == plugin_name:
                        plugin['Enabled'] = True
                print(f"  ✓ Plugin already present: {plugin_name}")
        
        # Write updated project file
        with open(project_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent='\t')
        
        print("  ✓ Plugins configured\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        return False


def _setup_engine_ini(
    engine_ini: Path,
    multicast_host: str,
    multicast_port: int,
    web_remote_port: int,
    backup: bool
) -> bool:
    """Configure DefaultEngine.ini for remote execution"""
    print("Step 2: Configuring DefaultEngine.ini...")
    
    try:
        # Create Config directory if needed
        engine_ini.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup if requested
        if backup and engine_ini.exists():
            backup_path = engine_ini.with_suffix('.ini.backup')
            shutil.copy2(engine_ini, backup_path)
            print(f"  Created backup: {backup_path.name}")
        
        # Read existing config
        if engine_ini.exists():
            with open(engine_ini, 'r', encoding='utf-8') as f:
                config_lines = f.readlines()
        else:
            config_lines = []
        
        # Python script plugin configuration
        python_config = f"""
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
bRemoteExecution=True
RemoteExecutionMulticastGroupEndpoint={multicast_host}:{multicast_port}
RemoteExecutionMulticastBindAddress=0.0.0.0
RemoteExecutionSendBufferSizeBytes=2097152
RemoteExecutionReceiveBufferSizeBytes=2097152
RemoteExecutionMulticastTtl=0
"""

        # WebRemoteControl configuration (part of RemoteControl plugin)
        web_config = f"""
[/Script/WebRemoteControl.WebRemoteControlSettings]
bServerStartByDefault=True
RemoteControlHttpServerPort={web_remote_port}
+RemoteControlAllowlist=/Script/PythonScriptPlugin.PythonScriptLibrary
"""

        # Remove existing sections if present
        filtered_lines = []
        skip_section = False
        for line in config_lines:
            if line.strip().startswith('[/Script/PythonScriptPlugin.PythonScriptPluginSettings]'):
                skip_section = True
            elif line.strip().startswith('[/Script/WebRemoteControl.WebRemoteControlSettings]'):
                skip_section = True
            elif line.strip().startswith('[') and line.strip() != '[':
                skip_section = False
            
            if not skip_section:
                filtered_lines.append(line)
        
        # Add our configurations
        config_content = ''.join(filtered_lines).rstrip() + '\n' + python_config + '\n' + web_config
        
        # Write updated config
        with open(engine_ini, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"  + Python remote execution: {multicast_host}:{multicast_port}")
        print(f"  + WebRemoteControl: localhost:{web_remote_port}")
        print("  ✓ Engine configuration updated\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        return False


def _create_init_script(init_script: Path, project_dir: Path, backup: bool) -> bool:
    """Create init_unreal.py startup script"""
    print("Step 3: Creating init_unreal.py...")
    
    try:
        # Create Content/Python directory
        init_script.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup if requested
        if backup and init_script.exists():
            backup_path = init_script.with_suffix('.py.backup')
            shutil.copy2(init_script, backup_path)
            print(f"  Created backup: {backup_path.name}")
        
        # Get scripts directory path
        scripts_dir = project_dir / 'scripts'
        command_file = scripts_dir / '.unreal_command.py'
        
        # Create init_unreal.py content
        init_content = f'''"""
Unreal Engine Startup Script - Enables Python command reception

This script runs when Unreal starts and sets up:
1. File-based command watcher
2. Remote execution (upyre) listener
3. Python path for unreallib module access
"""

import unreal
import sys
import threading
import time
from pathlib import Path

# Add scripts folder to Python path so we can import unreallib
SCRIPTS_DIR = Path(r"{scripts_dir.as_posix()}")
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
    unreal.log(f"✓ Added to Python path: {{SCRIPTS_DIR}}")

# Command file location
COMMAND_FILE = Path(r"{command_file.as_posix()}")
COMMAND_FILE.parent.mkdir(parents=True, exist_ok=True)

class UnrealCommandWatcher:
    """Watch for command files and execute them"""
    
    def __init__(self):
        self.running = True
        self.last_modified = 0
        unreal.log("Python Command Watcher started")
        unreal.log(f"Watching: {{COMMAND_FILE}}")
    
    def check_for_commands(self):
        """Check if command file has been updated"""
        try:
            if COMMAND_FILE.exists():
                current_modified = COMMAND_FILE.stat().st_mtime
                
                if current_modified > self.last_modified:
                    self.last_modified = current_modified
                    
                    # Read and execute command
                    with open(COMMAND_FILE, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    if code.strip():
                        unreal.log("Executing external command...")
                        try:
                            exec(code, {{'unreal': unreal}})
                            unreal.log("✓ Command executed successfully")
                        except Exception as e:
                            unreal.log_error(f"Error executing command: {{e}}")
                    
                    # Clear the file
                    with open(COMMAND_FILE, 'w') as f:
                        f.write("")
        
        except Exception as e:
            unreal.log_warning(f"Command watcher error: {{e}}")
    
    def start(self):
        """Start watching (runs in main thread via timer)"""
        def tick():
            if self.running:
                self.check_for_commands()
                # Schedule next tick
                unreal.PythonScriptLibrary.set_editor_timer_override(
                    "UnrealCommandWatcher",
                    0.5,  # Check every 0.5 seconds
                    False
                )
        
        # Start the timer
        unreal.PythonScriptLibrary.set_editor_timer_override(
            "UnrealCommandWatcher", 
            0.5,
            False
        )
        unreal.log("✓ Command watcher active")

# Create and start watcher
watcher = UnrealCommandWatcher()

# Start checking for commands (non-blocking)
unreal.log("=" * 60)
unreal.log("Unreal Python Command Interface Ready")
unreal.log(f"Send commands to: {{COMMAND_FILE}}")
unreal.log("=" * 60)

# Start Remote Execution (upyre) listener
try:
    import remote_execution
    import __main__
    __main__._remote_exec = remote_execution.RemoteExecution()
    config = remote_execution.RemoteExecutionConfig()
    unreal.log("")
    unreal.log("Remote Execution (upyre) started:")
    unreal.log(f"  Multicast: {{config.multicast_group_endpoint}}")
    unreal.log(f"  Command: {{config.command_endpoint}}")
except Exception as e:
    unreal.log_warning(f"Could not start Remote Execution: {{e}}")

# Initial check
watcher.check_for_commands()

# Set up periodic checking using editor tick
def check_commands(delta_time):
    """Called by editor tick"""
    watcher.check_for_commands()

unreal.register_slate_post_tick_callback(check_commands)
unreal.log("✓ Slate tick callback registered")
'''
        
        # Write init script
        with open(init_script, 'w', encoding='utf-8') as f:
            f.write(init_content)
        
        print(f"  Created: {init_script.relative_to(project_dir)}")
        print("  ✓ Startup script created\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        return False


def _create_env_file(
    env_file: Path,
    project_name: str,
    project_dir: Path,
    multicast_host: str,
    multicast_port: int,
    web_remote_port: int,
    backup: bool
) -> bool:
    """Create .env configuration file"""
    print("Step 4: Creating .env configuration...")
    
    try:
        # Backup if requested
        if backup and env_file.exists():
            backup_path = env_file.with_suffix('.env.backup')
            shutil.copy2(env_file, backup_path)
            print(f"  Created backup: {backup_path.name}")
        
        env_content = f"""# Unreal Engine Configuration
UNREAL_ENGINE_PATH=C:/Program Files/Epic Games/UE_5.6/Engine/Binaries/Win64/UnrealEditor-Cmd.exe

# Project Configuration
PROJECT={project_name}
PROJECT_FOLDER={project_dir.as_posix()}
PROJECT_FILE={project_name}.uproject

# Level Configuration
LEVEL=Main
LEVEL_PATH=/Game/Main
AUTO_LOAD_LEVEL=true

# Remote Control Settings (upyrc/UDP)
UNREAL_REMOTE_HOST={multicast_host}
UNREAL_REMOTE_PORT={multicast_port}
UNREAL_BIND_ADDRESS=0.0.0.0
UNREAL_COMMAND_HOST=127.0.0.1
UNREAL_COMMAND_PORT={multicast_port + 10}

# WebRemoteControl Settings (HTTP)
WEB_REMOTE_ENABLED=true
WEB_REMOTE_HOST=localhost
WEB_REMOTE_PORT={web_remote_port}

# Scene Population Settings
GRID_ROWS=5
GRID_COLS=5
GRID_SPACING=200
CIRCLE_OBJECTS=12
CIRCLE_RADIUS=500
SPIRAL_OBJECTS=20
SPIRAL_MAX_RADIUS=800
SPIRAL_HEIGHT_INCREMENT=50
SCATTER_OBJECTS=30
SCATTER_AREA_SIZE=1000

# Logging
LOG_LEVEL=INFO
ENABLE_VERBOSE_LOGGING=false
"""
        
        # Write .env file
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"  Created: {env_file.relative_to(project_dir)}")
        print("  ✓ Configuration file created\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        return False


def _copy_libraries(scripts_dir: Path) -> bool:
    """Copy unreallib, examples, and remotecontrol to the project scripts folder"""
    print("Step 5: Copying libraries and examples...")
    
    try:
        # Find the source directory (where this setup.py is located)
        source_scripts_dir = Path(__file__).parent.parent
        
        # Libraries to copy
        libraries = ['unreallib', 'examples', 'remotecontrol']
        
        for lib_name in libraries:
            source_lib = source_scripts_dir / lib_name
            dest_lib = scripts_dir / lib_name
            
            if source_lib.exists():
                # Copy the library
                if dest_lib.exists():
                    print(f"  ✓ {lib_name} already exists, skipping")
                else:
                    shutil.copytree(source_lib, dest_lib)
                    print(f"  + Copied {lib_name}/")
            else:
                print(f"  ! Warning: {lib_name} not found at {source_lib}")
        
        print("  ✓ Libraries copied\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        return False


def find_current_project() -> Optional[Path]:
    """
    Attempt to find the currently open Unreal project.
    
    First tries to detect from running Unreal Editor processes.
    Falls back to searching for .uproject files in workspace.
    
    Returns:
        Path to .uproject file if found, None otherwise
    """
    import subprocess
    
    # Try to find running Unreal Editor process with project file
    try:
        # Get all UnrealEditor processes with command line arguments
        cmd = 'Get-Process | Where-Object {$_.ProcessName -like "*UnrealEditor*"} | Select-Object -ExpandProperty Path'
        result = subprocess.run(
            ['powershell', '-Command', cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            # Found Unreal Editor process, now look for .uproject files being accessed
            # Check recent files in common Unreal project locations
            unreal_projects_dir = Path.home() / 'Documents' / 'Unreal Projects'
            
            if unreal_projects_dir.exists():
                # Find all .uproject files
                uprojects = list(unreal_projects_dir.rglob('*.uproject'))
                
                # Check which one was modified most recently (likely the open one)
                if uprojects:
                    most_recent = max(uprojects, key=lambda p: p.stat().st_mtime)
                    return most_recent
    except Exception as e:
        print(f"  (Could not detect running Unreal Editor: {e})")
    
    # Fallback: Try to find from current working directory
    cwd = Path.cwd()
    
    # Check if we're in a scripts folder
    if cwd.name == 'scripts' and cwd.parent.is_dir():
        project_dir = cwd.parent
        uprojects = list(project_dir.glob('*.uproject'))
        if uprojects:
            return uprojects[0]
    
    # Check parent directories
    for parent in [cwd] + list(cwd.parents):
        uprojects = list(parent.glob('*.uproject'))
        if uprojects:
            return uprojects[0]
    
    return None


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Setup Unreal Remote Control for a project'
    )
    parser.add_argument(
        'project',
        nargs='?',
        type=Path,
        help='Path to .uproject file (optional - auto-detects if not provided)'
    )
    parser.add_argument(
        '--multicast-host',
        default='239.0.0.1',
        help='Multicast group IP (default: 239.0.0.1)'
    )
    parser.add_argument(
        '--multicast-port',
        type=int,
        default=6766,
        help='Multicast port (default: 6766)'
    )
    parser.add_argument(
        '--web-port',
        type=int,
        default=30010,
        help='WebRemoteControl port (default: 30010)'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup files'
    )
    
    args = parser.parse_args()
    
    # Auto-detect project if not provided
    project_path = args.project
    if not project_path:
        print("No project specified, attempting auto-detection...")
        project_path = find_current_project()
        if not project_path:
            print("✗ Error: Could not find .uproject file")
            print("Please specify project path or run from project directory")
            sys.exit(1)
        print(f"✓ Found project: {project_path}\n")
    
    success = setup_project(
        project_path,
        args.multicast_host,
        args.multicast_port,
        args.web_port,
        not args.no_backup
    )
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
