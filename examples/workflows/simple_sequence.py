"""
Example: Simple linear workflow

Demonstrates a simple sequential workflow where tasks depend on each other.
"""

from unreallib.workflow import WorkflowGraph, WorkflowExecutor
from unreallib.tasks import ClearLevelTask, SpawnGridTask

# Create workflow
workflow = WorkflowGraph()

# Sequential tasks
clear = ClearLevelTask("clear")
small_grid = SpawnGridTask("small_grid", rows=3, cols=3, spacing=150, shape='cube')
large_grid = SpawnGridTask("large_grid", rows=10, cols=10, spacing=100, shape='sphere')

# Chain them: clear → small_grid → large_grid
workflow.add_task(clear)
workflow.add_task(small_grid, depends_on=["clear"])
workflow.add_task(large_grid, depends_on=["small_grid"])

# Execute
print(workflow.visualize())
executor = WorkflowExecutor(workflow)
results = executor.execute()
