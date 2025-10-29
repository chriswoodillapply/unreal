"""
Tasks for spawning actors in various patterns
"""

from typing import Dict, Any, List
from unreallib.workflow import Task, TaskResult, TaskStatus


class SpawnGridTask(Task):
    """
    Spawns actors in a grid pattern
    
    Args:
        name: Task name
        rows: Number of rows
        cols: Number of columns
        spacing: Distance between actors
        shape: Actor shape ('cube', 'sphere', 'cylinder')
        scale: Uniform scale for actors
    
    Usage:
        task = SpawnGridTask("grid", rows=5, cols=5, spacing=200, shape='cube')
    """
    
    def __init__(
        self, 
        name: str,
        rows: int = 5,
        cols: int = 5,
        spacing: float = 200.0,
        shape: str = 'cube',
        scale: float = 1.0
    ):
        super().__init__(
            name,
            rows=rows,
            cols=cols,
            spacing=spacing,
            shape=shape,
            scale=scale
        )
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Spawn grid of actors with optional upsert support"""
        from unreallib import actors
        from unreallib.utils import ActorRegistry
        import unreal
        
        rows = self.params['rows']
        cols = self.params['cols']
        spacing = self.params['spacing']
        shape = self.params['shape']
        scale = self.params['scale']
        
        # Check if upsert mode is enabled
        config = context.get('config')
        upsert_mode = config.upsert_mode if config else False
        prefix = config.actor_id_prefix if config else "workflow_grid_"
        
        if upsert_mode:
            # Use actor registry for upsert
            registry = ActorRegistry(prefix=prefix)
            actor_list = []
            created_count = 0
            updated_count = 0
            
            spawn_funcs = {
                'cube': actors.spawn_cube,
                'sphere': actors.spawn_sphere,
                'cylinder': actors.spawn_cylinder
            }
            spawn_func = spawn_funcs.get(shape, actors.spawn_cube)
            
            for row in range(rows):
                for col in range(cols):
                    x = col * spacing - (cols - 1) * spacing / 2
                    y = row * spacing - (rows - 1) * spacing / 2
                    z = 0
                    
                    actor_id = f"{row}_{col}"
                    
                    def create_actor():
                        return spawn_func((x, y, z), scale)
                    
                    def update_actor(actor):
                        # Update position if needed
                        actor.set_actor_location(unreal.Vector(x, y, z), False, False)
                        actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
                    
                    actor, was_created = registry.update_or_create(
                        actor_id,
                        create_actor,
                        update_actor
                    )
                    
                    actor_list.append(actor)
                    if was_created:
                        created_count += 1
                    else:
                        updated_count += 1
            
            return TaskResult(
                status=TaskStatus.SUCCESS,
                output={
                    'actors': actor_list,
                    'actor_count': len(actor_list),
                    'created': created_count,
                    'updated': updated_count
                },
                metadata={
                    'pattern': 'grid',
                    'rows': rows,
                    'cols': cols,
                    'shape': shape,
                    'upsert_mode': True
                }
            )
        else:
            # Standard spawn without upsert
            actor_list = actors.spawn_grid(
                rows=rows,
                cols=cols,
                spacing=spacing,
                shape=shape,
                scale=scale
            )
            
            return TaskResult(
                status=TaskStatus.SUCCESS,
                output={'actors': actor_list, 'actor_count': len(actor_list)},
                metadata={
                    'pattern': 'grid',
                    'rows': rows,
                    'cols': cols,
                    'shape': shape,
                    'upsert_mode': False
                }
            )


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
