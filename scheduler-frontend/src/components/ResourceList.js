import React, { useEffect, useState } from "react";
import { getResources } from "../api";
import "../css/ResourceList.css";

export default function ResourceList() {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    refresh();
  }, []);

  const refresh = async () => {
    const data = await getResources();
    setResources(data);
  };

  return (
    <div className="resource-panel">
      <h2>Hospital Resources</h2>
      <button className="refresh-btn" onClick={refresh}>Refresh</button>

      <div className="resource-grid">
        {resources.map((res) => (
          <div key={res.id} className={`resource-card ${res.status}`}>
            <h3>{res.name}</h3>
            <p>Type: {res.type}</p>
            <p>Status: <span className={`status-${res.status}`}>{res.status}</span></p>
          </div>
        ))}
      </div>
    </div>
  );
}