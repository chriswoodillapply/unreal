import unreal

# Check what's REALLY in the folders with full detail
folders = [
    '/Game/Imported/teal_chair',
    '/Game/Imported/white_chair', 
    '/Game/Imported/table'
]

for folder in folders:
    unreal.log(f"\n{'='*60}")
    unreal.log(f"Folder: {folder}")
    unreal.log(f"{'='*60}")
    
    if not unreal.EditorAssetLibrary.does_directory_exist(folder):
        unreal.log("✗ Folder doesn't exist")
        continue
    
    assets = unreal.EditorAssetLibrary.list_assets(folder, recursive=False)
    unreal.log(f"Total assets in folder: {len(assets)}")
    
    meshes = []
    materials = []
    textures = []
    other = []
    
    for asset_path in assets:
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)
        asset_name = asset_path.split('/')[-1]
        asset_type = type(asset).__name__
        
        if isinstance(asset, unreal.StaticMesh):
            meshes.append(asset_name)
        elif isinstance(asset, unreal.Material) or isinstance(asset, unreal.MaterialInstance):
            materials.append(asset_name)
        elif isinstance(asset, unreal.Texture2D):
            textures.append(asset_name)
        else:
            other.append(f"{asset_name} ({asset_type})")
    
    unreal.log(f"\nStaticMeshes ({len(meshes)}):")
    for mesh in meshes:
        unreal.log(f"  - {mesh}")
    
    unreal.log(f"\nMaterials ({len(materials)}):")
    for mat in materials[:5]:  # Show first 5
        unreal.log(f"  - {mat}")
    if len(materials) > 5:
        unreal.log(f"  ... and {len(materials)-5} more")
    
    unreal.log(f"\nTextures ({len(textures)}):")
    for tex in textures[:5]:  # Show first 5
        unreal.log(f"  - {tex}")
    if len(textures) > 5:
        unreal.log(f"  ... and {len(textures)-5} more")
    
    if other:
        unreal.log(f"\nOther ({len(other)}):")
        for o in other:
            unreal.log(f"  - {o}")
