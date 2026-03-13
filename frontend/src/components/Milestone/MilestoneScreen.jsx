import { useState, useEffect } from 'react'
import { getMilestoneProgress, getMilestoneHistory, getContributions, runScenario } from '../../api/index.js'
import { formatRupeesExact, formatMonthYear, formatDate } from '../../utils/format.js'

const S = {
  screen:   { padding:'16px', background:'#f7f8fa', minHeight:'100vh' },
  header:   { fontSize:'22px', fontWeight:'800', color:'#1F3864', marginBottom:'16px' },
  hero:     { background:'linear-gradient(135deg, #1F3864, #2E75B6)', borderRadius:'20px',
              padding:'24px 20px', marginBottom:'14px', color:'#fff' },
  heroLabel:{ fontSize:'11px', color:'rgba(255,255,255,0.6)', letterSpacing:'0.8px', marginBottom:'8px' },
  heroVal:  { fontSize:'36px', fontWeight:'800', marginBottom:'4px' },
  heroSub:  { fontSize:'14px', color:'rgba(255,255,255,0.75)', marginBottom:'18px' },
  barTrack: { height:'14px', borderRadius:'14px', background:'rgba(255,255,255,0.2)', overflow:'hidden', marginBottom:'12px' },
  barFill:  (pct) => ({ height:'100%', width:`${Math.min(pct,100)}%`,
                         background:'linear-gradient(90deg, #7FC8F8, #fff)', borderRadius:'14px' }),
  heroRow:  { display:'flex', gap:'8px' },
  heroStat: { flex:1, background:'rgba(255,255,255,0.12)', borderRadius:'12px', padding:'10px 8px', textAlign:'center' },
  heroSV:   { fontSize:'15px', fontWeight:'800' },
  heroSL:   { fontSize:'9px', color:'rgba(255,255,255,0.6)', marginTop:'3px' },
  card:     { background:'#fff', borderRadius:'16px', padding:'18px', marginBottom:'12px',
              boxShadow:'0 1px 4px rgba(0,0,0,0.06)' },
  cardHd:   { fontSize:'13px', fontWeight:'700', color:'#1F3864', marginBottom:'12px', letterSpacing:'0.4px' },
  // Scenario
  sliderRow:{ marginBottom:'14px' },
  sliderLbl:{ display:'flex', justifyContent:'space-between', fontSize:'13px', color:'#555', marginBottom:'6px' },
  sliderVal:{ fontWeight:'700', color:'#1F3864' },
  slider:   { width:'100%', accentColor:'#1F3864' },
  scenResult:{ background:'#D5E8F0', borderRadius:'10px', padding:'12px', textAlign:'center', marginTop:'8px' },
  scenDate: { fontSize:'20px', fontWeight:'800', color:'#1F3864' },
  scenSub:  { fontSize:'12px', color:'#2E75B6', marginTop:'2px' },
  // Contributions
  contribBar:{ height:'16px', borderRadius:'8px', overflow:'hidden', display:'flex', marginBottom:'8px' },
  contribLeg:{ display:'flex', gap:'16px', flexWrap:'wrap' },
  legItem:  { display:'flex', alignItems:'center', gap:'6px', fontSize:'12px', color:'#555' },
  legDot:   (c) => ({ width:'10px', height:'10px', borderRadius:'50%', background:c }),
  // History table
  histRow:  { display:'flex', justifyContent:'space-between', alignItems:'center',
              padding:'10px 0', borderBottom:'1px solid #f0f0f0' },
  histMonth:{ fontSize:'13px', fontWeight:'600', color:'#1a1a2e' },
  histVal:  { fontSize:'13px', fontWeight:'700', color:'#1F3864' },
  histDelta:(n) => ({ fontSize:'12px', color: n>=0?'#1A7A4A':'#C00000', fontWeight:'600' }),
  loading:  { textAlign:'center', padding:'60px 20px', color:'#888' },
}

