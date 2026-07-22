export default function StatCard({ label, value, sub, accent = 'teal' }) {
  const accents = {
    teal: 'bg-teal-50 text-teal-700 ring-teal-100',
    amber: 'bg-amber-50 text-amber-700 ring-amber-100',
    rose: 'bg-rose-50 text-rose-700 ring-rose-100',
    indigo: 'bg-indigo-50 text-indigo-700 ring-indigo-100',
  }
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm font-medium text-slate-500">{label}</p>
      <p className="mt-2 text-3xl font-bold text-slate-900">{value}</p>
      {sub && (
        <span className={`mt-3 inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ${accents[accent]}`}>
          {sub}
        </span>
      )}
    </div>
  )
}
