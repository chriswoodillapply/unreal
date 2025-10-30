"""
Iterator task: Apply materials from generated data
"""

from typing import Dict, Any
from unreallib.workflow.task import Task, TaskResult, TaskStatus


class ForEachMaterialTask(Task):
    """
    Iterate over material mappings and apply materials
    
    This is a meta-task that takes material mapping data from context
    or params and applies materials to actors.
    """
    
    def __init__(
        self,
        name: str,
        material_map: Dict[str, str] = None,
        data_key: str = "material_map"
    ):
        """
        Initialize for-each material task
        
        Args:
            name: Task name
            material_map: Dict mapping actor_id to material_path
            data_key: Key in context containing material mapping
        """
        super().__init__(
            name,
            material_map=material_map or {},
            data_key=data_key
        )
        
        self.material_map = material_map or {}
        self.data_key = data_key
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Apply materials for each actor"""
        from unreallib import materials
        from unreallib.utils import ActorRegistry
        
        # Get material map from params or context
        material_map = self.material_map
        if not material_map:
            material_map = context.get(self.data_key, {})
        
        if not material_map:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': f'No material mapping found'}
            )
        
        # Get config for registry
        config = context.get('workflow_config')
        prefix = config.actor_id_prefix if config else "workflow_"
        registry = ActorRegistry(prefix=prefix)
        
        # Apply materials
        modified_count = 0
        matching_actors = []
        errors = []
        
        for actor_id, material_path in material_map.items():
            # Get actor from registry
            actor = registry.get(actor_id)
            
            if not actor:
                errors.append(f"Actor '{actor_id}' not found in registry")
                continue
            
            # Apply material
            try:
                success = materials.set_actor_material(actor, material_path)
                if success:
                    modified_count += 1
                    matching_actors.append(f"{prefix}{actor_id}")
                    print(f"  Applied material {material_path} to {prefix}{actor_id}")
                else:
                    errors.append(f"Failed to apply material to '{actor_id}'")
            except Exception as e:
                errors.append(f"Error applying material to '{actor_id}': {str(e)}")
        
        if modified_count > 0:
            status = TaskStatus.SUCCESS
        elif errors:
            status = TaskStatus.FAILURE
        else:
            status = TaskStatus.SUCCESS
        
        return TaskResult(
            status=status,
            output={
                'modified_count': modified_count,
                'material_map_size': len(material_map),
                'matching_actors': matching_actors,
                'errors': errors
            }
        )
