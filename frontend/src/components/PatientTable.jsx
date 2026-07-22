const RISK_STYLES = {
  low: 'bg-emerald-50 text-emerald-700 ring-emerald-200',
  medium: 'bg-amber-50 text-amber-700 ring-amber-200',
  high: 'bg-orange-50 text-orange-700 ring-orange-200',
  critical: 'bg-rose-50 text-rose-700 ring-rose-200',
}

export function RiskBadge({ level }) {
  return (
    <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-semibold capitalize ring-1 ${RISK_STYLES[level] ?? RISK_STYLES.low}`}>
      {level}
    </span>
  )
}

export default function PatientTable({ patients, loading, onSelect }) {
  if (loading) {
    return <div className="py-16 text-center text-slate-400">Loading patients…</div>
  }
  if (!patients.length) {
    return <div className="py-16 text-center text-slate-400">No patients found.</div>
  }

  return (
    <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
          <tr>
            <th className="px-4 py-3">MRN</th>
            <th className="px-4 py-3">Patient</th>
            <th className="px-4 py-3">Age / Gender</th>
            <th className="px-4 py-3">Diagnosis</th>
            <th className="px-4 py-3">Risk</th>
            <th className="px-4 py-3">Score</th>
            <th className="px-4 py-3">Bed</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {patients.map((p) => (
            <tr
              key={p.id}
              onClick={() => onSelect?.(p)}
              className="cursor-pointer transition hover:bg-teal-50/40"
            >
              <td className="px-4 py-3 font-mono text-xs text-slate-500">{p.mrn}</td>
              <td className="px-4 py-3 font-medium text-slate-900">
                {p.first_name} {p.last_name}
              </td>
              <td className="px-4 py-3 capitalize text-slate-600">
                {p.age} / {p.gender}
              </td>
              <td className="px-4 py-3 text-slate-600">{p.primary_diagnosis ?? '—'}</td>
              <td className="px-4 py-3"><RiskBadge level={p.risk_level} /></td>
              <td className="px-4 py-3 tabular-nums text-slate-700">
                {p.risk_score?.toFixed(0)}
              </td>
              <td className="px-4 py-3 text-slate-600">
                {p.is_admitted ? p.bed_number ?? 'Admitted' : 'OPD'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
