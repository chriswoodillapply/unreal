"""
Unit tests for workflow executor
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unreallib.workflow import (
    WorkflowGraph, 
    WorkflowExecutor, 
    WorkflowConfig,
    Task, 
    TaskResult, 
    TaskStatus
)


class CounterTask(Task):
    """Task that increments a counter in context"""
    
    def __init__(self, name: str, increment: int = 1):
        super().__init__(name, increment=increment)
        self.execute_count = 0
    
    def execute(self, context):
        self.execute_count += 1
        
        # Get counter from context or start at 0
        current = context.get('counter', 0)
        new_value = current + self.params['increment']
        
        # Update counter in context for next task
        context['counter'] = new_value
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output=new_value
        )


class FailingTask(Task):
    """Task that always fails"""
    
    def execute(self, context):
        raise RuntimeError("Task failed intentionally")


class TestWorkflowExecutor:
    """Tests for WorkflowExecutor"""
    
    def test_executor_creation(self):
        """Test executor initialization"""
        graph = WorkflowGraph()
        executor = WorkflowExecutor(graph)
        
        assert executor.graph is graph
        assert isinstance(executor.config, WorkflowConfig)
        assert executor.context == {}
        assert executor.results == {}
    
    def test_executor_with_config(self):
        """Test executor with custom config"""
        graph = WorkflowGraph()
        config = WorkflowConfig(clear_before_execute=True)
        
        executor = WorkflowExecutor(graph, config)
        
        assert executor.config is config
        assert executor.config.clear_before_execute is True
    
    def test_execute_empty_workflow(self):
        """Test executing empty workflow"""
        graph = WorkflowGraph()
        executor = WorkflowExecutor(graph)
        
        results = executor.execute()
        
        assert results == {}
    
    def test_execute_single_task(self):
        """Test executing single task"""
        graph = WorkflowGraph()
        graph.add_task(CounterTask("task1", increment=5))
        
        executor = WorkflowExecutor(graph)
        results = executor.execute()
        
        assert len(results) == 1
        assert results["task1"].success is True
        assert results["task1"].output == 5
    
    def test_execute_linear_tasks(self):
        """Test executing linear task chain"""
        graph = WorkflowGraph()
        graph.add_task(CounterTask("task1", increment=1))
        graph.add_task(CounterTask("task2", increment=2), depends_on=["task1"])
        graph.add_task(CounterTask("task3", increment=3), depends_on=["task2"])
        
        executor = WorkflowExecutor(graph)
        results = executor.execute()
        
        assert len(results) == 3
        assert all(r.success for r in results.values())
        # Counter should be 1 + 2 + 3 = 6
        assert results["task3"].output == 6
    
    def test_context_passing(self):
        """Test that task outputs are added to context"""
        graph = WorkflowGraph()
        graph.add_task(CounterTask("task1", increment=10))
        
        executor = WorkflowExecutor(graph)
        results = executor.execute()
        
        # Task output should be in context
        assert executor.context["task1"] == 10
    
    def test_initial_context(self):
        """Test providing initial context"""
        graph = WorkflowGraph()
        graph.add_task(CounterTask("task1", increment=5))
        
        executor = WorkflowExecutor(graph)
        results = executor.execute(initial_context={'counter': 100})
        
        # Should add to initial counter
        assert results["task1"].output == 105
    
    def test_failed_task_handling(self):
        """Test handling of failed task"""
        graph = WorkflowGraph()
        graph.add_task(FailingTask("bad_task"))
        
        executor = WorkflowExecutor(graph)
        results = executor.execute()
        
        assert results["bad_task"].status == TaskStatus.FAILED
        assert "failed intentionally" in results["bad_task"].error
    
    def test_dependency_failure_skips_downstream(self):
        """Test that downstream tasks are skipped when dependency fails"""
        graph = WorkflowGraph()
        graph.add_task(FailingTask("task1"))
        graph.add_task(CounterTask("task2"), depends_on=["task1"])
        
        executor = WorkflowExecutor(graph)
        results = executor.execute()
        
        assert results["task1"].status == TaskStatus.FAILED
        assert results["task2"].status == TaskStatus.SKIPPED
    
    def test_parallel_execution_independent(self):
        """Test that parallel branches share context and accumulate state"""
        graph = WorkflowGraph()
        graph.add_task(CounterTask("root", increment=1))
        graph.add_task(CounterTask("branch1", increment=10), depends_on=["root"])
        graph.add_task(CounterTask("branch2", increment=20), depends_on=["root"])
        
        executor = WorkflowExecutor(graph)
        results = executor.execute()
        
        # Both branches should succeed
        assert results["branch1"].success is True
        assert results["branch2"].success is True
        # Since they execute sequentially and share context:
        # root: 0 + 1 = 1
        # branch1: 1 + 10 = 11
        # branch2: 11 + 20 = 31 (sees accumulated state)
        assert results["branch1"].output == 11
        assert results["branch2"].output == 31
    
    def test_config_in_context(self):
        """Test that config is added to context"""
        graph = WorkflowGraph()
        config = WorkflowConfig(actor_id_prefix="test_")
        
        executor = WorkflowExecutor(graph, config)
        executor.execute()
        
        assert 'workflow_config' in executor.context
        assert executor.context['workflow_config'] is config
    
    def test_get_task_output(self):
        """Test getting task output"""
        graph = WorkflowGraph()
        graph.add_task(CounterTask("task1", increment=42))
        
        executor = WorkflowExecutor(graph)
        executor.execute()
        
        output = executor.get_task_output("task1")
        
        assert output == 42
    
    def test_get_nonexistent_task_output(self):
        """Test getting output from nonexistent task"""
        graph = WorkflowGraph()
        executor = WorkflowExecutor(graph)
        executor.execute()
        
        output = executor.get_task_output("nonexistent")
        
        assert output is None


class TestWorkflowExecutorConfig:
    """Tests for executor configuration behavior"""
    
    def test_config_clear_before_execute(self):
        """Test clear_before_execute config (can't actually test without Unreal)"""
        graph = WorkflowGraph()
        config = WorkflowConfig(clear_before_execute=True)
        
        executor = WorkflowExecutor(graph, config)
        
        # Just verify config is set - actual clearing requires Unreal
        assert executor.config.clear_before_execute is True
    
    def test_config_save_after(self):
        """Test save_level_after config"""
        graph = WorkflowGraph()
        config = WorkflowConfig(save_level_after=True)
        
        executor = WorkflowExecutor(graph, config)
        
        # Just verify config is set - actual saving requires Unreal
        assert executor.config.save_level_after is True
