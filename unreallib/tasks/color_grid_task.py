"""
Color Grid Task - Applies colors to actors in a grid pattern
"""

from typing import Optional
from unreallib.workflow.task import Task, TaskResult


class ColorGridTask(Task):
    """Task to apply colors to actors in a grid pattern"""
    
    def __init__(
        self,
        name: str,
        prefix: str = "workflow_",
        color_map: Optional[dict] = None
    ):
        """
        Initialize color grid task
        
        Args:
            name: Task identifier
            prefix: Prefix for actor labels to target
            color_map: Dictionary mapping actor IDs to colors
        """
        super().__init__(name)
        self.prefix = prefix
        self.color_map = color_map or {}
    
    def execute(self, context: dict) -> TaskResult:
        """Apply colors based on color map"""
        import unreal
        from unreallib import materials
        
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        all_actors = editor_actor_subsystem.get_all_level_actors()
        
        modified_count = 0
        for actor in all_actors:
            label = actor.get_actor_label()
            if label.startswith(self.prefix):
                # Check if we have a color for this actor
                for actor_id, color_data in self.color_map.items():
                    full_id = f"{self.prefix}{actor_id}"
                    if label == full_id:
                        color = color_data.get('color', (1.0, 1.0, 1.0))
                        opacity = color_data.get('opacity', 1.0)
                        materials.set_actor_color(actor, color, opacity)
                        modified_count += 1
                        break
        
        return TaskResult(
            output={
                'modified_count': modified_count,
                'color_map_size': len(self.color_map)
            },
            metadata={'task_type': 'color_grid'}
        )
