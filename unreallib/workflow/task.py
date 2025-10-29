"""
Base Task class and task execution framework
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import time


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TaskResult:
    """Result of task execution"""
    status: TaskStatus
    output: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def success(self) -> bool:
        return self.status == TaskStatus.SUCCESS
    
    def __str__(self) -> str:
        if self.status == TaskStatus.SUCCESS:
            return f"✓ Success (in {self.execution_time:.3f}s)"
        elif self.status == TaskStatus.FAILED:
            return f"✗ Failed: {self.error}"
        else:
            return f"{self.status.value}"


class Task(ABC):
    """
    Base class for all workflow tasks
    
    Subclass this to implement custom tasks using the strategy pattern.
    Each task should implement execute() to perform its work.
    """
    
    def __init__(self, name: str, **kwargs):
        """
        Initialize task
        
        Args:
            name: Unique identifier for this task
            **kwargs: Additional task-specific parameters
        """
        self.name = name
        self.params = kwargs
        self.result: Optional[TaskResult] = None
        
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> TaskResult:
        """
        Execute the task
        
        Args:
            context: Shared context containing outputs from previous tasks
        
        Returns:
            TaskResult with status and output data
        """
        pass
    
    def run(self, context: Dict[str, Any]) -> TaskResult:
        """
        Run the task with timing and error handling
        
        Args:
            context: Shared execution context
            
        Returns:
            TaskResult
        """
        print(f"[{self.name}] Starting...")
        start_time = time.time()
        
        try:
            result = self.execute(context)
            result.execution_time = time.time() - start_time
            self.result = result
            print(f"[{self.name}] {result}")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            result = TaskResult(
                status=TaskStatus.FAILED,
                error=str(e),
                execution_time=execution_time
            )
            self.result = result
            print(f"[{self.name}] {result}")
            return result
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
