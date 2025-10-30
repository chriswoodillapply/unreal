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
    """Reload all unreallib modules to pick up code changes"""
    # First, remove all unreallib modules from cache to force fresh imports
    to_remove = [m for m in list(sys.modules.keys()) if m.startswith('unreallib') or m.startswith('remotecontrol')]
    for m in to_remove:
        del sys.modules[m]
    print(f"🔄 Cleared {len(to_remove)} cached modules for fresh reload")

_reload_unreallib()

from unreallib.workflow import WorkflowLoader, WorkflowExecutor

# ============================================================
# CONFIGURATION - Change these settings
# ============================================================

WORKFLOW_NAME = 'import_external_model'  # Options: import_external_model, import_models_demo, material_grid_v2, scene_setup

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
