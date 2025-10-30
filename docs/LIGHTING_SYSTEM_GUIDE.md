# Lighting System Usage Guide

This guide shows how to use the JSON-based lighting system for creating and managing lights in Unreal Engine workflows.

## Quick Start

### 1. Basic Light Creation

Create a simple workflow with lights:

```json
{
  "name": "Simple Lighting",
  "config": {
    "upsert_mode": true
  },
  "tasks": [
    {
      "name": "generate_lights",
      "type": "LightsGeneratorTask",
      "params": {
        "lights": [
          {
            "actor_id": "main_light",
            "light_type": "point",
            "location": [300, 0, 400],
            "intensity": 10000.0
          }
        ]
      }
    },
    {
      "name": "create_lights",
      "type": "ForEachLightTask",
      "params": {
        "lights_input": "generate_lights.lights"
      },
      "depends_on": ["generate_lights"]
    }
  ]
}
```

### 2. Load and Execute

```python
from unreallib.workflow import WorkflowLoader, WorkflowExecutor

# Load workflow
loader = WorkflowLoader()
workflow = loader.load('your_lighting_workflow.json')

# Execute
executor = WorkflowExecutor()
result = executor.execute(workflow)
```

## Available Example Workflows

### Studio Lighting (`lighting_studio.json`)
Professional three-point lighting setup with:
- Key light (warm, 12000 intensity)
- Fill light (cool, 6000 intensity)
- Rim light (spot, 10000 intensity)
- Two colored backdrop lights

**Use for**: Product visualization, character showcases, clean studio renders

### Outdoor Scene (`lighting_outdoor.json`)
Natural outdoor lighting with:
- Directional sun light (warm, 4.0 intensity)
- Sky ambient fill (cool, 0.8 intensity)
- Ground bounce light (earthy, 0.3 intensity)

**Use for**: Exterior scenes, landscapes, architectural visualization

### Interior Room (`lighting_room.json`)
Realistic room lighting with:
- Main ceiling light (10000 intensity)
- Four corner ceiling lights (6000 each)
- Table lamp (warm, 4000 intensity)
- Window light (spot, 15000 intensity)
- Accent spot light

**Use for**: Interior scenes, architectural interiors, room visualization

### Complete Scene (`complete_scene_with_lights.json`)
Full scene with actors, camera, and lighting:
- Spawns geometry
- Creates camera
- Sets up four-light system

**Use for**: Learning, testing, complete scene creation

## System Architecture

### Task Flow

```
LightsGeneratorTask (validates config)
         ↓
    [lights array]
         ↓
ForEachLightTask (creates lights)
         ↓
   CreateLightTask (primitive)
```

### Tasks

#### LightsGeneratorTask
**Purpose**: Parse and validate light configurations
**Input**: Array of light definitions
**Output**: Validated light configurations
**Use**: First step in lighting pipeline

#### ForEachLightTask  
**Purpose**: Iterate and create each light
**Input**: Reference to lights array (e.g., "generate_lights.lights")
**Output**: Created light actors
**Use**: Second step - actual light creation

#### CreateLightTask
**Purpose**: Create individual light actor (primitive task)
**Input**: Single light configuration
**Output**: Light actor
**Use**: Can be used standalone or via ForEachLightTask

## Common Patterns

### Pattern 1: Upsert Mode (Recommended)

Allows re-running workflows without duplicates:

```json
{
  "config": {
    "upsert_mode": true,
    "actor_id_prefix": "scene_"
  }
}
```

When you re-run the workflow, lights with matching `actor_id` values will be updated instead of creating new ones.

### Pattern 2: Default Values

Set defaults for all lights:

```json
{
  "name": "generate_lights",
  "type": "LightsGeneratorTask",
  "params": {
    "default_intensity": 8000.0,
    "default_color": [1.0, 0.9, 0.8],
    "default_rotation": [0, 0, 0],
    "lights": [
      // Lights without these properties inherit defaults
    ]
  }
}
```

### Pattern 3: Mixed Light Types

Combine different light types for complex setups:

```json
{
  "lights": [
    {
      "light_type": "directional",  // Sun
      "rotation": [-45, 135, 0],
      "intensity": 4.0
    },
    {
      "light_type": "point",  // Fill
      "location": [0, 0, 300],
      "intensity": 5000.0
    },
    {
      "light_type": "spot",  // Accent
      "location": [200, 0, 400],
      "rotation": [-45, 0, 0],
      "intensity": 10000.0
    }
  ]
}
```

### Pattern 4: Scene Composition

Combine lights with other tasks:

```json
{
  "tasks": [
    {"name": "spawn_objects", "type": "SpawnActorTask", ...},
    {"name": "create_camera", "type": "CreateCameraTask", ...},
    {"name": "generate_lights", "type": "LightsGeneratorTask", ...},
    {
      "name": "create_lights",
      "type": "ForEachLightTask",
      "depends_on": ["spawn_objects", "generate_lights"]
    }
  ]
}
```

