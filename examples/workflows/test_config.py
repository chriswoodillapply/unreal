"""
Simple test of workflow config - no unicode characters
"""

from unreallib.workflow import WorkflowGraph, WorkflowExecutor, WorkflowConfig
from unreallib.tasks import SpawnGridTask

# Create workflow
workflow = WorkflowGraph()
workflow.add_task(SpawnGridTask("test_grid", rows=2, cols=2, spacing=150, shape='cube'))

# Test config with clear_before_execute
config = WorkflowConfig(clear_before_execute=True, save_level_after=False)

print("Config:", config)

# Execute
executor = WorkflowExecutor(workflow, config)
results = executor.execute()

print("Complete!")
