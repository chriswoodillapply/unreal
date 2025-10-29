"""
Unreal Remote Client - Execute Python code in Unreal Engine

Provides unified interface for sending Python commands to Unreal via:
- upyrc (UDP multicast) - Primary method, requires RemoteExecution running
- File-based commands - Fallback method, requires init_unreal.py watcher
"""

import sys
import time
from pathlib import Path
from typing import Optional, Union
from .config import RemoteControlConfig


class UnrealRemoteClient:
    """Client for executing Python code in Unreal Engine"""
    
    def __init__(self, config: Optional[RemoteControlConfig] = None):
        """
        Initialize remote client
        
        Args:
            config: RemoteControlConfig instance. If None, creates from .env
        """
        self.config = config or RemoteControlConfig()
        self._upyrc_available = False
        self._check_upyrc()
    
    def _check_upyrc(self):
        """Check if upyrc is available"""
        try:
            from upyrc import upyre
            self._upyrc_available = True
        except ImportError:
            self._upyrc_available = False
    
    def execute(
        self,
        code: str,
        method: str = 'auto',
        exec_type: str = 'file',
        raise_on_error: bool = True
    ) -> bool:
        """
        Execute Python code in Unreal Engine
        
        Args:
            code: Python code to execute
            method: 'upyrc', 'file', or 'auto' (tries upyrc first, falls back to file)
            exec_type: 'file' or 'statement' (for upyrc execution mode)
            raise_on_error: Whether to raise exceptions or return False
        
        Returns:
            True if successful, False otherwise
        """
        if method == 'auto':
            if self._upyrc_available:
                try:
                    return self._execute_upyrc(code, exec_type, raise_on_error)
                except Exception as e:
                    print(f"upyrc failed: {e}, falling back to file method...")
                    return self._execute_file(code, raise_on_error)
            else:
                return self._execute_file(code, raise_on_error)
        
        elif method == 'upyrc':
            if not self._upyrc_available:
                error_msg = "upyrc not available. Install with: pip install upyrc"
                if raise_on_error:
                    raise RuntimeError(error_msg)
                print(f"Error: {error_msg}")
                return False
            return self._execute_upyrc(code, exec_type, raise_on_error)
        
        elif method == 'file':
            return self._execute_file(code, raise_on_error)
        
        else:
            raise ValueError(f"Invalid method: {method}. Use 'upyrc', 'file', or 'auto'")
    
    def _execute_upyrc(
        self,
        code: str,
        exec_type: str = 'file',
        raise_on_error: bool = True
    ) -> bool:
        """Execute code via upyrc (UDP multicast)"""
        from upyrc import upyre
        
        print(f"\n{'='*60}")
        print("Unreal Remote Control (upyrc/UDP)")
        print(f"{'='*60}")
        
        try:
            # Get upyrc configuration
            exec_config = self.config.get_upyrc_config()
            print(f"Project: {self.config.PROJECT_FILE}")
            print(f"Multicast: {exec_config.MULTICAST_GROUP}")
            
            # Show code preview
            code_preview = code[:100] + "..." if len(code) > 100 else code
            print(f"\nCode: {code_preview}")
            print("\nSending to Unreal Engine...")
            
            # Map exec_type string to enum
            exec_type_enum = (
                upyre.ExecTypes.EXECUTE_FILE if exec_type == 'file'
                else upyre.ExecTypes.EXECUTE_STATEMENT
            )
            
            # Execute
            with upyre.PythonRemoteConnection(exec_config) as conn:
                result = conn.execute_python_command(
                    code,
                    exec_type=exec_type_enum,
                    raise_exc=raise_on_error
                )
                
                print("✓ Command executed successfully!")
                if result:
                    if hasattr(result, 'output') and result.output:
                        print(f"\nOutput:\n{result.output}")
                    elif isinstance(result, list):
                        for item in result:
                            if hasattr(item, 'output') and item.output:
                                print(f"\n{item.type}: {item.output}")
            
            print(f"{'='*60}\n")
            return True
            
        except Exception as e:
            print(f"✗ Error: {e}")
            if raise_on_error:
                import traceback
                traceback.print_exc()
            self._print_troubleshooting()
            print(f"{'='*60}\n")
            return False
    
    def _execute_file(self, code: str, raise_on_error: bool = True) -> bool:
        """Execute code via file-based command system"""
        print(f"\n{'='*60}")
        print("Unreal Remote Control (File-based)")
        print(f"{'='*60}")
        
        try:
            command_file = self.config.COMMAND_FILE
            print(f"Command file: {command_file}")
            
            # Ensure parent directory exists
            command_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Show code preview
            code_preview = code[:100] + "..." if len(code) > 100 else code
            print(f"\nCode: {code_preview}")
            print("\nWriting to command file...")
            
            # Write code to command file
            with open(command_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            print("✓ Command written successfully!")
            print("\nWaiting for Unreal to process...")
            
            # Wait a moment for processing
            time.sleep(0.5)
            
            # Check if file was cleared (indicates processing)
            if command_file.exists():
                content = command_file.read_text(encoding='utf-8')
                if content.strip():
                    print("⚠ Warning: Command file not cleared (may not have been processed)")
                else:
                    print("✓ Command file cleared (processed by Unreal)")
            
            print(f"{'='*60}\n")
            return True
            
        except Exception as e:
            print(f"✗ Error: {e}")
            if raise_on_error:
                import traceback
                traceback.print_exc()
            self._print_troubleshooting()
            print(f"{'='*60}\n")
            return False
    
    def execute_file(
        self,
        script_path: Union[str, Path],
        method: str = 'auto',
        exec_type: str = 'file',
        raise_on_error: bool = True
    ) -> bool:
        """
        Execute a Python file in Unreal Engine
        
        Args:
            script_path: Path to Python script file
            method: 'upyrc', 'file', or 'auto'
            exec_type: 'file' or 'statement' (for upyrc execution mode)
            raise_on_error: Whether to raise exceptions
        
        Returns:
            True if successful, False otherwise
        """
        script_path = Path(script_path)
        
        if not script_path.exists():
            error_msg = f"File not found: {script_path}"
            if raise_on_error:
                raise FileNotFoundError(error_msg)
            print(f"Error: {error_msg}")
            return False
        
        print(f"Loading script: {script_path}")
        code = script_path.read_text(encoding='utf-8')
        return self.execute(code, method, exec_type, raise_on_error)
    
    def _print_troubleshooting(self):
        """Print troubleshooting guide"""
        print("\nTroubleshooting:")
        print("1. Make sure Unreal Editor is running")
        print("2. Ensure the project is loaded")
        print("3. Check that PythonScriptPlugin is enabled")
        print("4. Verify init_unreal.py is running (check Output Log)")
        if self._upyrc_available:
            print("5. Confirm RemoteExecution listener is active")
            print(f"   (should see 'Remote Execution (upyre) started' in logs)")
    
    def test_connection(self, method: str = 'auto') -> bool:
        """
        Test connection to Unreal Engine
        
        Args:
            method: 'upyrc', 'file', or 'auto'
        
        Returns:
            True if connection successful
        """
        test_code = "import unreal; unreal.log('Connection test successful!')"
        print(f"\nTesting connection ({method} method)...")
        return self.execute(test_code, method=method, raise_on_error=False)
    
    def __repr__(self):
        """String representation"""
        return f"""UnrealRemoteClient(
    Project: {self.config.PROJECT_NAME}
    upyrc available: {self._upyrc_available}
    Multicast: {self.config.MULTICAST_GROUP}
    Command file: {self.config.COMMAND_FILE}
)"""
