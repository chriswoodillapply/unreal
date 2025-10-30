"""
Tests for Lighting System - LightsGeneratorTask and ForEachLightTask
"""

import sys
from unittest.mock import Mock, MagicMock, patch

# Mock unreal module before imports
sys.modules['unreal'] = MagicMock()

import pytest
from unreallib.tasks.generators import LightsGeneratorTask, ForEachLightTask
from unreallib.workflow.task import TaskStatus


class TestLightsGeneratorTask:
    """Test LightsGeneratorTask - JSON light configuration parsing and validation"""
    
    def test_generator_creation(self):
        """Test creating a lights generator task"""
        task = LightsGeneratorTask('test_gen', lights=[])
        assert task.name == 'test_gen'
        assert task.lights == []
    
    def test_generator_with_single_light(self):
        """Test generating a single light configuration"""
        lights = [
            {
                'light_type': 'point',
                'location': [100, 200, 300]
            }
        ]
        
        task = LightsGeneratorTask('gen', lights=lights)
        result = task.execute({})
        
        assert result.status == TaskStatus.SUCCESS
        assert len(result.output['lights']) == 1
        assert result.output['count'] == 1
        
        light = result.output['lights'][0]
        assert light['light_type'] == 'point'
        assert light['location'] == (100, 200, 300)
        assert light['actor_id'] == 'light_0'  # Default ID
    
    def test_generator_with_multiple_lights(self):
        """Test generating multiple light configurations"""
        lights = [
            {'light_type': 'point', 'location': [0, 0, 300]},
            {'light_type': 'spot', 'location': [100, 0, 400]},
            {'light_type': 'directional', 'location': [0, 0, 0]}
        ]
        
        task = LightsGeneratorTask('gen', lights=lights)
        result = task.execute({})
        
        assert result.status == TaskStatus.SUCCESS
        assert len(result.output['lights']) == 3
        assert result.output['count'] == 3
    
    def test_generator_applies_defaults(self):
        """Test that generator applies default values"""
        lights = [
            {'light_type': 'point', 'location': [0, 0, 300]}
        ]
        
        task = LightsGeneratorTask(
            'gen',
            lights=lights,
            default_intensity=8000.0,
            default_color=(1.0, 0.9, 0.8),
            default_rotation=(-45, 0, 0)
        )
        result = task.execute({})
        
        light = result.output['lights'][0]
        assert light['intensity'] == 8000.0
        assert light['color'] == (1.0, 0.9, 0.8)
        assert light['rotation'] == (-45, 0, 0)
    
    def test_generator_light_overrides_defaults(self):
        """Test that light-specific values override defaults"""
        lights = [
            {
                'light_type': 'point',
                'location': [0, 0, 300],
                'intensity': 12000.0,
                'color': [1.0, 0.0, 0.0]
            }
        ]
        
        task = LightsGeneratorTask(
            'gen',
            lights=lights,
            default_intensity=5000.0,
            default_color=(1.0, 1.0, 1.0)
        )
        result = task.execute({})
        
        light = result.output['lights'][0]
        assert light['intensity'] == 12000.0
        assert light['color'] == (1.0, 0.0, 0.0)
    
    def test_generator_custom_actor_id(self):
        """Test that custom actor_id is preserved"""
        lights = [
            {
                'light_type': 'point',
                'location': [0, 0, 300],
                'actor_id': 'key_light'
            }
        ]
        
        task = LightsGeneratorTask('gen', lights=lights)
        result = task.execute({})
        
        assert result.output['lights'][0]['actor_id'] == 'key_light'
    
    def test_generator_optional_properties(self):
        """Test that optional properties are included"""
        lights = [
            {
                'light_type': 'spot',
                'location': [0, 0, 400],
                'radius': 5000.0,
                'cast_shadows': True,
                'inner_cone_angle': 20.0,
                'outer_cone_angle': 45.0
            }
        ]
        
        task = LightsGeneratorTask('gen', lights=lights)
        result = task.execute({})
        
        light = result.output['lights'][0]
        assert light['radius'] == 5000.0
        assert light['cast_shadows'] is True
        assert light['inner_cone_angle'] == 20.0
        assert light['outer_cone_angle'] == 45.0
    
    def test_generator_fails_without_lights(self):
        """Test that generator fails when no lights provided"""
        task = LightsGeneratorTask('gen', lights=[])
        result = task.execute({})
        
        assert result.status == TaskStatus.FAILURE
        assert 'error' in result.output
    
    def test_generator_fails_missing_light_type(self):
        """Test that generator fails when light_type is missing"""
        lights = [
            {'location': [0, 0, 300]}  # Missing light_type
        ]
        
        task = LightsGeneratorTask('gen', lights=lights)
        result = task.execute({})
        
        assert result.status == TaskStatus.FAILURE
        assert 'light_type' in result.output['error']
    
    def test_generator_fails_missing_location(self):
        """Test that generator fails when location is missing"""
        lights = [
            {'light_type': 'point'}  # Missing location
        ]
        
        task = LightsGeneratorTask('gen', lights=lights)
        result = task.execute({})
        
        assert result.status == TaskStatus.FAILURE
        assert 'location' in result.output['error']
    
    def test_generator_fails_invalid_light_type(self):
        """Test that generator fails with invalid light type"""
        lights = [
            {
                'light_type': 'invalid_type',
                'location': [0, 0, 300]
            }
        ]
        
        task = LightsGeneratorTask('gen', lights=lights)
        result = task.execute({})
        
        assert result.status == TaskStatus.FAILURE
        assert 'invalid light_type' in result.output['error']
    
    def test_generator_converts_lists_to_tuples(self):
        """Test that lists are converted to tuples"""
        lights = [
            {
                'light_type': 'point',
                'location': [100, 200, 300],
                'rotation': [45, 90, 0],
                'color': [1.0, 0.5, 0.0]
            }
        ]
        
        task = LightsGeneratorTask('gen', lights=lights)
        result = task.execute({})
        
        light = result.output['lights'][0]
        assert isinstance(light['location'], tuple)
        assert isinstance(light['rotation'], tuple)
        assert isinstance(light['color'], tuple)
    
    def test_get_schema(self):
        """Test that JSON schema is available"""
        schema = LightsGeneratorTask.get_schema()
        
        assert 'type' in schema
        assert 'properties' in schema
        assert 'lights' in schema['properties']


