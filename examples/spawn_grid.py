"""
Test using unreallib.actors directly (no workflow)
"""

print("Testing unreallib.actors module...")

from unreallib import actors

print("Module imported successfully!")

# Spawn a 3x3 grid
print("\nSpawning 3x3 grid of spheres...")
grid_actors = actors.spawn_grid(
    rows=3,
    cols=3,
    spacing=200.0,
    shape='sphere',
    scale=1.0
)

print(f"\nCreated {len(grid_actors)} spheres!")
print("Check your level - you should see a 3x3 grid of spheres")
