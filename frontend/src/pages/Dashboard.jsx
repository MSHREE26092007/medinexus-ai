import { useEffect, useState } from 'react'
import { getDashboardStats, getPatients } from '../api'
import StatCard from '../components/StatCard'
import PatientTable from '../components/PatientTable'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [patients, setPatients] = useState([])
  const [search, setSearch] = useState('')
  const [riskFilter, setRiskFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getDashboardStats().then(setStats).catch(() => setError('Backend unreachable — is FastAPI running on :8000?'))
  }, [])

  // Debounced search + filter
  useEffect(() => {
    setLoading(true)
    const t = setTimeout(() => {
      getPatients({
        search: search || undefined,
        risk_level: riskFilter || undefined,
      })
        .then((d) => setPatients(d.patients))
        .catch(() => setError('Backend unreachable — is FastAPI running on :8000?'))
        .finally(() => setLoading(false))
    }, 250)
    return () => clearTimeout(t)
  }, [search, riskFilter])

  if (error) {
    return (
      <div className="m-8 rounded-xl border border-rose-200 bg-rose-50 p-6 text-rose-700">
        {error}
      </div>
    )
  }

  return (
    <div className="space-y-6 p-8">
      <header>
        <h2 className="text-2xl font-bold text-slate-900">Clinical Dashboard</h2>
        <p className="text-sm text-slate-500">Live overview of ward status and patient risk</p>
      </header>

      {/* Metric cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Total Patients"
          value={stats?.total_patients ?? '—'}
          sub={`${stats?.admitted_patients ?? 0} admitted`}
          accent="teal"
        />
        <StatCard
          label="High Risk"
          value={stats?.high_risk_count ?? '—'}
          sub="Needs review"
          accent="amber"
        />
        <StatCard
          label="Critical"
          value={stats?.critical_count ?? '—'}
          sub="Immediate attention"
          accent="rose"
        />
        <StatCard
          label="Bed Occupancy"
          value={stats ? `${stats.bed_occupancy_pct}%` : '—'}
          sub={`${stats?.admitted_patients ?? 0} / 50 beds`}
          accent="indigo"
        />
      </div>

      {/* Disease distribution strip */}
      {stats?.disease_distribution?.length > 0 && (
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold text-slate-700">Top Diagnoses</h3>
          <div className="flex flex-wrap gap-2">
            {stats.disease_distribution.map((d) => (
              <button
                key={d.diagnosis}
                onClick={() => setSearch(d.diagnosis)}
                className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600 transition hover:border-teal-300 hover:bg-teal-50 hover:text-teal-700"
              >
                {d.diagnosis} · {d.count}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Search + filters */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by name, MRN, or diagnosis…"
          className="w-full max-w-md rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm shadow-sm outline-none transition focus:border-teal-400 focus:ring-2 focus:ring-teal-100"
        />
        <select
          value={riskFilter}
          onChange={(e) => setRiskFilter(e.target.value)}
          className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm shadow-sm outline-none focus:border-teal-400"
        >
          <option value="">All risk levels</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
        {(search || riskFilter) && (
          <button
            onClick={() => { setSearch(''); setRiskFilter('') }}
            className="text-sm text-slate-500 hover:text-slate-700"
          >
            Clear
          </button>
        )}
      </div>

      <PatientTable patients={patients} loading={loading} />
    </div>
  )
}
