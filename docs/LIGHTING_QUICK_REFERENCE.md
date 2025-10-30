# Lighting System Quick Reference

## Minimal Example

```json
{
  "name": "My Lights",
  "config": {"upsert_mode": true},
  "tasks": [
    {
      "name": "gen",
      "type": "LightsGeneratorTask",
      "params": {
        "lights": [
          {
            "actor_id": "light1",
            "light_type": "point",
            "location": [300, 0, 400],
            "intensity": 10000.0
          }
        ]
      }
    },
    {
      "name": "create",
      "type": "ForEachLightTask",
      "params": {"lights_input": "gen.lights"},
      "depends_on": ["gen"]
    }
  ]
}
```

## Light Types

| Type | Use Case | Key Properties |
|------|----------|----------------|
| `point` | General, fill, ambient | location, intensity, radius |
| `spot` | Focused, dramatic | location, rotation, cone angles |
| `directional` | Sun, outdoor | rotation, intensity (location ignored) |

## Common Intensities

| Light Type | Subtle | Normal | Bright | Dramatic |
|------------|--------|--------|--------|----------|
| Point | 1K-3K | 5K-10K | 10K-20K | 20K+ |
| Spot | 5K-10K | 15K-30K | 30K-50K | 50K+ |
| Directional | 0.5-1.5 | 2.0-5.0 | 5.0-10.0 | 10.0+ |

## Color Presets

```json
// Warm (indoor, sunset)
"color": [1.0, 0.9, 0.8]

// Neutral white
"color": [1.0, 1.0, 1.0]

// Cool (outdoor, tech)
"color": [0.8, 0.9, 1.0]

// Golden hour
"color": [1.0, 0.7, 0.4]

// Moonlight
"color": [0.6, 0.7, 1.0]
```

## Required vs Optional

### Required
- `light_type`: "point" | "spot" | "directional"
- `location`: [x, y, z]

### Optional (with defaults)
- `actor_id`: "light_0", "light_1", ...
- `rotation`: [0, 0, 0]
- `intensity`: 5000.0 (or task default)
- `color`: [1.0, 1.0, 1.0] (or task default)

## Task Parameters

### LightsGeneratorTask
```json
{
  "type": "LightsGeneratorTask",
  "params": {
    "lights": [],                      // REQUIRED
    "default_intensity": 5000.0,       // optional
    "default_color": [1.0, 1.0, 1.0],  // optional
    "default_rotation": [0, 0, 0]      // optional
  }
}
```

### ForEachLightTask
```json
{
  "type": "ForEachLightTask",
  "params": {
    "lights_input": "task_name.lights", // REQUIRED
    "use_registry": true                 // optional (default: true)
  }
}
```

## Three-Point Lighting Template

```json
{
  "lights": [
    {
      "actor_id": "key",
      "light_type": "point",
      "location": [400, 300, 400],
      "intensity": 12000.0,
      "color": [1.0, 0.9, 0.8]
    },
    {
      "actor_id": "fill",
      "light_type": "point",
      "location": [-300, -200, 300],
      "intensity": 6000.0,
      "color": [0.6, 0.7, 1.0]
    },
    {
      "actor_id": "rim",
      "light_type": "spot",
      "location": [-200, 400, 200],
      "rotation": [0, -135, 0],
      "intensity": 10000.0
    }
  ]
}
```

## Python Usage

```python
from unreallib.workflow import WorkflowLoader, WorkflowExecutor

loader = WorkflowLoader()
workflow = loader.load('my_lights')  # .json optional
executor = WorkflowExecutor()
result = executor.execute(workflow)
```

## Coordinate System

```
Z (up)
↑
|
|___Y (right)
 \
  \
   X (forward)
```

## Common Patterns

### Outdoor Scene
```json
{
  "light_type": "directional",
  "rotation": [-45, 135, 0],  // Sun angle
  "intensity": 4.0,
  "color": [1.0, 0.95, 0.85]
}
```

### Ceiling Light
```json
{
  "light_type": "point",
  "location": [0, 0, 300],
  "intensity": 8000.0,
  "radius": 800.0
}
```

### Window Light
```json
{
  "light_type": "spot",
  "location": [0, 500, 200],
  "rotation": [0, -90, 0],
  "intensity": 15000.0,
  "outer_cone_angle": 60.0
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Too bright | Divide intensity by 2 |
| Too dark | Multiply intensity by 2 |
| Duplicates | Enable `upsert_mode`, add `actor_id` |
| Not visible | Check location, increase intensity |
| Wrong direction | Adjust rotation (spot/directional) |

## Example Workflows

Located in `scripts/workflows/`:
- `lighting_studio.json` - Studio setup
- `lighting_outdoor.json` - Outdoor scene
- `lighting_room.json` - Interior room
- `complete_scene_with_lights.json` - Full scene

## Full Documentation

- Schema: `docs/LIGHT_CONFIGURATION_SCHEMA.md`
- Guide: `docs/LIGHTING_SYSTEM_GUIDE.md`
- Summary: `docs/LIGHTING_SYSTEM_SUMMARY.md`
