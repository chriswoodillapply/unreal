"""
Tests for WorkflowLoader - JSON workflow loading
"""

import pytest
import json
import tempfile
from pathlib import Path

from unreallib.workflow import WorkflowLoader, WorkflowGraph, WorkflowConfig
from unreallib.tasks import SpawnGridTask, ClearLevelTask


class TestWorkflowLoader:
    """Test workflow loading from JSON"""
    
    def test_loader_creation(self):
        """Test creating a workflow loader"""
        loader = WorkflowLoader()
        assert loader.workflows_dir.exists()
    
    def test_load_simple_workflow(self):
        """Test loading a simple workflow"""
        loader = WorkflowLoader()
        workflow = loader.load('simple_grid')
        
        assert isinstance(workflow, WorkflowGraph)
        assert len(workflow.tasks) == 2
        assert 'clear_scene' in workflow.tasks
        assert 'spawn_grid' in workflow.tasks
    
    def test_load_workflow_without_extension(self):
        """Test loading workflow without .json extension"""
        loader = WorkflowLoader()
        workflow = loader.load('simple_grid')  # No .json
        assert isinstance(workflow, WorkflowGraph)
    
    def test_load_workflow_with_extension(self):
        """Test loading workflow with .json extension"""
        loader = WorkflowLoader()
        workflow = loader.load('simple_grid.json')  # With .json
        assert isinstance(workflow, WorkflowGraph)
    
    def test_load_nonexistent_workflow_raises(self):
        """Test loading non-existent workflow raises error"""
        loader = WorkflowLoader()
        with pytest.raises(FileNotFoundError):
            loader.load('nonexistent_workflow')
    
    def test_workflow_config_loaded(self):
        """Test that workflow config is loaded correctly"""
        loader = WorkflowLoader()
        workflow = loader.load('simple_grid')
        
        assert isinstance(loader.last_config, WorkflowConfig)
        assert loader.last_config.upsert_mode == False
        assert loader.last_config.clear_before_execute == True
    
    def test_workflow_tasks_created(self):
        """Test that tasks are created with correct types"""
        loader = WorkflowLoader()
        workflow = loader.load('simple_grid')
        
        clear_task = workflow.tasks['clear_scene']
        grid_task = workflow.tasks['spawn_grid']
        
        assert isinstance(clear_task, ClearLevelTask)
        assert isinstance(grid_task, SpawnGridTask)
    
    def test_workflow_dependencies(self):
        """Test that task dependencies are set up correctly"""
        loader = WorkflowLoader()
        workflow = loader.load('simple_grid')
        
        # spawn_grid depends on clear_scene
        deps = workflow.dependencies['spawn_grid']
        assert 'clear_scene' in deps
    
    def test_task_parameters(self):
        """Test that task parameters are passed correctly"""
        loader = WorkflowLoader()
        workflow = loader.load('simple_grid')
        
        grid_task = workflow.tasks['spawn_grid']
        assert grid_task.params['rows'] == 5
        assert grid_task.params['cols'] == 5
        assert grid_task.params['spacing'] == 200
        assert grid_task.params['shape'] == 'cube'
    
    def test_list_workflows(self):
        """Test listing available workflows"""
        loader = WorkflowLoader()
        workflows = loader.list_workflows()
        
        assert isinstance(workflows, list)
        assert 'simple_grid.json' in workflows
    
    def test_get_workflow_info(self):
        """Test getting workflow metadata"""
        loader = WorkflowLoader()
        info = loader.get_workflow_info('simple_grid')
        
        assert info['name'] == 'Simple Grid'
        assert 'grid' in info['description'].lower()
        assert info['task_count'] == 2
        assert info['file'] == 'simple_grid.json'
    
    def test_load_colored_grid_workflow(self):
        """Test loading the colored grid workflow"""
        loader = WorkflowLoader()
        workflow = loader.load('colored_grid')
        
        assert len(workflow.tasks) == 2
        assert loader.last_config.upsert_mode == True
    
    def test_load_multiple_patterns_workflow(self):
        """Test loading the multiple patterns workflow"""
        loader = WorkflowLoader()
        workflow = loader.load('multiple_patterns')
        
        assert len(workflow.tasks) == 4
        assert 'clear_all' in workflow.tasks
        assert 'grid' in workflow.tasks
        assert 'circle' in workflow.tasks
        assert 'spiral' in workflow.tasks


class TestWorkflowLoaderErrors:
    """Test error handling in workflow loader"""
    
    def test_invalid_task_type_raises(self):
        """Test that invalid task type raises error"""
        # Create temp workflow with invalid task type
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            workflow_def = {
                "name": "Invalid",
                "tasks": [{
                    "name": "bad_task",
                    "type": "NonExistentTask"
                }]
            }
            json.dump(workflow_def, f)
            temp_file = f.name
        
        try:
            loader = WorkflowLoader(Path(temp_file).parent)
            with pytest.raises(ValueError, match="Unknown task type"):
                loader.load(Path(temp_file).name)
        finally:
            Path(temp_file).unlink()
    
    def test_missing_task_name_raises(self):
        """Test that missing task name raises error"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            workflow_def = {
                "name": "Invalid",
                "tasks": [{
                    "type": "ClearLevelTask"
                    # Missing "name"
                }]
            }
            json.dump(workflow_def, f)
            temp_file = f.name
        
        try:
            loader = WorkflowLoader(Path(temp_file).parent)
            with pytest.raises(ValueError, match="missing 'name'"):
                loader.load(Path(temp_file).name)
        finally:
            Path(temp_file).unlink()
    
    def test_missing_task_type_raises(self):
        """Test that missing task type raises error"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            workflow_def = {
                "name": "Invalid",
                "tasks": [{
                    "name": "task1"
                    # Missing "type"
                }]
            }
            json.dump(workflow_def, f)
            temp_file = f.name
        
        try:
            loader = WorkflowLoader(Path(temp_file).parent)
            with pytest.raises(ValueError, match="missing 'type'"):
                loader.load(Path(temp_file).name)
        finally:
            Path(temp_file).unlink()
