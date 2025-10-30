"""
Test Lighting System in Unreal Engine

This script tests the lighting system components directly in Unreal.
Run this from within Unreal Engine's Python console or via remote execution.
"""

import sys
from pathlib import Path

# Ensure scripts are in path - handle both file and remote execution
try:
    scripts_dir = Path(__file__).parent
except NameError:
    # When executed via remote control, __file__ might not be defined
    scripts_dir = Path(r'C:\Users\cwood\Documents\Unreal Projects\firstperson\scripts')

if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

import unreal
from unreallib.tasks.generators import LightsGeneratorTask, ForEachLightTask
from unreallib.workflow.task import TaskStatus
from unreallib.workflow import WorkflowLoader, WorkflowExecutor


def test_lights_generator_task():
    """Test LightsGeneratorTask"""
    print("\n" + "="*80)
    print("TEST 1: LightsGeneratorTask - Single Light")
    print("="*80)
    
    lights = [
        {
            'actor_id': 'test_light',
            'light_type': 'point',
            'location': [300, 0, 400],
            'intensity': 10000.0,
            'color': [1.0, 0.9, 0.8]
        }
    ]
    
    task = LightsGeneratorTask('test_gen', lights=lights)
    result = task.execute({})
    
    print(f"Status: {result.status}")
    print(f"Output: {result.output}")
    
    assert result.status == TaskStatus.SUCCESS, "Generator task should succeed"
    assert len(result.output['lights']) == 1, "Should have 1 light"
    assert result.output['lights'][0]['actor_id'] == 'test_light', "Actor ID should match"
    
    print("✓ PASSED")
    return True


def test_lights_generator_multiple():
    """Test LightsGeneratorTask with multiple lights"""
    print("\n" + "="*80)
    print("TEST 2: LightsGeneratorTask - Multiple Lights")
    print("="*80)
    
    lights = [
        {
            'actor_id': 'key_light',
            'light_type': 'point',
            'location': [400, 300, 400],
            'intensity': 12000.0,
            'color': [1.0, 0.9, 0.8]
        },
        {
            'actor_id': 'fill_light',
            'light_type': 'point',
            'location': [-300, -200, 300],
            'intensity': 6000.0,
            'color': [0.6, 0.7, 1.0]
        },
        {
            'actor_id': 'rim_light',
            'light_type': 'spot',
            'location': [-200, 400, 200],
            'rotation': [0, -135, 0],
            'intensity': 10000.0
        }
    ]
    
    task = LightsGeneratorTask('test_gen', lights=lights)
    result = task.execute({})
    
    print(f"Status: {result.status}")
    print(f"Light count: {result.output['count']}")
    
    assert result.status == TaskStatus.SUCCESS, "Generator should succeed"
    assert result.output['count'] == 3, "Should have 3 lights"
    
    print("✓ PASSED")
    return True


def test_lights_generator_defaults():
    """Test default value application"""
    print("\n" + "="*80)
    print("TEST 3: LightsGeneratorTask - Default Values")
    print("="*80)
    
    lights = [
        {
            'light_type': 'point',
            'location': [0, 0, 300]
            # No intensity, color, rotation specified
        }
    ]
    
    task = LightsGeneratorTask(
        'test_gen',
        lights=lights,
        default_intensity=8000.0,
        default_color=(1.0, 0.9, 0.8),
        default_rotation=(-45, 0, 0)
    )
    result = task.execute({})
    
    light = result.output['lights'][0]
    print(f"Applied intensity: {light['intensity']}")
    print(f"Applied color: {light['color']}")
    print(f"Applied rotation: {light['rotation']}")
    
    assert light['intensity'] == 8000.0, "Should use default intensity"
    assert light['color'] == (1.0, 0.9, 0.8), "Should use default color"
    assert light['rotation'] == (-45, 0, 0), "Should use default rotation"
    
    print("✓ PASSED")
    return True


