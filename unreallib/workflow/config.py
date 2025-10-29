"""
Workflow configuration and settings
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class WorkflowConfig:
    """
    Global configuration for workflow execution
    
    Attributes:
        clear_before_execute: If True, clear all actors before running workflow
        upsert_mode: If True, update existing actors instead of always creating new ones
        actor_id_prefix: Prefix for actor labels/IDs (for tracking)
        save_level_after: If True, save level after workflow completes
        metadata: Additional custom configuration
    """
    
    clear_before_execute: bool = False
    upsert_mode: bool = False
    actor_id_prefix: str = "workflow_"
    save_level_after: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            'clear_before_execute': self.clear_before_execute,
            'upsert_mode': self.upsert_mode,
            'actor_id_prefix': self.actor_id_prefix,
            'save_level_after': self.save_level_after,
            'metadata': self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowConfig':
        """Create config from dictionary"""
        return cls(
            clear_before_execute=data.get('clear_before_execute', False),
            upsert_mode=data.get('upsert_mode', False),
            actor_id_prefix=data.get('actor_id_prefix', 'workflow_'),
            save_level_after=data.get('save_level_after', False),
            metadata=data.get('metadata', {}),
        )
    
    def __repr__(self) -> str:
        return (
            f"WorkflowConfig("
            f"clear={self.clear_before_execute}, "
            f"upsert={self.upsert_mode}, "
            f"save={self.save_level_after})"
        )


# Preset configurations
PRESET_CONFIGS = {
    'default': WorkflowConfig(),
    
    'clean_slate': WorkflowConfig(
        clear_before_execute=True,
        upsert_mode=False,
    ),
    
    'incremental': WorkflowConfig(
        clear_before_execute=False,
        upsert_mode=True,
    ),
    
    'production': WorkflowConfig(
        clear_before_execute=True,
        upsert_mode=False,
        save_level_after=True,
    ),
}


def get_preset_config(name: str) -> WorkflowConfig:
    """
    Get a preset configuration
    
    Args:
        name: Preset name ('default', 'clean_slate', 'incremental', 'production')
        
    Returns:
        WorkflowConfig instance
    """
    if name not in PRESET_CONFIGS:
        raise ValueError(
            f"Unknown preset '{name}'. "
            f"Available: {', '.join(PRESET_CONFIGS.keys())}"
        )
    return PRESET_CONFIGS[name]
