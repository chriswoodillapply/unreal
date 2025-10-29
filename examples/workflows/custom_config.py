"""
Example: Custom workflow configuration

Shows how to create custom configurations for specific needs.
"""

from unreallib.workflow import WorkflowGraph, WorkflowExecutor, WorkflowConfig
from unreallib.tasks import ClearLevelTask, SpawnGridTask, SpawnCircleTask

# Create workflow
workflow = WorkflowGraph()
workflow.add_task(ClearLevelTask("clear"))
workflow.add_task(SpawnGridTask("grid", rows=4, cols=4, spacing=180, shape='cube'), depends_on=["clear"])
workflow.add_task(SpawnCircleTask("circle", count=10, radius=450, shape='sphere'), depends_on=["clear"])

# Custom configuration
config = WorkflowConfig(
    clear_before_execute=False,  # ClearLevelTask handles this
    upsert_mode=False,
    actor_id_prefix="demo_",
    save_level_after=True,      # Save when done
    metadata={
        'author': 'workflow_system',
        'scene_type': 'demonstration',
        'version': '1.0'
    }
)

print(f"Using config: {config}")
print(f"Metadata: {config.metadata}")

# Execute
executor = WorkflowExecutor(workflow, config)
results = executor.execute()

# Check results
success_count = sum(1 for r in results.values() if r.success)
print(f"\n✓ {success_count}/{len(results)} tasks succeeded")
