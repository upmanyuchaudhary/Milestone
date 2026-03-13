// Format a number as Indian Rupees
export const formatRupees = (value) => {
  if (value === null || value === undefined) return '—'
  const num = parseFloat(value)
  if (num >= 100000) return `₹${(num / 100000).toFixed(2)}L`
  if (num >= 1000)   return `₹${(num / 1000).toFixed(1)}K`
  return `₹${num.toFixed(0)}`
}

// Format as full rupee string with commas
export const formatRupeesFull = (value) => {
  if (value === null || value === undefined) return '—'
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(value)
}

// Format percentage
export const formatPct = (value) => {
  if (value === null || value === undefined) return '—'
  const num = parseFloat(value)
  return `${num >= 0 ? '+' : ''}${num.toFixed(2)}%`
}

// Format date as "Mar 2026"
export const formatMonthYear = (dateStr) => {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })
}

// Format date as "13 Mar 2026"
export const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

// Category colour
export const catColor = (cat) => ({ A: '#1A7A4A', B: '#2E75B6', C: '#C00000' }[cat] || '#666')
export const catBg    = (cat) => ({ A: '#D5F0E3', B: '#D5E8F0', C: '#FDECEA' }[cat] || '#F2F2F2')

// Output state colour
export const stateColor = (state) => {
  const map = {
    STRONG_HOLD: '#1A7A4A', HOLD: '#2E75B6',
    WATCH: '#C55A11',       REVIEW: '#C55A11',
    EXIT_WATCH: '#C00000',  EXIT_NOW: '#C00000', EXIT: '#C00000'
  }
  return map[state] || '#666'
}
