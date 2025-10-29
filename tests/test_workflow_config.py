"""
Unit tests for workflow configuration
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unreallib.workflow import WorkflowConfig, get_preset_config


class TestWorkflowConfig:
    """Tests for WorkflowConfig class"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = WorkflowConfig()
        
        assert config.clear_before_execute is False
        assert config.upsert_mode is False
        assert config.actor_id_prefix == "workflow_"
        assert config.save_level_after is False
        assert config.metadata == {}
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = WorkflowConfig(
            clear_before_execute=True,
            upsert_mode=True,
            actor_id_prefix="test_",
            save_level_after=True,
            metadata={'version': '1.0'}
        )
        
        assert config.clear_before_execute is True
        assert config.upsert_mode is True
        assert config.actor_id_prefix == "test_"
        assert config.save_level_after is True
        assert config.metadata == {'version': '1.0'}
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        config = WorkflowConfig(
            clear_before_execute=True,
            save_level_after=True
        )
        
        data = config.to_dict()
        
        assert isinstance(data, dict)
        assert data['clear_before_execute'] is True
        assert data['save_level_after'] is True
        assert data['upsert_mode'] is False
        assert 'actor_id_prefix' in data
        assert 'metadata' in data
    
    def test_from_dict(self):
        """Test creation from dictionary"""
        data = {
            'clear_before_execute': True,
            'upsert_mode': False,
            'actor_id_prefix': 'custom_',
            'save_level_after': True,
            'metadata': {'author': 'test'}
        }
        
        config = WorkflowConfig.from_dict(data)
        
        assert config.clear_before_execute is True
        assert config.upsert_mode is False
        assert config.actor_id_prefix == 'custom_'
        assert config.save_level_after is True
        assert config.metadata == {'author': 'test'}
    
    def test_from_dict_partial(self):
        """Test creation from partial dictionary uses defaults"""
        data = {'clear_before_execute': True}
        
        config = WorkflowConfig.from_dict(data)
        
        assert config.clear_before_execute is True
        assert config.upsert_mode is False  # default
        assert config.actor_id_prefix == 'workflow_'  # default
    
    def test_repr(self):
        """Test string representation"""
        config = WorkflowConfig(clear_before_execute=True)
        
        repr_str = repr(config)
        
        assert 'WorkflowConfig' in repr_str
        assert 'clear=True' in repr_str


class TestPresetConfigs:
    """Tests for preset configurations"""
    
    def test_default_preset(self):
        """Test default preset"""
        config = get_preset_config('default')
        
        assert config.clear_before_execute is False
        assert config.upsert_mode is False
        assert config.save_level_after is False
    
    def test_clean_slate_preset(self):
        """Test clean_slate preset"""
        config = get_preset_config('clean_slate')
        
        assert config.clear_before_execute is True
        assert config.upsert_mode is False
    
    def test_incremental_preset(self):
        """Test incremental preset"""
        config = get_preset_config('incremental')
        
        assert config.clear_before_execute is False
        assert config.upsert_mode is True
    
    def test_production_preset(self):
        """Test production preset"""
        config = get_preset_config('production')
        
        assert config.clear_before_execute is True
        assert config.upsert_mode is False
        assert config.save_level_after is True
    
    def test_invalid_preset_raises(self):
        """Test that invalid preset name raises ValueError"""
        with pytest.raises(ValueError, match="Unknown preset"):
            get_preset_config('nonexistent')
