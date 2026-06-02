import DataTable from '../components/DataTable.jsx';
import MetricCard from '../components/MetricCard.jsx';
import PageHeader from '../components/PageHeader.jsx';
import StatusBadge from '../components/StatusBadge.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { useDashboard } from '../hooks/useFimData.js';

export default function Dashboard() {
  const { data, loading, error } = useDashboard();

  if (loading) return <div className="cyber-card">Loading dashboard...</div>;
  if (!data) return <div className="cyber-card">Unable to load dashboard data.</div>;

  const integrityTotal = Object.values(data.integrity).reduce((total, value) => total + value, 0);
  const eventColumns = [
    { key: 'event', label: 'Event' },
    { key: 'path', label: 'Path' },
    { key: 'severity', label: 'Severity' },
    { key: 'status', label: 'Status' },
  ];

  return (
    <>
      <ErrorBanner error={error} />
      <PageHeader
        title="Dashboard"
        subtitle="Real-time overview for file integrity status, alerts, and hashing benchmark snapshots."
        action={<button className="cyber-button">Run Verification</button>}
      />
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {data.metrics.map((metric) => <MetricCard key={metric.label} {...metric} />)}
      </section>
      <section className="mt-6 grid gap-6 xl:grid-cols-[1fr_1.2fr]">
        <div className="cyber-card">
          <h2 className="text-lg font-bold">Integrity Status</h2>
          <p className="mt-1 text-sm text-cyber-muted">Distribution from latest verification run.</p>
          <div className="mt-6 space-y-4">
            {Object.entries(data.integrity).map(([key, value]) => (
              <div key={key}>
                <div className="mb-2 flex justify-between text-sm">
                  <span className="capitalize text-cyber-muted">{key}</span>
                  <span className="font-semibold text-cyber-text">{value}</span>
                </div>
                <div className="h-2 rounded-full bg-slate-800">
                  <div className="h-2 rounded-full bg-cyber-cyan" style={{ width: `${Math.max((value / integrityTotal) * 100, 2)}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="cyber-card">
          <h2 className="mb-4 text-lg font-bold">Recent Security Events</h2>
          <DataTable
            columns={eventColumns}
            rows={data.recentEvents}
            renderCell={(row, key) => (['event', 'severity', 'status'].includes(key) ? <StatusBadge value={row[key]} /> : <span className="font-mono text-sm">{row[key]}</span>)}
          />
        </div>
      </section>
      <section className="mt-6 cyber-card">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold">Benchmark Snapshot</h2>
            <p className="text-sm text-cyber-muted">Mock comparison from latest SHA-256, PBKDF2, and Argon2id benchmark.</p>
          </div>
          <button className="cyber-button-secondary">View Benchmark</button>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {data.benchmarks.map((item) => (
            <div key={item.algorithm} className="rounded-2xl border border-cyber-border bg-slate-950/40 p-4">
              <div className="mb-3 flex items-center gap-2"><span className={`h-3 w-3 rounded-full ${item.color}`} />{item.algorithm}</div>
              <div className="text-2xl font-bold">{item.totalTime.toLocaleString()} ms</div>
              <div className="text-sm text-cyber-muted">{item.throughput} MB/s throughput</div>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
