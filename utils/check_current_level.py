"""
Quick test to show which level is currently active in Unreal
"""

import unreal

# Get current level info
editor_level_lib = unreal.EditorLevelLibrary()
current_world = editor_level_lib.get_editor_world()

print("\n" + "="*70)
print("CURRENT LEVEL INFORMATION")
print("="*70)

print(f"World: {current_world.get_name()}")
print(f"World Path: {current_world.get_path_name()}")

# Get all actors in current level
editor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
all_actors = editor_subsystem.get_all_level_actors()

print(f"\nTotal Actors: {len(all_actors)}")

# Count workflow actors
workflow_actors = [a for a in all_actors if a.get_actor_label().startswith("workflow_")]
print(f"Workflow Actors: {len(workflow_actors)}")

if workflow_actors:
    print("\nWorkflow Actors:")
    for actor in sorted(workflow_actors, key=lambda a: a.get_actor_label())[:10]:
        print(f"  - {actor.get_actor_label()}")
    if len(workflow_actors) > 10:
        print(f"  ... and {len(workflow_actors) - 10} more")

# Show level asset path
level_asset_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
current_level_path = level_asset_subsystem.get_current_level().get_outer().get_path_name()

print(f"\nCurrent Level Asset: {current_level_path}")

print("="*70)
