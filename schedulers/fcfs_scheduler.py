"""
First-Come-First-Served (FCFS) Scheduler
Implements FCFS scheduling algorithm - processes requests in order of arrival
"""

from typing import List
from datetime import datetime
from models.resource import Request, Resource, ResourceStatus
from schedulers.base_scheduler import BaseScheduler

class FCFSScheduler(BaseScheduler):
    """First-Come-First-Served Scheduler"""

    def __init__(self):
        super().__init__("FCFS (First-Come-First-Served)")

    def add_request(self, request: Request):
        """Add request to queue (maintains arrival order)"""
        self.request_queue.append(request)

    def get_next_request(self) -> Request:
        """Get next request (first in queue)"""
        if self.request_queue:
            return self.request_queue[0]
        return None

    def schedule(self, available_resources: List[Resource]) -> List[tuple]:
        """
        FCFS Scheduling Algorithm:
        - Process requests in order of arrival
        - Allocate first available matching resource
        - No preemption
        """
        allocations = []

        # Process requests in FIFO order
        remaining_requests = []

        for request in self.request_queue:
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
                        break

            # If not allocated, keep in queue
            if not allocated:
                remaining_requests.append(request)

        # Update queue with unallocated requests
        self.request_queue = remaining_requests

        return allocations
