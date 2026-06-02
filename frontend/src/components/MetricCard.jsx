const toneMap = {
  cyan: 'from-cyan-400/20 to-sky-500/5 text-cyan-300',
  green: 'from-emerald-400/20 to-green-500/5 text-emerald-300',
  red: 'from-red-400/20 to-rose-500/5 text-red-300',
  amber: 'from-amber-400/20 to-orange-500/5 text-amber-300',
};

export default function MetricCard({ label, value, trend, tone = 'cyan' }) {
  return (
    <div className="cyber-card overflow-hidden">
      <div className={`-m-5 mb-4 h-1 bg-gradient-to-r ${toneMap[tone] ?? toneMap.cyan}`} />
      <p className="text-sm text-cyber-muted">{label}</p>
      <div className="mt-3 flex items-end justify-between gap-3">
        <h3 className="text-3xl font-bold text-cyber-text">{value}</h3>
        <span className={`text-xs font-semibold ${toneMap[tone]?.split(' ').at(-1) ?? 'text-cyan-300'}`}>{trend}</span>
      </div>
    </div>
  );
}
