"""
Task implementations for Unreal scene generation

Provides concrete task classes following the strategy pattern.
Each task is in its own module for better organization.
"""

from .clear_level import ClearLevelTask
from .spawn_grid_task import SpawnGridTask
from .spawn_circle_task import SpawnCircleTask
from .spawn_spiral_task import SpawnSpiralTask
from .set_actor_color_task import SetActorColorTask
from .color_grid_task import ColorGridTask

__all__ = [
    'ClearLevelTask',
    'SpawnGridTask',
    'SpawnCircleTask',
    'SpawnSpiralTask',
    'SetActorColorTask',
    'ColorGridTask',
]
