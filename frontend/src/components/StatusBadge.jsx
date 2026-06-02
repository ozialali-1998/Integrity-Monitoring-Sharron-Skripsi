const toneMap = {
  Active: 'border-emerald-400/40 bg-emerald-400/10 text-emerald-300',
  Inactive: 'border-slate-400/30 bg-slate-400/10 text-slate-300',
  OPEN: 'border-red-400/40 bg-red-400/10 text-red-300',
  RESOLVED: 'border-emerald-400/40 bg-emerald-400/10 text-emerald-300',
  HIGH: 'border-red-400/40 bg-red-400/10 text-red-300',
  MEDIUM: 'border-amber-400/40 bg-amber-400/10 text-amber-300',
  INFO: 'border-sky-400/40 bg-sky-400/10 text-sky-300',
  MODIFIED: 'border-red-400/40 bg-red-400/10 text-red-300',
  ADDED: 'border-amber-400/40 bg-amber-400/10 text-amber-300',
  DELETED: 'border-red-400/40 bg-red-400/10 text-red-300',
  UNCHANGED: 'border-emerald-400/40 bg-emerald-400/10 text-emerald-300',
};

export default function StatusBadge({ value }) {
  return (
    <span className={`inline-flex rounded-full border px-2.5 py-1 text-xs font-semibold ${toneMap[value] ?? toneMap.INFO}`}>
      {value}
    </span>
  );
}
