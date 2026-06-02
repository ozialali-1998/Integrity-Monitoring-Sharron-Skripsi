import DataTable from '../components/DataTable.jsx';
import PageHeader from '../components/PageHeader.jsx';
import StatusBadge from '../components/StatusBadge.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { useLogs } from '../hooks/useFimData.js';

export default function Logs() {
  const { data: logs = [], loading, error } = useLogs();

  return (
    <>
      <ErrorBanner error={error} />
      <PageHeader title="Logs" subtitle="Audit trail for baseline generation, verification events, and benchmark activity." action={<button className="cyber-button-secondary">Export Logs</button>} />
      <section className="mb-6 grid gap-4 lg:grid-cols-[1fr_180px_180px_160px]">
        <input className="cyber-input" placeholder="Search path, event, or message..." />
        <select className="cyber-input"><option>All Types</option><option>VERIFICATION</option><option>BASELINE</option><option>BENCHMARK</option></select>
        <select className="cyber-input"><option>All Severity</option><option>HIGH</option><option>MEDIUM</option><option>INFO</option></select>
        <button className="cyber-button-secondary">Apply</button>
      </section>
      {loading ? <div className="cyber-card">Loading logs...</div> : <DataTable
        columns={[{ key: 'time', label: 'Time' }, { key: 'type', label: 'Type' }, { key: 'event', label: 'Event' }, { key: 'severity', label: 'Severity' }, { key: 'message', label: 'Message' }]}
        rows={logs}
        renderCell={(row, key) => (key === 'severity' || ['MODIFIED', 'ADDED', 'DELETED'].includes(row[key]) ? <StatusBadge value={row[key]} /> : row[key])}
      />}
    </>
  );
}
