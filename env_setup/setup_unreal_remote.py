"""
Unreal Engine Python Remote Execution Setup

This script configures an Unreal Engine project for Python remote execution:
1. Enables required plugins (PythonScriptPlugin, RemoteControl, etc.)
2. Configures DefaultEngine.ini for remote execution
3. Creates init_unreal.py startup script with file watcher
4. Sets up scripts directory with .env configuration

Usage:
    python env_setup/setup_unreal_remote.py --project "C:/Path/To/Project.uproject"
    
    Optional flags:
    --multicast-host    Multicast IP (default: 239.0.0.1)
    --multicast-port    Multicast port (default: 6766)
    --web-port          HTTP port for WebRemoteControl (default: 30010)
    --no-backup         Skip creating backups of modified files
"""

import sys
from pathlib import Path

# Add parent directory to path to import remotecontrol
sys.path.insert(0, str(Path(__file__).parent.parent))

from remotecontrol.setup import setup_project
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Setup Unreal Engine project for Python remote execution'
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to .uproject file'
    )
    parser.add_argument(
        '--multicast-host',
        default='239.0.0.1',
        help='Multicast group IP for upyrc (default: 239.0.0.1)'
    )
    parser.add_argument(
        '--multicast-port',
        type=int,
        default=6766,
        help='Multicast port for upyrc (default: 6766)'
    )
    parser.add_argument(
        '--web-port',
        type=int,
        default=30010,
        help='HTTP port for WebRemoteControl (default: 30010)'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup files'
    )
    
    args = parser.parse_args()
    
    # Run setup
    success = setup_project(
        project_path=Path(args.project),
        multicast_host=args.multicast_host,
        multicast_port=args.multicast_port,
        web_remote_port=args.web_port,
        backup=not args.no_backup
    )
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Open the project in Unreal Editor")
        print("2. Accept plugin rebuild if prompted")
        print("3. Check Output Log for 'Remote Execution (upyre) started'")
        print("4. Install Python dependencies in scripts directory:")
        print("   cd scripts")
        print("   pip install -r requirements.txt")
        print("5. Test the connection:")
        print("   python -m remotecontrol examples/spawn_shapes.py --method=file")
        return 0
    else:
        print("\n❌ Setup failed. Check error messages above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