def test_lights_generator_validation():
    """Test validation failures"""
    print("\n" + "="*80)
    print("TEST 4: LightsGeneratorTask - Validation")
    print("="*80)
    
    # Test missing light_type
    print("\n  Test 4a: Missing light_type")
    lights = [{'location': [0, 0, 300]}]
    task = LightsGeneratorTask('test_gen', lights=lights)
    result = task.execute({})
    assert result.status == TaskStatus.FAILURE, "Should fail without light_type"
    print(f"  Error: {result.output['error']}")
    print("  ✓ Correctly rejected")
    
    # Test missing location
    print("\n  Test 4b: Missing location")
    lights = [{'light_type': 'point'}]
    task = LightsGeneratorTask('test_gen', lights=lights)
    result = task.execute({})
    assert result.status == TaskStatus.FAILURE, "Should fail without location"
    print(f"  Error: {result.output['error']}")
    print("  ✓ Correctly rejected")
    
    # Test invalid light_type
    print("\n  Test 4c: Invalid light_type")
    lights = [{'light_type': 'invalid', 'location': [0, 0, 300]}]
    task = LightsGeneratorTask('test_gen', lights=lights)
    result = task.execute({})
    assert result.status == TaskStatus.FAILURE, "Should fail with invalid type"
    print(f"  Error: {result.output['error']}")
    print("  ✓ Correctly rejected")
    
    print("\n✓ PASSED")
    return True


def test_foreach_light_task():
    """Test ForEachLightTask creates actual lights"""
    print("\n" + "="*80)
    print("TEST 5: ForEachLightTask - Create Actual Lights")
    print("="*80)
    
    # Clear existing test lights
    print("\nCleaning up any existing test lights...")
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor and actor.get_actor_label().startswith('test_foreach_'):
            unreal.EditorLevelLibrary.destroy_actor(actor)
    
    # Generate lights
    lights = [
        {
            'actor_id': 'test_foreach_key',
            'light_type': 'point',
            'location': [200, 100, 300],
            'intensity': 8000.0,
            'color': [1.0, 0.9, 0.8]
        },
        {
            'actor_id': 'test_foreach_fill',
            'light_type': 'point',
            'location': [-200, -100, 250],
            'intensity': 5000.0,
            'color': [0.6, 0.7, 1.0]
        }
    ]
    
    gen_task = LightsGeneratorTask('gen', lights=lights)
    gen_result = gen_task.execute({})
    
    print(f"Generated {gen_result.output['count']} light configs")
    
    # Create lights
    context = {'gen': gen_result.output}
    create_task = ForEachLightTask('create', lights_input='gen.lights')
    create_result = create_task.execute(context)
    
    print(f"Status: {create_result.status}")
    print(f"Successful: {create_result.output['successful']}")
    print(f"Failed: {create_result.output['failed']}")
    print(f"Created lights: {create_result.output['created_lights']}")
    
    assert create_result.status == TaskStatus.SUCCESS, "Should successfully create lights"
    assert create_result.output['successful'] == 2, "Should create 2 lights"
    assert create_result.output['failed'] == 0, "Should have no failures"
    
    # Verify lights exist in level
    print("\nVerifying lights in level...")
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    test_lights = [a for a in all_actors if a and 'test_foreach' in a.get_actor_label()]
    print(f"Found {len(test_lights)} test lights in level")
    
    for light in test_lights:
        print(f"  - {light.get_actor_label()} at {light.get_actor_location()}")
    
    assert len(test_lights) == 2, "Should have 2 lights in level"
    
    print("✓ PASSED")
    return True


