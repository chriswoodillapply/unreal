"""
Test the romantic dining room lighting workflow
"""

import unreal

print("\n" + "="*70)
print("🕯️  ROMANTIC DINING ROOM LIGHTING TEST")
print("="*70)

from unreallib.workflow import WorkflowLoader, WorkflowExecutor
from unreallib.workflow.task import TaskStatus

# Load and execute the romantic dining workflow
print("\n📖 Loading romantic dining room lighting workflow...")
try:
    loader = WorkflowLoader()
    workflow = loader.load('lighting_romantic_dining')
    print(f"   ✓ Loaded workflow")
    print(f"   Tasks: {list(workflow.tasks.keys())}")
except Exception as e:
    print(f"   ✗ Error loading workflow: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Execute the workflow
print("\n🎬 Executing romantic lighting workflow...")
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
                print(f"       ⚠ Failed: {task_result.output['failed']}")
    
    # Check if all tasks succeeded
    all_success = all(r.status == TaskStatus.SUCCESS for r in results.values())
    print(f"\n   ✓ Workflow completed: {'All tasks succeeded' if all_success else 'Some tasks failed'}")
except Exception as e:
    print(f"   ✗ Error executing workflow: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Verify lights were created
print("\n🔍 Verifying romantic lights in scene...")
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
romantic_lights = [a for a in all_actors if a.get_name().startswith('romance_')]

print(f"   Found {len(romantic_lights)} romantic lights:")
for light in romantic_lights:
    location = light.get_actor_location()
    print(f"     • {light.get_name()} at ({location.x:.0f}, {location.y:.0f}, {location.z:.0f})")

print("\n" + "="*70)
print("✅ ROMANTIC DINING ROOM LIGHTING TEST COMPLETE")
print("="*70)
print("\n🌟 Lighting breakdown:")
print("   • 2 candle clusters (warm orange glow)")
print("   • 2 chandelier lights (soft warm key)")
print("   • 2 wall sconces (directional warm accents)")
print("   • 1 rim light (cool blue-white moonlight)")
print("   • 2 bounce fills (ambient warmth)")
print("   • 1 directional moonlight (subtle cool fill)")
print("\n💡 Check your viewport to see the romantic atmosphere!")
