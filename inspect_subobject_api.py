"""Inspect SubobjectDataSubsystem API to understand object signatures"""
import unreal

# Create a test Blueprint to inspect the API
print("=" * 60)
print("INSPECTING SubobjectDataSubsystem API")
print("=" * 60)

# Get subsystem
subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
print(f"\n1. SubobjectDataSubsystem: {type(subsystem)}")
print(f"   Methods: {[m for m in dir(subsystem) if not m.startswith('_')]}")

# Try to load an existing Blueprint to inspect
bp_path = "/Game/Imported/teal_chair_Blueprint"
if unreal.EditorAssetLibrary.does_asset_exist(bp_path):
    bp = unreal.EditorAssetLibrary.load_asset(bp_path)
    print(f"\n2. Loaded Blueprint: {bp.get_name()}")
    
    # Call k2_gather_subobject_data_for_blueprint
    result = subsystem.k2_gather_subobject_data_for_blueprint(bp)
    print(f"\n3. k2_gather_subobject_data_for_blueprint result:")
    print(f"   Type: {type(result)}")
    print(f"   Value: {result}")
    
    # Try to inspect what it contains
    if hasattr(result, '__len__'):
        print(f"   Length: {len(result)}")
        if len(result) > 0:
            print(f"   First element type: {type(result[0])}")
            print(f"   First element: {result[0]}")
    
    # Check for common attributes
    for attr in ['handle', 'handles', 'data', 'get_handle', 'get_data']:
        if hasattr(result, attr):
            val = getattr(result, attr)
            print(f"   Has attribute '{attr}': {type(val)} = {val}")
    
    # List all non-private attributes
    attrs = [a for a in dir(result) if not a.startswith('_')]
    print(f"   All attributes: {attrs}")
    
    # Try calling methods if any
    for attr in attrs:
        val = getattr(result, attr)
        if callable(val):
            print(f"   Method: {attr}()")
else:
    print(f"\nBlueprint not found at: {bp_path}")
    print("Please create a Blueprint first or update the path")

# Check AddNewSubobjectParams
print(f"\n4. AddNewSubobjectParams:")
params = unreal.AddNewSubobjectParams()
params_attrs = [a for a in dir(params) if not a.startswith('_')]
print(f"   Attributes: {params_attrs}")

# Check what properties it has
for attr in ['parent_handle', 'new_class', 'blueprint_context']:
    if hasattr(params, attr):
        print(f"   Has property: {attr}")

print("\n" + "=" * 60)
print("API INSPECTION COMPLETE")
print("=" * 60)
