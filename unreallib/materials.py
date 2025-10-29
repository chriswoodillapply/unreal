"""
Material utilities for Unreal Engine

Functions for applying and manipulating materials on actors.
"""

import unreal
from typing import Tuple, Optional


def set_actor_color(actor: unreal.Actor, color: Tuple[float, float, float], opacity: float = 1.0):
    """
    Set the color of a static mesh actor by creating a dynamic material instance
    
    Args:
        actor: The actor to modify
        color: RGB color tuple (values 0-1)
        opacity: Opacity value (0-1)
    
    Example:
        >>> from unreallib.materials import set_actor_color
        >>> set_actor_color(actor, (1.0, 0.0, 0.0))  # Red
        >>> set_actor_color(actor, (0.0, 1.0, 0.0), 0.5)  # Semi-transparent green
    """
    # Get the static mesh component
    static_mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
    
    if not static_mesh_component:
        unreal.log_warning(f"Actor {actor.get_actor_label()} has no StaticMeshComponent")
        return
    
    # Load base material
    base_material = unreal.EditorAssetLibrary.load_asset(
        "/Engine/BasicShapes/BasicShapeMaterial"
    )
    
    # Create dynamic material instance
    dynamic_material = unreal.MaterialInstanceDynamic.create(
        base_material,
        static_mesh_component
    )
    
    # Set color parameter
    linear_color = unreal.LinearColor(color[0], color[1], color[2], opacity)
    dynamic_material.set_vector_parameter_value("Color", linear_color)
    
    # Apply material to component
    static_mesh_component.set_material(0, dynamic_material)
    
    unreal.log(f"Set color of {actor.get_actor_label()} to RGB{color}")


def set_actor_material(actor: unreal.Actor, material_path: str, material_index: int = 0):
    """
    Apply a material to an actor
    
    Args:
        actor: The actor to modify
        material_path: Path to the material asset
        material_index: Which material slot to modify
    """
    static_mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
    
    if not static_mesh_component:
        unreal.log_warning(f"Actor {actor.get_actor_label()} has no StaticMeshComponent")
        return
    
    material = unreal.EditorAssetLibrary.load_asset(material_path)
    
    if material:
        static_mesh_component.set_material(material_index, material)
        unreal.log(f"Applied material {material_path} to {actor.get_actor_label()}")
    else:
        unreal.log_error(f"Could not load material: {material_path}")


# Preset colors
COLORS = {
    'red': (1.0, 0.0, 0.0),
    'green': (0.0, 1.0, 0.0),
    'blue': (0.0, 0.0, 1.0),
    'yellow': (1.0, 1.0, 0.0),
    'cyan': (0.0, 1.0, 1.0),
    'magenta': (1.0, 0.0, 1.0),
    'white': (1.0, 1.0, 1.0),
    'black': (0.0, 0.0, 0.0),
    'orange': (1.0, 0.5, 0.0),
    'purple': (0.5, 0.0, 1.0),
    'pink': (1.0, 0.4, 0.7),
    'lime': (0.5, 1.0, 0.0),
}


def get_color(color_name: str) -> Optional[Tuple[float, float, float]]:
    """
    Get RGB color tuple by name
    
    Args:
        color_name: Name of the color (e.g., 'red', 'blue')
    
    Returns:
        RGB tuple or None if not found
    """
    return COLORS.get(color_name.lower())
