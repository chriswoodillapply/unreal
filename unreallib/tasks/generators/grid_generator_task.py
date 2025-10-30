"""
Generator task: Generate grid positions and parameters
"""

from typing import Dict, Any, List
from unreallib.workflow.task import Task, TaskResult, TaskStatus


class GridGeneratorTask(Task):
    """
    Generate grid positions and parameters
    
    This is a generator task that produces a list of positions and parameters
    that can be iterated over by primitive tasks. It doesn't spawn actors itself,
    it just calculates where they should go.
    """
    
    def __init__(
        self,
        name: str,
        rows: int = 3,
        cols: int = 3,
        spacing: float = 200.0,
        center_offset: tuple = (0, 0, 0),
        shape: str = "sphere",
        scale: float = 1.0
    ):
        """
        Initialize grid generator
        
        Args:
            name: Task name
            rows: Number of rows
            cols: Number of columns
            spacing: Distance between grid points
            center_offset: (x, y, z) offset for grid center
            shape: Default shape for all grid points
            scale: Default scale for all grid points
        """
        super().__init__(
            name,
            rows=rows,
            cols=cols,
            spacing=spacing,
            center_offset=center_offset,
            shape=shape,
            scale=scale
        )
        
        self.rows = rows
        self.cols = cols
        self.spacing = spacing
        self.center_offset = center_offset
        self.shape = shape
        self.scale = scale
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Generate grid positions"""
        
        # Calculate grid center offset
        center_x = (self.cols - 1) * self.spacing / 2
        center_y = (self.rows - 1) * self.spacing / 2
        
        offset_x, offset_y, offset_z = self.center_offset
        
        # Generate grid points
        grid_points = []
        
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculate position
                x = col * self.spacing - center_x + offset_x
                y = row * self.spacing - center_y + offset_y
                z = offset_z
                
                # Create grid point data
                point = {
                    'actor_id': f"{row}_{col}",
                    'row': row,
                    'col': col,
                    'location': (x, y, z),
                    'shape': self.shape,
                    'scale': self.scale,
                    'index': row * self.cols + col
                }
                
                grid_points.append(point)
        
        # Store in context for use by other tasks
        context['grid_points'] = grid_points
        context['grid_config'] = {
            'rows': self.rows,
            'cols': self.cols,
            'spacing': self.spacing,
            'total_points': len(grid_points)
        }
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={
                'grid_points': grid_points,
                'total_points': len(grid_points),
                'rows': self.rows,
                'cols': self.cols
            }
        )
