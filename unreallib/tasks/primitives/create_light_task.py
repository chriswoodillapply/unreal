"""
Primitive task: Create a light actor
"""

from typing import Dict, Any
from unreallib.workflow.task import Task, TaskResult, TaskStatus
import unreal


class CreateLightTask(Task):
    """
    Create a single light actor
    
    Primitive operation that creates one light at a specific location.
    """
    
    def __init__(
        self,
        name: str,
        light_type: str = "point",  # point, spot, directional
        location: tuple = (0, 0, 300),
        rotation: tuple = (-45, 0, 0),
        intensity: float = 5000.0,
        color: tuple = (1.0, 1.0, 1.0),  # RGB 0-1
        actor_id: str = None,
        use_registry: bool = True
    ):
        """
        Initialize create light task
        
        Args:
            name: Task name
            light_type: Type of light (point, spot, directional)
            location: (x, y, z) location
            rotation: (pitch, yaw, roll) rotation in degrees
            intensity: Light intensity
            color: (R, G, B) color values 0-1
            actor_id: Optional ID for actor registry (enables upsert)
            use_registry: Whether to register light for upsert operations
        """
        super().__init__(
            name,
            light_type=light_type,
            location=location,
            rotation=rotation,
            intensity=intensity,
            color=color,
            actor_id=actor_id,
            use_registry=use_registry
        )
        
        self.light_type = light_type
        self.location = location
        self.rotation = rotation
        self.intensity = intensity
        self.color = color
        self.actor_id = actor_id
        self.use_registry = use_registry
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Create a light actor"""
        from unreallib.utils import ActorRegistry
        
        # Map light type to Unreal class
        light_classes = {
            'point': unreal.PointLight.static_class(),
            'spot': unreal.SpotLight.static_class(),
            'directional': unreal.DirectionalLight.static_class()
        }
        
        if self.light_type not in light_classes:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': f"Unknown light type: {self.light_type}"}
            )
        
        light_class = light_classes[self.light_type]
        
        # Check if we should use upsert mode
        config = context.get('workflow_config')
        use_upsert = self.use_registry and config and config.upsert_mode
        
        if use_upsert and self.actor_id:
            # Use actor registry for upsert
            prefix = config.actor_id_prefix if config else "workflow_"
            registry = ActorRegistry(prefix=prefix)
            
            def create_light():
                light = unreal.EditorLevelLibrary.spawn_actor_from_class(
                    light_class,
                    unreal.Vector(*self.location),
                    unreal.Rotator(*self.rotation)
                )
                self._configure_light(light)
                return light
            
            def update_light(light):
                light.set_actor_location(
                    unreal.Vector(*self.location),
                    False,
                    False
                )
                light.set_actor_rotation(
                    unreal.Rotator(*self.rotation),
                    False
                )
                self._configure_light(light)
            
            light, was_created = registry.update_or_create(
                self.actor_id,
                create_light,
                update_light
            )
            
            action = "created" if was_created else "updated"
        else:
            # Simple spawn without registry
            light = unreal.EditorLevelLibrary.spawn_actor_from_class(
                light_class,
                unreal.Vector(*self.location),
                unreal.Rotator(*self.rotation)
            )
            self._configure_light(light)
            action = "created"
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={
                'light': light,
                'action': action,
                'light_type': self.light_type,
                'location': self.location
            }
        )
    
    def _configure_light(self, light):
        """Configure light properties"""
        # Get the light component - different component types for different lights
        light_component = light.get_component_by_class(unreal.LightComponent)
        
        if light_component:
            light_component.set_editor_property('intensity', self.intensity)
            # Set color using the correct property name
            r, g, b = self.color
            color = unreal.LinearColor(r, g, b, 1.0)
            light_component.set_light_color(color)