class TestForEachLightTask:
    """Test ForEachLightTask - Creates lights from generator output"""
    
    @patch('unreallib.tasks.generators.for_each_light_task.CreateLightTask')
    def test_foreach_creates_single_light(self, mock_create_task_class):
        """Test creating a single light"""
        # Setup mock
        mock_task_instance = Mock()
        mock_result = Mock()
        mock_result.status = TaskStatus.SUCCESS
        mock_result.output = {'action': 'created', 'light_type': 'point'}
        mock_task_instance.execute.return_value = mock_result
        mock_create_task_class.return_value = mock_task_instance
        
        # Create task
        lights = [
            {
                'light_type': 'point',
                'location': (0, 0, 300),
                'rotation': (0, 0, 0),
                'intensity': 5000.0,
                'color': (1.0, 1.0, 1.0),
                'actor_id': 'light_0'
            }
        ]
        
        context = {'test_lights': lights}
        task = ForEachLightTask('foreach', lights_input='test_lights')
        result = task.execute(context)
        
        assert result.status == TaskStatus.SUCCESS
        assert result.output['successful'] == 1
        assert result.output['failed'] == 0
        assert len(result.output['created_lights']) == 1
    
    @patch('unreallib.tasks.generators.for_each_light_task.CreateLightTask')
    def test_foreach_creates_multiple_lights(self, mock_create_task_class):
        """Test creating multiple lights"""
        # Setup mock
        mock_task_instance = Mock()
        mock_result = Mock()
        mock_result.status = TaskStatus.SUCCESS
        mock_result.output = {'action': 'created'}
        mock_task_instance.execute.return_value = mock_result
        mock_create_task_class.return_value = mock_task_instance
        
        # Create task with multiple lights
        lights = [
            {'light_type': 'point', 'location': (0, 0, 300), 'rotation': (0, 0, 0),
             'intensity': 5000.0, 'color': (1.0, 1.0, 1.0), 'actor_id': 'light_0'},
            {'light_type': 'spot', 'location': (100, 0, 400), 'rotation': (-45, 0, 0),
             'intensity': 8000.0, 'color': (1.0, 0.9, 0.8), 'actor_id': 'light_1'},
            {'light_type': 'directional', 'location': (0, 0, 0), 'rotation': (-45, 135, 0),
             'intensity': 3.0, 'color': (1.0, 0.95, 0.85), 'actor_id': 'light_2'}
        ]
        
        context = {'test_lights': lights}
        task = ForEachLightTask('foreach', lights_input='test_lights')
        result = task.execute(context)
        
        assert result.status == TaskStatus.SUCCESS
        assert result.output['successful'] == 3
        assert result.output['failed'] == 0
        assert mock_create_task_class.call_count == 3
    
    @patch('unreallib.tasks.generators.for_each_light_task.CreateLightTask')
    def test_foreach_handles_partial_failure(self, mock_create_task_class):
        """Test handling when some lights fail to create"""
        # Setup mock to fail on second light
        call_count = [0]
        
        def side_effect(*args, **kwargs):
            call_count[0] += 1
            mock_instance = Mock()
            if call_count[0] == 2:
                # Second light fails
                mock_result = Mock()
                mock_result.status = TaskStatus.FAILURE
                mock_result.output = {'error': 'Failed to create'}
                mock_instance.execute.return_value = mock_result
            else:
                # Other lights succeed
                mock_result = Mock()
                mock_result.status = TaskStatus.SUCCESS
                mock_result.output = {'action': 'created'}
                mock_instance.execute.return_value = mock_result
            return mock_instance
        
        mock_create_task_class.side_effect = side_effect
        
        lights = [
            {'light_type': 'point', 'location': (0, 0, 300), 'rotation': (0, 0, 0),
             'intensity': 5000.0, 'color': (1.0, 1.0, 1.0), 'actor_id': 'light_0'},
            {'light_type': 'spot', 'location': (100, 0, 400), 'rotation': (-45, 0, 0),
             'intensity': 8000.0, 'color': (1.0, 0.9, 0.8), 'actor_id': 'light_1'},
            {'light_type': 'point', 'location': (200, 0, 300), 'rotation': (0, 0, 0),
             'intensity': 5000.0, 'color': (1.0, 1.0, 1.0), 'actor_id': 'light_2'}
        ]
        
        context = {'test_lights': lights}
        task = ForEachLightTask('foreach', lights_input='test_lights')
        result = task.execute(context)
        
        assert result.status == TaskStatus.PARTIAL_SUCCESS
        assert result.output['successful'] == 2
        assert result.output['failed'] == 1
        assert len(result.output['failed_lights']) == 1
    
    def test_foreach_fails_no_lights_found(self):
        """Test that task fails when lights input is not found"""
        context = {}
        task = ForEachLightTask('foreach', lights_input='missing_lights')
        result = task.execute(context)
        
        assert result.status == TaskStatus.FAILURE
        assert 'No lights found' in result.output['error']
    
    def test_foreach_fails_invalid_lights_type(self):
        """Test that task fails when lights input is not a list"""
        context = {'test_lights': 'not_a_list'}
        task = ForEachLightTask('foreach', lights_input='test_lights')
        result = task.execute(context)
        
        assert result.status == TaskStatus.FAILURE
        assert 'must be a list' in result.output['error']
    
    def test_foreach_resolves_dotted_reference(self):
        """Test resolving dotted reference like 'task_name.lights'"""
        lights = [
            {'light_type': 'point', 'location': (0, 0, 300), 'rotation': (0, 0, 0),
             'intensity': 5000.0, 'color': (1.0, 1.0, 1.0), 'actor_id': 'light_0'}
        ]
        
        context = {
            'gen_task': {
                'lights': lights,
                'count': 1
            }
        }
        
        task = ForEachLightTask('foreach', lights_input='gen_task.lights')
        
        # Test the resolve method directly
        resolved = task._resolve_input(context, 'gen_task.lights')
        assert resolved == lights
    
    def test_foreach_resolves_nested_reference(self):
        """Test resolving nested reference"""
        context = {
            'task1': {
                'output': {
                    'lights': ['light1', 'light2']
                }
            }
        }
        
        task = ForEachLightTask('foreach', lights_input='task1.output.lights')
        resolved = task._resolve_input(context, 'task1.output.lights')
        assert resolved == ['light1', 'light2']


