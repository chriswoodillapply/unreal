"""
Unit tests for workflow graph (DAG)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unreallib.workflow import WorkflowGraph, Task, TaskResult, TaskStatus


class DummyTask(Task):
    """Dummy task for testing"""
    
    def execute(self, context):
        return TaskResult(status=TaskStatus.SUCCESS)


class TestWorkflowGraph:
    """Tests for WorkflowGraph"""
    
    def test_empty_graph(self):
        """Test empty workflow graph"""
        graph = WorkflowGraph()
        
        assert len(graph) == 0
        assert graph.get_execution_order() == []
    
    def test_add_single_task(self):
        """Test adding a single task"""
        graph = WorkflowGraph()
        task = DummyTask("task1")
        
        graph.add_task(task)
        
        assert len(graph) == 1
        assert "task1" in graph
        assert graph["task1"] is task
    
    def test_add_task_with_dependencies(self):
        """Test adding task with dependencies"""
        graph = WorkflowGraph()
        task1 = DummyTask("task1")
        task2 = DummyTask("task2")
        
        graph.add_task(task1)
        graph.add_task(task2, depends_on=["task1"])
        
        assert len(graph) == 2
        assert graph.dependencies["task2"] == ["task1"]
    
    def test_duplicate_task_raises(self):
        """Test that adding duplicate task raises error"""
        graph = WorkflowGraph()
        task1 = DummyTask("task1")
        task2 = DummyTask("task1")  # Same name
        
        graph.add_task(task1)
        
        with pytest.raises(ValueError, match="already exists"):
            graph.add_task(task2)
    
    def test_missing_dependency_raises(self):
        """Test that missing dependency raises error"""
        graph = WorkflowGraph()
        task = DummyTask("task1")
        
        with pytest.raises(ValueError, match="hasn't been added"):
            graph.add_task(task, depends_on=["nonexistent"])
    
    def test_execution_order_single_task(self):
        """Test execution order for single task"""
        graph = WorkflowGraph()
        graph.add_task(DummyTask("task1"))
        
        order = graph.get_execution_order()
        
        assert order == ["task1"]
    
    def test_execution_order_linear(self):
        """Test execution order for linear dependencies"""
        graph = WorkflowGraph()
        graph.add_task(DummyTask("task1"))
        graph.add_task(DummyTask("task2"), depends_on=["task1"])
        graph.add_task(DummyTask("task3"), depends_on=["task2"])
        
        order = graph.get_execution_order()
        
        assert order == ["task1", "task2", "task3"]
    
    def test_execution_order_parallel(self):
        """Test execution order for parallel tasks"""
        graph = WorkflowGraph()
        graph.add_task(DummyTask("root"))
        graph.add_task(DummyTask("branch1"), depends_on=["root"])
        graph.add_task(DummyTask("branch2"), depends_on=["root"])
        
        order = graph.get_execution_order()
        
        # Root should be first, branches can be in any order
        assert order[0] == "root"
        assert set(order[1:]) == {"branch1", "branch2"}
    
    def test_execution_order_diamond(self):
        """Test execution order for diamond dependency"""
        graph = WorkflowGraph()
        graph.add_task(DummyTask("root"))
        graph.add_task(DummyTask("left"), depends_on=["root"])
        graph.add_task(DummyTask("right"), depends_on=["root"])
        graph.add_task(DummyTask("bottom"), depends_on=["left", "right"])
        
        order = graph.get_execution_order()
        
        # Root first, bottom last
        assert order[0] == "root"
        assert order[-1] == "bottom"
        assert set(order[1:3]) == {"left", "right"}
    
    def test_circular_dependency_raises(self):
        """Test that circular dependency is detected"""
        graph = WorkflowGraph()
        
        # Create a cycle: task1 -> task2 -> task3 -> task1
        graph.add_task(DummyTask("task1"))
        graph.add_task(DummyTask("task2"), depends_on=["task1"])
        graph.add_task(DummyTask("task3"), depends_on=["task2"])
        
        # This should work so far
        graph.validate()
        
        # Now manually create a cycle (bypassing the normal checks)
        graph.dependencies["task1"] = ["task3"]
        
        with pytest.raises(ValueError, match="Circular dependency"):
            graph.get_execution_order()
    
    def test_validate_success(self):
        """Test successful validation"""
        graph = WorkflowGraph()
        graph.add_task(DummyTask("task1"))
        graph.add_task(DummyTask("task2"), depends_on=["task1"])
        
        assert graph.validate() is True
    
    def test_visualize(self):
        """Test workflow visualization"""
        graph = WorkflowGraph()
        graph.add_task(DummyTask("root"))
        graph.add_task(DummyTask("child"), depends_on=["root"])
        
        viz = graph.visualize()
        
        assert "Workflow Graph" in viz
        assert "root" in viz
        assert "child" in viz
    
    def test_contains(self):
        """Test __contains__ operator"""
        graph = WorkflowGraph()
        graph.add_task(DummyTask("task1"))
        
        assert "task1" in graph
        assert "task2" not in graph
    
    def test_getitem(self):
        """Test __getitem__ operator"""
        graph = WorkflowGraph()
        task = DummyTask("task1")
        graph.add_task(task)
        
        assert graph["task1"] is task
