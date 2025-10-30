# Lighting System - Implementation Summary

## Overview

A complete JSON-based lighting system for Unreal Engine workflows that allows you to define, validate, and create multiple lights through configuration files.

## What Was Created

### 1. Core Tasks

#### LightsGeneratorTask (`unreallib/tasks/generators/lights_generator_task.py`)
- **Purpose**: Parses and validates JSON light configurations
- **Features**:
  - Validates required fields (light_type, location)
  - Validates light types (point, spot, directional)
  - Supports default values for optional properties
  - Includes JSON schema specification
  - Comprehensive error handling

#### ForEachLightTask (`unreallib/tasks/generators/for_each_light_task.py`)
- **Purpose**: Creates multiple lights from validated configurations
- **Features**:
  - Iterates over light configurations
  - Creates each light using CreateLightTask
  - Supports upsert mode via actor registry
  - Reports success/failure for each light
  - Resolves context references

### 2. Documentation

#### LIGHT_CONFIGURATION_SCHEMA.md (`scripts/docs/`)
Complete schema reference including:
- Required and optional fields
- Light type descriptions (point, spot, directional)
- Color value guidelines and presets
- Intensity guidelines for each light type
- Coordinate system explanation
- Complete working examples (3-point lighting, outdoor, interior)
- Best practices

#### LIGHTING_SYSTEM_GUIDE.md (`scripts/docs/`)
User guide covering:
- Quick start examples
- System architecture explanation
- Common patterns and workflows
- Configuration reference
- Tips and best practices
- Troubleshooting guide
- Advanced usage examples

### 3. Example Workflows

#### lighting_studio.json
Professional studio setup with:
- Key light (warm, front-side)
- Fill light (cool, opposite side)
- Rim/back light (spot)
- Two colored backdrop lights

#### lighting_outdoor.json
Natural outdoor lighting with:
- Directional sun light
- Sky ambient fill
- Ground bounce light

#### lighting_room.json
Interior room lighting with:
- Main ceiling light
- Four corner lights
- Table lamp (warm)
- Window light (spot)
- Accent light

#### complete_scene_with_lights.json
Full scene demonstration with:
- Geometry spawning
- Camera creation
- Complete lighting setup

## JSON Configuration Structure

### Basic Structure
```json
{
  "tasks": [
    {
      "name": "generate_lights",
      "type": "LightsGeneratorTask",
      "params": {
        "lights": [...]
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

### Light Definition
```json
{
  "actor_id": "unique_id",           // Required for upsert
  "light_type": "point",             // Required: point/spot/directional
  "location": [x, y, z],             // Required: position
  "rotation": [pitch, yaw, roll],    // Optional: default [0,0,0]
  "intensity": 5000.0,               // Optional: default from task
  "color": [r, g, b],                // Optional: RGB 0.0-1.0
  "radius": 5000.0,                  // Optional: attenuation radius
  "cast_shadows": true,              // Optional: shadow casting
  "inner_cone_angle": 20.0,          // Optional: spot lights only
  "outer_cone_angle": 45.0           // Optional: spot lights only
}
```

## Usage Example

### In Python (within Unreal)
```python
from unreallib.workflow import WorkflowLoader, WorkflowExecutor

# Load lighting workflow
loader = WorkflowLoader()
workflow = loader.load('lighting_studio.json')

# Execute
executor = WorkflowExecutor()
result = executor.execute(workflow)

# Check results
if result.status == TaskStatus.SUCCESS:
    print("All lights created successfully!")
```

### Direct Task Usage
```python
from unreallib.tasks.generators import LightsGeneratorTask, ForEachLightTask

# Create tasks directly
lights_config = [
    {
        'actor_id': 'key_light',
        'light_type': 'point',
        'location': [300, 200, 400],
        'intensity': 10000.0,
        'color': [1.0, 0.9, 0.8]
    }
]

