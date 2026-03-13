import { useState, useEffect } from 'react'
import { getHoldings, getPortfolioSummary } from '../../api/index.js'
import { formatRupeesExact, formatPct, pnlColor, catColor, catBg, scoreColor, stateColor, formatScore } from '../../utils/format.js'

const S = {
  screen:   { padding:'16px', background:'#f7f8fa', minHeight:'100vh' },
  header:   { fontSize:'22px', fontWeight:'800', color:'#1F3864', marginBottom:'16px' },
  summary:  { background:'#1F3864', borderRadius:'16px', padding:'18px', marginBottom:'14px', color:'#fff' },
  sumLabel: { fontSize:'11px', color:'rgba(255,255,255,0.6)', letterSpacing:'0.5px' },
  sumValue: { fontSize:'28px', fontWeight:'800', marginTop:'2px' },
  sumRow:   { display:'flex', gap:'16px', marginTop:'12px' },
  sumStat:  { flex:1 },
  sumStatV: { fontSize:'15px', fontWeight:'700' },
  sumStatL: { fontSize:'10px', color:'rgba(255,255,255,0.6)', marginTop:'1px' },
  holdCard: { background:'#fff', borderRadius:'14px', marginBottom:'10px',
              boxShadow:'0 1px 4px rgba(0,0,0,0.06)', overflow:'hidden' },
  holdMain: { padding:'14px 16px', cursor:'pointer', display:'flex', alignItems:'center', gap:'12px' },
  catTag:   (cat) => ({ padding:'3px 8px', borderRadius:'6px', fontSize:'11px', fontWeight:'700',
                         background:catBg(cat), color:catColor(cat) }),
  holdInfo: { flex:1 },
  holdName: { fontSize:'15px', fontWeight:'700', color:'#1a1a2e' },
  holdSub:  { fontSize:'11px', color:'#888', marginTop:'2px' },
  holdRight:{ textAlign:'right' },
  holdVal:  { fontSize:'15px', fontWeight:'700', color:'#1F3864' },
  holdPnl:  (n) => ({ fontSize:'12px', fontWeight:'600', color:pnlColor(n), marginTop:'2px' }),
  stateBadge:(s) => ({ fontSize:'10px', fontWeight:'700', color:stateColor(s), marginTop:'4px' }),
  // Expanded
  expanded: { padding:'14px 16px', borderTop:'1px solid #f0f0f0', background:'#f9f9fb' },
  scoreRow: { display:'flex', gap:'8px', marginBottom:'12px' },
  scorePill:{ flex:1, textAlign:'center', background:'#fff', borderRadius:'10px', padding:'8px 4px',
              boxShadow:'0 1px 3px rgba(0,0,0,0.06)' },
  scorePV:  (v) => ({ fontSize:'18px', fontWeight:'800', color:scoreColor(v) }),
  scorePL:  { fontSize:'9px', color:'#888', marginTop:'2px' },
  infoGrid: { display:'grid', gridTemplateColumns:'1fr 1fr', gap:'8px' },
  infoCell: { background:'#fff', borderRadius:'8px', padding:'8px 10px' },
  infoCL:   { fontSize:'10px', color:'#888' },
  infoCV:   { fontSize:'13px', fontWeight:'600', color:'#1a1a2e', marginTop:'2px' },
  loading:  { textAlign:'center', padding:'60px 20px', color:'#888' },
}

