"""
Set Actor Color Task - Applies colors to specific actors
"""

from typing import List, Tuple
from unreallib.workflow.task import Task, TaskResult


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
