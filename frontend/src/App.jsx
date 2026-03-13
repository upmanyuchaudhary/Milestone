import { useState } from 'react'
import HomeScreen from './components/Home/HomeScreen.jsx'
import PortfolioScreen from './components/Portfolio/PortfolioScreen.jsx'
import AlertsScreen from './components/Alerts/AlertsScreen.jsx'
import MilestoneScreen from './components/Milestone/MilestoneScreen.jsx'

const NAV = [
  { id: 'home',      label: 'Home',      icon: '⌂' },
  { id: 'portfolio', label: 'Portfolio', icon: '◈' },
  { id: 'alerts',    label: 'Alerts',    icon: '◉' },
  { id: 'milestone', label: 'Milestone', icon: '▲' },
]

const styles = {
  app:    { display:'flex', flexDirection:'column', minHeight:'100vh', maxWidth:'480px', margin:'0 auto' },
  screen: { flex:1, overflowY:'auto', paddingBottom:'72px' },
  nav:    { position:'fixed', bottom:0, left:'50%', transform:'translateX(-50%)',
            width:'100%', maxWidth:'480px', background:'#fff',
            borderTop:'1px solid #e8eaed', display:'flex' },
  navBtn: (active) => ({
    flex:1, padding:'10px 0', background:'none', border:'none', cursor:'pointer',
    display:'flex', flexDirection:'column', alignItems:'center', gap:'2px',
    color: active ? '#1F3864' : '#9aa0a6',
    fontWeight: active ? '700' : '400',
  }),
  navIcon:  { fontSize:'20px' },
  navLabel: { fontSize:'11px' },
}

export default function App() {
  const [screen, setScreen] = useState('home')

  const screens = {
    home:      <HomeScreen      onNavigate={setScreen} />,
    portfolio: <PortfolioScreen onNavigate={setScreen} />,
    alerts:    <AlertsScreen    onNavigate={setScreen} />,
    milestone: <MilestoneScreen onNavigate={setScreen} />,
  }

  return (
    <div style={styles.app}>
      <div style={styles.screen}>
        {screens[screen]}
      </div>
      <nav style={styles.nav}>
        {NAV.map(n => (
          <button key={n.id} style={styles.navBtn(screen === n.id)} onClick={() => setScreen(n.id)}>
            <span style={styles.navIcon}>{n.icon}</span>
            <span style={styles.navLabel}>{n.label}</span>
          </button>
        ))}
      </nav>
    </div>
  )
}
