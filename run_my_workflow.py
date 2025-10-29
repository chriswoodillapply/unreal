"""
Run any workflow by name

Usage from command line in your Unreal project:
    python -m remotecontrol run_my_workflow.py --method file

Then edit this file to change which workflow runs.
"""

import unreal
import importlib, sys

# Hot-reload unreallib modules so edits are picked up in a persistent Unreal Python session
def _reload_unreallib():
    to_reload = [m for m in list(sys.modules.keys()) if m.startswith('unreallib') or m.startswith('remotecontrol')]
    for m in sorted(to_reload, reverse=True):  # reverse to reload leaf modules first
        try:
            importlib.reload(sys.modules[m])
        except Exception:
            pass

_reload_unreallib()

from unreallib.workflow import WorkflowLoader, WorkflowExecutor

# ============================================================
# CONFIGURATION - Change these settings
# ============================================================

WORKFLOW_NAME = 'colored_grid'  # Change to: colored_grid, multiple_patterns, or your custom workflow

# ============================================================

print("=" * 70)
print(f"RUNNING WORKFLOW: {WORKFLOW_NAME} (hot reload active)")
print("=" * 70)

# Load workflow
loader = WorkflowLoader()
workflow = loader.load(WORKFLOW_NAME)
config = loader.last_config

print(f"\nTasks to execute: {list(workflow.tasks.keys())}")
print(f"Config: upsert={config.upsert_mode}, clear_before={config.clear_before_execute}")

# Execute
print("\nExecuting...")
executor = WorkflowExecutor(workflow, config=config)
results = executor.execute()

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

for task_name, result in results.items():
    status = "✓" if result.status.value == "success" else "✗"
    print(f"{status} {task_name}: {result.status.value}")
    if result.output:
        print(f"  Output: {result.output}")

print("\nDone! Check your Unreal Engine viewport.")
