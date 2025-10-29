"""
Example: Using unreallib for clean actor spawning

Now that init_unreal.py adds scripts/ to sys.path,
you can import and use unreallib in your scripts!
"""

from unreallib import actors, level

# Clear the level
print("Clearing existing actors...")
level.clear_all_actors()

# Spawn a 5x5 grid of cubes
print("Spawning cube grid...")
actors.spawn_grid(rows=5, cols=5, spacing=200, shape='cube')

# Spawn a circle of spheres
print("Spawning sphere circle...")
actors.spawn_circle(count=12, radius=500, shape='sphere')

# Spawn a spiral of cylinders
print("Spawning cylinder spiral...")
actors.spawn_spiral(count=15, max_radius=400, height_increment=50, shape='cylinder')

# Report results
total = level.get_actor_count()
print(f"\n✓ Complete! Total actors in level: {total}")
