"""
Round Robin Scheduler
Implements Round Robin scheduling algorithm with time quantum for fair resource allocation
"""

from typing import List
from datetime import datetime
from collections import deque
from models.resource import Request, Resource, ResourceStatus
from schedulers.base_scheduler import BaseScheduler

class RoundRobinScheduler(BaseScheduler):
    """Round Robin Scheduler with configurable time quantum"""

    def __init__(self, time_quantum: int = 30):
        """
        Initialize Round Robin Scheduler
        Args:
            time_quantum: Time slice in minutes for each request
        """
        super().__init__(f"Round Robin (Quantum: {time_quantum}min)")
        self.time_quantum = time_quantum  # in minutes
        self.ready_queue = deque()  # Circular queue for requests
        self.remaining_time = {}  # Track remaining time for each request

    def add_request(self, request: Request):
        """Add request to ready queue"""
        self.ready_queue.append(request)
        self.request_queue.append(request)
        self.remaining_time[request.id] = request.duration

    def get_next_request(self) -> Request:
        """Get next request in round-robin order"""
        if self.ready_queue:
            return self.ready_queue[0]
        return None

    def schedule(self, available_resources: List[Resource]) -> List[tuple]:
        """
        Round Robin Scheduling Algorithm:
        - Each request gets a time quantum
        - If request duration > quantum, it's preempted and re-queued
        - Provides fair allocation among all requests
        - Prevents resource starvation
        """
        allocations = []

        # Process requests in round-robin order
        new_ready_queue = deque()
        requests_to_remove = []

        # Create a snapshot of current queue to avoid modification during iteration
        current_queue_size = len(self.ready_queue)

        for _ in range(current_queue_size):
            if not self.ready_queue:
                break

            request = self.ready_queue.popleft()
            allocated = False

            # Find first available resource of matching type
            for resource in available_resources:
                if (resource.resource_type == request.resource_type and
                    resource.status == ResourceStatus.AVAILABLE):

                    # Allocate resource to request
                    if resource.acquire():
                        resource.status = ResourceStatus.OCCUPIED
                        request.allocated_resource = resource

                        if request.start_time is None:
                            request.start_time = datetime.now()
                            # Calculate waiting time (only for first allocation)
                            waiting_time = (request.start_time - request.arrival_time).total_seconds()
                            request.waiting_time = max(0, waiting_time)

                        # Determine actual time slice
                        remaining = self.remaining_time.get(request.id, request.duration)
                        time_slice = min(self.time_quantum, remaining)

                        # Update remaining time
                        self.remaining_time[request.id] = remaining - time_slice

                        allocations.append((request, resource))
                        allocated = True

                        # If request needs more time, re-queue it (preemption)
                        if self.remaining_time[request.id] > 0:
                            new_ready_queue.append(request)
                        else:
                            # Request completed
                            request.end_time = datetime.now()
                            request.turnaround_time = (request.end_time - request.arrival_time).total_seconds()
                            requests_to_remove.append(request)

                        break

            # If not allocated, re-queue at end
            if not allocated:
                new_ready_queue.append(request)

        # Update ready queue
        self.ready_queue = new_ready_queue

        # Remove completed requests from request_queue
        for req in requests_to_remove:
            if req in self.request_queue:
                self.request_queue.remove(req)
            if req.id in self.remaining_time:
                del self.remaining_time[req.id]

        return allocations

    def reset(self):
        """Reset scheduler state"""
        super().reset()
        self.ready_queue.clear()
        self.remaining_time.clear()
