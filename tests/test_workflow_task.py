"""
Unit tests for workflow task system
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unreallib.workflow import Task, TaskResult, TaskStatus


class MockTask(Task):
    """Mock task for testing"""
    
    def __init__(self, name: str, should_fail: bool = False, **kwargs):
        super().__init__(name, **kwargs)
        self.should_fail = should_fail
        self.executed = False
    
    def execute(self, context):
        self.executed = True
        
        if self.should_fail:
            raise ValueError("Task failed")
        
        return TaskResult(
            status=TaskStatus.SUCCESS,
            output={'value': 42},
            metadata={'test': True}
        )


class TestTaskResult:
    """Tests for TaskResult"""
    
    def test_success_result(self):
        """Test successful task result"""
        result = TaskResult(
            status=TaskStatus.SUCCESS,
            output={'data': 'test'},
            execution_time=0.5
        )
        
        assert result.status == TaskStatus.SUCCESS
        assert result.success is True
        assert result.output == {'data': 'test'}
        assert result.execution_time == 0.5
        assert result.error is None
    
    def test_failed_result(self):
        """Test failed task result"""
        result = TaskResult(
            status=TaskStatus.FAILED,
            error="Something went wrong"
        )
        
        assert result.status == TaskStatus.FAILED
        assert result.success is False
        assert result.error == "Something went wrong"
    
    def test_result_str_success(self):
        """Test string representation of success"""
        result = TaskResult(
            status=TaskStatus.SUCCESS,
            execution_time=0.123
        )
        
        str_repr = str(result)
        
        assert 'Success' in str_repr
        assert '0.123s' in str_repr
    
    def test_result_str_failed(self):
        """Test string representation of failure"""
        result = TaskResult(
            status=TaskStatus.FAILED,
            error="Test error"
        )
        
        str_repr = str(result)
        
        assert 'Failed' in str_repr
        assert 'Test error' in str_repr


class TestTask:
    """Tests for Task base class"""
    
    def test_task_creation(self):
        """Test task initialization"""
        task = MockTask("test_task", param1="value1")
        
        assert task.name == "test_task"
        assert task.params == {"param1": "value1"}
        assert task.result is None
        assert task.executed is False
    
    def test_task_run_success(self):
        """Test successful task execution"""
        task = MockTask("test_task")
        context = {}
        
        result = task.run(context)
        
        assert task.executed is True
        assert result.status == TaskStatus.SUCCESS
        assert result.output == {'value': 42}
        assert result.execution_time > 0
        assert task.result is result
    
    def test_task_run_failure(self):
        """Test task execution with failure"""
        task = MockTask("test_task", should_fail=True)
        context = {}
        
        result = task.run(context)
        
        assert task.executed is True
        assert result.status == TaskStatus.FAILED
        assert result.error == "Task failed"
        assert result.execution_time > 0
    
    def test_task_repr(self):
        """Test task string representation"""
        task = MockTask("my_task")
        
        repr_str = repr(task)
        
        assert 'MockTask' in repr_str
        assert 'my_task' in repr_str
    
    def test_task_params_stored(self):
        """Test that task parameters are stored"""
        task = MockTask("task", rows=5, cols=3, shape='cube')
        
        assert task.params['rows'] == 5
        assert task.params['cols'] == 3
        assert task.params['shape'] == 'cube'


class TestTaskStatus:
    """Tests for TaskStatus enum"""
    
    def test_all_statuses_exist(self):
        """Test all expected statuses are defined"""
        assert TaskStatus.PENDING
        assert TaskStatus.RUNNING
        assert TaskStatus.SUCCESS
        assert TaskStatus.FAILED
        assert TaskStatus.SKIPPED
    
    def test_status_values(self):
        """Test status enum values"""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.RUNNING.value == "running"
        assert TaskStatus.SUCCESS.value == "success"
        assert TaskStatus.FAILED.value == "failed"
        assert TaskStatus.SKIPPED.value == "skipped"
