import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
})

// ── Home ─────────────────────────────────────────────────────────────────────
export const getHomeDashboard      = ()       => api.get('/home/dashboard')

// ── Portfolio ─────────────────────────────────────────────────────────────────
export const getHoldings           = ()       => api.get('/portfolio/holdings')
export const getHolding            = (id)     => api.get(`/portfolio/holdings/${id}`)
export const addHolding            = (data)   => api.post('/portfolio/holdings', data)
export const getPortfolioSummary   = ()       => api.get('/portfolio/summary')
export const getAllocation          = ()       => api.get('/portfolio/allocation')

// ── Milestone ─────────────────────────────────────────────────────────────────
export const getMilestoneProgress  = ()       => api.get('/milestone/progress')
export const getMilestoneHistory   = ()       => api.get('/milestone/history')
export const getContributions      = ()       => api.get('/milestone/contributions')
export const runScenario           = (data)   => api.post('/milestone/scenario', data)
export const updateMilestoneConfig = (data)   => api.put('/milestone/config', data)

// ── Alerts ────────────────────────────────────────────────────────────────────
export const getActiveAlerts       = ()       => api.get('/alerts/active')
export const respondToAlert        = (id, action) => api.post(`/alerts/${id}/action`, { action })
export const getAlertHistory       = ()       => api.get('/alerts/history')
export const getIgnoredAlerts      = ()       => api.get('/alerts/ignored')
export const getAccuracyLog        = ()       => api.get('/alerts/accuracy')

// ── Auth ──────────────────────────────────────────────────────────────────────
export const getLoginUrl           = ()       => api.get('/auth/login-url')
export const getAuthStatus         = ()       => api.get('/auth/status')

export default api
