import unreal

# Test what methods are available for adding components
unreal.log("\n=== EditorLevelLibrary methods ===")
for attr in dir(unreal.EditorLevelLibrary):
    if 'component' in attr.lower() or 'add' in attr.lower():
        unreal.log(f"  - {attr}")

unreal.log("\n=== EditorActorSubsystem methods ===")
subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for attr in dir(subsys):
    if 'component' in attr.lower() or 'add' in attr.lower():
        unreal.log(f"  - {attr}")

unreal.log("\n=== Testing add_component ===")
# Spawn test actor
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.Actor,
    unreal.Vector(0, 0, -10000),
    unreal.Rotator(0, 0, 0)
)

# Try different ways to add component
try:
    comp = unreal.EditorLevelLibrary.add_component_to_actor(actor, unreal.StaticMeshComponent)
    unreal.log(f"✓ add_component_to_actor worked: {comp}")
except Exception as e:
    unreal.log(f"✗ add_component_to_actor failed: {e}")

try:
    subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    comp = subsys.add_component(actor, unreal.StaticMeshComponent)
    unreal.log(f"✓ EditorActorSubsystem.add_component worked: {comp}")
except Exception as e:
    unreal.log(f"✗ EditorActorSubsystem.add_component failed: {e}")

# Clean up
unreal.EditorLevelLibrary.destroy_actor(actor)
