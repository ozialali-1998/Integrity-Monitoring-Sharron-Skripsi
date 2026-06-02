export default function PageHeader({ title, subtitle, action }) {
  return (
    <div className="mb-6 flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-cyber-cyan">FIM Security Monitor</p>
        <h1 className="mt-2 text-3xl font-bold text-cyber-text">{title}</h1>
        <p className="mt-1 text-sm text-cyber-muted">{subtitle}</p>
      </div>
      {action}
    </div>
  );
}
