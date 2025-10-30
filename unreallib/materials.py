"""
Material utilities for Unreal Engine

Functions for applying and manipulating materials on actors.
"""

import unreal
from typing import Tuple, Optional


def set_actor_color(actor: unreal.Actor, color: Tuple[float, float, float], opacity: float = 1.0, base_material_path: Optional[str] = None):
    """
    Set the color of a static mesh actor by creating a dynamic material instance
    
    Args:
        actor: The actor to modify
        color: RGB color tuple (values 0-1)
        opacity: Opacity value (0-1)
        base_material_path: Optional path to a material instance with Color parameter
                           Defaults to /Game/Workflow/MI_RuntimeColorBase if available,
                           otherwise BasicShapeMaterial
    
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
    
    # Determine which base material to use
    if base_material_path is None:
        # Try the workflow material first, fall back to basic shape
        runtime_mat = "/Game/Workflow/MI_RuntimeColorBase"
        if unreal.EditorAssetLibrary.does_asset_exist(runtime_mat):
            base_material_path = runtime_mat
        else:
            base_material_path = "/Engine/BasicShapes/BasicShapeMaterial"
    
    # Load base material
    base_material = unreal.EditorAssetLibrary.load_asset(base_material_path)
    
    if not base_material:
        unreal.log_error(f"Failed to load material: {base_material_path}")
        return
    
    # Create dynamic material instance using component method (UE5.6 compatible)
    dynamic_material = static_mesh_component.create_dynamic_material_instance(0, base_material)
    
    if not dynamic_material:
        unreal.log_error(f"Failed to create dynamic material instance from {base_material_path}")
        return
    
    # Set color parameter
    linear_color = unreal.LinearColor(color[0], color[1], color[2], opacity)
    dynamic_material.set_vector_parameter_value("Color", linear_color)
    
    unreal.log(f"Set color of {actor.get_actor_label()} to RGB{color}")


def set_actor_material(actor: unreal.Actor, material_path: str, material_index: int = 0):
    """
    Apply a material to an actor
    
    Args:
        actor: The actor to modify
        material_path: Path to the material asset
        material_index: Which material slot to modify
        
    Returns:
        True if material was applied successfully, False otherwise
    """
    static_mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
    
    if not static_mesh_component:
        unreal.log_warning(f"Actor {actor.get_actor_label()} has no StaticMeshComponent")
        return False
    
    material = unreal.EditorAssetLibrary.load_asset(material_path)
    
    if material:
        static_mesh_component.set_material(material_index, material)
        unreal.log(f"Applied material {material_path} to {actor.get_actor_label()}")
        return True
    else:
        unreal.log_error(f"Could not load material: {material_path}")
        return False


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
