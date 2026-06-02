import apiClient from './apiClient.js';
import { mockApi } from './mockApi.js';

const normalizeDirectory = (directory) => ({
  id: directory.id,
  name: directory.name,
  path: directory.path,
  status: directory.is_active === 0 ? 'Inactive' : 'Active',
  files: directory.total_files ?? directory.files ?? 0,
  algorithm: directory.algorithm ?? 'SHA-256',
  lastScan: directory.updated_at ?? directory.lastScan ?? '-',
});

const normalizeVerificationLog = (log) => ({
  id: log.id,
  event: log.event_type ?? log.event,
  path: log.relative_path ?? log.path,
  severity: log.severity,
  status: log.status,
  checkedAt: log.checked_at ?? log.checkedAt,
  previousHash: log.previous_hash ?? log.previousHash ?? '-',
  currentHash: log.current_hash ?? log.currentHash ?? '-',
});

const normalizeBenchmark = (result) => ({
  id: result.id,
  algorithm: result.algorithm,
  totalTime: result.total_duration_ms ?? result.totalTime ?? 0,
  average: result.average_duration_ms ?? result.average ?? 0,
  throughput: result.throughput_mb_per_sec ?? result.throughput ?? 0,
  files: result.total_files ?? result.files ?? 0,
  verificationTime: result.verification_duration_ms ?? result.verificationTime ?? 0,
  accuracy: result.accuracy_percent ?? result.accuracy ?? null,
  averageCpu: result.average_cpu_percent ?? result.averageCpu ?? null,
  maxCpu: result.max_cpu_percent ?? result.maxCpu ?? null,
  memoryPeakBytes: result.memory_peak_bytes ?? result.memoryPeakBytes ?? null,
  color: result.algorithm === 'PBKDF2' ? 'bg-violet-400' : result.algorithm === 'Argon2id' ? 'bg-emerald-400' : 'bg-sky-400',
});

const normalizeLog = (log) => ({
  id: log.id,
  time: log.checked_at ?? log.created_at ?? log.time,
  type: log.activity_type ?? 'VERIFICATION',
  event: log.event_type ?? log.event,
  message: log.message ?? `${log.relative_path ?? log.path} status: ${log.event_type ?? log.event}`,
  severity: log.severity ?? 'INFO',
});

const normalizeSettings = (settings) => {
  if (!Array.isArray(settings)) return settings;
  const values = Object.fromEntries(settings.map((item) => [item.setting_key, item.setting_value]));
  return {
    defaultAlgorithm: values.default_hash_algorithm ?? 'SHA-256',
    pbkdf2Iterations: Number(values.pbkdf2_iterations ?? 100000),
    argon2Memory: Number(values.argon2id_memory_cost ?? 65536),
    argon2TimeCost: Number(values.argon2id_time_cost ?? 3),
    scanHiddenFiles: values.scan_hidden_files !== 'false',
    maxFileSizeMb: Number(values.max_file_size_mb ?? 100),
  };
};

export const fimApi = {
  async getDashboard() {
    const [directories, logs, benchmarks] = await Promise.all([
      this.getDirectories(),
      this.getVerificationResults(),
      this.getBenchmarkResults(),
    ]);
    const activeDirectories = directories.filter((directory) => directory.status === 'Active').length;
    const openAlerts = logs.filter((log) => log.status === 'OPEN' && log.event !== 'UNCHANGED').length;
    return {
      metrics: [
        { label: 'Active Directories', value: String(activeDirectories), trend: `${directories.length} configured`, tone: 'cyan' },
        { label: 'Baseline Files', value: directories.reduce((total, directory) => total + Number(directory.files || 0), 0).toLocaleString(), trend: 'from backend', tone: 'green' },
        { label: 'Open Alerts', value: String(openAlerts), trend: 'needs review', tone: openAlerts > 0 ? 'red' : 'green' },
        { label: 'Last Verification', value: logs[0]?.checkedAt?.slice(11, 16) ?? '-', trend: logs[0]?.checkedAt ?? 'no runs yet', tone: 'amber' },
      ],
      integrity: {
        unchanged: logs.filter((log) => log.event === 'UNCHANGED').length,
        modified: logs.filter((log) => log.event === 'MODIFIED').length,
        added: logs.filter((log) => log.event === 'ADDED').length,
        deleted: logs.filter((log) => log.event === 'DELETED').length,
        error: logs.filter((log) => log.event === 'ERROR').length,
      },
      recentEvents: logs.filter((log) => log.event !== 'UNCHANGED').slice(0, 3),
      benchmarks,
    };
  },

  async getDirectories() {
    const { data } = await apiClient.get('/directories');
    return data.map(normalizeDirectory);
  },

  async createDirectory(payload) {
    const { data } = await apiClient.post('/directories', payload);
    return normalizeDirectory(data);
  },

  async getVerificationResults() {
    const { data } = await apiClient.get('/logs');
    return data.map(normalizeVerificationLog);
  },

  async runVerification(payload) {
    const { data } = await apiClient.post('/verifications/run', payload);
    return data;
  },

  async getBenchmarkResults() {
    const { data } = await apiClient.get('/benchmarks');
    return data.map(normalizeBenchmark);
  },

  async runBenchmark(payload) {
    const { data } = await apiClient.post('/benchmarks/run', payload);
    return data.map(normalizeBenchmark);
  },

  async getLogs() {
    const { data } = await apiClient.get('/logs');
    return data.map(normalizeLog);
  },

  async getSettings() {
    const { data } = await apiClient.get('/settings');
    return normalizeSettings(data);
  },
};

export const fallbackApi = mockApi;