## Configuration Reference

### Task Parameters

#### LightsGeneratorTask
```json
{
  "type": "LightsGeneratorTask",
  "params": {
    "lights": [],                    // Required: array of light configs
    "default_intensity": 5000.0,     // Optional: default intensity
    "default_color": [1.0, 1.0, 1.0], // Optional: default RGB color
    "default_rotation": [0, 0, 0]    // Optional: default rotation
  }
}
```

#### ForEachLightTask
```json
{
  "type": "ForEachLightTask",
  "params": {
    "lights_input": "task_name.lights", // Required: reference to lights
    "use_registry": true                 // Optional: enable upsert
  }
}
```

#### CreateLightTask (Direct)
```json
{
  "type": "CreateLightTask",
  "params": {
    "light_type": "point",              // Required: point/spot/directional
    "location": [0, 0, 300],            // Required: [x, y, z]
    "rotation": [0, 0, 0],              // Optional: [pitch, yaw, roll]
    "intensity": 5000.0,                // Optional: brightness
    "color": [1.0, 1.0, 1.0],           // Optional: [r, g, b]
    "actor_id": "my_light",             // Optional: for upsert
    "use_registry": true                 // Optional: enable upsert
  }
}
```

## Tips and Best Practices

### Intensity Values
- Start lower than you think - easier to increase
- Point lights: 5000-15000 for normal scenes
- Spot lights: 10000-30000 for focused effects
- Directional: 2.0-5.0 for outdoor scenes

### Color Temperature
- Warm (indoor/sunset): `[1.0, 0.9, 0.8]`
- Neutral: `[1.0, 1.0, 1.0]`
- Cool (outdoor/tech): `[0.8, 0.9, 1.0]`

### Positioning
- Key light: 45° up and to the side
- Fill light: Opposite side, lower intensity
- Rim light: Behind subject, pointing toward camera
- Always test from camera view

### Performance
- Fewer, stronger lights > many weak lights
- Use directional lights for primary outdoor lighting
- Enable shadows only on key lights
- Consider light radius/attenuation

### Workflow
1. Start with basic geometry and camera
2. Add one key light, adjust until good
3. Add fill light to soften shadows
4. Add rim/accent lights for depth
5. Iterate using upsert mode

## Troubleshooting

### Lights not appearing
- Check intensity values (might be too low)
- Verify location is in visible area
- Ensure light type is valid

### Scene too bright/dark
- Adjust intensity values (multiply/divide by 2)
- Check color values are 0.0-1.0
- Verify directional light intensity (should be 0.5-10.0)

### Lights creating duplicates
- Enable `upsert_mode` in config
- Ensure each light has unique `actor_id`
- Verify `use_registry: true` in ForEachLightTask

### Validation errors
- Check required fields: `light_type`, `location`
- Verify `light_type` is one of: point, spot, directional
- Ensure arrays have correct length (location: 3, color: 3)

## Advanced Usage

### Programmatic Light Generation

Create lights dynamically in Python:

```python
from unreallib.tasks.generators import LightsGeneratorTask, ForEachLightTask

# Define lights programmatically
lights_config = []
for i in range(4):
    lights_config.append({
        'actor_id': f'grid_light_{i}',
        'light_type': 'point',
        'location': [i * 200, 0, 300],
        'intensity': 8000.0
    })

# Create tasks
gen_task = LightsGeneratorTask('gen_lights', lights=lights_config)
create_task = ForEachLightTask('create_lights', lights_input='gen_lights.lights')
```

### Get JSON Schema

```python
from unreallib.tasks.generators import LightsGeneratorTask
import json

schema = LightsGeneratorTask.get_schema()
print(json.dumps(schema, indent=2))
```

## Examples Directory

Check these workflow files in `scripts/workflows/`:
- `lighting_studio.json` - Professional studio setup
- `lighting_outdoor.json` - Natural outdoor lighting
- `lighting_room.json` - Interior room lighting
- `complete_scene_with_lights.json` - Full scene example

## Next Steps

1. Read [LIGHT_CONFIGURATION_SCHEMA.md](LIGHT_CONFIGURATION_SCHEMA.md) for complete schema reference
2. Try the example workflows
3. Modify examples for your needs
4. Create custom lighting configurations
5. Combine with other workflow tasks

## API Reference

See full documentation:
- `LightsGeneratorTask` - [lights_generator_task.py](../unreallib/tasks/generators/lights_generator_task.py)
- `ForEachLightTask` - [for_each_light_task.py](../unreallib/tasks/generators/for_each_light_task.py)
- `CreateLightTask` - [create_light_task.py](../unreallib/tasks/primitives/create_light_task.py)
