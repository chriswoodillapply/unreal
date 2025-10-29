"""
Example: Spawn a simple grid of cubes

This script spawns cubes directly using Unreal's API.
Self-contained - no external dependencies.
"""

import unreal

# Get editor actor subsystem
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# Load cube mesh
cube_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")

# Grid parameters
rows = 5
cols = 5
spacing = 200.0

unreal.log(f"Spawning {rows}x{cols} grid of cubes...")

# Spawn grid
count = 0
for row in range(rows):
    for col in range(cols):
        x = col * spacing - (cols - 1) * spacing / 2
        y = row * spacing - (rows - 1) * spacing / 2
        z = 0
        
        location = unreal.Vector(x, y, z)
        rotation = unreal.Rotator(0, 0, 0)
        
        actor = editor_actor_subsystem.spawn_actor_from_object(
            cube_mesh,
            location,
            rotation
        )
        count += 1

unreal.log(f"✓ Spawned {count} cubes successfully!")
