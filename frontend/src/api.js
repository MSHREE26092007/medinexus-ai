import axios from 'axios'

// Demo mode (VITE_DEMO=1 at build time): serve the bundled snapshot instead of
// the FastAPI backend, so the dashboard works as a static site (GitHub Pages).
const DEMO = import.meta.env.VITE_DEMO === '1'

const api = axios.create({ baseURL: '/api' })

let _demoPatients = null
async function demoPatients() {
  if (!_demoPatients) {
    const r = await fetch(`${import.meta.env.BASE_URL}demo/patients.json`)
    _demoPatients = (await r.json()).patients
  }
  return _demoPatients
}

export const getDashboardStats = () => {
  if (DEMO) return fetch(`${import.meta.env.BASE_URL}demo/stats.json`).then((r) => r.json())
  return api.get('/dashboard/stats').then((r) => r.data)
}

export const getPatients = async (params = {}) => {
  if (DEMO) {
    let list = await demoPatients()
    const q = (params.search || '').toLowerCase()
    if (q) {
      list = list.filter(
        (p) =>
          `${p.first_name} ${p.last_name}`.toLowerCase().includes(q) ||
          p.mrn.toLowerCase().includes(q) ||
          (p.primary_diagnosis || '').toLowerCase().includes(q),
      )
    }
    if (params.risk_level) list = list.filter((p) => p.risk_level === params.risk_level)
    return { total: list.length, patients: list }
  }
  return api.get('/patients/', { params }).then((r) => r.data)
}

const demoReadOnly = () =>
  Promise.reject(new Error('Read-only demo — run locally for full CRUD (see README)'))

export const getPatient = (id) =>
  DEMO
    ? demoPatients().then((l) => l.find((p) => p.id === id))
    : api.get(`/patients/${id}`).then((r) => r.data)
export const createPatient = (data) =>
  DEMO ? demoReadOnly() : api.post('/patients/', data).then((r) => r.data)
export const updatePatient = (id, data) =>
  DEMO ? demoReadOnly() : api.put(`/patients/${id}`, data).then((r) => r.data)
export const deletePatient = (id) => (DEMO ? demoReadOnly() : api.delete(`/patients/${id}`))
export const getVitals = (id, limit = 100) =>
  DEMO
    ? Promise.resolve([])
    : api.get(`/patients/${id}/vitals`, { params: { limit } }).then((r) => r.data)

export default api
