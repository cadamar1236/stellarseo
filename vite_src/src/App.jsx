import { useState, useEffect, useCallback, useRef, useMemo } from 'react'
import { Search, Bell, User, Menu, TrendingUp, TrendingDown, BarChart3, Globe, FileText, Settings as SettingsIcon, Activity, Zap, ArrowUpRight, ArrowDownRight, Clock, ExternalLink, CheckCircle, XCircle, AlertCircle, Loader2, Target, DollarSign, Users, Rocket, Plus, Filter, Download, Share2, ChevronDown, Edit3, Trash2, RefreshCw, PieChart, LineChart as LineChartIcon } from 'lucide-react'

const BASE = window.__BACKEND_URL__ || '';
async function apiFetch(path, opts = {}) {
  for (let i = 0; i < 3; i++) {
    try {
      const r = await fetch(BASE + path, opts);
      if (r.ok) return r.json();
    } catch (_) {}
    await new Promise(r => setTimeout(r, 1000));
  }
  return null;
}

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [notifications, setNotifications] = useState([])
  const [showNotifications, setShowNotifications] = useState(false)
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [user, setUser] = useState(null)
  const [authLoading, setAuthLoading] = useState(true)
  const [authError, setAuthError] = useState(null)
  const styleRef = useRef(null)

  useEffect(() => {
    async function checkAuth() {
      const data = await apiFetch('/api/auth/me')
      if (data && data.email) {
        setUser(data)
      }
      setAuthLoading(false)
    }
    checkAuth()
  }, [])

  useEffect(() => {
    const style = document.createElement('style')
    style.textContent = `
      :root { --accent: #1E3A5F; --accent2: #F7931E; }
      .glass { background: rgba(255,255,255,0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; }
      .gradient-text { background: linear-gradient(135deg, #1E3A5F, #F7931E, #FF6B6B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
      .shimmer { background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
      @keyframes shimmer { 0% { background-position: -200% 0 } 100% { background-position: 200% 0 } }
      @keyframes fadeIn { from { opacity:0; transform:translateY(8px) } to { opacity:1; transform:translateY(0) } }
      .fade-in { animation: fadeIn 0.3s ease forwards; }
      @keyframes countUp { from { opacity:0; transform:translateY(10px) } to { opacity:1; transform:translateY(0) } }
      .count-up { animation: countUp 0.5s ease forwards; }
      ::-webkit-scrollbar { width: 6px; }
      ::-webkit-scrollbar-track { background: transparent; }
      ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
      ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
    `
    document.head.appendChild(style)
    styleRef.current = style
    return () => { if (styleRef.current) styleRef.current.remove() }
  }, [])

  if (authLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#06080f]">
        <div className="text-center">
          <Rocket className="w-12 h-12 text-[#F7931E] animate-pulse mx-auto mb-4" />
          <p className="text-slate-400 text-sm">Loading StellarSEO...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return <LandingPage onLogin={(r) => setUser(r)} />
  }

  return (
    <div className="flex h-screen overflow-hidden bg-[#06080f] text-slate-100">
      <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar user={user} notifications={notifications} setShowNotifications={setShowNotifications} showNotifications={showNotifications} setShowUserMenu={setShowUserMenu} showUserMenu={showUserMenu} setSidebarOpen={setSidebarOpen} />
        <main className="flex-1 overflow-y-auto p-6">
          {currentPage === 'dashboard' && <DashboardContent />}
          {currentPage === 'analytics' && <AnalyticsContent />}
          {currentPage === 'reports' && <ReportsContent />}
          {currentPage === 'settings' && <SettingsContent />}
        </main>
      </div>
      {showNotifications && <NotificationsPanel notifications={notifications} onClose={() => setShowNotifications(false)} />}
    </div>
  )
}

