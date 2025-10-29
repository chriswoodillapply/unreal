"""
Tests for UnrealRemoteClient
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from remotecontrol.client import UnrealRemoteClient
from remotecontrol.config import RemoteControlConfig


def test_client_creation():
    """Test creating remote client"""
    client = UnrealRemoteClient()
    
    assert client.config is not None
    assert isinstance(client.config, RemoteControlConfig)


def test_client_with_custom_config():
    """Test creating client with custom config"""
    config = RemoteControlConfig()
    client = UnrealRemoteClient(config)
    
    assert client.config is config


def test_upyrc_availability():
    """Test upyrc availability detection"""
    client = UnrealRemoteClient()
    
    # Should be boolean
    assert isinstance(client._upyrc_available, bool)


def test_invalid_method_raises():
    """Test that invalid method raises error"""
    client = UnrealRemoteClient()
    
    with pytest.raises(ValueError):
        client.execute("test code", method='invalid_method')


def test_client_repr():
    """Test client string representation"""
    client = UnrealRemoteClient()
    repr_str = repr(client)
    
    assert "UnrealRemoteClient" in repr_str
    assert "Project:" in repr_str
