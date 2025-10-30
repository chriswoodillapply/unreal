"""
Primitive task: Apply a material to a single actor
"""

from typing import Dict, Any
from unreallib.workflow.task import Task, TaskResult, TaskStatus


class ApplyMaterialTask(Task):
    """
    Apply a material to a single actor
    
    Primitive operation that sets material on one actor. Can be used standalone
    or iterated by generator tasks.
    """
    
    def __init__(
        self,
        name: str,
        actor_id: str = None,
        material_path: str = None,
        material_slot: int = 0
    ):
        """
        Initialize apply material task
        
        Args:
            name: Task name
            actor_id: Actor ID to find in registry (if using upsert mode)
            material_path: Full path to material asset
            material_slot: Material slot index (default 0)
        """
        super().__init__(
            name,
            actor_id=actor_id,
            material_path=material_path,
            material_slot=material_slot
        )
        
        self.actor_id = actor_id
        self.material_path = material_path
        self.material_slot = material_slot
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Apply material to actor"""
        from unreallib import materials
        from unreallib.utils import ActorRegistry
        
        # Get actor - either from context or from registry
        actor = context.get('actor')
        
        if not actor and self.actor_id:
            # Look up actor by ID in registry
            config = context.get('workflow_config')
            prefix = config.actor_id_prefix if config else "workflow_"
            registry = ActorRegistry(prefix=prefix)
            actor = registry.get(self.actor_id)
        
        if not actor:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': 'No actor specified or found'}
            )
        
        if not self.material_path:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': 'No material_path specified'}
            )
        
        # Apply the material
        success = materials.set_actor_material(
            actor,
            self.material_path,
            self.material_slot
        )
        
        if success:
            return TaskResult(
                status=TaskStatus.SUCCESS,
                output={
                    'actor_label': actor.get_actor_label(),
                    'material_path': self.material_path,
                    'material_slot': self.material_slot
                }
            )
        else:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': f'Failed to apply material: {self.material_path}'}
            )
