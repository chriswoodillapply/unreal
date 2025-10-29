"""
Workflow Loader - Load and execute workflows from JSON files

This module provides functionality to load workflow definitions from JSON
files and convert them into executable workflow graphs.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from unreallib.workflow import WorkflowGraph, WorkflowConfig
from unreallib.tasks import (
    ClearLevelTask,
    SpawnGridTask,
    SpawnCircleTask,
    SpawnSpiralTask,
    SetActorColorTask,
    ColorGridTask,
    MaterialUpsertTask,
)


# Task type registry - maps string names to task classes
TASK_REGISTRY = {
    'ClearLevelTask': ClearLevelTask,
    'SpawnGridTask': SpawnGridTask,
    'SpawnCircleTask': SpawnCircleTask,
    'SpawnSpiralTask': SpawnSpiralTask,
    'SetActorColorTask': SetActorColorTask,
    'ColorGridTask': ColorGridTask,
    'MaterialUpsertTask': MaterialUpsertTask,
}


class WorkflowLoader:
    """Loads and creates workflows from JSON definitions"""
    
    def __init__(self, workflows_dir: Optional[Path] = None):
        """
        Initialize workflow loader
        
        Args:
            workflows_dir: Directory containing workflow JSON files
                          (defaults to scripts/workflows/)
        """
        if workflows_dir is None:
            # Default to workflows directory next to this file
            workflows_dir = Path(__file__).parent.parent.parent / 'workflows'
        
        self.workflows_dir = Path(workflows_dir)
        self.last_config = None  # Store config from last loaded workflow
    
    def load(self, workflow_file: str) -> WorkflowGraph:
        """
        Load a workflow from a JSON file
        
        Args:
            workflow_file: Filename (with or without .json extension)
        
        Returns:
            WorkflowGraph ready to execute
        
        Example:
            loader = WorkflowLoader()
            workflow = loader.load('simple_grid.json')
            executor = WorkflowExecutor()
            executor.execute(workflow)
        """
        # Add .json extension if not present
        if not workflow_file.endswith('.json'):
            workflow_file = f"{workflow_file}.json"
        
        workflow_path = self.workflows_dir / workflow_file
        
        if not workflow_path.exists():
            raise FileNotFoundError(f"Workflow file not found: {workflow_path}")
        
        # Load JSON
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow_def = json.load(f)
        
        return self._build_workflow(workflow_def)
    
    def _build_workflow(self, definition: Dict[str, Any]) -> WorkflowGraph:
        """
        Build a workflow graph from a definition dictionary
        
        Args:
            definition: Workflow definition with config and tasks
        
        Returns:
            WorkflowGraph
        """
        # Extract config
        config_dict = definition.get('config', {})
        config = WorkflowConfig.from_dict(config_dict)
        
        # Store config for access via loader.last_config
        self.last_config = config
        
        # Create workflow graph (doesn't take config)
        workflow = WorkflowGraph()
        
        # Add tasks
        tasks_def = definition.get('tasks', [])
        for task_def in tasks_def:
            # Check if task is enabled (default to True if not specified)
            if not task_def.get('enabled', True):
                print(f"⊘ Skipping disabled task: {task_def.get('name', 'unnamed')}")
                continue
            
            task = self._create_task(task_def)
            dependencies = task_def.get('depends_on', [])
            workflow.add_task(task, dependencies)
        
        return workflow
    
    def _create_task(self, task_def: Dict[str, Any]):
        """
        Create a task instance from a definition
        
        Args:
            task_def: Task definition with type, name, and params
        
        Returns:
            Task instance
        """
        task_type = task_def.get('type')
        task_name = task_def.get('name')
        task_params = task_def.get('params', {})
        
        if not task_type:
            raise ValueError(f"Task definition missing 'type': {task_def}")
        
        if not task_name:
            raise ValueError(f"Task definition missing 'name': {task_def}")
        
        # Look up task class
        task_class = TASK_REGISTRY.get(task_type)
        if not task_class:
            available = ', '.join(TASK_REGISTRY.keys())
            raise ValueError(
                f"Unknown task type '{task_type}'. "
                f"Available types: {available}"
            )
        
        # Create task instance
        try:
            task = task_class(task_name, **task_params)
            return task
        except Exception as e:
            raise ValueError(
                f"Error creating task '{task_name}' of type '{task_type}': {e}"
            ) from e
    
    def list_workflows(self) -> List[str]:
        """
        List all available workflow JSON files
        
        Returns:
            List of workflow filenames
        """
        if not self.workflows_dir.exists():
            return []
        
        return [
            f.name for f in self.workflows_dir.glob('*.json')
        ]
    
    def get_workflow_info(self, workflow_file: str) -> Dict[str, Any]:
        """
        Get metadata about a workflow without loading it
        
        Args:
            workflow_file: Workflow filename
        
        Returns:
            Dictionary with name, description, task count, etc.
        """
        if not workflow_file.endswith('.json'):
            workflow_file = f"{workflow_file}.json"
        
        workflow_path = self.workflows_dir / workflow_file
        
        if not workflow_path.exists():
            raise FileNotFoundError(f"Workflow file not found: {workflow_path}")
        
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow_def = json.load(f)
        
        return {
            'name': workflow_def.get('name', 'Unnamed'),
            'description': workflow_def.get('description', ''),
            'task_count': len(workflow_def.get('tasks', [])),
            'config': workflow_def.get('config', {}),
            'file': workflow_file
        }
