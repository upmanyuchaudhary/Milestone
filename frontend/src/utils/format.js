// ── Number formatting ─────────────────────────────────────────────────────────

export const formatRupees = (n) => {
  if (n === null || n === undefined) return '—'
  const abs = Math.abs(n)
  if (abs >= 100000) return `₹${(n / 100000).toFixed(2)}L`
  if (abs >= 1000)   return `₹${(n / 1000).toFixed(1)}K`
  return `₹${Number(n).toFixed(0)}`
}

export const formatRupeesExact = (n) => {
  if (n === null || n === undefined) return '—'
  return `₹${Number(n).toLocaleString('en-IN', { maximumFractionDigits: 0 })}`
}

export const formatPct = (n, decimals = 1) => {
  if (n === null || n === undefined) return '—'
  const sign = n > 0 ? '+' : ''
  return `${sign}${Number(n).toFixed(decimals)}%`
}

export const formatScore = (n) => {
  if (n === null || n === undefined) return '—'
  return Number(n).toFixed(1)
}

// ── Color helpers ─────────────────────────────────────────────────────────────

export const pnlColor = (n) => {
  if (n === null || n === undefined) return '#555'
  return n >= 0 ? '#1A7A4A' : '#C00000'
}

export const scoreColor = (score) => {
  if (score === null || score === undefined) return '#888'
  if (score >= 8) return '#1A7A4A'
  if (score >= 6) return '#2E75B6'
  if (score >= 4) return '#C55A11'
  return '#C00000'
}

export const catColor = (cat) => ({
  A: '#1F3864', B: '#2E75B6', C: '#C55A11'
}[cat] || '#888')

export const catBg = (cat) => ({
  A: '#D5E8F0', B: '#EAF3FB', C: '#FCE4D6'
}[cat] || '#eee')

export const stateColor = (state) => ({
  STRONG_HOLD: '#1A7A4A',
  HOLD:        '#2E75B6',
  WATCH:       '#C55A11',
  REVIEW:      '#E67300',
  EXIT_WATCH:  '#C00000',
  EXIT:        '#C00000',
  EXIT_NOW:    '#C00000',
}[state] || '#888')

// ── Date helpers ──────────────────────────────────────────────────────────────

export const formatDate = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

export const formatMonthYear = (my) => {
  if (!my) return '—'
  const [y, m] = my.split('-')
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  return `${months[parseInt(m) - 1]} ${y}`
}
