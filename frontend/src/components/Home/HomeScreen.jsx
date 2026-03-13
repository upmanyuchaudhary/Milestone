import { useState, useEffect } from 'react'
import { getHomeDashboard, getAuthStatus } from '../../api/index.js'
import { formatRupeesExact, formatPct, pnlColor } from '../../utils/format.js'

const S = {
  screen:    { padding:'16px', background:'#f7f8fa', minHeight:'100vh' },
  header:    { display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'20px' },
  title:     { fontSize:'22px', fontWeight:'800', color:'#1F3864' },
  authBadge: (ok) => ({ fontSize:'11px', padding:'4px 10px', borderRadius:'20px',
                         background: ok ? '#D5F0E3' : '#FDECEA',
                         color:      ok ? '#1A7A4A' : '#C00000', fontWeight:'600' }),
  card:      { background:'#fff', borderRadius:'16px', padding:'20px',
                marginBottom:'14px', boxShadow:'0 1px 4px rgba(0,0,0,0.06)' },
  // Milestone hero
  milLabel:  { fontSize:'12px', color:'#888', marginBottom:'6px', fontWeight:'600', letterSpacing:'0.5px' },
  milValue:  { fontSize:'32px', fontWeight:'800', color:'#1F3864', marginBottom:'2px' },
  milTarget: { fontSize:'13px', color:'#888', marginBottom:'14px' },
  barTrack:  { height:'10px', borderRadius:'10px', background:'#e8eaed', overflow:'hidden', marginBottom:'10px' },
  barFill:   (pct) => ({ height:'100%', width:`${Math.min(pct,100)}%`,
                          background:'linear-gradient(90deg, #2E75B6, #1F3864)', borderRadius:'10px',
                          transition:'width 0.6s ease' }),
  milStats:  { display:'flex', gap:'8px' },
  milStat:   { flex:1, textAlign:'center', background:'#f7f8fa', borderRadius:'10px', padding:'10px 6px' },
  milStatV:  { fontSize:'15px', fontWeight:'700', color:'#1F3864' },
  milStatL:  { fontSize:'10px', color:'#888', marginTop:'2px' },
  // Health card
  healthRow: { display:'flex', justifyContent:'space-between', alignItems:'center' },
  healthBadge:(h) => ({
    padding:'5px 14px', borderRadius:'20px', fontWeight:'700', fontSize:'13px',
    background: h === 'HEALTHY' ? '#D5F0E3' : h === 'ATTENTION' ? '#FFF9DB' : '#FDECEA',
    color:      h === 'HEALTHY' ? '#1A7A4A' : h === 'ATTENTION' ? '#C55A11' : '#C00000',
  }),
  dayChange:  (n) => ({ fontSize:'14px', fontWeight:'600', color: pnlColor(n) }),
  // Story cards
  storyTitle: { fontSize:'13px', fontWeight:'700', color:'#1F3864', marginBottom:'10px' },
  storyCard:  (type) => ({
    padding:'12px 14px', borderRadius:'12px', marginBottom:'8px',
    borderLeft:'3px solid',
    borderColor: type==='POSITIVE'?'#1A7A4A': type==='ALERT'?'#C00000': type==='SIP'?'#2E75B6':'#C55A11',
    background:  type==='POSITIVE'?'#D5F0E3': type==='ALERT'?'#FDECEA': type==='SIP'?'#D5E8F0':'#FFF9DB',
  }),
  storyText:  { fontSize:'13px', color:'#222', fontWeight:'500' },
  storySub:   { fontSize:'11px', color:'#666', marginTop:'3px' },
  // Action strip
  actionStrip:{ background:'#1F3864', borderRadius:'14px', padding:'14px 18px',
                display:'flex', justifyContent:'space-between', alignItems:'center' },
  actionText: { color:'#fff', fontSize:'14px', fontWeight:'600' },
  actionBtn:  { background:'#fff', color:'#1F3864', border:'none', borderRadius:'8px',
                padding:'7px 14px', fontWeight:'700', fontSize:'13px', cursor:'pointer' },
  loading:    { textAlign:'center', padding:'60px 20px', color:'#888', fontSize:'15px' },
  error:      { textAlign:'center', padding:'40px 20px', color:'#C00000', fontSize:'14px' },
}

