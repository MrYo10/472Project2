"""
Resource Manager
Manages hospital resources with thread-safe operations using locks and semaphores
Demonstrates OS concepts: mutual exclusion, synchronization, deadlock prevention
"""

import threading
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from models.resource import (
    Resource, Bed, Doctor, OperatingRoom,
    ResourceType, ResourceStatus, Request, Priority
)
from schedulers.base_scheduler import BaseScheduler

class ResourceManager:
    """Thread-safe resource manager for hospital resources"""

    def __init__(self):
        self.resources: Dict[ResourceType, List[Resource]] = {
            ResourceType.BED: [],
            ResourceType.DOCTOR: [],
            ResourceType.OPERATING_ROOM: []
        }

        # Locks for thread-safe operations
        self.manager_lock = threading.Lock()
        self.allocation_lock = threading.Lock()

        # Semaphores for resource counting
        self.resource_semaphores: Dict[ResourceType, threading.Semaphore] = {
            ResourceType.BED: threading.Semaphore(0),
            ResourceType.DOCTOR: threading.Semaphore(0),
            ResourceType.OPERATING_ROOM: threading.Semaphore(0)
        }

        # Active allocations
        self.active_allocations: List[tuple] = []  # (Request, Resource, end_time)
        self.request_counter = 0

    def add_resource(self, resource: Resource):
        """Add a resource to the pool (thread-safe)"""
        with self.manager_lock:
            self.resources[resource.resource_type].append(resource)
            # Increment semaphore count
            self.resource_semaphores[resource.resource_type].release()

    def remove_resource(self, resource_id: str, resource_type: ResourceType) -> bool:
        """Remove a resource from the pool"""
        with self.manager_lock:
            resources = self.resources[resource_type]
            for i, resource in enumerate(resources):
                if resource.id == resource_id:
                    if resource.status == ResourceStatus.AVAILABLE:
                        resources.pop(i)
                        # Decrement semaphore (non-blocking)
                        self.resource_semaphores[resource_type].acquire(blocking=False)
                        return True
            return False

    def get_available_resources(self, resource_type: ResourceType = None) -> List[Resource]:
        """Get list of available resources"""
        with self.manager_lock:
            if resource_type:
                return [r for r in self.resources[resource_type]
                        if r.status == ResourceStatus.AVAILABLE]
            else:
                all_available = []
                for resources in self.resources.values():
                    all_available.extend([r for r in resources
                                        if r.status == ResourceStatus.AVAILABLE])
                return all_available

    def get_all_resources(self, resource_type: ResourceType = None) -> List[Resource]:
        """Get all resources regardless of status"""
        with self.manager_lock:
            if resource_type:
                return self.resources[resource_type].copy()
            else:
                all_resources = []
                for resources in self.resources.values():
                    all_resources.extend(resources)
                return all_resources

    def create_request(self, patient_name: str, resource_type: ResourceType,
                      priority: Priority, duration: int) -> Request:
        """Create a new resource request"""
        with self.manager_lock:
            self.request_counter += 1
            return Request(
                id=self.request_counter,
                patient_name=patient_name,
                resource_type=resource_type,
                priority=priority,
                duration=duration,
                arrival_time=datetime.now()
            )

    def allocate_resources(self, scheduler: BaseScheduler) -> List[tuple]:
        """
        Allocate resources using the provided scheduler
        Returns list of (Request, Resource) allocations
        """
        with self.allocation_lock:
            # Get all available resources
            available_resources = self.get_available_resources()

            # Use scheduler to determine allocations
            allocations = scheduler.schedule(available_resources)

            # Track active allocations with end times
            current_time = datetime.now()
            for request, resource in allocations:
                end_time = current_time + timedelta(minutes=request.duration)
                self.active_allocations.append((request, resource, end_time))

            return allocations

    def release_resource(self, resource: Resource):
        """Release a resource back to available pool"""
        with self.manager_lock:
            resource.release()
            resource.status = ResourceStatus.AVAILABLE

            # Remove from active allocations
            self.active_allocations = [
                (req, res, end) for req, res, end in self.active_allocations
                if res.id != resource.id
            ]

    def check_and_release_expired(self) -> List[Resource]:
        """Check and release resources with expired allocations"""
        released = []
        current_time = datetime.now()

        with self.allocation_lock:
            remaining_allocations = []

            for request, resource, end_time in self.active_allocations:
                if current_time >= end_time:
                    # Release expired allocation
                    self.release_resource(resource)
                    released.append(resource)

                    # Mark request as completed
                    request.end_time = current_time
                    request.turnaround_time = (request.end_time - request.arrival_time).total_seconds()
                else:
                    remaining_allocations.append((request, resource, end_time))

            self.active_allocations = remaining_allocations

        return released

    def get_resource_statistics(self) -> Dict:
        """Get statistics about resource utilization"""
        with self.manager_lock:
            stats = {}

            for resource_type in ResourceType:
                total = len(self.resources[resource_type])
                available = len([r for r in self.resources[resource_type]
                               if r.status == ResourceStatus.AVAILABLE])
                occupied = len([r for r in self.resources[resource_type]
                              if r.status == ResourceStatus.OCCUPIED])

                stats[resource_type.value] = {
                    'total': total,
                    'available': available,
                    'occupied': occupied,
                    'utilization': (occupied / total * 100) if total > 0 else 0
                }

            return stats

    def initialize_default_resources(self):
        """Initialize with default set of resources"""
        # Add Beds
        for i in range(1, 11):
            dept = "ICU" if i <= 3 else "General" if i <= 7 else "Emergency"
            bed = Bed(f"B{i:03d}", f"Bed {i}", dept)
            self.add_resource(bed)

        # Add Doctors
        specializations = ["Cardiology", "Neurology", "Orthopedics", "General Practice",
                          "Emergency Medicine", "Surgery"]
        for i in range(1, 9):
            spec = specializations[(i - 1) % len(specializations)]
            doctor = Doctor(f"D{i:03d}", f"Dr. {chr(64+i)}", spec)
            self.add_resource(doctor)

        # Add Operating Rooms
        equipment_levels = ["Advanced", "Standard", "Basic"]
        for i in range(1, 6):
            equipment = equipment_levels[(i - 1) % len(equipment_levels)]
            or_room = OperatingRoom(f"OR{i:03d}", f"OR {i}", equipment)
            self.add_resource(or_room)
