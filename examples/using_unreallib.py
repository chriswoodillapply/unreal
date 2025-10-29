"""
Example: Using unreallib module for spawning

This demonstrates how to use unreallib when the module is available
in Unreal's Python path. For standalone examples, see simple_grid.py.

NOTE: This requires adding the scripts folder to Unreal's Python path.
See README_NEW.md for setup instructions.
"""

# This will work if scripts folder is in Unreal's sys.path
try:
    from unreallib import actors, level
    
    print("Clearing level...")
    level.clear_all_actors()
    
    print("Spawning grid...")
    actors.spawn_grid(rows=5, cols=5, spacing=200, shape='cube')
    
    print(f"✓ Complete! Total actors: {level.get_actor_count()}")
    
except ImportError as e:
    print(f"Error: unreallib not available - {e}")
    print("Use examples/simple_grid.py for standalone execution")
