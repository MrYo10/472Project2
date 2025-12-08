from core.resource_manager import ResourceManager
from schedulers.fcfs_scheduler import FCFSScheduler
from schedulers.priority_scheduler import PriorityScheduler
from schedulers.round_robin_scheduler import RoundRobinScheduler
from models.resource import ResourceType, Priority

def main():
    # ---------------------------
    # 1. Initialize resource manager
    # ---------------------------
    rm = ResourceManager()
    rm.initialize_default_resources()
    print("Default resources initialized.\n")

    # ---------------------------
    # 2. Create some demo requests
    # ---------------------------
    req1 = rm.create_request("Alice", ResourceType.BED, Priority.MEDIUM, 30)
    req2 = rm.create_request("Bob", ResourceType.DOCTOR, Priority.CRITICAL, 20)
    req3 = rm.create_request("Charlie", ResourceType.BED, Priority.LOW, 45)
    req4 = rm.create_request("Diana", ResourceType.BED, Priority.HIGH, 15)

    # Pick scheduler here:
    # scheduler = FCFSScheduler()
    # scheduler = PriorityScheduler()
    scheduler = RoundRobinScheduler(time_quantum=20)

    # Add requests into the scheduler
    scheduler.add_request(req1)
    scheduler.add_request(req2)
    scheduler.add_request(req3)
    scheduler.add_request(req4)

    # ---------------------------
    # 3. Allocate resources
    # ---------------------------
    allocations = rm.allocate_resources(scheduler)

    # ---------------------------
    # 4. Print results
    # ---------------------------
    print(f"Running Scheduler: {scheduler.name}\n")
    for req, res in allocations:
        print(f"Request {req.id} ({req.patient_name}) allocated to {res.name} ({res.resource_type.value})")

    print("\nActive allocations:")
    for (req, res, end_time) in rm.active_allocations:
        print(f" - {res.name} assigned to {req.patient_name} until {end_time}")

if __name__ == "__main__":
    main()