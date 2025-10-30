"""
Primitive task: Create a camera actor
"""

from typing import Dict, Any
from unreallib.workflow.task import Task, TaskResult, TaskStatus
import unreal


class CreateCameraTask(Task):
    """
    Create a single camera actor
    
    Primitive operation that creates one camera at a specific location.
    """
    
    def __init__(
        self,
        name: str,
        location: tuple = (0, 0, 200),
        rotation: tuple = (0, 0, 0),
        fov: float = 90.0,
        actor_id: str = None,
        use_registry: bool = True
    ):
        """
        Initialize create camera task
        
        Args:
            name: Task name
            location: (x, y, z) location
            rotation: (pitch, yaw, roll) rotation in degrees
            fov: Field of view in degrees
            actor_id: Optional ID for actor registry (enables upsert)
            use_registry: Whether to register camera for upsert operations
        """
        super().__init__(
            name,
            location=location,
            rotation=rotation,
            fov=fov,
            actor_id=actor_id,
            use_registry=use_registry
        )
        
        self.location = location
        self.rotation = rotation
        self.fov = fov
        self.actor_id = actor_id
        self.use_registry = use_registry
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Create a camera actor"""
        from unreallib.utils import ActorRegistry
        
        # Check if we should use upsert mode
        config = context.get('workflow_config')
        use_upsert = self.use_registry and config and config.upsert_mode
        
        if use_upsert and self.actor_id:
            # Use actor registry for upsert
            prefix = config.actor_id_prefix if config else "workflow_"
            registry = ActorRegistry(prefix=prefix)
            
            def create_camera():
                camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
                    unreal.CameraActor.static_class(),
                    unreal.Vector(*self.location),
                    unreal.Rotator(*self.rotation)
                )
                # Set FOV
                camera_component = camera.get_editor_property('camera_component')
                if camera_component:
                    camera_component.set_editor_property('field_of_view', self.fov)
                return camera
            
            def update_camera(camera):
                camera.set_actor_location(
                    unreal.Vector(*self.location),
                    False,
                    False
                )
                camera.set_actor_rotation(
                    unreal.Rotator(*self.rotation),
                    False
                )
                camera_component = camera.get_editor_property('camera_component')
                if camera_component:
                    camera_component.set_editor_property('field_of_view', self.fov)
            
            camera, was_created = registry.update_or_create(
                self.actor_id,
                create_camera,
                update_camera
            )
            
            action = "created" if was_created else "updated"
        else:
            # Simple spawn without registry
            camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.CameraActor.static_class(),
                unreal.Vector(*self.location),
                unreal.Rotator(*self.rotation)
            )
            camera_component = camera.get_editor_property('camera_component')
            if camera_component:
                camera_component.set_editor_property('field_of_view', self.fov)
            action = "created"
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={
                'camera': camera,
                'action': action,
                'location': self.location,
                'fov': self.fov
            }
        )
