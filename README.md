# Healthcare Resource Scheduling System

A full-stack web application that demonstrates and compares different scheduling algorithms for healthcare resource allocation. The system implements three classic CPU scheduling algorithms adapted for healthcare resource management: First-Come-First-Served (FCFS), Priority-Based Scheduling, and Round Robin.

## Project Overview

This project simulates a hospital resource management system where patients request healthcare resources (doctors, beds, equipment) and different scheduling algorithms determine the allocation order. It includes both a Python backend API and a React frontend for visualization and interaction.

## Features

- **Three Scheduling Algorithms:**
  - **FCFS (First-Come-First-Served):** Processes requests in arrival order
  - **Priority-Based:** Allocates resources based on patient priority levels (HIGH, MEDIUM, LOW)
  - **Round Robin:** Fair time-sharing with configurable time quantum

- **Resource Types:**
  - Doctors (8 available)
  - Beds (15 available)
  - Medical Equipment (10 available)

- **Full-Stack Application:**
  - FastAPI backend with RESTful endpoints
  - React frontend with real-time resource visualization
  - CORS-enabled for seamless frontend-backend communication

- **Comprehensive Testing:**
  - Standalone test suite demonstrating each algorithm
  - Input/output comparison for algorithm analysis

## Project Structure

```
472Project 2/
├── backend/                      # Python FastAPI backend
│   ├── core/
│   │   └── resource_manager.py   # Resource allocation engine
│   ├── models/
│   │   └── resource.py           # Data models (Request, Resource, enums)
│   ├── schedulers/
│   │   ├── base_scheduler.py     # Abstract scheduler interface
│   │   ├── fcfs_scheduler.py     # FCFS implementation
│   │   ├── priority_scheduler.py # Priority-based implementation
│   │   └── round_robin_scheduler.py # Round Robin implementation
│   └── main.py                   # FastAPI application & routes
│
├── scheduler-frontend/           # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── api.js               # API client
│   │   └── App.js               # Main application
│   └── package.json
│
├── test_schedulers.py            # Comprehensive test suite
└── requirements.txt              # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MrYo10/472Project2.git
   cd 472Project2
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   ```bash
   cd scheduler-frontend
   npm install
   cd ..
   ```

### Running the Application

#### Option 1: Run Both Frontend and Backend Together (VSCode)

If using VSCode, use the provided launch configuration:
1. Open the project in VSCode
2. Go to Run and Debug (Ctrl+Shift+D / Cmd+Shift+D)
3. Select "Run Frontend + Backend" from the dropdown
4. Press F5 or click the green play button

#### Option 2: Run Manually

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload
```
The backend will start on `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd scheduler-frontend
npm start
```
The frontend will start on `http://localhost:3000`

### Running Tests

Run the comprehensive test suite to see all algorithms in action:

```bash
python test_schedulers.py
```

This will execute 5 test scenarios:
1. FCFS Scheduler demonstration
2. Priority Scheduler demonstration
3. Round Robin Scheduler demonstration
4. Algorithm comparison with identical inputs
5. Resource shortage scenario

## API Endpoints

### POST `/request`
Add a new patient request to the queue.

**Request Body:**
```json
{
  "patient_name": "John Doe",
  "resource_type": "doctor",
  "priority": 3,
  "duration": 30
}
```

**Priority Levels:**
- `1` = LOW
- `2` = MEDIUM
- `3` = HIGH

**Resource Types:**
- `"doctor"`
- `"bed"`
- `"equipment"`

### POST `/schedule/{alg}`
Execute scheduling algorithm and allocate resources.

**Parameters:**
- `alg`: Algorithm to use (`fcfs`, `priority`, or `rr`)

**Response:**
```json
{
  "scheduler": "Priority-Based Scheduler",
  "allocations": [
    {
      "patient": "John Doe",
      "resource": "Dr. Smith",
      "resource_type": "doctor",
      "duration": 30
    }
  ]
}
```

### GET `/resources`
Get current status of all resources.

### GET `/queue`
Get all pending requests in the queue.

## Algorithm Comparison

| Algorithm | Advantages | Disadvantages | Best Use Case |
|-----------|-----------|---------------|---------------|
| **FCFS** | Simple, fair arrival order | Ignores urgency | Non-emergency scenarios |
| **Priority** | Critical cases first | Low-priority starvation | Emergency departments |
| **Round Robin** | Fair time distribution | Context switching overhead | Balanced workloads |

## Technologies Used

**Backend:**
- Python 3.x
- FastAPI - Modern web framework
- Pydantic - Data validation
- Uvicorn - ASGI server

**Frontend:**
- React 19.x
- React Scripts
- JavaScript (ES6+)

## Development

### Backend Development
The backend uses FastAPI with hot-reload enabled:
```bash
cd backend
uvicorn main:app --reload
```

### Frontend Development
React development server with hot-reload:
```bash
cd scheduler-frontend
npm start
```

## Example Usage

1. Start both backend and frontend
2. Open `http://localhost:3000` in your browser
3. Add patient requests through the UI
4. Select a scheduling algorithm (FCFS, Priority, or Round Robin)
5. View resource allocations and compare algorithm performance

