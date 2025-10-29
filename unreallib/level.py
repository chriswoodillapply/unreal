"""
Level utilities for Unreal Engine

Functions for managing levels, world settings, and global operations.
"""


def get_current_level():
    """
    Get the currently loaded level
    
    Returns:
        The current level
    """
    import unreal
    
    editor_level_lib = unreal.EditorLevelLibrary()
    return editor_level_lib.get_editor_world()


def clear_all_actors():
    """
    Delete all actors in the current level (except essential ones)
    
    Returns:
        Number of actors deleted
    """
    import unreal
    
    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = editor_actor_subsystem.get_all_level_actors()
    
    count = 0
    for actor in all_actors:
        # Skip essential actors
        actor_name = actor.get_name()
        if any(x in actor_name for x in ['PlayerStart', 'LightSource', 'SkyAtmosphere', 'Camera']):
            continue
        
        # Delete actor
        editor_actor_subsystem.destroy_actor(actor)
        count += 1
    
    unreal.log(f"✓ Deleted {count} actors from level")
    return count


def get_actor_count():
    """
    Get total number of actors in current level
    
    Returns:
        Number of actors
    """
    import unreal
    
    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    all_actors = editor_actor_subsystem.get_all_level_actors()
    return len(all_actors)


def save_current_level():
    """
    Save the currently loaded level
    
    Returns:
        True if successful
    """
    import unreal
    
    editor_level_lib = unreal.EditorLevelLibrary()
    success = editor_level_lib.save_current_level()
    
    if success:
        unreal.log("✓ Level saved")
    else:
        unreal.log_error("✗ Failed to save level")
    
    return success


def load_level(level_path: str):
    """
    Load a level by path
    
    Args:
        level_path: Path to level (e.g., '/Game/Maps/MyLevel')
    
    Returns:
        True if successful
    """
    import unreal
    
    editor_level_lib = unreal.EditorLevelLibrary()
    success = editor_level_lib.load_level(level_path)
    
    if success:
        unreal.log(f"✓ Loaded level: {level_path}")
    else:
        unreal.log_error(f"✗ Failed to load level: {level_path}")
    
    return success