class TestLightingSystemIntegration:
    """Integration tests for the complete lighting system"""
    
    @patch('unreallib.tasks.generators.for_each_light_task.CreateLightTask')
    def test_full_pipeline(self, mock_create_task_class):
        """Test complete pipeline: generate -> create lights"""
        # Setup mock
        mock_task_instance = Mock()
        mock_result = Mock()
        mock_result.status = TaskStatus.SUCCESS
        mock_result.output = {'action': 'created'}
        mock_task_instance.execute.return_value = mock_result
        mock_create_task_class.return_value = mock_task_instance
        
        # Step 1: Generate lights
        light_configs = [
            {
                'actor_id': 'key_light',
                'light_type': 'point',
                'location': [400, 300, 400],
                'intensity': 12000.0,
                'color': [1.0, 0.9, 0.8]
            },
            {
                'actor_id': 'fill_light',
                'light_type': 'point',
                'location': [-300, -200, 300],
                'intensity': 6000.0,
                'color': [0.6, 0.7, 1.0]
            }
        ]
        
        gen_task = LightsGeneratorTask('gen', lights=light_configs)
        gen_result = gen_task.execute({})
        
        assert gen_result.status == TaskStatus.SUCCESS
        assert len(gen_result.output['lights']) == 2
        
        # Step 2: Create lights from generated configs
        context = {'gen': gen_result.output}
        create_task = ForEachLightTask('create', lights_input='gen.lights')
        create_result = create_task.execute(context)
        
        assert create_result.status == TaskStatus.SUCCESS
        assert create_result.output['successful'] == 2
        assert create_result.output['failed'] == 0
    
    def test_three_point_lighting_config(self):
        """Test a realistic three-point lighting configuration"""
        lights = [
            {
                'actor_id': 'key_light',
                'light_type': 'point',
                'location': [400, 300, 400],
                'intensity': 12000.0,
                'color': [1.0, 0.9, 0.8]
            },
            {
                'actor_id': 'fill_light',
                'light_type': 'point',
                'location': [-300, -200, 300],
                'intensity': 6000.0,
                'color': [0.6, 0.7, 1.0]
            },
            {
                'actor_id': 'rim_light',
                'light_type': 'spot',
                'location': [-200, 400, 200],
                'rotation': [0, -135, 0],
                'intensity': 10000.0,
                'inner_cone_angle': 20.0,
                'outer_cone_angle': 40.0
            }
        ]
        
        task = LightsGeneratorTask('gen', lights=lights)
        result = task.execute({})
        
        assert result.status == TaskStatus.SUCCESS
        assert result.output['count'] == 3
        
        # Verify each light
        created_lights = result.output['lights']
        assert created_lights[0]['actor_id'] == 'key_light'
        assert created_lights[1]['actor_id'] == 'fill_light'
        assert created_lights[2]['actor_id'] == 'rim_light'
        assert created_lights[2]['inner_cone_angle'] == 20.0
