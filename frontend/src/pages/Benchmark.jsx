import DataTable from '../components/DataTable.jsx';
import PageHeader from '../components/PageHeader.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { useBenchmarkResults } from '../hooks/useFimData.js';

export default function Benchmark() {
  const { data: rows = [], loading, error } = useBenchmarkResults();
  const maxTime = Math.max(...rows.map((row) => row.totalTime), 1);

  return (
    <>
      <ErrorBanner error={error} />
      <PageHeader title="Benchmark" subtitle="Compare SHA-256, PBKDF2, and Argon2id performance for thesis research data." action={<button className="cyber-button">Run Benchmark</button>} />
      <section className="mb-6 cyber-card">
        <h2 className="text-lg font-bold">Benchmark Configuration</h2>
        <div className="mt-4 grid gap-4 lg:grid-cols-3">
          <select className="cyber-input"><option>Dataset Skripsi</option><option>Config Server</option></select>
          <input className="cyber-input" defaultValue="PBKDF2 iterations: 100000" />
          <input className="cyber-input" defaultValue="Argon2id memory: 65536 KiB" />
        </div>
        <div className="mt-4 flex flex-wrap gap-3 text-sm text-cyber-muted">
          <label><input type="checkbox" defaultChecked className="mr-2" />SHA-256</label>
          <label><input type="checkbox" defaultChecked className="mr-2" />PBKDF2</label>
          <label><input type="checkbox" defaultChecked className="mr-2" />Argon2id</label>
        </div>
      </section>
      {loading ? <div className="cyber-card">Loading benchmark results...</div> : <section className="mb-6 grid gap-4 lg:grid-cols-3">
        {rows.map((row) => (
          <div key={row.algorithm} className="cyber-card">
            <div className="mb-4 flex items-center gap-2"><span className={`h-3 w-3 rounded-full ${row.color}`} />{row.algorithm}</div>
            <div className="text-3xl font-bold">{row.totalTime.toLocaleString()} ms</div>
            <div className="mt-2 text-sm text-cyber-muted">{row.average} ms/file · {row.throughput} MB/s</div>
            <div className="mt-4 h-2 rounded-full bg-slate-800"><div className={`h-2 rounded-full ${row.color}`} style={{ width: `${(row.totalTime / maxTime) * 100}%` }} /></div>
          </div>
        ))}
      </section>}
      <DataTable columns={[{ key: 'algorithm', label: 'Algorithm' }, { key: 'totalTime', label: 'Total Time (ms)' }, { key: 'average', label: 'Avg/File (ms)' }, { key: 'throughput', label: 'Throughput MB/s' }, { key: 'files', label: 'Files' }]} rows={rows} />
    </>
  );
}