export default function MilestoneScreen() {
  const [progress, setProgress]     = useState(null)
  const [history,  setHistory]      = useState([])
  const [contrib,  setContrib]      = useState(null)
  const [loading,  setLoading]      = useState(true)
  const [scenario, setScenario]     = useState(null)
  const [sipSlider,setSipSlider]    = useState(30000)
  const [computing,setComputing]    = useState(false)

  useEffect(() => {
    Promise.all([getMilestoneProgress(), getMilestoneHistory(), getContributions()])
      .then(([p, h, c]) => {
        setProgress(p.data)
        setHistory(h.data)
        setContrib(c.data)
        setSipSlider(p.data.required_monthly || 30000)
      })
      .finally(() => setLoading(false))
  }, [])

  const computeScenario = async (sip) => {
    setComputing(true)
    try {
      const res = await runScenario({ monthly_sip: sip })
      setScenario(res.data)
    } finally { setComputing(false) }
  }

  useEffect(() => {
    const t = setTimeout(() => computeScenario(sipSlider), 500)
    return () => clearTimeout(t)
  }, [sipSlider])

  if (loading || !progress) return <div style={S.loading}>Loading milestone…</div>

  const pct = parseFloat(progress.progress_pct)
  const dab = progress.days_ahead_behind

  return (
    <div style={S.screen}>
      <div style={S.header}>Milestone</div>

      {/* Hero */}
      <div style={S.hero}>
        <div style={S.heroLabel}>PORTFOLIO GOAL</div>
        <div style={S.heroVal}>{formatRupeesExact(progress.current_value)}</div>
        <div style={S.heroSub}>of {formatRupeesExact(progress.target_value)} · {pct.toFixed(1)}% complete</div>
        <div style={S.barTrack}><div style={S.barFill(pct)} /></div>
        <div style={S.heroRow}>
          <div style={S.heroStat}>
            <div style={S.heroSV}>{formatDate(progress.projected_date)}</div>
            <div style={S.heroSL}>Projected completion</div>
          </div>
          <div style={S.heroStat}>
            <div style={S.heroSV}>{dab >= 0 ? `+${dab}` : dab} days</div>
            <div style={S.heroSL}>{dab >= 0 ? 'Ahead of plan' : 'Behind plan'}</div>
          </div>
        </div>
      </div>

      {/* Scenario modelling */}
      <div style={S.card}>
        <div style={S.cardHd}>SCENARIO MODELLING</div>
        <div style={S.sliderRow}>
          <div style={S.sliderLbl}>
            <span>Monthly SIP</span>
            <span style={S.sliderVal}>{formatRupeesExact(sipSlider)}</span>
          </div>
          <input type="range" style={S.slider}
            min="5000" max="100000" step="1000" value={sipSlider}
            onChange={e => setSipSlider(Number(e.target.value))} />
        </div>
        {scenario && !computing && (
          <div style={S.scenResult}>
            <div style={S.scenDate}>{formatDate(scenario.projected_date)}</div>
            <div style={S.scenSub}>
              {scenario.months_to_target} months to target
              {scenario.days_delta !== 0 && ` · ${scenario.days_delta > 0 ? '+' : ''}${scenario.days_delta} days vs current plan`}
            </div>
          </div>
        )}
        {computing && <div style={{textAlign:'center',color:'#888',fontSize:'13px',padding:'12px'}}>Calculating…</div>}
      </div>

      {/* Contribution breakdown */}
      {contrib && (
        <div style={S.card}>
          <div style={S.cardHd}>HOW IT'S BEING BUILT</div>
          <div style={S.contribBar}>
            <div style={{flex:contrib.equity_appreciation_pct||0, background:'#1F3864'}} />
            <div style={{flex:contrib.sip_pct||0, background:'#2E75B6'}} />
            <div style={{flex:contrib.rebalancing_pct||0, background:'#7FC8F8'}} />
          </div>
          <div style={S.contribLeg}>
            <div style={S.legItem}><span style={S.legDot('#1F3864')} />Equity growth</div>
            <div style={S.legItem}><span style={S.legDot('#2E75B6')} />SIP contributions</div>
            <div style={S.legItem}><span style={S.legDot('#7FC8F8')} />Rebalancing</div>
          </div>
          {contrib.message && <div style={{fontSize:'12px',color:'#888',marginTop:'10px'}}>{contrib.message}</div>}
        </div>
      )}

      {/* Monthly history */}
      {history.length > 0 && (
        <div style={S.card}>
          <div style={S.cardHd}>MONTHLY HISTORY</div>
          {history.slice().reverse().map(m => (
            <div key={m.month_year} style={S.histRow}>
              <div style={S.histMonth}>{formatMonthYear(m.month_year)}</div>
              <div style={{textAlign:'right'}}>
                <div style={S.histVal}>{formatRupeesExact(m.portfolio_value)}</div>
                <div style={S.histDelta(m.monthly_change)}>
                  {m.monthly_change >= 0 ? '+' : ''}{formatRupeesExact(m.monthly_change)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {history.length === 0 && (
        <div style={{...S.card, textAlign:'center', color:'#888', padding:'30px'}}>
          Monthly history builds after your first full month of tracking
        </div>
      )}
    </div>
  )
}
