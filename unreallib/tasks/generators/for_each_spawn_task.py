"""
Iterator task: Spawn actors from generated data
"""

from typing import Dict, Any
from unreallib.workflow.task import Task, TaskResult, TaskStatus


class ForEachSpawnTask(Task):
    """
    Iterate over grid_points (or similar data) and spawn actors
    
    This is a meta-task that takes generated data from context
    and spawns an actor for each data point.
    """
    
    def __init__(
        self,
        name: str,
        data_key: str = "grid_points",
        use_registry: bool = True
    ):
        """
        Initialize for-each spawn task
        
        Args:
            name: Task name
            data_key: Key in context containing list of spawn parameters
            use_registry: Whether to use actor registry for upsert
        """
        super().__init__(
            name,
            data_key=data_key,
            use_registry=use_registry
        )
        
        self.data_key = data_key
        self.use_registry = use_registry
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Spawn actors for each data point"""
        from unreallib import actors
        from unreallib.utils import ActorRegistry
        
        # Get data points from context
        data_points = context.get(self.data_key, [])
        
        if not data_points:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': f'No data found in context["{self.data_key}"]'}
            )
        
        # Get spawn functions
        spawn_funcs = {
            'cube': actors.spawn_cube,
            'sphere': actors.spawn_sphere,
            'cylinder': actors.spawn_cylinder
        }
        
        # Check if we should use upsert mode
        config = context.get('workflow_config')
        use_upsert = self.use_registry and config and config.upsert_mode
        
        spawned_actors = []
        created_count = 0
        updated_count = 0
        
        if use_upsert:
            prefix = config.actor_id_prefix if config else "workflow_"
            registry = ActorRegistry(prefix=prefix)
        
        # Iterate and spawn
        for point in data_points:
            shape = point.get('shape', 'sphere')
            location = point.get('location', (0, 0, 0))
            scale = point.get('scale', 1.0)
            actor_id = point.get('actor_id')
            rotation = point.get('rotation', (0, 0, 0))
            
            if shape not in spawn_funcs:
                print(f"  Warning: Unknown shape '{shape}', skipping")
                continue
            
            spawn_func = spawn_funcs[shape]
            
            if use_upsert and actor_id:
                # Use registry for upsert
                def create_actor():
                    return spawn_func(location, scale)
                
                def update_actor(actor):
                    import unreal
                    actor.set_actor_location(
                        unreal.Vector(*location),
                        False,
                        False
                    )
                    actor.set_actor_scale3d(
                        unreal.Vector(scale, scale, scale)
                    )
                
                actor, was_created = registry.update_or_create(
                    actor_id,
                    create_actor,
                    update_actor
                )
                
                if was_created:
                    created_count += 1
                else:
                    updated_count += 1
            else:
                # Simple spawn
                actor = spawn_func(location, scale)
                created_count += 1
            
            # Apply rotation if specified
            if rotation != (0, 0, 0):
                import unreal
                pitch, yaw, roll = rotation
                actor.set_actor_rotation(
                    unreal.Rotator(pitch, yaw, roll),
                    False
                )
            
            spawned_actors.append(actor)
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={
                'actors': spawned_actors,
                'actor_count': len(spawned_actors),
                'created': created_count,
                'updated': updated_count
            }
        )
