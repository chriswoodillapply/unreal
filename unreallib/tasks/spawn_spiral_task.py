"""
Spawn Spiral Task - Creates actors in a spiral pattern
"""

from typing import Dict, Any
from unreallib.workflow import Task, TaskResult, TaskStatus


class SpawnSpiralTask(Task):
    """
    Spawns actors in a spiral pattern
    
    Args:
        name: Task name
        count: Number of actors
        max_radius: Maximum spiral radius
        height_increment: Vertical spacing between actors
        shape: Actor shape ('cube', 'sphere', 'cylinder')
    
    Usage:
        task = SpawnSpiralTask("spiral", count=15, max_radius=400, height_increment=50)
    """
    
    def __init__(
        self,
        name: str,
        count: int = 15,
        max_radius: float = 400.0,
        height_increment: float = 50.0,
        shape: str = 'cylinder'
    ):
        super().__init__(
            name,
            count=count,
            max_radius=max_radius,
            height_increment=height_increment,
            shape=shape
        )
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Spawn spiral of actors"""
        from unreallib import actors
        
        actor_list = actors.spawn_spiral(
            count=self.params['count'],
            max_radius=self.params['max_radius'],
            height_increment=self.params['height_increment'],
            shape=self.params['shape']
        )
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={'actors': actor_list, 'count': len(actor_list)},
            metadata={
                'pattern': 'spiral',
                'max_radius': self.params['max_radius'],
                'height_increment': self.params['height_increment'],
                'shape': self.params['shape']
            }
        )
