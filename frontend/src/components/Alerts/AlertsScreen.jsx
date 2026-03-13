import { useState, useEffect } from 'react'
import { getActiveAlerts, respondToAlert, getAlertHistory, getIgnoredAlerts } from '../../api/index.js'
import { formatRupeesExact, stateColor, catColor, catBg } from '../../utils/format.js'

const PRIORITY = { EXIT:1, EXIT_NOW:1, EXIT_WATCH:2, REVIEW:2, REBALANCE:3, SIP:4, WATCH:5 }
const typeBg = { EXIT:'#FDECEA', EXIT_NOW:'#FDECEA', EXIT_WATCH:'#FDECEA',
                 REVIEW:'#FCE4D6', REBALANCE:'#FFF9DB', SIP:'#D5E8F0', WATCH:'#F2F2F2' }
const typeBorder = { EXIT:'#C00000', EXIT_NOW:'#C00000', EXIT_WATCH:'#C00000',
                     REVIEW:'#C55A11', REBALANCE:'#C55A11', SIP:'#2E75B6', WATCH:'#888' }

const S = {
  screen:  { padding:'16px', background:'#f7f8fa', minHeight:'100vh' },
  header:  { fontSize:'22px', fontWeight:'800', color:'#1F3864', marginBottom:'6px' },
  calm:    { background:'#D5F0E3', borderRadius:'16px', padding:'28px 20px', textAlign:'center', marginBottom:'16px' },
  calmIcon:{ fontSize:'36px', marginBottom:'8px' },
  calmHd:  { fontSize:'16px', fontWeight:'700', color:'#1A7A4A', marginBottom:'4px' },
  calmSub: { fontSize:'13px', color:'#2E8B57' },
  alertCard:{ borderRadius:'14px', padding:'16px', marginBottom:'12px',
              boxShadow:'0 1px 4px rgba(0,0,0,0.08)' },
  alertTop: { display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:'10px' },
  alertLeft:{ display:'flex', gap:'8px', alignItems:'center' },
  catTag:  (cat) => ({ padding:'3px 8px', borderRadius:'6px', fontSize:'11px', fontWeight:'700',
                       background:catBg(cat), color:catColor(cat) }),
  alertType:(t)=> ({ fontSize:'12px', fontWeight:'700', color:stateColor(t), textTransform:'uppercase' }),
  alertSig: { fontSize:'11px', color:'#888', marginTop:'2px' },
  impact:  { display:'flex', gap:'8px', marginBottom:'12px' },
  impPill: (color) => ({ flex:1, background:'#fff', borderRadius:'8px', padding:'8px',
                         textAlign:'center', boxShadow:'0 1px 3px rgba(0,0,0,0.06)' }),
  impV:    (c) => ({ fontSize:'16px', fontWeight:'800', color:c }),
  impL:    { fontSize:'10px', color:'#888', marginTop:'2px' },
  alertTxt:{ fontSize:'13px', color:'#333', lineHeight:'1.5', marginBottom:'12px' },
  btnRow:  { display:'flex', gap:'8px' },
  btnAct:  { flex:2, background:'#1F3864', color:'#fff', border:'none', borderRadius:'10px',
             padding:'10px', fontWeight:'700', fontSize:'13px', cursor:'pointer' },
  btnIgn:  { flex:1, background:'#f0f0f0', color:'#555', border:'none', borderRadius:'10px',
             padding:'10px', fontWeight:'600', fontSize:'13px', cursor:'pointer' },
  secTitle:{ fontSize:'14px', fontWeight:'700', color:'#1F3864', margin:'20px 0 10px' },
  histCard:{ background:'#fff', borderRadius:'10px', padding:'12px 14px', marginBottom:'8px',
             boxShadow:'0 1px 3px rgba(0,0,0,0.05)' },
  histRow: { display:'flex', justifyContent:'space-between', alignItems:'center' },
  histSym: { fontWeight:'700', color:'#1a1a2e', fontSize:'14px' },
  histAct: (a) => ({ fontSize:'11px', fontWeight:'700', padding:'2px 8px', borderRadius:'6px',
                     background: a==='ACTED'?'#D5F0E3':a==='IGNORED'?'#FDECEA':'#FFF9DB',
                     color:      a==='ACTED'?'#1A7A4A':a==='IGNORED'?'#C00000':'#C55A11' }),
  histOut: { fontSize:'12px', color:'#888', marginTop:'4px' },
}

