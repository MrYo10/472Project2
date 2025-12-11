"""
Simple Test Suite for Scheduling Algorithms
Demonstrates input, expected output, and actual output for each algorithm
"""
from core.resource_manager import ResourceManager
from schedulers.fcfs_scheduler import FCFSScheduler
from schedulers.priority_scheduler import PriorityScheduler
from schedulers.round_robin_scheduler import RoundRobinScheduler
from models.resource import ResourceType, Priority


def print_header(title):
    """Print section header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def test_fcfs():
    """Test FCFS Scheduler"""
    print_header("TEST 1: FIRST-COME-FIRST-SERVED (FCFS) SCHEDULER")

    rm = ResourceManager()
    rm.initialize_default_resources()
    scheduler = FCFSScheduler()

    # Create requests
    print("\n INPUT - Patient Requests (in arrival order):")
    requests = [
        rm.create_request("Alice", ResourceType.DOCTOR, Priority.LOW, 30),
        rm.create_request("Bob", ResourceType.DOCTOR, Priority.HIGH, 45),
        rm.create_request("Charlie", ResourceType.BED, Priority.MEDIUM, 20),
        rm.create_request("Diana", ResourceType.DOCTOR, Priority.HIGH, 60),
    ]

    for i, req in enumerate(requests, 1):
        print(f"  {i}. {req.patient_name:<10} needs {req.resource_type.value:<15} "
              f"Priority: {req.priority.name:<8} Duration: {req.duration} min")

    # Expected output
    print("\n EXPECTED OUTPUT:")
    print("  FCFS processes requests in arrival order (ignores priority):")
    print("  1. Alice   → gets Doctor (arrived first, despite LOW priority)")
    print("  2. Bob     → gets Doctor")
    print("  3. Charlie → gets Bed")
    print("  4. Diana   → gets Doctor")

    # Actual allocation
    for req in requests:
        scheduler.add_request(req)

    allocations = rm.allocate_resources(scheduler)

    print("\n ACTUAL OUTPUT:")
    if allocations:
        for i, (req, res) in enumerate(allocations, 1):
            print(f"  {i}. {req.patient_name:<10} → {res.name} ({res.resource_type.value})")
    else:
        print("  ERROR: No allocations made")

    print("\n KEY INSIGHT:")
    print("  - FCFS serves requests in First-In-First-Out order")
    print("  - Alice (LOW priority) is served before Bob (HIGH priority)")
    print("  - Simple and fair, but ignores urgency")


def test_priority():
    """Test Priority Scheduler"""
    print_header("TEST 2: PRIORITY-BASED SCHEDULER")

    rm = ResourceManager()
    rm.initialize_default_resources()
    scheduler = PriorityScheduler()

    # Create same requests as FCFS
    print("\n INPUT - Patient Requests (same as Test 1):")
    requests = [
        rm.create_request("Alice", ResourceType.DOCTOR, Priority.LOW, 30),
        rm.create_request("Bob", ResourceType.DOCTOR, Priority.HIGH, 45),
        rm.create_request("Charlie", ResourceType.BED, Priority.MEDIUM, 20),
        rm.create_request("Diana", ResourceType.DOCTOR, Priority.HIGH, 60),
        rm.create_request("Eve", ResourceType.DOCTOR, Priority.MEDIUM, 25),
    ]

    for i, req in enumerate(requests, 1):
        print(f"  {i}. {req.patient_name:<10} needs {req.resource_type.value:<15} "
              f"Priority: {req.priority.name:<8} Duration: {req.duration} min")

    # Expected output
    print("\n EXPECTED OUTPUT:")
    print("  Priority scheduler processes HIGH priority first:")
    print("  1. Bob     → gets Doctor (HIGH priority)")
    print("  2. Diana   → gets Doctor (HIGH priority)")
    print("  3. Eve     → gets Doctor (MEDIUM priority)")
    print("  4. Charlie → gets Bed (MEDIUM priority)")
    print("  5. Alice   → gets Doctor (LOW priority, served last)")

    # Actual allocation
    for req in requests:
        scheduler.add_request(req)

    allocations = rm.allocate_resources(scheduler)

    print("\n ACTUAL OUTPUT:")
    if allocations:
        for i, (req, res) in enumerate(allocations, 1):
            print(f"  {i}. {req.patient_name:<10} → {res.name} ({res.resource_type.value}) "
                  f"[Priority: {req.priority.name}]")
    else:
        print("  ERROR: No allocations made")

    print("\n KEY INSIGHT:")
    print("  - Priority scheduler serves urgent cases first")
    print("  - Bob and Diana (HIGH) get resources before Alice (LOW)")
    print("  - Risk: LOW priority requests may experience starvation")


def test_round_robin():
    """Test Round Robin Scheduler"""
    print_header("TEST 3: ROUND ROBIN SCHEDULER")

    rm = ResourceManager()
    rm.initialize_default_resources()
    time_quantum = 30
    scheduler = RoundRobinScheduler(time_quantum=time_quantum)

    # Create requests with varying durations
    print(f"\n INPUT - Patient Requests (Time Quantum: {time_quantum} min):")
    requests = [
        rm.create_request("Patient-A", ResourceType.DOCTOR, Priority.MEDIUM, 90),
        rm.create_request("Patient-B", ResourceType.DOCTOR, Priority.MEDIUM, 45),
        rm.create_request("Patient-C", ResourceType.DOCTOR, Priority.MEDIUM, 20),
        rm.create_request("Patient-D", ResourceType.BED, Priority.MEDIUM, 60),
    ]

    for i, req in enumerate(requests, 1):
        quanta = (req.duration + time_quantum - 1) // time_quantum
        print(f"  {i}. {req.patient_name} needs {req.resource_type.value:<15} "
              f"Duration: {req.duration:2d} min ({quanta} time slices)")

    # Expected output
    print("\n EXPECTED OUTPUT:")
    print(f"  Round Robin gives each request {time_quantum} minutes at a time:")
    print("  Round 1:")
    print("    - Patient-A: 30 min (60 remaining)")
    print("    - Patient-B: 30 min (15 remaining)")
    print("    - Patient-C: 20 min (COMPLETE)")
    print("    - Patient-D: 30 min (30 remaining)")
    print("  Round 2:")
    print("    - Patient-A: 30 min (30 remaining)")
    print("    - Patient-B: 15 min (COMPLETE)")
    print("    - Patient-D: 30 min (COMPLETE)")
    print("  Round 3:")
    print("    - Patient-A: 30 min (COMPLETE)")

    # Actual allocation
    for req in requests:
        scheduler.add_request(req)

    allocations = rm.allocate_resources(scheduler)

    print("\n ACTUAL OUTPUT:")
    if allocations:
        for i, (req, res) in enumerate(allocations, 1):
            quanta = (req.duration + time_quantum - 1) // time_quantum
            print(f"  {i}. {req.patient_name} → {res.name} "
                  f"({req.duration} min = {quanta} time slices)")
    else:
        print("  ERROR: No allocations made")

    print("\n KEY INSIGHT:")
    print("  - Round Robin provides fair CPU time-sharing")
    print("  - Short jobs (Patient-C: 20 min) complete quickly")
    print("  - Long jobs (Patient-A: 90 min) don't monopolize resources")
    print("  - Prevents starvation, ensures fairness")


def test_comparison():
    """Compare all algorithms with same input"""
    print_header("TEST 4: ALGORITHM COMPARISON")

    print("\n Common Input (4 patients needing DOCTOR):")
    print("  1. Emergency-1 (HIGH priority,   45 min)")
    print("  2. Routine-1   (LOW priority,    30 min)")
    print("  3. Urgent-1    (MEDIUM priority, 60 min)")
    print("  4. Emergency-2 (HIGH priority,   20 min)")

    # Test each algorithm
    results = {}

    # FCFS
    rm1 = ResourceManager()
    rm1.initialize_default_resources()
    scheduler1 = FCFSScheduler()
    requests1 = [
        rm1.create_request("Emergency-1", ResourceType.DOCTOR, Priority.HIGH, 45),
        rm1.create_request("Routine-1", ResourceType.DOCTOR, Priority.LOW, 30),
        rm1.create_request("Urgent-1", ResourceType.DOCTOR, Priority.MEDIUM, 60),
        rm1.create_request("Emergency-2", ResourceType.DOCTOR, Priority.HIGH, 20),
    ]
    for req in requests1:
        scheduler1.add_request(req)
    results['FCFS'] = rm1.allocate_resources(scheduler1)

    # Priority
    rm2 = ResourceManager()
    rm2.initialize_default_resources()
    scheduler2 = PriorityScheduler()
    requests2 = [
        rm2.create_request("Emergency-1", ResourceType.DOCTOR, Priority.HIGH, 45),
        rm2.create_request("Routine-1", ResourceType.DOCTOR, Priority.LOW, 30),
        rm2.create_request("Urgent-1", ResourceType.DOCTOR, Priority.MEDIUM, 60),
        rm2.create_request("Emergency-2", ResourceType.DOCTOR, Priority.HIGH, 20),
    ]
    for req in requests2:
        scheduler2.add_request(req)
    results['Priority'] = rm2.allocate_resources(scheduler2)

    # Round Robin
    rm3 = ResourceManager()
    rm3.initialize_default_resources()
    scheduler3 = RoundRobinScheduler(time_quantum=30)
    requests3 = [
        rm3.create_request("Emergency-1", ResourceType.DOCTOR, Priority.HIGH, 45),
        rm3.create_request("Routine-1", ResourceType.DOCTOR, Priority.LOW, 30),
        rm3.create_request("Urgent-1", ResourceType.DOCTOR, Priority.MEDIUM, 60),
        rm3.create_request("Emergency-2", ResourceType.DOCTOR, Priority.HIGH, 20),
    ]
    for req in requests3:
        scheduler3.add_request(req)
    results['Round Robin'] = rm3.allocate_resources(scheduler3)

    # Display results
    print("\n RESULTS COMPARISON:\n")

    for alg_name, allocations in results.items():
        print(f"  {alg_name}:")
        if allocations:
            order = [req.patient_name for req, _ in allocations]
            print(f"    Order: {' → '.join(order)}")
        else:
            print("    ERROR: No allocations")
        print()


def test_resource_shortage():
    """Test when resources are limited"""
    print_header("TEST 5: RESOURCE SHORTAGE SCENARIO")

    rm = ResourceManager()
    rm.initialize_default_resources()
    scheduler = PriorityScheduler()

    # 10 requests for DOCTOR (only 8 available)
    print("\n INPUT:")
    print("  10 patients need DOCTOR, but only 8 doctors available\n")

    requests = []
    for i in range(1, 11):
        priority = Priority.HIGH if i <= 3 else Priority.MEDIUM if i <= 7 else Priority.LOW
        req = rm.create_request(f"Patient-{i}", ResourceType.DOCTOR, priority, 30)
        requests.append(req)
        print(f"  {i:2d}. Patient-{i} (Priority: {priority.name})")

    print("\n EXPECTED OUTPUT:")
    print("  Priority scheduler allocates to highest priority first:")
    print("  - Patient-1, Patient-2, Patient-3 (HIGH) get doctors")
    print("  - Patient-4 through Patient-8 (MEDIUM) get doctors")
    print("  - Patient-9, Patient-10 (LOW) remain in queue (insufficient resources)")

    for req in requests:
        scheduler.add_request(req)

    allocations = rm.allocate_resources(scheduler)

    print(f"\n ACTUAL OUTPUT:")
    print(f"  Allocated: {len(allocations)}/10 patients")
    for i, (req, res) in enumerate(allocations, 1):
        print(f"  {i:2d}. {req.patient_name} → {res.name} [{req.priority.name}]")

    print(f"\n  Waiting: {10 - len(allocations)} patients remain in queue")

    print("\n KEY INSIGHT:")
    print("  - When resources are scarce, priority scheduling ensures critical")
    print("    patients are served first")
    print("  - Lower priority patients must wait for resources to free up")


def main():
    """Run all tests"""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║         HEALTHCARE RESOURCE SCHEDULING ALGORITHM TEST SUITE                ║
║                                                                            ║
║  Demonstrates three scheduling algorithms with detailed examples:         ║
║    • First-Come-First-Served (FCFS)                                       ║
║    • Priority-Based Scheduling                                            ║
║    • Round Robin                                                           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)

    try:
        test_fcfs()
        test_priority()
        test_round_robin()
        test_comparison()
        test_resource_shortage()

        print("\n" + "=" * 80)
        print("  ALL TESTS COMPLETED")
        print("=" * 80)

    except Exception as e:
        print(f"\n\n ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
