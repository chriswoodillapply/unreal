import unreal

# Create a test Blueprint to inspect its properties
bp_path = "/Game/Imported/teal_chair_Blueprint"

# Check if it exists, if not create one
if not unreal.EditorAssetLibrary.does_asset_exist(bp_path):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    blueprint_factory = unreal.BlueprintFactory()
    blueprint_factory.set_editor_property('parent_class', unreal.Actor)
    
    bp = asset_tools.create_asset(
        asset_name="teal_chair_Blueprint",
        package_path="/Game/Imported",
        asset_class=unreal.Blueprint,
        factory=blueprint_factory
    )
else:
    bp = unreal.EditorAssetLibrary.load_asset(bp_path)

unreal.log(f"Blueprint type: {type(bp)}")
unreal.log(f"Blueprint class: {bp.__class__.__name__}")

# Try different ways to access SCS
unreal.log("\n=== Trying different access methods ===")

# Method 1: Direct attribute
try:
    scs = bp.simple_construction_script
    unreal.log(f"✓ Direct attribute worked: {type(scs)}")
except AttributeError as e:
    unreal.log(f"✗ Direct attribute failed: {e}")

# Method 2: get_editor_property
try:
    scs = bp.get_editor_property("simple_construction_script")
    unreal.log(f"✓ get_editor_property worked: {type(scs)}")
except Exception as e:
    unreal.log(f"✗ get_editor_property failed: {e}")

# Method 3: Check all available properties
unreal.log("\n=== Available properties containing 'script' or 'construction' ===")
try:
    for prop_name in dir(bp):
        prop_lower = prop_name.lower()
        if 'script' in prop_lower or 'construction' in prop_lower or 'scs' in prop_lower:
            unreal.log(f"  - {prop_name}")
except Exception as e:
    unreal.log(f"Error listing properties: {e}")

unreal.log("\n=== Checking Blueprint generated class ===")
try:
    bp_class = bp.generated_class()
    unreal.log(f"Generated class: {bp_class}")
    if bp_class:
        cdo = unreal.get_default_object(bp_class)
        unreal.log(f"CDO: {cdo}")
except Exception as e:
    unreal.log(f"Error getting generated class: {e}")
