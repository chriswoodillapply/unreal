"""
Configuration management for Unreal Remote Control

Loads settings from .env file and provides unified configuration.
"""

import os
from pathlib import Path
from typing import Optional, Tuple
from dotenv import load_dotenv


class RemoteControlConfig:
    """Configuration for Unreal Engine remote control"""
    
    def __init__(self, env_file: Optional[Path] = None):
        """
        Initialize configuration from .env file
        
        Args:
            env_file: Path to .env file. If None, searches parent directories
        """
        # Find .env file
        if env_file is None:
            env_file = self._find_env_file()
        
        if env_file and env_file.exists():
            load_dotenv(env_file)
            self.env_file = env_file
        else:
            self.env_file = None
        
        # Load all configuration
        self._load_project_config()
        self._load_remote_config()
        self._load_scene_config()
    
    def _find_env_file(self) -> Optional[Path]:
        """Find .env file in current or parent directories"""
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            env_path = parent / '.env'
            if env_path.exists():
                return env_path
        return None
    
    def _load_project_config(self):
        """Load Unreal project configuration"""
        # Project paths (authoritative from .env, with simple defaults)
        self.PROJECT_NAME = os.getenv('PROJECT', 'firstperson')
        self.PROJECT_FOLDER = Path(os.getenv(
            'PROJECT_FOLDER',
            f'C:/Users/cwood/Documents/Unreal Projects/{self.PROJECT_NAME}'
        ))
        # If PROJECT_FILE explicitly set, use it; else derive
        env_project_file = os.getenv('PROJECT_FILE')
        if env_project_file:
            self.PROJECT_FILE = Path(env_project_file)
        else:
            self.PROJECT_FILE = self.PROJECT_FOLDER / f"{self.PROJECT_NAME}.uproject"
        
        # Scripts and content paths
        self.SCRIPTS_FOLDER = self.PROJECT_FOLDER / 'scripts'
        self.CONTENT_FOLDER = self.PROJECT_FOLDER / 'Content'
        self.PYTHON_FOLDER = self.CONTENT_FOLDER / 'Python'
        
        # Command file for file-based remote control
        self.COMMAND_FILE = self.SCRIPTS_FOLDER / '.unreal_command.py'
        
        # Unreal Engine executable
        self.UNREAL_ENGINE_PATH = Path(os.getenv(
            'UNREAL_ENGINE_PATH',
            'C:/Program Files/Epic Games/UE_5.6/Engine/Binaries/Win64/UnrealEditor-Cmd.exe'
        ))
        
        # Level configuration
        self.LEVEL = os.getenv('LEVEL', 'Main')
        self.LEVEL_PATH = os.getenv('LEVEL_PATH', f'/Game/{self.LEVEL}')
        self.AUTO_LOAD_LEVEL = os.getenv('AUTO_LOAD_LEVEL', 'true').lower() == 'true'
    
    def _load_remote_config(self):
        """Load remote execution configuration"""
        # upyrc (UDP multicast) settings
        self.MULTICAST_HOST = os.getenv('UNREAL_REMOTE_HOST', '239.0.0.1')
        self.MULTICAST_PORT = int(os.getenv('UNREAL_REMOTE_PORT', '6766'))
        self.MULTICAST_GROUP = (self.MULTICAST_HOST, self.MULTICAST_PORT)
        self.MULTICAST_BIND_ADDRESS = os.getenv('UNREAL_BIND_ADDRESS', '0.0.0.0')
        
        # Command endpoint (derived from multicast config)
        self.COMMAND_HOST = os.getenv('UNREAL_COMMAND_HOST', '127.0.0.1')
        self.COMMAND_PORT = int(os.getenv('UNREAL_COMMAND_PORT', '6776'))
        self.COMMAND_ENDPOINT = (self.COMMAND_HOST, self.COMMAND_PORT)
        
        # WebRemoteControl HTTP settings
        self.WEB_REMOTE_ENABLED = os.getenv('WEB_REMOTE_ENABLED', 'true').lower() == 'true'
        self.WEB_REMOTE_PORT = int(os.getenv('WEB_REMOTE_PORT', '30010'))
        self.WEB_REMOTE_HOST = os.getenv('WEB_REMOTE_HOST', 'localhost')
        self.WEB_REMOTE_URL = f"http://{self.WEB_REMOTE_HOST}:{self.WEB_REMOTE_PORT}"
    
    def _load_scene_config(self):
        """Load scene population configuration"""
        # Grid layout
        self.GRID_ROWS = int(os.getenv('GRID_ROWS', '5'))
        self.GRID_COLS = int(os.getenv('GRID_COLS', '5'))
        self.GRID_SPACING = float(os.getenv('GRID_SPACING', '200'))
        
        # Circle layout
        self.CIRCLE_OBJECTS = int(os.getenv('CIRCLE_OBJECTS', '12'))
        self.CIRCLE_RADIUS = float(os.getenv('CIRCLE_RADIUS', '500'))
        
        # Spiral layout
        self.SPIRAL_OBJECTS = int(os.getenv('SPIRAL_OBJECTS', '20'))
        self.SPIRAL_MAX_RADIUS = float(os.getenv('SPIRAL_MAX_RADIUS', '800'))
        self.SPIRAL_HEIGHT_INCREMENT = float(os.getenv('SPIRAL_HEIGHT_INCREMENT', '50'))
        
        # Scatter layout
        self.SCATTER_OBJECTS = int(os.getenv('SCATTER_OBJECTS', '30'))
        self.SCATTER_AREA_SIZE = float(os.getenv('SCATTER_AREA_SIZE', '1000'))
        
        # Logging
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.VERBOSE_LOGGING = os.getenv('ENABLE_VERBOSE_LOGGING', 'false').lower() == 'true'
    
    def get_upyrc_config(self):
        """Get configuration dict for upyrc library"""
        try:
            from upyrc import upyre
            return upyre.RemoteExecutionConfig(
                multicast_group=self.MULTICAST_GROUP,
                multicast_bind_address=self.MULTICAST_BIND_ADDRESS
            )
        except ImportError:
            raise ImportError(
                "upyrc not installed. Run: pip install upyrc\n"
                "Or: pip install -r requirements.txt"
            )
    
    def __repr__(self):
        """String representation"""
        return f"""RemoteControlConfig(
    Project: {self.PROJECT_NAME}
    Folder: {self.PROJECT_FOLDER}
    Multicast: {self.MULTICAST_GROUP}
    Command: {self.COMMAND_ENDPOINT}
    Web Remote: {self.WEB_REMOTE_URL}
)"""
