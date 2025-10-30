"""
Simple test script to verify lighting system works in Unreal
Run this from Unreal's Python console or copy-paste it
"""

# This will work when run directly in Unreal's Python console
import unreal

print("\n" + "="*60)
print("TESTING LIGHTING SYSTEM")
print("="*60)

# Test 1: Create a single point light
print("\nTest 1: Creating a simple point light...")
try:
    light_class = unreal.PointLight.static_class()
    light = unreal.EditorLevelLibrary.spawn_actor_from_class(
        light_class,
        unreal.Vector(300, 0, 400),
        unreal.Rotator(0, 0, 0)
    )
    
    # Configure it
    light_component = light.get_component_by_class(unreal.LightComponent)
    if light_component:
        light_component.set_editor_property('intensity', 10000.0)
        color = unreal.LinearColor(1.0, 0.9, 0.8, 1.0)
        light_component.set_light_color(color)
    
    light.set_actor_label("test_simple_light")
    print(f"✓ Created light at {light.get_actor_location()}")
    print(f"  Intensity: {light_component.get_editor_property('intensity')}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 2: Create different light types
print("\nTest 2: Creating different light types...")
light_types = {
    'point': unreal.PointLight,
    'spot': unreal.SpotLight,
    'directional': unreal.DirectionalLight
}

for idx, (name, light_cls) in enumerate(light_types.items()):
    try:
        light = unreal.EditorLevelLibrary.spawn_actor_from_class(
            light_cls.static_class(),
            unreal.Vector(idx * 200, 200, 300),
            unreal.Rotator(-45, 0, 0)
        )
        light.set_actor_label(f"test_{name}_light")
        print(f"  ✓ Created {name} light")
    except Exception as e:
        print(f"  ✗ Failed to create {name} light: {e}")

print("\n" + "="*60)
print("BASIC LIGHTING TEST COMPLETE")
print("Check your viewport for the test lights!")
print("="*60)