def test_full_workflow_json():
    """Test loading and executing a complete lighting workflow from JSON"""
    print("\n" + "="*80)
    print("TEST 6: Full Workflow - Load and Execute JSON")
    print("="*80)
    
    # Clear existing lights
    print("\nCleaning up existing workflow lights...")
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor and 'demo_' in actor.get_actor_label():
            unreal.EditorLevelLibrary.destroy_actor(actor)
    
    # Load workflow
    print("\nLoading workflow: complete_scene_with_lights.json")
    loader = WorkflowLoader()
    workflow = loader.load('complete_scene_with_lights')
    
    print(f"Loaded workflow: {workflow.name}")
    print(f"Tasks: {len(workflow.tasks)}")
    for task_name in workflow.tasks:
        print(f"  - {task_name}")
    
    # Execute workflow
    print("\nExecuting workflow...")
    executor = WorkflowExecutor()
    result = executor.execute(workflow)
    
    print(f"\nWorkflow Status: {result.status}")
    print(f"Executed tasks: {len(result.task_results)}")
    
    for task_name, task_result in result.task_results.items():
        print(f"  {task_name}: {task_result.status}")
        if task_result.status != TaskStatus.SUCCESS:
            print(f"    Error: {task_result.output}")
    
    assert result.status == TaskStatus.SUCCESS, "Workflow should complete successfully"
    
    # Verify objects in scene
    print("\nVerifying scene objects...")
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    demo_actors = [a for a in all_actors if a and 'demo_' in a.get_actor_label()]
    
    print(f"Found {len(demo_actors)} demo actors:")
    for actor in demo_actors:
        label = actor.get_actor_label()
        location = actor.get_actor_location()
        print(f"  - {label} at {location}")
    
    assert len(demo_actors) >= 6, "Should have at least 6 actors (2 objects, 1 camera, 4 lights)"
    
    print("✓ PASSED")
    return True


def test_studio_lighting_workflow():
    """Test the studio lighting workflow"""
    print("\n" + "="*80)
    print("TEST 7: Studio Lighting Workflow")
    print("="*80)
    
    # Clear existing lights
    print("\nCleaning up existing studio lights...")
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor and 'studio_' in actor.get_actor_label():
            unreal.EditorLevelLibrary.destroy_actor(actor)
    
    # Load and execute
    print("\nLoading workflow: lighting_studio.json")
    loader = WorkflowLoader()
    workflow = loader.load('lighting_studio')
    
    print(f"Executing {workflow.name}...")
    executor = WorkflowExecutor()
    result = executor.execute(workflow)
    
    print(f"Status: {result.status}")
    
    # Check results
    assert result.status == TaskStatus.SUCCESS, "Studio lighting should succeed"
    
    # Verify lights
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    studio_lights = [a for a in all_actors if a and 'studio_' in a.get_actor_label()]
    
    print(f"\nCreated {len(studio_lights)} studio lights:")
    for light in studio_lights:
        print(f"  - {light.get_actor_label()}")
    
    assert len(studio_lights) == 5, "Should have 5 studio lights"
    
    print("✓ PASSED")
    return True


def cleanup_test_lights():
    """Clean up all test lights"""
    print("\n" + "="*80)
    print("CLEANUP: Removing Test Lights")
    print("="*80)
    
    prefixes = ['test_', 'demo_', 'studio_']
    removed = 0
    
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor:
            label = actor.get_actor_label()
            if any(label.startswith(prefix) for prefix in prefixes):
                print(f"  Removing: {label}")
                unreal.EditorLevelLibrary.destroy_actor(actor)
                removed += 1
    
    print(f"\nRemoved {removed} test actors")


def run_all_tests():
    """Run all lighting system tests"""
    print("\n" + "="*80)
    print("LIGHTING SYSTEM TEST SUITE")
    print("="*80)
    
    tests = [
        ("Lights Generator - Single", test_lights_generator_task),
        ("Lights Generator - Multiple", test_lights_generator_multiple),
        ("Lights Generator - Defaults", test_lights_generator_defaults),
        ("Lights Generator - Validation", test_lights_generator_validation),
        ("ForEach Light Task", test_foreach_light_task),
        ("Full Workflow JSON", test_full_workflow_json),
        ("Studio Lighting", test_studio_lighting_workflow),
    ]
    
    passed = 0
    failed = 0
    errors = []
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            failed += 1
            errors.append((test_name, str(e)))
            print(f"\n✗ FAILED: {test_name}")
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Cleanup
    try:
        cleanup_test_lights()
    except Exception as e:
        print(f"Cleanup error: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if errors:
        print("\nFailed tests:")
        for test_name, error in errors:
            print(f"  - {test_name}: {error}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    return failed == 0


if __name__ == '__main__':
    print("\nStarting Lighting System Tests...")
    print("This will create and remove test lights in your level.")
    
    success = run_all_tests()
    
    if success:
        print("\n✓ Test suite completed successfully")
    else:
        print("\n✗ Test suite had failures")
