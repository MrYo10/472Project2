"""
Resource Models for Hospital Scheduler
Defines data structures for Beds, Doctors, and Operating Rooms
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import threading

class ResourceType(Enum):
    BED = "Bed"
    DOCTOR = "Doctor"
    OPERATING_ROOM = "Operating Room"

class ResourceStatus(Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"

class Priority(Enum):
    CRITICAL = 1    # Emergency cases
    HIGH = 2        # Urgent care
    MEDIUM = 3      # Regular cases
    LOW = 4         # Routine checkups

@dataclass
class Resource:
    """Base class for all hospital resources"""
    id: str
    name: str
    resource_type: ResourceType
    status: ResourceStatus
    lock: threading.Lock = None

    def __post_init__(self):
        if self.lock is None:
            self.lock = threading.Lock()

    def acquire(self):
        """Acquire resource (thread-safe)"""
        return self.lock.acquire(blocking=False)

    def release(self):
        """Release resource"""
        if self.lock.locked():
            self.lock.release()

@dataclass
class Bed(Resource):
    """Hospital Bed Resource"""
    department: str = "General"

    def __init__(self, id: str, name: str, department: str = "General"):
        super().__init__(
            id=id,
            name=name,
            resource_type=ResourceType.BED,
            status=ResourceStatus.AVAILABLE
        )
        self.department = department

@dataclass
class Doctor(Resource):
    """Doctor Resource"""
    specialization: str = "General Practice"

    def __init__(self, id: str, name: str, specialization: str = "General Practice"):
        super().__init__(
            id=id,
            name=name,
            resource_type=ResourceType.DOCTOR,
            status=ResourceStatus.AVAILABLE
        )
        self.specialization = specialization

@dataclass
class OperatingRoom(Resource):
    """Operating Room Resource"""
    equipment_level: str = "Standard"

    def __init__(self, id: str, name: str, equipment_level: str = "Standard"):
        super().__init__(
            id=id,
            name=name,
            resource_type=ResourceType.OPERATING_ROOM,
            status=ResourceStatus.AVAILABLE
        )
        self.equipment_level = equipment_level

@dataclass
class Request:
    """Resource allocation request"""
    id: int
    patient_name: str
    resource_type: ResourceType
    priority: Priority
    duration: int  # in minutes
    arrival_time: datetime
    start_time: datetime = None
    end_time: datetime = None
    allocated_resource: Resource = None
    waiting_time: int = 0  # in seconds
    turnaround_time: int = 0  # in seconds

    def __lt__(self, other):
        """For priority queue comparison"""
        return self.priority.value < other.priority.value
