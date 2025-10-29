"""
Examples of spawning basic shapes in Unreal Engine

This demonstrates how to use unreallib to spawn individual actors
with different shapes, positions, and labels.

Usage:
    python -m remotecontrol examples/spawn_shapes.py --method=file
"""

import unreal
from unreallib import actors

print("="*60)
print("SPAWNING BASIC SHAPES EXAMPLE")
print("="*60)

# Clear any existing example shapes
print("\nClearing old example shapes...")
editor_actor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
all_actors = editor_actor.get_all_level_actors()
for actor in all_actors:
    if actor.get_actor_label().startswith("example_"):
        editor_actor.destroy_actor(actor)
        print(f"  Deleted: {actor.get_actor_label()}")

# Example 1: Spawn individual cubes
print("\n1. Spawning three colored cubes...")
cube1 = actors.spawn_cube(location=(0, 0, 50))
cube1.set_actor_label("example_cube_red")
print(f"   Created: {cube1.get_actor_label()} at {cube1.get_actor_location()}")

cube2 = actors.spawn_cube(location=(200, 0, 50))
cube2.set_actor_label("example_cube_green")
print(f"   Created: {cube2.get_actor_label()} at {cube2.get_actor_location()}")

cube3 = actors.spawn_cube(location=(400, 0, 50))
cube3.set_actor_label("example_cube_blue")
print(f"   Created: {cube3.get_actor_label()} at {cube3.get_actor_location()}")

# Example 2: Spawn different shapes
print("\n2. Spawning different shapes...")
sphere = actors.spawn_sphere(location=(0, 200, 50))
sphere.set_actor_label("example_sphere")
print(f"   Created: {sphere.get_actor_label()}")

cylinder = actors.spawn_cylinder(location=(200, 200, 50))
cylinder.set_actor_label("example_cylinder")
print(f"   Created: {cylinder.get_actor_label()}")

# Example 3: Spawn with different scales
print("\n3. Spawning with different scales...")
small = actors.spawn_cube(location=(0, 400, 50), scale=0.5)
small.set_actor_label("example_small_cube")
print(f"   Created: {small.get_actor_label()} (scale 0.5)")

large = actors.spawn_cube(location=(200, 400, 50), scale=2.0)
large.set_actor_label("example_large_cube")
print(f"   Created: {large.get_actor_label()} (scale 2.0)")

print("\n" + "="*60)
print("COMPLETE! Check your level for the spawned shapes.")
print("="*60)
