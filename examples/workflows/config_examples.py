"""
Example: Using workflow configuration

Demonstrates different execution modes:
- clean_slate: Clear before execute
- incremental: Keep existing, add new
- upsert: Update existing or create new
"""

from unreallib.workflow import (
    WorkflowGraph, 
    WorkflowExecutor, 
    WorkflowConfig,
    get_preset_config
)
from unreallib.tasks import SpawnGridTask, SpawnCircleTask

# Example 1: Clean Slate (default - clear before executing)
print("\n" + "="*60)
print("Example 1: Clean Slate Mode")
print("="*60)

workflow1 = WorkflowGraph()
workflow1.add_task(SpawnGridTask("grid", rows=3, cols=3, spacing=200, shape='cube'))

config1 = get_preset_config('clean_slate')
executor1 = WorkflowExecutor(workflow1, config1)
results1 = executor1.execute()


# Example 2: Incremental Mode (keep existing actors)
print("\n" + "="*60)
print("Example 2: Incremental Mode")
print("="*60)

workflow2 = WorkflowGraph()
workflow2.add_task(SpawnCircleTask("circle", count=8, radius=400, shape='sphere'))

config2 = WorkflowConfig(
    clear_before_execute=False,  # Don't clear
    upsert_mode=False,            # Just add new actors
)
executor2 = WorkflowExecutor(workflow2, config2)
results2 = executor2.execute()


# Example 3: Production Mode (clear + save)
print("\n" + "="*60)
print("Example 3: Production Mode (with save)")
print("="*60)

workflow3 = WorkflowGraph()
workflow3.add_task(SpawnGridTask("final_grid", rows=5, cols=5, spacing=150, shape='cylinder'))

config3 = get_preset_config('production')
executor3 = WorkflowExecutor(workflow3, config3)
results3 = executor3.execute()

print("\n✓ All examples complete!")
print("\nConfiguration presets used:")
print("  - clean_slate: clear_before_execute=True")
print("  - incremental: clear_before_execute=False, upsert_mode=True")
print("  - production:  clear_before_execute=True, save_level_after=True")