gen_task = LightsGeneratorTask('gen', lights=lights_config)
create_task = ForEachLightTask('create', lights_input='gen.lights')
```

## Key Features

### 1. Validation
- Required field checking
- Type validation
- Range validation (colors, angles)
- Descriptive error messages

### 2. Defaults
- Default intensity, color, rotation
- Per-task or per-light level
- Reduces configuration verbosity

### 3. Upsert Mode
- Update existing lights instead of creating duplicates
- Uses actor registry with unique IDs
- Perfect for iterative workflow development

### 4. Composability
- Works with other workflow tasks
- Can depend on actor spawning
- Integrates with camera and material tasks

### 5. Error Handling
- Individual light failures don't stop entire workflow
- Detailed success/failure reporting
- Partial success status when some lights fail

## Integration Points

### Task Registry
Tasks are registered in `unreallib/workflow/loader.py`:
```python
TASK_REGISTRY = {
    'LightsGeneratorTask': LightsGeneratorTask,
    'ForEachLightTask': ForEachLightTask,
    # ... other tasks
}
```

### Module Exports
Tasks are exported from:
- `unreallib/tasks/generators/__init__.py`
- `unreallib/tasks/__init__.py`

### Workflow System
- Compatible with WorkflowGraph
- Supports task dependencies
- Works with WorkflowExecutor

## Light Types Supported

### Point Light
Emits in all directions from a point
- Use for: General lighting, fill, ambient
- Key params: location, intensity, radius

### Spot Light
Emits in a cone from a point
- Use for: Focused lighting, dramatic effects
- Key params: location, rotation, intensity, cone angles

### Directional Light
Emits parallel rays (like sun)
- Use for: Outdoor/sun lighting, global illumination
- Key params: rotation, intensity, color
- Note: Location doesn't matter (rays are parallel)

## Best Practices

1. **Start Simple**: Begin with one light, iterate
2. **Use Upsert Mode**: Enable for workflow iteration
3. **Meaningful IDs**: Use descriptive actor_ids
4. **Layer Lights**: Multiple softer lights > one harsh light
5. **Test Intensity**: Start lower, increase as needed
6. **Color Temperature**: Match scene mood (warm/cool)
7. **Consider Performance**: Limit shadows, use directional for primary outdoor

## Testing

To test the system:
```python
# In Unreal Python console
import sys
sys.path.append(r'C:\Users\cwood\Documents\Unreal Projects\firstperson\scripts')

from unreallib.workflow import WorkflowLoader, WorkflowExecutor

loader = WorkflowLoader()
workflow = loader.load('lighting_studio')  # .json is optional
executor = WorkflowExecutor()
result = executor.execute(workflow)

print(f"Status: {result.status}")
print(f"Output: {result.output}")
```

## Files Created

```
scripts/
├── unreallib/
│   └── tasks/
│       └── generators/
│           ├── lights_generator_task.py     (NEW)
│           ├── for_each_light_task.py       (NEW)
│           └── __init__.py                  (UPDATED)
├── workflows/
│   ├── lighting_studio.json                 (NEW)
│   ├── lighting_outdoor.json                (NEW)
│   ├── lighting_room.json                   (NEW)
│   └── complete_scene_with_lights.json      (NEW)
└── docs/
    ├── LIGHT_CONFIGURATION_SCHEMA.md        (NEW)
    ├── LIGHTING_SYSTEM_GUIDE.md             (NEW)
    └── LIGHTING_SYSTEM_SUMMARY.md           (THIS FILE)
```

## Schema Access

Get the JSON schema programmatically:
```python
from unreallib.tasks.generators import LightsGeneratorTask
import json

schema = LightsGeneratorTask.get_schema()
print(json.dumps(schema, indent=2))
```

## Next Steps

1. **Test the examples**: Run the provided workflow files
2. **Create custom configs**: Modify examples for your needs
3. **Extend functionality**: Add more light properties (temperature, IES profiles, etc.)
4. **Build presets**: Create reusable lighting setups
5. **Integrate with scenes**: Combine with your existing workflows

## Support

See documentation:
- **Schema Reference**: `docs/LIGHT_CONFIGURATION_SCHEMA.md`
- **User Guide**: `docs/LIGHTING_SYSTEM_GUIDE.md`
- **Code**: `unreallib/tasks/generators/lights_generator_task.py`
