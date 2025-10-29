"""
Actor utilities for Unreal Engine

Functions for spawning, manipulating, and organizing actors in levels.
"""

import math
from typing import Optional, Tuple, List


def spawn_cube(location: Tuple[float, float, float] = (0, 0, 0), scale: float = 1.0):
    """
    Spawn a cube actor at specified location
    
    Args:
        location: (x, y, z) tuple for actor location
        scale: Uniform scale for the actor
    
    Returns:
        The spawned actor
    
    Example:
        >>> from unreallib.actors import spawn_cube
        >>> cube = spawn_cube((100, 200, 50), scale=2.0)
    """
    import unreal
    
    # Get editor actor subsystem
    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    # Load cube mesh
    cube_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    
    # Spawn static mesh actor
    actor_location = unreal.Vector(*location)
    actor_rotation = unreal.Rotator(0, 0, 0)
    
    actor = editor_actor_subsystem.spawn_actor_from_object(
        cube_mesh,
        actor_location,
        actor_rotation
    )
    
    # Set scale
    if scale != 1.0:
        actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    
    unreal.log(f"Spawned cube at {location} with scale {scale}")
    return actor


def spawn_sphere(location: Tuple[float, float, float] = (0, 0, 0), scale: float = 1.0):
    """
    Spawn a sphere actor at specified location
    
    Args:
        location: (x, y, z) tuple for actor location
        scale: Uniform scale for the actor
    
    Returns:
        The spawned actor
    """
    import unreal
    
    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    sphere_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Sphere")
    
    actor_location = unreal.Vector(*location)
    actor_rotation = unreal.Rotator(0, 0, 0)
    
    actor = editor_actor_subsystem.spawn_actor_from_object(
        sphere_mesh,
        actor_location,
        actor_rotation
    )
    
    if scale != 1.0:
        actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    
    unreal.log(f"Spawned sphere at {location} with scale {scale}")
    return actor


def spawn_cylinder(location: Tuple[float, float, float] = (0, 0, 0), scale: float = 1.0):
    """
    Spawn a cylinder actor at specified location
    
    Args:
        location: (x, y, z) tuple for actor location
        scale: Uniform scale for the actor
    
    Returns:
        The spawned actor
    """
    import unreal
    
    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    cylinder_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cylinder")
    
    actor_location = unreal.Vector(*location)
    actor_rotation = unreal.Rotator(0, 0, 0)
    
    actor = editor_actor_subsystem.spawn_actor_from_object(
        cylinder_mesh,
        actor_location,
        actor_rotation
    )
    
    if scale != 1.0:
        actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    
    unreal.log(f"Spawned cylinder at {location} with scale {scale}")
    return actor


def spawn_grid(
    rows: int = 5,
    cols: int = 5,
    spacing: float = 200.0,
    shape: str = 'cube',
    scale: float = 1.0
) -> List:
    """
    Spawn a grid of actors
    
    Args:
        rows: Number of rows
        cols: Number of columns
        spacing: Distance between actors
        shape: 'cube', 'sphere', or 'cylinder'
        scale: Uniform scale for actors
    
    Returns:
        List of spawned actors
    """
    import unreal
    
    spawn_funcs = {
        'cube': spawn_cube,
        'sphere': spawn_sphere,
        'cylinder': spawn_cylinder
    }
    
    spawn_func = spawn_funcs.get(shape, spawn_cube)
    actors = []
    
    unreal.log(f"Spawning {rows}x{cols} grid of {shape}s...")
    
    for row in range(rows):
        for col in range(cols):
            x = col * spacing - (cols - 1) * spacing / 2
            y = row * spacing - (rows - 1) * spacing / 2
            z = 0
            
            actor = spawn_func((x, y, z), scale)
            actors.append(actor)
    
    unreal.log(f"✓ Spawned {len(actors)} {shape}s in grid")
    return actors


def spawn_circle(
    count: int = 12,
    radius: float = 500.0,
    shape: str = 'cube',
    scale: float = 1.0,
    height: float = 0.0
) -> List:
    """
    Spawn actors in a circle
    
    Args:
        count: Number of actors
        radius: Radius of circle
        shape: 'cube', 'sphere', or 'cylinder'
        scale: Uniform scale for actors
        height: Z position for circle
    
    Returns:
        List of spawned actors
    """
    import unreal
    
    spawn_funcs = {
        'cube': spawn_cube,
        'sphere': spawn_sphere,
        'cylinder': spawn_cylinder
    }
    
    spawn_func = spawn_funcs.get(shape, spawn_cube)
    actors = []
    
    unreal.log(f"Spawning {count} {shape}s in circle (radius={radius})...")
    
    for i in range(count):
        angle = (2 * math.pi * i) / count
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = height
        
        actor = spawn_func((x, y, z), scale)
        actors.append(actor)
    
    unreal.log(f"✓ Spawned {len(actors)} {shape}s in circle")
    return actors


def spawn_spiral(
    count: int = 20,
    max_radius: float = 800.0,
    height_increment: float = 50.0,
    shape: str = 'cube',
    scale: float = 1.0
) -> List:
    """
    Spawn actors in a spiral
    
    Args:
        count: Number of actors
        max_radius: Maximum radius of spiral
        height_increment: Height increase per actor
        shape: 'cube', 'sphere', or 'cylinder'
        scale: Uniform scale for actors
    
    Returns:
        List of spawned actors
    """
    import unreal
    
    spawn_funcs = {
        'cube': spawn_cube,
        'sphere': spawn_sphere,
        'cylinder': spawn_cylinder
    }
    
    spawn_func = spawn_funcs.get(shape, spawn_cube)
    actors = []
    
    unreal.log(f"Spawning {count} {shape}s in spiral...")
    
    for i in range(count):
        t = i / max(count - 1, 1)
        angle = 4 * math.pi * t  # 2 full rotations
        radius = max_radius * t
        
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = i * height_increment
        
        actor = spawn_func((x, y, z), scale)
        actors.append(actor)
    
    unreal.log(f"✓ Spawned {len(actors)} {shape}s in spiral")
    return actors
