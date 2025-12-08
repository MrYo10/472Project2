import React, { useState } from "react";
import { createRequest } from "../api";

export default function RequestForm() {
  const [form, setForm] = useState({
    patient_name: "",
    resource_type: "Bed",
    priority: 2,
    duration: 30
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await createRequest(form);
    alert("Request submitted! ID = " + res.id);
  };

  return (
    <div>
      <h2>Create Request</h2>
      <form onSubmit={handleSubmit}>

        <input
          placeholder="Patient Name"
          value={form.patient_name}
          onChange={(e) => setForm({ ...form, patient_name: e.target.value })}
        />

        <select
          value={form.resource_type}
          onChange={(e) => setForm({ ...form, resource_type: e.target.value })}
        >
          <option>Bed</option>
          <option>Doctor</option>
          <option>Operating Room</option>
        </select>

        <select
          value={form.priority}
          onChange={(e) => setForm({ ...form, priority: parseInt(e.target.value) })}
        >
          <option value={1}>Critical</option>
          <option value={2}>High</option>
          <option value={3}>Medium</option>
          <option value={4}>Low</option>
        </select>

        <input
          type="number"
          placeholder="Duration (min)"
          value={form.duration}
          onChange={(e) => setForm({ ...form, duration: parseInt(e.target.value) })}
        />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}