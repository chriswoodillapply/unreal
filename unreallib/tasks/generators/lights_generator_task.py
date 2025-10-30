"""
Generator task: Generate light configurations from JSON-like structure

This task takes a list of light configurations and outputs them for
iteration by ForEach tasks or for batch processing.
"""

from typing import Dict, Any, List
from unreallib.workflow.task import Task, TaskResult, TaskStatus


class LightsGeneratorTask(Task):
    """
    Generate light configurations from a structured definition
    
    This is a generator task that produces a list of light configurations
    that can be iterated over by primitive tasks. It doesn't create lights itself,
    it just parses and validates the light definitions.
    
    Example JSON structure:
        {
            "lights": [
                {
                    "actor_id": "key_light",
                    "light_type": "point",
                    "location": [300, 200, 400],
                    "rotation": [0, 0, 0],
                    "intensity": 10000.0,
                    "color": [1.0, 0.9, 0.8],
                    "radius": 5000.0,  # Optional: light attenuation radius
                    "cast_shadows": true  # Optional: whether light casts shadows
                }
            ]
        }
    """
    
    def __init__(
        self,
        name: str,
        lights: List[Dict[str, Any]] = None,
        default_intensity: float = 5000.0,
        default_color: tuple = (1.0, 1.0, 1.0),
        default_rotation: tuple = (0, 0, 0)
    ):
        """
        Initialize lights generator
        
        Args:
            name: Task name
            lights: List of light configuration dictionaries
            default_intensity: Default intensity for lights without specified intensity
            default_color: Default RGB color (0-1) for lights without specified color
            default_rotation: Default rotation for lights without specified rotation
        """
        super().__init__(
            name,
            lights=lights or [],
            default_intensity=default_intensity,
            default_color=default_color,
            default_rotation=default_rotation
        )
        
        self.lights = lights or []
        self.default_intensity = default_intensity
        self.default_color = default_color
        self.default_rotation = default_rotation
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Parse and validate light configurations"""
        
        if not self.lights:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': 'No lights defined'}
            )
        
        # Process each light configuration with defaults
        processed_lights = []
        
        for idx, light_config in enumerate(self.lights):
            # Validate required fields
            if 'light_type' not in light_config:
                return TaskResult(
                    status=TaskStatus.FAILURE,
                    output={'error': f'Light {idx} missing required field: light_type'}
                )
            
            if 'location' not in light_config:
                return TaskResult(
                    status=TaskStatus.FAILURE,
                    output={'error': f'Light {idx} missing required field: location'}
                )
            
            # Validate light type
            valid_types = ['point', 'spot', 'directional']
            if light_config['light_type'] not in valid_types:
                return TaskResult(
                    status=TaskStatus.FAILURE,
                    output={
                        'error': f'Light {idx} has invalid light_type: {light_config["light_type"]}. '
                                f'Must be one of: {", ".join(valid_types)}'
                    }
                )
            
            # Build complete light configuration with defaults
            processed_light = {
                'light_type': light_config['light_type'],
                'location': tuple(light_config['location']),
                'rotation': tuple(light_config.get('rotation', self.default_rotation)),
                'intensity': light_config.get('intensity', self.default_intensity),
                'color': tuple(light_config.get('color', self.default_color)),
                'actor_id': light_config.get('actor_id', f'light_{idx}'),
            }
            
            # Optional properties (for potential future use)
            if 'radius' in light_config:
                processed_light['radius'] = light_config['radius']
            
            if 'cast_shadows' in light_config:
                processed_light['cast_shadows'] = light_config['cast_shadows']
            
            if 'inner_cone_angle' in light_config:
                processed_light['inner_cone_angle'] = light_config['inner_cone_angle']
            
            if 'outer_cone_angle' in light_config:
                processed_light['outer_cone_angle'] = light_config['outer_cone_angle']
            
            processed_lights.append(processed_light)
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={
                'lights': processed_lights,
                'count': len(processed_lights)
            }
        )
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        """
        Get JSON schema for light configurations
        
        Returns:
            JSON schema dictionary describing the light configuration format
        """
        return {
            "type": "object",
            "properties": {
                "lights": {
                    "type": "array",
                    "description": "Array of light configurations",
                    "items": {
                        "type": "object",
                        "required": ["light_type", "location"],
                        "properties": {
                            "actor_id": {
                                "type": "string",
                                "description": "Unique identifier for the light (for upsert operations)"
                            },
                            "light_type": {
                                "type": "string",
                                "enum": ["point", "spot", "directional"],
                                "description": "Type of light to create"
                            },
                            "location": {
                                "type": "array",
                                "description": "3D position [x, y, z] in Unreal units",
                                "items": {"type": "number"},
                                "minItems": 3,
                                "maxItems": 3
                            },
                            "rotation": {
                                "type": "array",
                                "description": "Rotation [pitch, yaw, roll] in degrees",
                                "items": {"type": "number"},
                                "minItems": 3,
                                "maxItems": 3
                            },
                            "intensity": {
                                "type": "number",
                                "description": "Light intensity (brightness)",
                                "minimum": 0
                            },
                            "color": {
                                "type": "array",
                                "description": "RGB color values [r, g, b] from 0.0 to 1.0",
                                "items": {
                                    "type": "number",
                                    "minimum": 0.0,
                                    "maximum": 1.0
                                },
                                "minItems": 3,
                                "maxItems": 3
                            },
                            "radius": {
                                "type": "number",
                                "description": "Light attenuation radius (optional)",
                                "minimum": 0
                            },
                            "cast_shadows": {
                                "type": "boolean",
                                "description": "Whether the light casts shadows (optional)"
                            },
                            "inner_cone_angle": {
                                "type": "number",
                                "description": "Inner cone angle for spot lights (degrees, optional)",
                                "minimum": 0,
                                "maximum": 90
                            },
                            "outer_cone_angle": {
                                "type": "number",
                                "description": "Outer cone angle for spot lights (degrees, optional)",
                                "minimum": 0,
                                "maximum": 90
                            }
                        }
                    }
                }
            }
        }