function LandingPage({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loginError, setLoginError] = useState(null)
  const [loggingIn, setLoggingIn] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoginError(null)
    if (!email || !password) {
      setLoginError('Please enter email and password')
      return
    }
    setLoggingIn(true)
    const result = await apiFetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    if (result && result.email) {
      onLogin(result)
      return
    }
    // Demo fallback
    if (email === 'sarah@stellar.com' && password === 'demo123') {
      onLogin({ name: 'Sarah Chen', email: 'sarah@stellar.com', role: 'admin' })
      return
    }
    setLoginError('Invalid credentials. Try sarah@stellar.com / demo123')
    setLoggingIn(false)
  }

  const fillDemo = () => {
    setEmail('sarah@stellar.com')
    setPassword('demo123')
  }

  return (
    <div className="min-h-screen bg-[#06080f] flex items-center justify-center p-4">
      <div className="glass p-8 w-full max-w-md fade-in">
        <div className="flex items-center justify-center gap-2 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#1E3A5F] to-[#F7931E] flex items-center justify-center">
            <Rocket className="w-5 h-5 text-white" />
          </div>
          <span className="font-semibold text-xl">RankStellar</span>
        </div>
        <h1 className="text-2xl font-bold gradient-text text-center mb-2">Welcome Back</h1>
        <p className="text-sm text-slate-500 text-center mb-6">Sign in to your StellarSEO dashboard</p>
        {loginError && (
          <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
            {loginError}
          </div>
        )}
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#F7931E]/50 focus:ring-1 focus:ring-[#F7931E]/20 transition-all" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="********" className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#F7931E]/50 focus:ring-1 focus:ring-[#F7931E]/20 transition-all" />
          </div>
          <button type="submit" disabled={loggingIn} className="w-full py-2.5 rounded-lg bg-gradient-to-r from-[#1E3A5F] to-[#F7931E] text-white font-medium text-sm hover:opacity-90 transition-all disabled:opacity-50">
            {loggingIn ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        <div className="mt-4 text-center">
          <button onClick={fillDemo} className="text-xs text-slate-500 hover:text-[#F7931E] transition-colors underline">
            Use demo credentials
          </button>
        </div>
      </div>
    </div>
  )
}

