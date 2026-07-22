import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getDashboardStats = () => api.get('/dashboard/stats').then(r => r.data)

export const getPatients = (params = {}) =>
  api.get('/patients/', { params }).then(r => r.data)

export const getPatient = (id) => api.get(`/patients/${id}`).then(r => r.data)
export const createPatient = (data) => api.post('/patients/', data).then(r => r.data)
export const updatePatient = (id, data) => api.put(`/patients/${id}`, data).then(r => r.data)
export const deletePatient = (id) => api.delete(`/patients/${id}`)
export const getVitals = (id, limit = 100) =>
  api.get(`/patients/${id}/vitals`, { params: { limit } }).then(r => r.data)

export default api
