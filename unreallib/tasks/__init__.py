"""
Task implementations for Unreal scene generation

Provides concrete task classes following the strategy pattern.
"""

from .clear_level import ClearLevelTask
from .spawn_actors import (
    SpawnGridTask,
    SpawnCircleTask,
    SpawnSpiralTask,
)
from .material_tasks import (
    SetActorColorTask,
    ColorGridTask,
)

__all__ = [
    'ClearLevelTask',
    'SpawnGridTask',
    'SpawnCircleTask',
    'SpawnSpiralTask',
    'SetActorColorTask',
    'ColorGridTask',
]
