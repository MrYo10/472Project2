import React from "react";
import { runScheduler } from "../api";

export default function SchedulePanel({ setAllocations }) {
  const run = async (alg) => {
    const res = await runScheduler(alg);
    setAllocations(res.allocations || []);
  };

  return (
    <div>
      <h2>Run Scheduler</h2>

      <button onClick={() => run("fcfs")}>FCFS</button>
      <button onClick={() => run("priority")}>Priority</button>
      <button onClick={() => run("rr")}>Round Robin</button>
    </div>
  );
}