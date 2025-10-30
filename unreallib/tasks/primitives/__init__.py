"""
Primitive tasks - Basic building blocks

These tasks perform single, atomic operations:
- SpawnActorTask: Spawn one actor
- ApplyMaterialTask: Apply material to one actor
- CreateCameraTask: Create one camera
- CreateLightTask: Create one light

Use these as building blocks in workflows, or combine with generators.
"""

from .spawn_actor_task import SpawnActorTask
from .apply_material_task import ApplyMaterialTask
from .create_camera_task import CreateCameraTask
from .create_light_task import CreateLightTask
from .import_model_task import ImportModelTask

__all__ = [
    'SpawnActorTask',
    'ApplyMaterialTask',
    'CreateCameraTask',
    'CreateLightTask',
    'ImportModelTask',
]
