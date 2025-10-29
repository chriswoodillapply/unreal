"""
Tests for RemoteControlConfig
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import os
import tempfile
from remotecontrol.config import RemoteControlConfig


def test_config_creation():
    """Test creating config without .env file"""
    config = RemoteControlConfig()
    
    assert config.PROJECT_NAME is not None
    assert config.MULTICAST_GROUP is not None
    assert isinstance(config.MULTICAST_PORT, int)


def test_config_from_env_file(tmp_path, monkeypatch):
    """Test loading config from .env file"""
    # Clear all existing env vars that config might use
    for key in ['PROJECT', 'PROJECT_FOLDER', 'UNREAL_REMOTE_HOST', 'UNREAL_REMOTE_PORT', 'GRID_ROWS']:
        monkeypatch.delenv(key, raising=False)
    
    # Create temporary .env file
    env_content = """PROJECT=TestProject
PROJECT_FOLDER=C:/Test/TestProject
UNREAL_REMOTE_HOST=192.168.1.1
UNREAL_REMOTE_PORT=7777
GRID_ROWS=10
"""
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    
    # Load config
    config = RemoteControlConfig(env_file)
    
    assert config.PROJECT_NAME == "TestProject"
    assert config.MULTICAST_HOST == "192.168.1.1"
    assert config.MULTICAST_PORT == 7777
    assert config.GRID_ROWS == 10


def test_multicast_config():
    """Test multicast configuration"""
    config = RemoteControlConfig()
    
    assert len(config.MULTICAST_GROUP) == 2
    assert isinstance(config.MULTICAST_GROUP[0], str)
    assert isinstance(config.MULTICAST_GROUP[1], int)


def test_paths_config():
    """Test path configuration"""
    config = RemoteControlConfig()
    
    assert isinstance(config.PROJECT_FOLDER, Path)
    assert isinstance(config.SCRIPTS_FOLDER, Path)
    assert isinstance(config.CONTENT_FOLDER, Path)


def test_scene_config():
    """Test scene configuration"""
    config = RemoteControlConfig()
    
    assert config.GRID_ROWS > 0
    assert config.GRID_COLS > 0
    assert config.CIRCLE_RADIUS > 0


def test_config_repr():
    """Test config string representation"""
    config = RemoteControlConfig()
    repr_str = repr(config)
    
    assert "RemoteControlConfig" in repr_str
    assert "Project:" in repr_str
    assert "Multicast:" in repr_str
