"""
Example: Complex scene generation using workflow DAG

This demonstrates how to build complex scenes by composing tasks
with dependencies in a directed acyclic graph (DAG).
"""

from unreallib.workflow import WorkflowGraph, WorkflowExecutor
from unreallib.tasks import (
    ClearLevelTask,
    SpawnGridTask,
    SpawnCircleTask,
    SpawnSpiralTask,
)

# Create workflow graph
workflow = WorkflowGraph()

# Define tasks
clear = ClearLevelTask("clear_scene")
grid = SpawnGridTask("cube_grid", rows=5, cols=5, spacing=200, shape='cube')
circle = SpawnCircleTask("sphere_circle", count=12, radius=500, shape='sphere')
spiral = SpawnSpiralTask("cylinder_spiral", count=15, max_radius=400, height_increment=50, shape='cylinder')

# Build DAG - clear first, then spawn in parallel
workflow.add_task(clear)
workflow.add_task(grid, depends_on=["clear_scene"])
workflow.add_task(circle, depends_on=["clear_scene"])
workflow.add_task(spiral, depends_on=["clear_scene"])

# Visualize workflow
print(workflow.visualize())

# Execute workflow
executor = WorkflowExecutor(workflow)
results = executor.execute()

# Check results
if all(r.success for r in results.values()):
    print("✓ All tasks completed successfully!")
    
    # Get actor counts from each task
    grid_count = results["cube_grid"].output['count']
    circle_count = results["sphere_circle"].output['count']
    spiral_count = results["cylinder_spiral"].output['count']
    total = grid_count + circle_count + spiral_count
    
    print(f"\nScene Summary:")
    print(f"  Cubes (grid):      {grid_count}")
    print(f"  Spheres (circle):  {circle_count}")
    print(f"  Cylinders (spiral): {spiral_count}")
    print(f"  Total actors:      {total}")
else:
    print("✗ Some tasks failed!")
