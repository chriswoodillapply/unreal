import unreal

# Create a simple test Blueprint
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
blueprint_factory = unreal.BlueprintFactory()
blueprint_factory.set_editor_property('parent_class', unreal.Actor)

bp_path = "/Game/TestBP"

# Delete if exists
if unreal.EditorAssetLibrary.does_asset_exist(bp_path):
    unreal.EditorAssetLibrary.delete_asset(bp_path)

# Create
blueprint = asset_tools.create_asset(
    asset_name="TestBP",
    package_path="/Game",
    asset_class=unreal.Blueprint,
    factory=blueprint_factory
)

unreal.log(f"Created Blueprint: {blueprint}")
unreal.log(f"Type: {type(blueprint)}")

# Save and reload
unreal.EditorAssetLibrary.save_loaded_asset(blueprint)
blueprint = unreal.EditorAssetLibrary.load_asset(bp_path)

unreal.log(f"\nReloaded Blueprint: {blueprint}")
unreal.log(f"Type: {type(blueprint)}")

# Check all attributes containing "script" or "construction"
unreal.log("\n=== Attributes containing 'script' or 'construction' ===")
for attr in dir(blueprint):
    if 'script' in attr.lower() or 'construction' in attr.lower():
        unreal.log(f"  {attr}")

# Try accessing SCS different ways
unreal.log("\n=== Trying to access SCS ===")

# Method 1: Direct attribute
try:
    scs = blueprint.simple_construction_script
    unreal.log(f"✓ Direct attribute worked: {scs}")
except AttributeError as e:
    unreal.log(f"✗ Direct attribute failed: {e}")

# Method 2: get_editor_property
try:
    scs = blueprint.get_editor_property("SimpleConstructionScript")
    unreal.log(f"✓ get_editor_property('SimpleConstructionScript') worked: {scs}")
except Exception as e:
    unreal.log(f"✗ get_editor_property('SimpleConstructionScript') failed: {e}")

# Method 3: Different casing
try:
    scs = blueprint.get_editor_property("simple_construction_script")
    unreal.log(f"✓ get_editor_property('simple_construction_script') worked: {scs}")
except Exception as e:
    unreal.log(f"✗ get_editor_property('simple_construction_script') failed: {e}")

unreal.log("\n=== Test complete ===")