function HoldingCard({ h }) {
  const [expanded, setExpanded] = useState(false)
  const scores = h.latest_scores

  return (
    <div style={S.holdCard}>
      <div style={S.holdMain} onClick={() => setExpanded(!expanded)}>
        <span style={S.catTag(h.category)}>Cat {h.category}</span>
        <div style={S.holdInfo}>
          <div style={S.holdName}>{h.tradingsymbol}</div>
          <div style={S.holdSub}>{h.quantity} shares · avg {formatRupeesExact(h.average_buy_price)}</div>
        </div>
        <div style={S.holdRight}>
          <div style={S.holdVal}>{h.current_value ? formatRupeesExact(h.current_value) : '—'}</div>
          <div style={S.holdPnl(h.pnl_absolute)}>{h.pnl_pct ? formatPct(h.pnl_pct) : '—'}</div>
          {scores?.output_state && (
            <div style={S.stateBadge(scores.output_state)}>{scores.output_state}</div>
          )}
        </div>
      </div>

      {expanded && (
        <div style={S.expanded}>
          {scores ? (
            <>
              <div style={S.scoreRow}>
                {[
                  { label:'Trend', val: scores.trend_strength_score },
                  { label:'Order Book', val: scores.orderbook_score },
                  { label:'Health', val: scores.portfolio_health_score },
                  { label:'Milestone', val: scores.milestone_score },
                ].map(s => (
                  <div key={s.label} style={S.scorePill}>
                    <div style={S.scorePV(s.val)}>{formatScore(s.val)}</div>
                    <div style={S.scorePL}>{s.label}</div>
                  </div>
                ))}
              </div>
              <div style={S.infoGrid}>
                <div style={S.infoCell}>
                  <div style={S.infoCL}>Composite Score</div>
                  <div style={{...S.infoCV, color:scoreColor(scores.composite_score)}}>
                    {formatScore(scores.composite_score)} / 10
                  </div>
                </div>
                <div style={S.infoCell}>
                  <div style={S.infoCL}>State</div>
                  <div style={{...S.infoCV, color:stateColor(scores.output_state)}}>
                    {scores.output_state || '—'}
                  </div>
                </div>
                <div style={S.infoCell}>
                  <div style={S.infoCL}>Entry Date</div>
                  <div style={S.infoCV}>{h.entry_date}</div>
                </div>
                <div style={S.infoCell}>
                  <div style={S.infoCL}>Stop Loss</div>
                  <div style={S.infoCV}>{h.stop_loss_price ? formatRupeesExact(h.stop_loss_price) : 'Not set'}</div>
                </div>
              </div>
            </>
          ) : (
            <div style={{textAlign:'center', color:'#888', fontSize:'13px', padding:'10px 0'}}>
              Scores available after first Layer 1 sync (3:45 PM on trading days)
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function PortfolioScreen() {
  const [holdings, setHoldings] = useState([])
  const [summary,  setSummary]  = useState(null)
  const [loading,  setLoading]  = useState(true)

  useEffect(() => {
    Promise.all([getHoldings(), getPortfolioSummary()])
      .then(([h, s]) => { setHoldings(h.data); setSummary(s.data) })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div style={S.loading}>Loading portfolio…</div>

  const totalValue = holdings.reduce((acc, h) => acc + (h.current_value || 0), 0)
  const totalCost  = holdings.reduce((acc, h) => acc + (h.quantity * h.average_buy_price), 0)
  const totalPnl   = totalValue - totalCost

  return (
    <div style={S.screen}>
      <div style={S.header}>Portfolio</div>

      <div style={S.summary}>
        <div style={S.sumLabel}>TOTAL PORTFOLIO</div>
        <div style={S.sumValue}>{totalValue ? formatRupeesExact(totalValue) : '—'}</div>
        <div style={S.sumRow}>
          <div style={S.sumStat}>
            <div style={{...S.sumStatV, color: totalPnl >= 0 ? '#7DCEA0' : '#F1948A'}}>
              {totalPnl ? formatRupeesExact(totalPnl) : '—'}
            </div>
            <div style={S.sumStatL}>Total P&L</div>
          </div>
          <div style={S.sumStat}>
            <div style={S.sumStatV}>{holdings.length}</div>
            <div style={S.sumStatL}>Holdings</div>
          </div>
          <div style={S.sumStat}>
            <div style={S.sumStatV}>{holdings.filter(h=>h.category==='A').length}A · {holdings.filter(h=>h.category==='B').length}B · {holdings.filter(h=>h.category==='C').length}C</div>
            <div style={S.sumStatL}>Categories</div>
          </div>
        </div>
      </div>

      {holdings.length === 0 ? (
        <div style={{textAlign:'center', padding:'40px 20px', color:'#888'}}>
          <div style={{fontSize:'32px', marginBottom:'12px'}}>◈</div>
          <div style={{fontWeight:'700', color:'#1F3864', marginBottom:'6px'}}>No holdings yet</div>
          <div style={{fontSize:'13px'}}>Holdings will appear here after your first sync</div>
        </div>
      ) : (
        holdings.map(h => <HoldingCard key={h.id} h={h} />)
      )}
    </div>
  )
}
