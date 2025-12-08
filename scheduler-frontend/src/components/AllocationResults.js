export default function AllocationResults({ allocations }) {
  if (!allocations.length) return <p>No allocations yet.</p>;

  return (
    <div>
      <h2>Scheduling Output</h2>
      {allocations.map((a, i) => (
        <p key={i}>
          <strong>{a.patient}</strong> → {a.resource} ({a.resource_type})
        </p>
      ))}
    </div>
  );
}