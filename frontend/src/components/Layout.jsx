const navItems = ['Dashboard', 'Directory Monitoring', 'Verification', 'Benchmark', 'Logs', 'Settings'];

export default function Layout({ currentPage, onNavigate, children }) {
  return (
    <div className="min-h-screen text-cyber-text">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-72 border-r border-cyber-border bg-slate-950/80 p-5 backdrop-blur-xl lg:block">
        <div className="mb-8 rounded-2xl border border-cyber-cyan/30 bg-cyber-cyan/10 p-4">
          <div className="text-lg font-bold text-cyber-text">FIM Security</div>
          <div className="text-sm text-cyber-muted">Integrity Monitoring</div>
        </div>
        <nav className="space-y-2">
          {navItems.map((item) => (
            <button
              key={item}
              onClick={() => onNavigate(item)}
              className={`w-full rounded-xl px-4 py-3 text-left text-sm font-semibold transition ${
                currentPage === item
                  ? 'bg-cyber-cyan text-slate-950 shadow-glow'
                  : 'text-cyber-muted hover:bg-cyber-elevated hover:text-cyber-text'
              }`}
            >
              {item}
            </button>
          ))}
        </nav>
      </aside>
      <div className="lg:pl-72">
        <header className="sticky top-0 z-10 border-b border-cyber-border bg-slate-950/70 px-5 py-4 backdrop-blur-xl lg:px-8">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex flex-wrap gap-2 lg:hidden">
              {navItems.map((item) => (
                <button
                  key={item}
                  onClick={() => onNavigate(item)}
                  className={`rounded-full px-3 py-1.5 text-xs font-semibold ${currentPage === item ? 'bg-cyber-cyan text-slate-950' : 'bg-cyber-panel text-cyber-muted'}`}
                >
                  {item}
                </button>
              ))}
            </div>
            <div className="text-sm text-cyber-muted">Research Console / <span className="text-cyber-text">{currentPage}</span></div>
            <div className="flex items-center gap-3 text-sm text-cyber-muted">
              <span className="h-2 w-2 rounded-full bg-cyber-green shadow-[0_0_16px_rgba(34,197,94,0.9)]" />
              Mock API Online · Last refresh 09:45 UTC
            </div>
          </div>
        </header>
        <main className="px-5 py-8 lg:px-8">{children}</main>
      </div>
    </div>
  );
}
