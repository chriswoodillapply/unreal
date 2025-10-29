"""
Test JSON workflow system in Unreal Engine
Loads and executes a workflow in the current level
"""

import unreal
from unreallib.workflow import WorkflowLoader, WorkflowExecutor

print("=" * 70)
print("TESTING JSON WORKFLOW SYSTEM")
print("=" * 70)

# Get current level
level_name = unreal.EditorLevelLibrary.get_editor_world().get_name()
print(f"\nCurrent Level: {level_name}")

# Create workflow loader
print("\n[1] Creating WorkflowLoader...")
loader = WorkflowLoader()

# List available workflows
print("\n[2] Available Workflows:")
workflows = loader.list_workflows()
for wf_file in workflows:
    info = loader.get_workflow_info(wf_file.replace('.json', ''))
    print(f"  ✓ {info['name']} ({wf_file})")
    print(f"    {info['description']}")
    print(f"    Tasks: {info['task_count']}")
print()

# Load simple_grid workflow
print("[3] Loading 'simple_grid' workflow...")
workflow = loader.load('simple_grid')
config = loader.last_config

print(f"  Config:")
print(f"    - upsert_mode: {config.upsert_mode}")
print(f"    - clear_before_execute: {config.clear_before_execute}")
print(f"    - actor_id_prefix: {config.actor_id_prefix}")
print(f"\n  Tasks: {list(workflow.tasks.keys())}")
print(f"  Dependencies: {workflow.dependencies}")

# Execute workflow
print("\n[4] Executing Workflow...")
print("-" * 70)
executor = WorkflowExecutor(config=config)

import time
start_time = time.time()
results = executor.execute(workflow)
elapsed = time.time() - start_time

# Show results
print("-" * 70)
print(f"\n[5] Workflow Results (completed in {elapsed:.2f}s):")
for task_name, result in results.items():
    status_symbol = "✓" if result.status.value == "success" else "✗"
    print(f"  {status_symbol} {task_name}: {result.status.value}")
    if result.output:
        print(f"    Output: {result.output}")

print("\n" + "=" * 70)
print("WORKFLOW TEST COMPLETE!")
print("=" * 70)

# Verify actors were created
editor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
all_actors = editor_subsystem.get_all_level_actors()
workflow_actors = [a for a in all_actors if a.get_actor_label().startswith('grid_')]

print(f"\nVerification: Found {len(workflow_actors)} actors with 'grid_' prefix")
print("\nYou should see a 5x5 grid of cubes in your level!")
