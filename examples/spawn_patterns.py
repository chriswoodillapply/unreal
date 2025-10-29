"""
Example: Spawn actors in different patterns

Demonstrates various spawning patterns available in unreallib.
"""

from unreallib import actors, level

print("Spawning various actor patterns...")

# Clear level first
level.clear_all_actors()

# Grid of cubes
actors.spawn_grid(rows=3, cols=3, spacing=300, shape='cube')

# Circle of spheres
actors.spawn_circle(count=12, radius=800, shape='sphere', height=100)

# Spiral of cylinders
actors.spawn_spiral(count=15, max_radius=600, height_increment=30, shape='cylinder')

print("✓ All patterns spawned!")
print(f"Total actors in level: {level.get_actor_count()}")
