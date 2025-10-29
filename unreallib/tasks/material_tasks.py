"""
Material-related workflow tasks
"""

from unreallib.workflow.task import Task, TaskResult
from typing import Tuple, Optional, List


class SetActorColorTask(Task):
    """Task to set the color of specific actors"""
    
    def __init__(
        self,
        name: str,
        actor_labels: List[str],
        color: Tuple[float, float, float],
        opacity: float = 1.0
    ):
        """
        Initialize color task
        
        Args:
            name: Task identifier
            actor_labels: List of actor labels to modify
            color: RGB color tuple (0-1 range)
            opacity: Opacity value (0-1)
        """
        super().__init__(name)
        self.actor_labels = actor_labels
        self.color = color
        self.opacity = opacity
    
    def execute(self, context: dict) -> TaskResult:
        """Apply color to specified actors"""
        import unreal
        from unreallib import materials
        
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        all_actors = editor_actor_subsystem.get_all_level_actors()
        
        modified_count = 0
        for actor in all_actors:
            label = actor.get_actor_label()
            if label in self.actor_labels:
                materials.set_actor_color(actor, self.color, self.opacity)
                modified_count += 1
        
        return TaskResult(
            output={
                'modified_count': modified_count,
                'color': self.color,
                'actor_labels': self.actor_labels
            },
            metadata={'task_type': 'set_actor_color'}
        )


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
