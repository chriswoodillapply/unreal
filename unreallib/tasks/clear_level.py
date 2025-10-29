"""
Task for clearing actors from level
"""

from typing import Dict, Any
from unreallib.workflow import Task, TaskResult, TaskStatus


class ClearLevelTask(Task):
    """
    Clears all actors from the current level
    
    Usage:
        task = ClearLevelTask("clear_scene")
    """
    
    def __init__(self, name: str = "clear_level"):
        super().__init__(name)
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Clear all actors from level"""
        from unreallib import level
        
        initial_count = level.get_actor_count()
        level.clear_all_actors()
        final_count = level.get_actor_count()
        deleted_count = initial_count - final_count
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={'deleted_count': deleted_count},
            metadata={
                'initial_actors': initial_count,
                'final_actors': final_count
            }
        )
