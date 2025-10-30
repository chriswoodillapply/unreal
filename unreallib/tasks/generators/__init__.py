"""
Generator tasks - Data generation and iteration

These tasks generate data or iterate over data:
- GridGeneratorTask: Generate grid positions
- ForEachSpawnTask: Spawn actors from generated data
- ForEachMaterialTask: Apply materials from mapping data
- LightsGeneratorTask: Generate light configurations from JSON structure
- ForEachLightTask: Create lights from generated configurations

Generators produce data that primitive tasks can consume.
"""

from .grid_generator_task import GridGeneratorTask
from .for_each_spawn_task import ForEachSpawnTask
from .for_each_material_task import ForEachMaterialTask
from .lights_generator_task import LightsGeneratorTask
from .for_each_light_task import ForEachLightTask

__all__ = [
    'GridGeneratorTask',
    'ForEachSpawnTask',
    'ForEachMaterialTask',
    'LightsGeneratorTask',
    'ForEachLightTask',
]