function AlertCard({ alert, onAction }) {
  const [acting, setActing] = useState(false)
  const bg     = typeBg[alert.output_state]     || '#f5f5f5'
  const border = typeBorder[alert.output_state] || '#ccc'

  const handleAction = async (action) => {
    setActing(true)
    try { await respondToAlert(alert.id, action); onAction() }
    finally { setActing(false) }
  }

  return (
    <div style={{...S.alertCard, background:bg, borderLeft:`4px solid ${border}`}}>
      <div style={S.alertTop}>
        <div>
          <div style={S.alertLeft}>
            <span style={S.catTag(alert.category)}>Cat {alert.category}</span>
            <span style={{fontWeight:'700', fontSize:'15px', color:'#1a1a2e'}}>{alert.tradingsymbol}</span>
          </div>
          <div style={S.alertType(alert.output_state)}>{alert.output_state?.replace('_',' ')}</div>
          <div style={S.alertSig}>{alert.signals_agreeing}/4 signals · {alert.persistence_days} day streak</div>
        </div>
        <div style={{textAlign:'right', fontSize:'12px', color:'#888'}}>
          Score: <strong style={{color:stateColor(alert.output_state)}}>{alert.composite_score}</strong>
        </div>
      </div>

      <div style={S.impact}>
        <div style={S.impPill('#C00000')}>
          <div style={S.impV('#C00000')}>₹{Math.abs(alert.rupee_impact).toLocaleString('en-IN',{maximumFractionDigits:0})}</div>
          <div style={S.impL}>At risk</div>
        </div>
        <div style={S.impPill('#1F3864')}>
          <div style={S.impV('#1F3864')}>{alert.milestone_impact_days}d</div>
          <div style={S.impL}>Milestone days</div>
        </div>
      </div>

      <div style={S.alertTxt}>{alert.plain_language_text}</div>

      {!alert.user_action && (
        <div style={S.btnRow}>
          <button style={S.btnAct} disabled={acting} onClick={() => handleAction('ACTED')}>
            ✓ I've acted on this
          </button>
          <button style={S.btnIgn} disabled={acting} onClick={() => handleAction('IGNORED')}>
            Ignore
          </button>
        </div>
      )}
    </div>
  )
}

export default function AlertsScreen({ onNavigate }) {
  const [alerts,  setAlerts]  = useState([])
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  const load = () => {
    Promise.all([getActiveAlerts(), getAlertHistory()])
      .then(([a, h]) => { setAlerts(a.data); setHistory(h.data) })
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const sorted = [...alerts].sort((a,b) => (PRIORITY[a.output_state]||9) - (PRIORITY[b.output_state]||9))

  if (loading) return <div style={{padding:'60px 20px', textAlign:'center', color:'#888'}}>Loading alerts…</div>

  return (
    <div style={S.screen}>
      <div style={S.header}>Alerts & Actions</div>

      {sorted.length === 0 ? (
        <div style={S.calm}>
          <div style={S.calmIcon}>✓</div>
          <div style={S.calmHd}>Your portfolio needs no attention</div>
          <div style={S.calmSub}>All holdings within thresholds. Come back tomorrow.</div>
        </div>
      ) : (
        <>
          <div style={{fontSize:'13px', color:'#888', marginBottom:'12px'}}>
            {sorted.length} recommendation{sorted.length>1?'s':''} — sorted by milestone impact
          </div>
          {sorted.map(a => <AlertCard key={a.id} alert={a} onAction={load} />)}
        </>
      )}

      {history.length > 0 && (
        <>
          <div style={S.secTitle}>Recent Actions</div>
          {history.slice(0,5).map(h => (
            <div key={h.id} style={S.histCard}>
              <div style={S.histRow}>
                <span style={S.histSym}>{h.tradingsymbol}</span>
                <span style={S.histAct(h.user_action)}>{h.user_action}</span>
              </div>
              <div style={S.histOut}>
                {h.outcome_rupee != null
                  ? `Outcome: ${h.outcome_rupee >= 0 ? '+' : ''}₹${Math.abs(h.outcome_rupee).toLocaleString('en-IN', {maximumFractionDigits:0})}`
                  : 'Outcome computing in 5 days…'}
              </div>
            </div>
          ))}
        </>
      )}
    </div>
  )
}
