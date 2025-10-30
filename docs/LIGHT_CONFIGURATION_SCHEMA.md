# Light Configuration JSON Schema

This document describes the JSON schema for configuring lights in the Unreal workflow system.

## Overview

The lighting system supports creating multiple lights with various properties through a JSON-based configuration. The system uses two tasks:

1. **LightsGeneratorTask** - Parses and validates light configurations
2. **ForEachLightTask** - Creates the actual light actors from the configurations

## Basic Structure

```json
{
  "name": "Lighting Setup",
  "description": "Create scene lighting",
  "config": {
    "upsert_mode": true,
    "actor_id_prefix": "scene_"
  },
  "tasks": [
    {
      "name": "generate_lights",
      "type": "LightsGeneratorTask",
      "params": {
        "lights": [
          // Light configurations here
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

## Light Configuration Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `light_type` | string | Type of light: `"point"`, `"spot"`, or `"directional"` |
| `location` | array[3] | 3D position `[x, y, z]` in Unreal units (cm) |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `actor_id` | string | `"light_{index}"` | Unique identifier for upsert operations |
| `rotation` | array[3] | `[0, 0, 0]` | Rotation `[pitch, yaw, roll]` in degrees |
| `intensity` | number | `5000.0` | Light brightness/intensity |
| `color` | array[3] | `[1.0, 1.0, 1.0]` | RGB color values (0.0 to 1.0) |
| `radius` | number | - | Light attenuation radius (optional) |
| `cast_shadows` | boolean | - | Whether light casts shadows (optional) |
| `inner_cone_angle` | number | - | Inner cone angle for spot lights (degrees, 0-90) |
| `outer_cone_angle` | number | - | Outer cone angle for spot lights (degrees, 0-90) |

## Light Types

### Point Light
A light that emits in all directions from a single point.

```json
{
  "actor_id": "key_light",
  "light_type": "point",
  "location": [300, 200, 400],
  "intensity": 10000.0,
  "color": [1.0, 0.9, 0.8]
}
```

**Common uses**: General lighting, ambient fill, decorative lights

### Spot Light
A light that emits in a cone from a point, like a flashlight or stage light.

```json
{
  "actor_id": "spotlight",
  "light_type": "spot",
  "location": [0, 0, 500],
  "rotation": [-90, 0, 0],
  "intensity": 15000.0,
  "color": [1.0, 1.0, 1.0],
  "inner_cone_angle": 20.0,
  "outer_cone_angle": 45.0
}
```

**Common uses**: Focused lighting, dramatic effects, stage lighting

### Directional Light
A light that emits parallel rays in one direction, like the sun.

```json
{
  "actor_id": "sun",
  "light_type": "directional",
  "location": [0, 0, 0],
  "rotation": [-45, 45, 0],
  "intensity": 3.0,
  "color": [1.0, 0.95, 0.8]
}
```

**Common uses**: Sun/moon lighting, outdoor scenes, primary directional lighting

## Color Values

Colors are specified as RGB arrays with values from 0.0 to 1.0:

```json
"color": [1.0, 1.0, 1.0]  // White
"color": [1.0, 0.0, 0.0]  // Red
"color": [0.0, 0.5, 1.0]  // Light blue
"color": [1.0, 0.9, 0.8]  // Warm white
"color": [0.6, 0.7, 1.0]  // Cool blue
```

### Common Color Presets

| Color | RGB | Description |
|-------|-----|-------------|
| Warm White | `[1.0, 0.9, 0.8]` | Tungsten/incandescent |
| Neutral White | `[1.0, 1.0, 1.0]` | Pure white |
| Cool White | `[0.8, 0.9, 1.0]` | Daylight |
| Golden Hour | `[1.0, 0.7, 0.4]` | Sunset/sunrise |
| Moonlight | `[0.6, 0.7, 1.0]` | Blue night light |

## Intensity Guidelines

Intensity values vary widely based on light type and desired effect:

### Point Lights
- Subtle accent: `1000 - 3000`
- Standard lighting: `5000 - 10000`
- Bright key light: `10000 - 20000`
- Dramatic/special: `20000+`

### Spot Lights
- Focused accent: `5000 - 10000`
- Stage/dramatic: `15000 - 30000`
- Search light: `50000+`

### Directional Lights
- Overcast: `0.5 - 1.5`
- Daylight: `2.0 - 5.0`
- Bright sun: `5.0 - 10.0`

## Complete Examples

### Three-Point Lighting Setup

```json
{
  "name": "Three Point Lighting",
  "type": "LightsGeneratorTask",
  "params": {
    "lights": [
      {
        "actor_id": "key_light",
        "light_type": "point",
        "location": [400, 300, 400],
        "intensity": 12000.0,
        "color": [1.0, 0.9, 0.8]
      },
      {
        "actor_id": "fill_light",
        "light_type": "point",
        "location": [-300, -200, 300],
        "intensity": 6000.0,
        "color": [0.6, 0.7, 1.0]
      },
      {
        "actor_id": "rim_light",
        "light_type": "spot",
        "location": [-200, 400, 200],
        "rotation": [0, -135, 0],
        "intensity": 8000.0,
        "color": [1.0, 1.0, 1.0],
        "inner_cone_angle": 15.0,
        "outer_cone_angle": 35.0
      }
    ]
  }
}
```

### Outdoor Scene Lighting

```json
{
  "name": "Outdoor Lighting",
  "type": "LightsGeneratorTask",
  "params": {
    "lights": [
      {
        "actor_id": "sun",
        "light_type": "directional",
        "location": [0, 0, 0],
        "rotation": [-45, 135, 0],
        "intensity": 4.0,
        "color": [1.0, 0.95, 0.85],
        "cast_shadows": true
      },
      {
        "actor_id": "sky_fill",
        "light_type": "directional",
        "location": [0, 0, 0],
        "rotation": [45, 0, 0],
        "intensity": 0.5,
        "color": [0.5, 0.6, 0.8]
      }
    ]
  }
}
```

### Interior Room Lighting

```json
{
  "name": "Room Lighting",
  "type": "LightsGeneratorTask",
  "params": {
    "default_intensity": 5000.0,
    "default_color": [1.0, 0.9, 0.8],
    "lights": [
      {
        "actor_id": "ceiling_light_1",
        "light_type": "point",
        "location": [200, 200, 300],
        "intensity": 8000.0
      },
      {
        "actor_id": "ceiling_light_2",
        "light_type": "point",
        "location": [-200, 200, 300],
        "intensity": 8000.0
      },
      {
        "actor_id": "table_lamp",
        "light_type": "point",
        "location": [150, -100, 120],
        "intensity": 4000.0,
        "color": [1.0, 0.8, 0.6]
      },
      {
        "actor_id": "window_light",
        "light_type": "spot",
        "location": [0, 500, 200],
        "rotation": [0, -90, 0],
        "intensity": 15000.0,
        "color": [0.9, 0.95, 1.0],
        "outer_cone_angle": 60.0
      }
    ]
  }
}
```

## Default Values

The `LightsGeneratorTask` supports default values for optional properties:

```json
{
  "name": "generate_lights",
  "type": "LightsGeneratorTask",
  "params": {
    "default_intensity": 5000.0,
    "default_color": [1.0, 1.0, 1.0],
    "default_rotation": [0, 0, 0],
    "lights": [
      // Lights without these properties will use the defaults
    ]
  }
}
```

## Coordinate System

Unreal Engine uses a left-handed Z-up coordinate system:

- **X**: Forward (red axis)
- **Y**: Right (green axis)  
- **Z**: Up (blue axis)

### Rotation
- **Pitch**: Rotation around Y axis (up/down)
- **Yaw**: Rotation around Z axis (left/right)
- **Roll**: Rotation around X axis (tilt)

All rotation values are in degrees.

## Upsert Mode

When `upsert_mode` is enabled in the workflow config, lights with the same `actor_id` will be updated instead of creating duplicates:

```json
{
  "config": {
    "upsert_mode": true,
    "actor_id_prefix": "scene_"
  }
}
```

This is useful for:
- Iterating on lighting setups
- Re-running workflows without manual cleanup
- Updating specific lights without affecting others

## Error Handling

The system validates:
- Required fields (`light_type`, `location`)
- Valid light types (`point`, `spot`, `directional`)
- Array lengths (location and color must have 3 values)
- Valid value ranges (colors 0-1, angles 0-90)

Failed lights are reported in the task output without stopping the entire workflow.

## Best Practices

1. **Use meaningful actor_ids**: Makes debugging and updating easier
2. **Start with lower intensities**: Easier to increase than fix overexposed scenes
3. **Use color temperature**: Warm for indoor/sunset, cool for outdoor/tech
4. **Layer lights**: Multiple softer lights often look better than one harsh light
5. **Consider shadows**: Enable `cast_shadows` only on key lights for performance
6. **Test iteratively**: Use upsert mode to quickly refine lighting setups

## Programmatic Access

Get the JSON schema programmatically:

```python
from unreallib.tasks.generators import LightsGeneratorTask

schema = LightsGeneratorTask.get_schema()
print(json.dumps(schema, indent=2))
```
