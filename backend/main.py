from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.resource_manager import ResourceManager
from schedulers.fcfs_scheduler import FCFSScheduler
from schedulers.priority_scheduler import PriorityScheduler
from schedulers.round_robin_scheduler import RoundRobinScheduler
from models.resource import ResourceType, Priority, Request

app = FastAPI()

# Allow React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rm = ResourceManager()
rm.initialize_default_resources()

# Store *pending* requests here
pending_requests: list[Request] = []


class RequestInput(BaseModel):
    patient_name: str
    resource_type: str
    priority: int
    duration: int


@app.post("/request")
def add_request(data: RequestInput):
    req = rm.create_request(
        data.patient_name,
        ResourceType(data.resource_type),
        Priority(data.priority),
        data.duration
    )

    # Save request in our pending queue
    pending_requests.append(req)

    return {"message": "Request added", "id": req.id}


@app.post("/schedule/{alg}")
def schedule(alg: str):
    # Pick scheduler
    if alg == "fcfs":
        scheduler = FCFSScheduler()
    elif alg == "priority":
        scheduler = PriorityScheduler()
    elif alg == "rr":
        scheduler = RoundRobinScheduler(time_quantum=20)
    else:
        return {"error": "Invalid algorithm"}

    # Add all pending requests to scheduler
    for req in pending_requests:
        scheduler.add_request(req)

    # Run algorithm
    allocations = rm.allocate_resources(scheduler)

    # Remove allocated ones from pending queue
    allocated_ids = [req.id for req, _ in allocations]
    remaining = [req for req in pending_requests if req.id not in allocated_ids]
    pending_requests.clear()
    pending_requests.extend(remaining)

    return {
        "scheduler": scheduler.name,
        "allocations": [
            {
                "patient": req.patient_name,
                "resource": res.name,
                "resource_type": res.resource_type.value,
                "duration": req.duration,
            }
            for req, res in allocations
        ]
    }


@app.get("/resources")
def get_resources():
    result = []
    for rtype, rlist in rm.resources.items():
        for res in rlist:
            result.append({
                "id": res.id,
                "name": res.name,
                "type": res.resource_type.value,
                "status": res.status.value
            })
    return result


@app.get("/queue")
def get_queue():
    return [
        {
            "id": req.id,
            "patient": req.patient_name,
            "resource_type": req.resource_type.value,
            "priority": req.priority.value,
            "duration": req.duration
        }
        for req in pending_requests
    ]