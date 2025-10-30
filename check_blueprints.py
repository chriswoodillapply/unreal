import unreal

# Check if Blueprints were created
bp_paths = [
    '/Game/Imported/teal_chair_Blueprint',
    '/Game/Imported/white_chair_Blueprint',
    '/Game/Imported/table_Blueprint'
]

unreal.log("\n=== Checking for Blueprints ===")
for bp_path in bp_paths:
    if unreal.EditorAssetLibrary.does_asset_exist(bp_path):
        bp = unreal.EditorAssetLibrary.load_asset(bp_path)
        unreal.log(f"✓ Found: {bp_path}")
        unreal.log(f"  Type: {type(bp).__name__}")
        
        # Try to get component count
        try:
            bp_class = bp.generated_class()
            if bp_class:
                cdo = unreal.get_default_object(bp_class)
                components = cdo.get_components_by_class(unreal.StaticMeshComponent)
                unreal.log(f"  Components: {len(components)} StaticMeshComponents")
                for i, comp in enumerate(components[:5]):  # Show first 5
                    mesh = comp.get_editor_property("static_mesh")
                    if mesh:
                        unreal.log(f"    {i+1}. {comp.get_name()}: {mesh.get_name()}")
        except Exception as e:
            unreal.log(f"  Error checking components: {e}")
    else:
        unreal.log(f"✗ Not found: {bp_path}")

unreal.log("\n=== Checking spawned actors in level ===")
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
for actor in all_actors:
    label = actor.get_actor_label()
    if 'chair' in label.lower() or 'table' in label.lower():
        unreal.log(f"Actor: {label} ({type(actor).__name__})")
        components = actor.get_components_by_class(unreal.StaticMeshComponent)
        unreal.log(f"  Components: {len(components)}")
