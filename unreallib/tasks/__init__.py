"""
Task implementations for Unreal scene generation

Architecture:
- primitives/: Single-operation tasks (spawn one actor, apply one material, etc.)
- generators/: Data generation and iteration tasks (grids, patterns, for-each)
- Legacy tasks (old combined tasks, will be deprecated)

Provides concrete task classes following the strategy pattern.
Each task is in its own module for better organization.
"""

# New architecture: Primitive tasks
from .primitives import (
    SpawnActorTask,
    ApplyMaterialTask,
    CreateCameraTask,
    CreateLightTask,
    ImportModelTask,
)

# New architecture: Generator tasks
from .generators import (
    GridGeneratorTask,
    ForEachSpawnTask,
    ForEachMaterialTask,
    LightsGeneratorTask,
    ForEachLightTask,
)

# Legacy tasks (old combined tasks)
from .clear_level import ClearLevelTask
from .spawn_grid_task import SpawnGridTask
from .spawn_circle_task import SpawnCircleTask
from .spawn_spiral_task import SpawnSpiralTask
from .set_actor_color_task import SetActorColorTask
from .color_grid_task import ColorGridTask
from .material_upsert_task import MaterialUpsertTask
from .apply_materials_task import ApplyMaterialsTask

__all__ = [
    # Primitive tasks
    'SpawnActorTask',
    'ApplyMaterialTask',
    'CreateCameraTask',
    'CreateLightTask',
    'ImportModelTask',
    # Generator tasks
    'GridGeneratorTask',
    'ForEachSpawnTask',
    'ForEachMaterialTask',
    'LightsGeneratorTask',
    'ForEachLightTask',
    # Legacy tasks
    'ClearLevelTask',
    'SpawnGridTask',
    'SpawnCircleTask',
    'SpawnSpiralTask',
    'SetActorColorTask',
    'ColorGridTask',
    'MaterialUpsertTask',
    'ApplyMaterialsTask',
]
