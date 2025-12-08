import React, { useState } from "react";
import RequestForm from "./components/RequestForm";
import SchedulePanel from "./components/SchedulePanel";
import AllocationResults from "./components/AllocationResults";
import ResourceList from "./components/ResourceList";
import "./App.css";

function App() {
  const [allocations, setAllocations] = useState([]);

  return (
    <div className="container">
      <h1>Hospital Resource Scheduler</h1>
      <div className="dashboard">
        <div className="panel">
          <RequestForm />
        </div>
        <div className="panel">
          <SchedulePanel setAllocations={setAllocations} />
        </div>
      </div>
      <div className="tables">
        <AllocationResults allocations={allocations} />
        <ResourceList />
      </div>
    </div>
  );
}

export default App;