"""
Spawn Circle Task - Creates actors in a circle pattern
"""

from typing import Dict, Any
from unreallib.workflow import Task, TaskResult, TaskStatus


class SpawnCircleTask(Task):
    """
    Spawns actors in a circle pattern
    
    Args:
        name: Task name
        count: Number of actors
        radius: Circle radius
        shape: Actor shape ('cube', 'sphere', 'cylinder')
    
    Usage:
        task = SpawnCircleTask("circle", count=12, radius=500, shape='sphere')
    """
    
    def __init__(
        self,
        name: str,
        count: int = 12,
        radius: float = 500.0,
        shape: str = 'sphere'
    ):
        super().__init__(
            name,
            count=count,
            radius=radius,
            shape=shape
        )
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Spawn circle of actors"""
        from unreallib import actors
        
        actor_list = actors.spawn_circle(
            count=self.params['count'],
            radius=self.params['radius'],
            shape=self.params['shape']
        )
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={'actors': actor_list, 'count': len(actor_list)},
            metadata={
                'pattern': 'circle',
                'radius': self.params['radius'],
                'shape': self.params['shape']
            }
        )
