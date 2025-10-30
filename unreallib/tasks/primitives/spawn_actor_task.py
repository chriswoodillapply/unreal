"""
Primitive task: Spawn a single actor
"""

from typing import Dict, Any
from unreallib.workflow.task import Task, TaskResult, TaskStatus
import unreal


class SpawnActorTask(Task):
    """
    Spawn a single actor at a specific location
    
    Primitive operation that creates one actor. Can be used standalone
    or iterated by generator tasks.
    """
    
    def __init__(
        self,
        name: str,
        shape: str = "sphere",
        location: tuple = (0, 0, 0),
        rotation: tuple = (0, 0, 0),
        scale: float = 1.0,
        actor_id: str = None,
        use_registry: bool = True
    ):
        """
        Initialize spawn actor task
        
        Args:
            name: Task name
            shape: Actor shape (sphere, cube, cylinder)
            location: (x, y, z) location
            rotation: (pitch, yaw, roll) rotation in degrees
            scale: Uniform scale factor
            actor_id: Optional ID for actor registry (enables upsert)
            use_registry: Whether to register actor for upsert operations
        """
        super().__init__(
            name,
            shape=shape,
            location=location,
            rotation=rotation,
            scale=scale,
            actor_id=actor_id,
            use_registry=use_registry
        )
        
        self.shape = shape
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.actor_id = actor_id
        self.use_registry = use_registry
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Spawn a single actor"""
        from unreallib import actors
        from unreallib.utils import ActorRegistry
        
        # Get spawn function for shape
        spawn_funcs = {
            'cube': actors.spawn_cube,
            'sphere': actors.spawn_sphere,
            'cylinder': actors.spawn_cylinder
        }
        
        if self.shape not in spawn_funcs:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': f"Unknown shape: {self.shape}"}
            )
        
        spawn_func = spawn_funcs[self.shape]
        
        # Check if we should use upsert mode
        config = context.get('workflow_config')
        use_upsert = self.use_registry and config and config.upsert_mode
        
        if use_upsert and self.actor_id:
            # Use actor registry for upsert
            prefix = config.actor_id_prefix if config else "workflow_"
            registry = ActorRegistry(prefix=prefix)
            
            def create_actor():
                return spawn_func(self.location, self.scale)
            
            def update_actor(actor):
                actor.set_actor_location(
                    unreal.Vector(*self.location),
                    False,
                    False
                )
                actor.set_actor_scale3d(unreal.Vector(self.scale, self.scale, self.scale))
            
            actor, was_created = registry.update_or_create(
                self.actor_id,
                create_actor,
                update_actor
            )
            
            action = "created" if was_created else "updated"
        else:
            # Simple spawn without registry
            actor = spawn_func(self.location, self.scale)
            action = "created"
        
        # Apply rotation if specified
        if self.rotation != (0, 0, 0):
            pitch, yaw, roll = self.rotation
            actor.set_actor_rotation(
                unreal.Rotator(pitch, yaw, roll),
                False
            )
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={
                'actor': actor,
                'action': action,
                'location': self.location,
                'shape': self.shape
            }
        )
