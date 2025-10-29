"""
Example: Spawn various actor patterns

Self-contained script that spawns cubes, spheres, and cylinders
in different geometric patterns.
"""

import unreal
import math

# Get editor actor subsystem
editor_actor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# Load meshes
cube_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
sphere_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Sphere")
cylinder_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cylinder")

def spawn_mesh(mesh, location, scale=1.0):
    """Helper to spawn a mesh at location"""
    actor = editor_actor.spawn_actor_from_object(
        mesh,
        unreal.Vector(*location),
        unreal.Rotator(0, 0, 0)
    )
    if scale != 1.0:
        actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    return actor

unreal.log("Spawning multiple patterns...")

# 1. Grid of cubes (center)
unreal.log("Pattern 1: Grid of cubes")
for row in range(3):
    for col in range(3):
        x = col * 300 - 300
        y = row * 300 - 300
        spawn_mesh(cube_mesh, (x, y, 0))

# 2. Circle of spheres
unreal.log("Pattern 2: Circle of spheres")
radius = 800
for i in range(12):
    angle = (2 * math.pi * i) / 12
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    spawn_mesh(sphere_mesh, (x, y, 100))

# 3. Spiral of cylinders
unreal.log("Pattern 3: Spiral of cylinders")
for i in range(15):
    t = i / 14
    angle = 4 * math.pi * t
    r = 600 * t
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    z = i * 30
    spawn_mesh(cylinder_mesh, (x, y, z), scale=0.5)

# Count total actors
all_actors = editor_actor.get_all_level_actors()
unreal.log(f"✓ Complete! Total actors in level: {len(all_actors)}")
