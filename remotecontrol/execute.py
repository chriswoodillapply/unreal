"""
Command-line tool for executing Python code in Unreal Engine

Usage:
    python -m remotecontrol.execute "import unreal; unreal.log('Hello!')"
    python -m remotecontrol.execute script.py
    python -m remotecontrol.execute examples/spawn_grid.py
    python -m remotecontrol.execute --method upyrc script.py
    python -m remotecontrol.execute --method file "import unreal; unreal.log('Test')"
"""

import sys
import argparse
from pathlib import Path
from .client import UnrealRemoteClient
from .config import RemoteControlConfig


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Execute Python code in Unreal Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute inline code
  python -m remotecontrol.execute "import unreal; unreal.log('Hello!')"
  
  # Execute a script file
  python -m remotecontrol.execute examples/spawn_grid.py
  
  # Force specific method
  python -m remotecontrol.execute --method upyrc script.py
  python -m remotecontrol.execute --method file script.py
  
  # Test connection
  python -m remotecontrol.execute --test
        """
    )
    
    parser.add_argument(
        'code_or_file',
        nargs='?',
        help='Python code string or path to .py file'
    )
    
    parser.add_argument(
        '--method',
        choices=['auto', 'upyrc', 'file'],
        default='auto',
        help='Execution method (default: auto)'
    )
    
    parser.add_argument(
        '--exec-type',
        choices=['file', 'statement'],
        default='file',
        help='Execution type for upyrc (default: file)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test connection to Unreal Engine'
    )
    
    parser.add_argument(
        '--config',
        type=Path,
        help='Path to .env config file'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = RemoteControlConfig(args.config) if args.config else RemoteControlConfig()
    client = UnrealRemoteClient(config)
    
    # Test connection if requested
    if args.test:
        print("Testing connection to Unreal Engine...")
        success = client.test_connection(method=args.method)
        return 0 if success else 1
    
    # Require code or file
    if not args.code_or_file:
        parser.print_help()
        return 1
    
    # Check if it's a file
    potential_file = Path(args.code_or_file)
    
    if potential_file.exists() and potential_file.suffix == '.py':
        # Execute file
        success = client.execute_file(
            potential_file,
            method=args.method,
            exec_type=args.exec_type,
            raise_on_error=False
        )
    else:
        # Execute inline code
        success = client.execute(
            args.code_or_file,
            method=args.method,
            exec_type=args.exec_type,
            raise_on_error=False
        )
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