function Sidebar({ currentPage, setCurrentPage, sidebarOpen, setSidebarOpen }) {
  const navItems = useMemo(() => [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'analytics', label: 'Analytics', icon: PieChart },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
  ], [])

  return (
    <>
      <aside className={${sidebarOpen ? 'w-64' : 'w-0'} flex-shrink-0 flex-col border-r border-white/5 bg-white/[0.02] h-full transition-all duration-300 hidden md:flex }>
        <div className="h-14 flex items-center px-4 border-b border-white/5">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#1E3A5F] to-[#F7931E] flex items-center justify-center">
              <Rocket className="w-4 h-4 text-white" />
            </div>
            <span className="font-semibold text-lg">RankStellar</span>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {(navItems || []).map(item => (
            <button
              key={item.id}
              onClick={() => setCurrentPage(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${
                currentPage === item.id
                  ? 'bg-[#1E3A5F]/20 text-[#F7931E] border border-[#F7931E]/30' 
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <item.icon className="w-4 h-4" />
              {item.label}
            </button>
          ))}
        </nav>
        <div className="p-4 border-t border-white/5">
          <div className="glass p-3 text-xs text-slate-400">
            <p className="font-medium text-slate-300 mb-1">AI-Powered SEO</p>
            <p className="mb-2">Unlock advanced analytics</p>
            <button className="w-full py-1.5 px-3 rounded-lg bg-[#F7931E] text-[#06080f] font-medium hover:bg-[e6841b] transition-colors text-xs">
              Upgrade to Pro
            </button>
          </div>
        </div>
      </aside>
      <button onClick={() => setSidebarOpen(!sidebarOpen)} className="md:hidden fixed top-4 left-4 z-50 p-2 glass">
        <Menu className="w-5 h-5" />
      </button>
    </>
  )
}

function TopBar({ user, notifications, setShowNotifications, showNotifications, setShowUserMenu, showUserMenu, setSidebarOpen }) {
  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-white/5 flex-shrink-0 bg-[#06080f]/80 backdrop-blur-xl">
      <div className="flex items-center gap-4">
        <button onClick={() => setSidebarOpen(prev => !prev)} className="md:hidden p-1 hover:bg-white/5 rounded-lg">
          <Menu className="w-5 h-5" />
        </button>
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input type="text" placeholder="Search keywords, domains..." className="w-72 pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#F7931E]/50 focus:ring-1 focus:ring-[#F7931E]/20 transition-all" />
        </div>
      </div>
      <div className="flex items-center gap-4">
        <div className="relative">
          <button onClick={() => setShowNotifications(!showNotifications)} className="relative p-2 hover:bg-white/5 rounded-lg transition-colors">
            <Bell className="w-5 h-5 text-slate-400" />
            {(notifications || []).length > 0 && (
              <span className="absolute top-1 right-1 w-2 h-2 bg-[#F7931E] rounded-full" />
            )}
          </button>
        </div>
        <div className="relative">
          <button onClick={() => setShowUserMenu(!showUserMenu)} className="flex items-center gap-2 p-1.5 hover:bg-white/5 rounded-lg transition-colors">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#1E3A5F] to-[#F7931E] flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
            <span className="text-sm text-slate-400 hidden sm:inline">{user?.name || 'User'}</span>
          </button>
          {showUserMenu && (
            <div className="absolute right-0 top-12 w-48 glass p-2">
              <button className="w-full text-left px-3 py-2 text-sm text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-lg transition-colors">Profile</button>
              <button className="w-full text-left px-3 py-2 text-sm text-slate-400 hover:text-slate-200 hover:bg-white/5 rounded-lg transition-colors">Sign Out</button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

function NotificationsPanel({ notifications, onClose }) {
  return (
    <div className="fixed right-0 top-14 w-80 max-h-500 glass p-4 overflow-y-auto z-50 fade-in">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-slate-300">Notifications</h3>
        <button onClick={onClose} className="text-sm text-slate-500 hover:text-slate-300">×</button>
      </div>
      {(notifications || []).length === 0 && (
        <p className="text-xs text-slate-500">No new notifications</p>
      )}
      {(notifications || []).map((n, i) => (
        <div key={i} className="p-3 hover:bg-white/[0.02] rounded-lg transition-colors">
          <p className="text-xs text-slate-300">{n.title || n.action || 'Update'}</p>
          <p className="text-[10px] text-slate-600">{n.time || ''}</p>
        </div>
      ))}
    </div>
  )
}

function KPICard({ icon: Icon, label, value, delta, color, format }) {
  const [displayValue, setDisplayValue] = useState(0)
  const targetValue = typeof value === 'number' ? value : parseInt(value) || 0

  useEffect(() => {
    let start = 0
    const duration = 1000
    const startTime = Date.now()
    const timer = setInterval(() => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      start = Math.floor(targetValue * eased)
      setDisplayValue(start)
      if (progress >= 1) clearInterval(timer)
    }, 16)
    return () => clearInterval(timer)
  }, [targetValue])

  const formattedValue = useMemo(() => {
    if (format === 'currency') return `${(displayValue).toLocaleString()}`
    if (format === 'percentage') return `${displayValue}%`
    if (format === 'decimal') return displayValue.toFixed(1)
    return displayValue.toLocaleString()
  }, [displayValue, format])

  return (
    <div className="glass p-5 fade-in hover:bg-white/[0.06] transition-all duration-300 cursor-pointer group">
      <div className="flex items-start justify-between mb-3">
        <div className={`p2 rounded-lg ${color || 'bg-[#1E3A5F]/20'}`}>
          <Icon className="w-5 h-5 text-[#F7931E]" />
        </div>
        {delta !== undefined && (
          <span className={`flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full ${
            delta >= 0 ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'
          }`}>
            {delta >= 0 ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
            {Math.abs(delta)}%
          </span>
        )}
      </div>
      <p className="text-sm text-slate-400 mb-1">{label}</p>
      <p className="text-2xl font-bold count-up text-slate-100">{formattedValue}</p>
    </div>
  )
}
