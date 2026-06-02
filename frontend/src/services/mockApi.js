const delay = (value, timeout = 180) => new Promise((resolve) => setTimeout(() => resolve(value), timeout));

const directories = [
  { id: 1, name: 'Dataset Skripsi', path: '/home/research/fim-dataset', status: 'Active', files: 1284, algorithm: 'SHA-256', lastScan: '2026-06-02 09:45' },
  { id: 2, name: 'Config Server', path: '/etc/research-app', status: 'Active', files: 312, algorithm: 'Argon2id', lastScan: '2026-06-02 08:20' },
  { id: 3, name: 'Sample Malware Lab', path: '/home/research/lab-sample', status: 'Inactive', files: 96, algorithm: 'PBKDF2', lastScan: '2026-06-01 21:12' },
];

const verificationResults = [
  { id: 1, event: 'MODIFIED', path: 'config/app.yaml', severity: 'HIGH', status: 'OPEN', checkedAt: '2026-06-02 09:45', previousHash: 'a8f3c1...', currentHash: 'c42bf0...' },
  { id: 2, event: 'ADDED', path: 'uploads/report-new.pdf', severity: 'MEDIUM', status: 'OPEN', checkedAt: '2026-06-02 09:45', previousHash: '-', currentHash: 'f9d002...' },
  { id: 3, event: 'DELETED', path: 'docs/archive.txt', severity: 'HIGH', status: 'OPEN', checkedAt: '2026-06-02 09:45', previousHash: 'bb817a...', currentHash: '-' },
  { id: 4, event: 'UNCHANGED', path: 'README.md', severity: 'INFO', status: 'RESOLVED', checkedAt: '2026-06-02 09:45', previousHash: 'ef67ac...', currentHash: 'ef67ac...' },
];

const benchmarkResults = [
  { algorithm: 'SHA-256', totalTime: 824, average: 0.64, throughput: 182.4, files: 1284, color: 'bg-sky-400' },
  { algorithm: 'PBKDF2', totalTime: 12840, average: 10.0, throughput: 12.8, files: 1284, color: 'bg-violet-400' },
  { algorithm: 'Argon2id', totalTime: 24320, average: 18.9, throughput: 6.7, files: 1284, color: 'bg-emerald-400' },
];

const logs = [
  { id: 1, time: '2026-06-02 09:45:11', type: 'VERIFICATION', event: 'MODIFIED', message: 'config/app.yaml hash changed from baseline.', severity: 'HIGH' },
  { id: 2, time: '2026-06-02 09:45:10', type: 'VERIFICATION', event: 'ADDED', message: 'uploads/report-new.pdf was not present in baseline.', severity: 'MEDIUM' },
  { id: 3, time: '2026-06-02 09:44:58', type: 'BASELINE', event: 'COMPLETED', message: 'Baseline generated for Dataset Skripsi.', severity: 'INFO' },
  { id: 4, time: '2026-06-02 09:30:02', type: 'BENCHMARK', event: 'COMPLETED', message: 'Benchmark completed for 3 algorithms.', severity: 'INFO' },
];

export const mockApi = {
  getDashboard: () => delay({
    metrics: [
      { label: 'Active Directories', value: '2', trend: '+1 this week', tone: 'cyan' },
      { label: 'Baseline Files', value: '1,692', trend: 'SHA-256 default', tone: 'green' },
      { label: 'Open Alerts', value: '3', trend: '2 high severity', tone: 'red' },
      { label: 'Last Verification', value: '09:45', trend: 'June 2, 2026', tone: 'amber' },
    ],
    integrity: { unchanged: 1241, modified: 1, added: 1, deleted: 1, error: 0 },
    recentEvents: verificationResults.slice(0, 3),
    benchmarks: benchmarkResults,
  }),
  getDirectories: () => delay(directories),
  getVerificationResults: () => delay(verificationResults),
  getBenchmarkResults: () => delay(benchmarkResults),
  getLogs: () => delay(logs),
  getSettings: () => delay({
    defaultAlgorithm: 'SHA-256',
    pbkdf2Iterations: 100000,
    argon2Memory: 65536,
    argon2TimeCost: 3,
    scanHiddenFiles: true,
    maxFileSizeMb: 100,
  }),
};
