"""
Count actors in the level
"""

import unreal

editor_actor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
all_actors = editor_actor.get_all_level_actors()

print(f"Total actors in level: {len(all_actors)}")

# Count test cubes
test_cubes = [a for a in all_actors if a.get_actor_label().startswith("TestCube")]
print(f"TestCube actors: {len(test_cubes)}")

if test_cubes:
    print("\nTestCube details:")
    for actor in test_cubes:
        loc = actor.get_actor_location()
        print(f"  - {actor.get_actor_label()} at ({loc.x}, {loc.y}, {loc.z})")

# Count workflow actors
workflow_actors = [a for a in all_actors if a.get_actor_label().startswith("workflow_")]
print(f"\nWorkflow actors: {len(workflow_actors)}")

if workflow_actors:
    print("Workflow actor details:")
    for actor in workflow_actors[:5]:  # First 5
        print(f"  - {actor.get_actor_label()}")
    if len(workflow_actors) > 5:
        print(f"  ... and {len(workflow_actors) - 5} more")

print("\nDone!")
