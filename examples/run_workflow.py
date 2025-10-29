"""
Example: Run workflow from JSON file

This demonstrates how to load and execute workflows defined in JSON files.

Usage:
    python -m remotecontrol examples/run_workflow.py --method file
"""

import unreal
from unreallib.workflow import WorkflowLoader, WorkflowExecutor

print("="*60)
print("RUNNING WORKFLOW FROM JSON FILE")
print("="*60)

# Create workflow loader
loader = WorkflowLoader()

# List available workflows
print("\nAvailable workflows:")
for workflow_file in loader.list_workflows():
    info = loader.get_workflow_info(workflow_file)
    print(f"  - {info['name']}: {info['description']}")
    print(f"    File: {info['file']}, Tasks: {info['task_count']}")

# Load and execute a workflow
print("\n" + "="*60)
print("Loading workflow: simple_grid.json")
print("="*60)

workflow = loader.load('simple_grid')
config = loader.last_config  # Get config from last loaded workflow

# Show workflow info
print(f"\nWorkflow config: upsert_mode={config.upsert_mode}, clear_before={config.clear_before_execute}")
print(f"Tasks: {len(workflow.tasks)}")

# Execute workflow
print("\nExecuting workflow...")
executor = WorkflowExecutor(config=config)
result = executor.execute(workflow)

print("\n" + "="*60)
print("WORKFLOW EXECUTION COMPLETE")
print("="*60)
print(f"Total execution time: {result['execution_time']:.2f}s")
print(f"Tasks executed: {len(result['task_results'])}")

for task_name, task_result in result['task_results'].items():
    print(f"  [{task_name}] {task_result}")

unreal.log("Workflow execution completed successfully!")