export default function HomeScreen({ onNavigate }) {
  const [data, setData]       = useState(null)
  const [authOk, setAuthOk]   = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  useEffect(() => {
    Promise.all([getHomeDashboard(), getAuthStatus()])
      .then(([dash, auth]) => {
        setData(dash.data)
        setAuthOk(auth.data.valid)
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div style={S.loading}>Loading your portfolio…</div>
  if (error)   return <div style={S.error}>Could not load dashboard — check API connection<br/><small>{error}</small></div>

  const { milestone_progress: mp, portfolio_health, total_value,
          day_change, day_change_pct, active_alert_count, story_cards } = data
  const pct = parseFloat(mp.progress_pct)

  return (
    <div style={S.screen}>
      {/* Header */}
      <div style={S.header}>
        <span style={S.title}>Milestone</span>
        <span style={S.authBadge(authOk)}>{authOk ? '● Connected' : '○ Login needed'}</span>
      </div>

      {/* Milestone Hero */}
      <div style={S.card}>
        <div style={S.milLabel}>GOAL PROGRESS</div>
        <div style={S.milValue}>{formatRupeesExact(mp.current_value)}</div>
        <div style={S.milTarget}>of {formatRupeesExact(mp.target_value)} target</div>
        <div style={S.barTrack}><div style={S.barFill(pct)} /></div>
        <div style={S.milStats}>
          <div style={S.milStat}>
            <div style={S.milStatV}>{pct.toFixed(1)}%</div>
            <div style={S.milStatL}>Complete</div>
          </div>
          <div style={S.milStat}>
            <div style={S.milStatV}>{formatRupeesExact(mp.required_monthly)}</div>
            <div style={S.milStatL}>Needed/month</div>
          </div>
          <div style={S.milStat}>
            <div style={S.milStatV}>{mp.days_ahead_behind >= 0 ? `+${mp.days_ahead_behind}` : mp.days_ahead_behind}</div>
            <div style={S.milStatL}>Days {mp.days_ahead_behind >= 0 ? 'ahead' : 'behind'}</div>
          </div>
        </div>
      </div>

      {/* Portfolio Health */}
      <div style={S.card}>
        <div style={S.healthRow}>
          <div>
            <div style={{fontSize:'12px',color:'#888',fontWeight:'600',letterSpacing:'0.5px'}}>PORTFOLIO HEALTH</div>
            <div style={{fontSize:'20px',fontWeight:'800',color:'#1F3864',marginTop:'4px'}}>
              {formatRupeesExact(total_value)}
            </div>
          </div>
          <div style={{textAlign:'right'}}>
            <span style={S.healthBadge(portfolio_health)}>
              {portfolio_health === 'HEALTHY' ? '✓ Healthy' :
               portfolio_health === 'ATTENTION' ? '⚠ Attention' :
               portfolio_health === 'PENDING_FIRST_SYNC' ? '○ Syncing' : '! Action needed'}
            </span>
            <div style={{...S.dayChange(day_change), marginTop:'8px'}}>
              {formatPct(day_change_pct)} today
            </div>
          </div>
        </div>
      </div>

      {/* Story Cards */}
      {story_cards?.length > 0 && (
        <div style={S.card}>
          <div style={S.storyTitle}>WHAT'S HAPPENING</div>
          {story_cards.map((card, i) => (
            <div key={i} style={S.storyCard(card.type)}>
              <div style={S.storyText}>{card.text}</div>
              {card.subtext && <div style={S.storySub}>{card.subtext}</div>}
            </div>
          ))}
        </div>
      )}

      {/* Action Strip — only if active alerts */}
      {active_alert_count > 0 && (
        <div style={S.actionStrip}>
          <span style={S.actionText}>
            {active_alert_count} recommendation{active_alert_count > 1 ? 's' : ''} waiting
          </span>
          <button style={S.actionBtn} onClick={() => onNavigate('alerts')}>
            Review →
          </button>
        </div>
      )}
    </div>
  )
}
