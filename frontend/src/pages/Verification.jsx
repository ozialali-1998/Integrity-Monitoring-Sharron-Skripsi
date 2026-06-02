import DataTable from '../components/DataTable.jsx';
import MetricCard from '../components/MetricCard.jsx';
import PageHeader from '../components/PageHeader.jsx';
import StatusBadge from '../components/StatusBadge.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { useVerificationResults } from '../hooks/useFimData.js';

export default function Verification() {
  const { data: rows = [], loading, error } = useVerificationResults();

  const counts = {
    unchanged: rows.filter((row) => row.event === 'UNCHANGED').length,
    modified: rows.filter((row) => row.event === 'MODIFIED').length,
    added: rows.filter((row) => row.event === 'ADDED').length,
    deleted: rows.filter((row) => row.event === 'DELETED').length,
  };

  return (
    <>
      <ErrorBanner error={error} />
      <PageHeader title="Verification" subtitle="Run integrity checks and investigate modified, added, or deleted files." action={<button className="cyber-button">Run Verification</button>} />
      <section className="mb-6 cyber-card">
        <div className="grid gap-4 lg:grid-cols-[1fr_1fr_180px]">
          <select className="cyber-input"><option>Dataset Skripsi</option><option>Config Server</option></select>
          <select className="cyber-input"><option>Latest baseline · SHA-256</option><option>Argon2id baseline</option></select>
          <button className="cyber-button">Start Check</button>
        </div>
      </section>
      <section className="mb-6 grid gap-4 md:grid-cols-4">
        <MetricCard label="Unchanged" value={counts.unchanged} trend="safe" tone="green" />
        <MetricCard label="Modified" value={counts.modified} trend="review" tone="red" />
        <MetricCard label="Added" value={counts.added} trend="new files" tone="amber" />
        <MetricCard label="Deleted" value={counts.deleted} trend="missing" tone="red" />
      </section>
      {loading ? <div className="cyber-card">Loading verification results...</div> : <DataTable
        columns={[{ key: 'event', label: 'Event' }, { key: 'path', label: 'Relative Path' }, { key: 'severity', label: 'Severity' }, { key: 'status', label: 'Status' }, { key: 'checkedAt', label: 'Checked At' }, { key: 'currentHash', label: 'Current Hash' }]}
        rows={rows}
        renderCell={(row, key) => (['event', 'severity', 'status'].includes(key) ? <StatusBadge value={row[key]} /> : <span className={key.includes('Hash') || key === 'path' ? 'font-mono text-xs' : ''}>{row[key]}</span>)}
      />}
    </>
  );
}
