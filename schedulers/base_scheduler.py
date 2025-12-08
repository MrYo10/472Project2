"""
Base Scheduler Interface
Defines the abstract interface for all scheduling algorithms
"""

from abc import ABC, abstractmethod
from typing import List
from models.resource import Request, Resource

class BaseScheduler(ABC):
    """Abstract base class for all scheduling algorithms"""

    def __init__(self, name: str):
        self.name = name
        self.request_queue = []
        self.completed_requests = []
        self.metrics = {
            'total_requests': 0,
            'completed_requests': 0,
            'average_waiting_time': 0.0,
            'average_turnaround_time': 0.0,
            'resource_utilization': 0.0
        }

    @abstractmethod
    def add_request(self, request: Request):
        """Add a request to the scheduler"""
        pass

    @abstractmethod
    def schedule(self, available_resources: List[Resource]) -> List[tuple]:
        """
        Execute scheduling algorithm
        Returns: List of (Request, Resource) tuples representing allocations
        """
        pass

    @abstractmethod
    def get_next_request(self) -> Request:
        """Get the next request to process based on algorithm"""
        pass

    def calculate_metrics(self):
        """Calculate scheduling performance metrics"""
        if not self.completed_requests:
            return self.metrics

        total_waiting = sum(req.waiting_time for req in self.completed_requests)
        total_turnaround = sum(req.turnaround_time for req in self.completed_requests)

        self.metrics['total_requests'] = len(self.request_queue) + len(self.completed_requests)
        self.metrics['completed_requests'] = len(self.completed_requests)
        self.metrics['average_waiting_time'] = total_waiting / len(self.completed_requests)
        self.metrics['average_turnaround_time'] = total_turnaround / len(self.completed_requests)

        return self.metrics

    def reset(self):
        """Reset scheduler state"""
        self.request_queue.clear()
        self.completed_requests.clear()
        self.metrics = {
            'total_requests': 0,
            'completed_requests': 0,
            'average_waiting_time': 0.0,
            'average_turnaround_time': 0.0,
            'resource_utilization': 0.0
        }
