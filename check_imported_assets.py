import unreal

# Check what assets were imported
folders = [
    '/Game/Imported/teal_chair',
    '/Game/Imported/white_chair',
    '/Game/Imported/table'
]

for folder in folders:
    unreal.log(f"\n=== Checking {folder} ===")
    if unreal.EditorAssetLibrary.does_directory_exist(folder):
        assets = unreal.EditorAssetLibrary.list_assets(folder, recursive=False)
        unreal.log(f"Total assets: {len(assets)}")
        
        meshes = []
        for asset_path in assets:
            asset = unreal.EditorAssetLibrary.load_asset(asset_path)
            asset_type = type(asset).__name__
            unreal.log(f"  - {asset_path.split('/')[-1]}: {asset_type}")
            if isinstance(asset, unreal.StaticMesh):
                meshes.append(asset)
        
        unreal.log(f"StaticMesh count: {len(meshes)}")
    else:
        unreal.log(f"Folder doesn't exist")
