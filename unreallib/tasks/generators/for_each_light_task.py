"""
Composite task: Create multiple lights from generator output

This task iterates over light configurations produced by a generator
and creates each light using the primitive CreateLightTask.
"""

from typing import Dict, Any
from unreallib.workflow.task import Task, TaskResult, TaskStatus
from unreallib.tasks.primitives.create_light_task import CreateLightTask


class ForEachLightTask(Task):
    """
    Create multiple lights by iterating over light configurations
    
    This is a composite task that takes a collection of light configurations
    (typically from LightsGeneratorTask) and creates each light individually.
    
    Example workflow usage:
        {
            "name": "generate_lights",
            "type": "LightsGeneratorTask",
            "params": {
                "lights": [...]
            }
        },
        {
            "name": "create_all_lights",
            "type": "ForEachLightTask",
            "params": {
                "lights_input": "generate_lights.lights"
            },
            "depends_on": ["generate_lights"]
        }
    """
    
    def __init__(
        self,
        name: str,
        lights_input: str = None,
        use_registry: bool = True
    ):
        """
        Initialize for each light task
        
        Args:
            name: Task name
            lights_input: Reference to lights array from context (e.g., "generate_lights.lights")
            use_registry: Whether to use actor registry for upsert operations
        """
        super().__init__(
            name,
            lights_input=lights_input,
            use_registry=use_registry
        )
        
        self.lights_input = lights_input
        self.use_registry = use_registry
    
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """Execute light creation for each light configuration"""
        
        # Get lights from context
        lights = self._resolve_input(context, self.lights_input)
        
        if not lights:
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': f'No lights found at input: {self.lights_input}'}
            )
        
        if not isinstance(lights, list):
            return TaskResult(
                status=TaskStatus.FAILURE,
                output={'error': f'Lights input must be a list, got: {type(lights).__name__}'}
            )
        
        # Create each light
        created_lights = []
        failed_lights = []
        
        for idx, light_config in enumerate(lights):
            try:
                # Create CreateLightTask for this light
                light_task = CreateLightTask(
                    name=f"{self.name}_light_{idx}",
                    light_type=light_config.get('light_type', 'point'),
                    location=light_config.get('location', (0, 0, 300)),
                    rotation=light_config.get('rotation', (0, 0, 0)),
                    intensity=light_config.get('intensity', 5000.0),
                    color=light_config.get('color', (1.0, 1.0, 1.0)),
                    actor_id=light_config.get('actor_id'),
                    use_registry=self.use_registry
                )
                
                # Execute the light creation
                result = light_task.execute(context)
                
                if result.status == TaskStatus.SUCCESS:
                    created_lights.append({
                        'actor_id': light_config.get('actor_id'),
                        'light_type': light_config.get('light_type'),
                        'location': light_config.get('location'),
                        'action': result.output.get('action', 'created')
                    })
                else:
                    failed_lights.append({
                        'actor_id': light_config.get('actor_id'),
                        'error': result.output.get('error', 'Unknown error')
                    })
            
            except Exception as e:
                failed_lights.append({
                    'actor_id': light_config.get('actor_id', f'light_{idx}'),
                    'error': str(e)
                })
        
        # Determine overall status
        if failed_lights and not created_lights:
            status = TaskStatus.FAILURE
        elif failed_lights:
            status = TaskStatus.PARTIAL_SUCCESS
        else:
            status = TaskStatus.SUCCESS
        
        return TaskResult(
            status=status,
            output={
                'created_lights': created_lights,
                'failed_lights': failed_lights,
                'total_attempted': len(lights),
                'successful': len(created_lights),
                'failed': len(failed_lights)
            }
        )
    
    def _resolve_input(self, context: Dict[str, Any], input_ref: str) -> Any:
        """
        Resolve an input reference from context
        
        Args:
            context: Execution context
            input_ref: Reference string (e.g., "task_name.output_key")
        
        Returns:
            Resolved value from context
        """
        if not input_ref:
            return None
        
        # Handle direct context keys
        if input_ref in context:
            return context[input_ref]
        
        # Handle dotted references (e.g., "task_name.lights")
        parts = input_ref.split('.')
        
        # Check if this is a task output reference
        if len(parts) >= 2:
            task_name = parts[0]
            # Look for task output in context
            if task_name in context:
                value = context[task_name]
                # Navigate through remaining parts
                for part in parts[1:]:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        return None
                return value
        
        return None
