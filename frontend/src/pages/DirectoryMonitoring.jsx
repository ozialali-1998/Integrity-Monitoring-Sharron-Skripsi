import DataTable from '../components/DataTable.jsx';
import PageHeader from '../components/PageHeader.jsx';
import StatusBadge from '../components/StatusBadge.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { useDirectories } from '../hooks/useFimData.js';

export default function DirectoryMonitoring() {
  const { data: directories = [], loading, error } = useDirectories();

  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'path', label: 'Absolute Path' },
    { key: 'status', label: 'Status' },
    { key: 'files', label: 'Files' },
    { key: 'algorithm', label: 'Algorithm' },
    { key: 'lastScan', label: 'Last Scan' },
  ];

  return (
    <>
      <ErrorBanner error={error} />
      <PageHeader title="Directory Monitoring" subtitle="Manage monitored directories and validate local backend-accessible paths." action={<button className="cyber-button">Add Directory</button>} />
      <section className="mb-6 grid gap-4 lg:grid-cols-[1fr_220px_160px]">
        <input className="cyber-input" placeholder="Search directory name or path..." />
        <select className="cyber-input"><option>All Status</option><option>Active</option><option>Inactive</option></select>
        <button className="cyber-button-secondary">Apply Filter</button>
      </section>
      {loading ? <div className="cyber-card">Loading directories...</div> : <DataTable
        columns={columns}
        rows={directories}
        renderCell={(row, key) => {
          if (key === 'status') return <StatusBadge value={row.status} />;
          if (key === 'path') return <span className="font-mono text-xs text-cyber-cyan">{row.path}</span>;
          return row[key];
        }}
      />}
      <section className="mt-6 cyber-card">
        <h2 className="text-lg font-bold">Add / Edit Directory</h2>
        <div className="mt-4 grid gap-4 lg:grid-cols-3">
          <input className="cyber-input" placeholder="Directory name" />
          <input className="cyber-input lg:col-span-2" placeholder="/absolute/path/to/monitor" />
          <input className="cyber-input lg:col-span-3" placeholder="Description for research context" />
        </div>
        <div className="mt-4 flex gap-3"><button className="cyber-button-secondary">Validate Path</button><button className="cyber-button">Save Directory</button></div>
      </section>
    </>
  );
}
