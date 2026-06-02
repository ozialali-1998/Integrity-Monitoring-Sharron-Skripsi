export default function DataTable({ columns, rows, renderCell }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-cyber-border bg-cyber-panel/70">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-cyber-border text-left text-sm">
          <thead className="bg-slate-950/40 text-xs uppercase tracking-wider text-cyber-muted">
            <tr>
              {columns.map((column) => (
                <th key={column.key} className="px-4 py-3 font-semibold">{column.label}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-cyber-border/70">
            {rows.map((row) => (
              <tr key={row.id ?? row.algorithm} className="transition hover:bg-cyber-elevated/50">
                {columns.map((column) => (
                  <td key={column.key} className="px-4 py-3 text-cyber-text">
                    {renderCell ? renderCell(row, column.key) : row[column.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
