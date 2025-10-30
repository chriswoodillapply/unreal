"""
Test the complete lighting workflow system in Unreal
This tests the LightsGeneratorTask and ForEachLightTask
"""

import unreal
print("\n" + "="*70)
print("LIGHTING WORKFLOW SYSTEM TEST")
print("="*70)

# Import workflow system
from unreallib.workflow import WorkflowLoader, WorkflowGraph, WorkflowExecutor
from unreallib.workflow.task import TaskStatus

# Test loading and executing the studio lighting workflow
print("\n1. Loading lighting_studio workflow...")
try:
    loader = WorkflowLoader()
    workflow = loader.load('lighting_studio')
    print(f"   ✓ Loaded workflow")
    print(f"   Tasks: {list(workflow.tasks.keys())}")
except Exception as e:
    print(f"   ✗ Error loading workflow: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Execute the workflow
print("\n2. Executing workflow...")
try:
    executor = WorkflowExecutor(workflow)
    results = executor.execute()
    print(f"   Tasks executed: {len(results)}")
    
    for task_name, task_result in results.items():
        print(f"     - {task_name}: {task_result.status}")
        if hasattr(task_result.output, 'get'):
            if 'lights' in task_result.output:
                print(f"       Generated {len(task_result.output['lights'])} light configs")
            if 'successful' in task_result.output:
                print(f"       Created {task_result.output['successful']} lights")
            if 'failed' in task_result.output and task_result.output['failed'] > 0:
                print(f"       Failed: {task_result.output['failed']}")
    
    # Check if all tasks succeeded
    all_success = all(r.status == TaskStatus.SUCCESS for r in results.values())
    print(f"\n   ✓ Workflow completed: {'All tasks succeeded' if all_success else 'Some tasks failed'}")
except Exception as e:
    print(f"   ✗ Error executing workflow: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Verify lights in scene
print("\n3. Verifying lights in scene...")
try:
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    studio_lights = [a for a in all_actors if a and 'studio_' in a.get_actor_label()]
    
    print(f"   Found {len(studio_lights)} studio lights:")
    for light in studio_lights:
        label = light.get_actor_label()
        location = light.get_actor_location()
        print(f"     - {label} at ({location.x:.0f}, {location.y:.0f}, {location.z:.0f})")
    
    expected_count = 5  # key, fill, rim, backdrop_left, backdrop_right
    if len(studio_lights) == expected_count:
        print(f"\n   ✓ All {expected_count} lights created successfully!")
    else:
        print(f"\n   ⚠ Expected {expected_count} lights, found {len(studio_lights)}")
except Exception as e:
    print(f"   ✗ Error verifying lights: {e}")

print("\n" + "="*70)
print("✅ LIGHTING WORKFLOW SYSTEM TEST COMPLETE")
print("="*70)
print("\nCheck your viewport to see the studio lighting setup!")
