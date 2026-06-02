import PageHeader from '../components/PageHeader.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { useSettings } from '../hooks/useFimData.js';

export default function Settings() {
  const { data: settings, loading, error } = useSettings();

  if (loading) return <div className="cyber-card">Loading settings...</div>;
  if (!settings) return <div className="cyber-card">Unable to load settings.</div>;

  return (
    <>
      <ErrorBanner error={error} />
      <PageHeader title="Settings" subtitle="Configure mock defaults for hashing, scanning, and benchmark behavior." action={<button className="cyber-button">Save Changes</button>} />
      <section className="grid gap-6 xl:grid-cols-2">
        <div className="cyber-card">
          <h2 className="text-lg font-bold">Hashing Defaults</h2>
          <div className="mt-4 space-y-4">
            <label className="block text-sm text-cyber-muted">Default Algorithm<select className="cyber-input mt-2" defaultValue={settings.defaultAlgorithm}><option>SHA-256</option><option>PBKDF2</option><option>Argon2id</option></select></label>
            <label className="block text-sm text-cyber-muted">PBKDF2 Iterations<input className="cyber-input mt-2" defaultValue={settings.pbkdf2Iterations} /></label>
            <label className="block text-sm text-cyber-muted">Argon2id Memory Cost<input className="cyber-input mt-2" defaultValue={settings.argon2Memory} /></label>
            <label className="block text-sm text-cyber-muted">Argon2id Time Cost<input className="cyber-input mt-2" defaultValue={settings.argon2TimeCost} /></label>
          </div>
        </div>
        <div className="cyber-card">
          <h2 className="text-lg font-bold">Scanning Preferences</h2>
          <div className="mt-4 space-y-4">
            <label className="flex items-center justify-between rounded-xl border border-cyber-border p-4 text-sm text-cyber-muted">
              Scan hidden files
              <input type="checkbox" defaultChecked={settings.scanHiddenFiles} />
            </label>
            <label className="block text-sm text-cyber-muted">Max File Size MB<input className="cyber-input mt-2" defaultValue={settings.maxFileSizeMb} /></label>
            <label className="block text-sm text-cyber-muted">Excluded Extensions<input className="cyber-input mt-2" placeholder=".tmp, .bak, .cache" /></label>
          </div>
        </div>
      </section>
    </>
  );
}
