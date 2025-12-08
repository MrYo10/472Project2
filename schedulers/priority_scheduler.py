"""
Priority Scheduler
Implements priority-based scheduling algorithm - processes highest priority requests first
Critical (Emergency) > High (Urgent) > Medium (Regular) > Low (Routine)
"""

from typing import List
from datetime import datetime
import heapq
from models.resource import Request, Resource, ResourceStatus
from schedulers.base_scheduler import BaseScheduler

class PriorityScheduler(BaseScheduler):
    """Priority-based Scheduler using min-heap"""

    def __init__(self):
        super().__init__("Priority Scheduling")
        self.priority_queue = []  # Min-heap based on priority value

    def add_request(self, request: Request):
        """Add request to priority queue"""
        # Use heapq with priority value (lower value = higher priority)
        heapq.heappush(self.priority_queue, (request.priority.value, request.id, request))
        self.request_queue.append(request)

    def get_next_request(self) -> Request:
        """Get highest priority request"""
        if self.priority_queue:
            _, _, request = self.priority_queue[0]
            return request
        return None

    def schedule(self, available_resources: List[Resource]) -> List[tuple]:
        """
        Priority Scheduling Algorithm:
        - Process requests based on priority (Critical > High > Medium > Low)
        - Within same priority, FCFS order
        - Allocate first available matching resource
        - No preemption (non-preemptive priority scheduling)
        """
        allocations = []

        # Process requests in priority order
        new_priority_queue = []
        new_request_queue = []

        while self.priority_queue:
            priority_val, req_id, request = heapq.heappop(self.priority_queue)
            allocated = False

            # Find first available resource of matching type
            for resource in available_resources:
                if (resource.resource_type == request.resource_type and
                    resource.status == ResourceStatus.AVAILABLE):

                    # Allocate resource to request
                    if resource.acquire():
                        resource.status = ResourceStatus.OCCUPIED
                        request.allocated_resource = resource
                        request.start_time = datetime.now()

                        # Calculate waiting time
                        waiting_time = (request.start_time - request.arrival_time).total_seconds()
                        request.waiting_time = max(0, waiting_time)

                        allocations.append((request, resource))
                        allocated = True

                        # Remove from request_queue
                        if request in self.request_queue:
                            self.request_queue.remove(request)
                        break

            # If not allocated, keep in priority queue
            if not allocated:
                heapq.heappush(new_priority_queue, (priority_val, req_id, request))
                new_request_queue.append(request)

        # Update queues with unallocated requests
        self.priority_queue = new_priority_queue
        self.request_queue = new_request_queue

        return allocations
