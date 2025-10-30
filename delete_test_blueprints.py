import unreal

bp_paths = [
    '/Game/Imported/teal_chair_Blueprint',
    '/Game/Imported/white_chair_Blueprint',
    '/Game/Imported/table_Blueprint'
]

for path in bp_paths:
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        unreal.EditorAssetLibrary.delete_asset(path)
        unreal.log(f"✓ Deleted {path}")
    else:
        unreal.log(f"Not found: {path}")

unreal.log("✓ All Blueprints deleted, ready to test SubobjectDataSubsystem")
