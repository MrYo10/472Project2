# Hospital Resource Scheduler

A desktop GUI application demonstrating Operating System scheduling algorithms applied to healthcare resource management (Beds, Doctors, Operating Rooms).

## Project Overview

This project applies OS concepts including process scheduling, synchronization, and resource management to solve real-world healthcare challenges. The system implements three classic scheduling algorithms:

- **FCFS (First-Come-First-Served)**: Processes requests in order of arrival
- **Priority Scheduling**: Processes critical/emergency cases first
- **Round Robin**: Fair time-sharing with configurable time quantum

## Key OS Concepts Demonstrated

1. **Process Scheduling Algorithms**
   - FCFS, Priority-based, and Round Robin schedulers
   - Request queue management
   - Performance metrics (waiting time, turnaround time)

2. **Concurrency & Synchronization**
   - Threading locks for resource access
   - Semaphores for resource counting
   - Mutual exclusion to prevent race conditions

3. **Resource Management**
   - Thread-safe resource allocation
   - Deadlock prevention
   - Resource utilization tracking

4. **Real-time Monitoring**
   - Live resource status updates
   - Performance visualization
   - Statistics dashboard

## Project Structure

```
472Project 2/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── models/
│   ├── __init__.py
│   └── resource.py                  # Data models (Bed, Doctor, OR, Request)
├── schedulers/
│   ├── __init__.py
│   ├── base_scheduler.py            # Abstract scheduler interface
│   ├── fcfs_scheduler.py            # FCFS implementation
│   ├── priority_scheduler.py        # Priority scheduling implementation
│   └── round_robin_scheduler.py     # Round Robin implementation
├── core/
│   ├── __init__.py
│   └── resource_manager.py          # Thread-safe resource manager
├── gui/
│   ├── __init__.py
│   ├── main_window.py               # Main application window
│   ├── resource_panel.py            # Resource management UI
│   ├── scheduler_panel.py           # Scheduling interface
│   └── statistics_panel.py          # Statistics and visualization
└── verification/
    ├── __init__.py
    └── algorithm_verification.py    # Algorithm verification with toy examples
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download this project**

2. **Install dependencies**
   ```bash
   cd "472Project 2"
   pip install -r requirements.txt
   ```

   Note: Tkinter comes pre-installed with Python on most systems.

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Run algorithm verification** (optional)
   ```bash
   python verification/algorithm_verification.py
   ```

## Usage Guide

### 1. Resource Management Tab
- View all hospital resources (Beds, Doctors, Operating Rooms)
- Color-coded status:
  - Green: Available
  - Red: Occupied
  - Yellow: Maintenance
- Real-time status updates

### 2. Request Scheduling Tab
- Create new resource requests:
  - Enter patient name
  - Select resource type
  - Set priority level (Critical, High, Medium, Low)
  - Specify duration in minutes
- Choose scheduling algorithm:
  - FCFS
  - Priority
  - Round Robin
- Execute scheduling to allocate resources
- View pending request queue

### 3. Statistics & Analysis Tab
- Resource utilization statistics
- Scheduler performance metrics:
  - Total/completed requests
  - Average waiting time
  - Average turnaround time
- Visual utilization charts

## Scheduling Algorithms

### FCFS (First-Come-First-Served)
- **Strategy**: Process requests in arrival order
- **Pros**: Simple, fair in terms of arrival time
- **Cons**: No priority handling, convoy effect
- **Use case**: Routine appointments, non-urgent care

### Priority Scheduling
- **Strategy**: Process highest priority requests first
  - Priority levels: CRITICAL (1) > HIGH (2) > MEDIUM (3) > LOW (4)
- **Pros**: Emergency cases handled immediately
- **Cons**: Low-priority starvation possible
- **Use case**: Emergency departments, critical care

### Round Robin
- **Strategy**: Each request gets a time quantum (default: 30 minutes)
  - If duration > quantum, request is preempted and re-queued
- **Pros**: Fair allocation, prevents starvation
- **Cons**: Higher overhead, context switching
- **Use case**: Fair resource sharing, multi-patient care

## Algorithm Verification

Run the verification script to see algorithms in action with toy examples:

```bash
python verification/algorithm_verification.py
```

This demonstrates:
- Correct scheduling order for each algorithm
- Resource allocation behavior
- Time quantum handling (Round Robin)
- Priority precedence (Priority Scheduler)

## Features

- **User-friendly GUI**: Intuitive Tkinter interface
- **Real-time Updates**: Automatic resource status updates
- **Thread-safe Operations**: Locks and semaphores for concurrency
- **Performance Metrics**: Detailed scheduling statistics
- **Visual Analytics**: Charts showing resource utilization
- **Algorithm Comparison**: Test different schedulers side-by-side

## Technical Highlights

### Thread Safety
- `threading.Lock` for mutual exclusion
- `threading.Semaphore` for resource counting
- Atomic operations for resource allocation

### Data Structures
- Priority queue (heapq) for Priority Scheduler
- Deque for Round Robin ready queue
- Lists for FCFS queue

### Performance Metrics
- Waiting time: Time from arrival to allocation
- Turnaround time: Time from arrival to completion
- Resource utilization: Percentage of resources in use

## Future Enhancements

- Preemptive priority scheduling
- Multi-resource allocation (bed + doctor + OR)
- Historical data persistence
- Advanced analytics and reporting
- Emergency override functionality
- Resource reservation system

## Authors

[Your Name]
[Partner Name if applicable]

## Course Information

Operating Systems Course Project
Fall 2024

## License

This project is created for educational purposes.
