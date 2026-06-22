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

function LineChart({ data, color, gradientId }) {
  const [animate, setAnimate] = useState(false)
  const width = 600
  const height = 200

  useEffect(() => {
    setTimeout(() => setAnimate(true), 100)
  }, [])

  const chartData = data || []
  const maxVal = chartData.length > 0 ? Math.max(...chartData.map(d => d.value)) : 100
  const minVal = chartData.length > 0 ? Math.min(...chartData.map(d => d.value)) : 0
  const range = maxVal - minVal || 1

  const points = useMemo(() => {
    return chartData.map((d, i) => {
      const x = (i / (chartData.length - 1 || 1)) * width
      const y = height - ((d.value - minVal) / range) * (height - 40) - 20
      return `${x},${y}`
    }).join(' ')
  }, [chartData, animate])

  return (
    <div className="glass p-5 fade-in">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-slate-300">Keyword Rankings (7 days)</h3>
        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1 text-xs text-slate-500">
            <div className="w-2 h-2 rounded-full bg-[#F7931E]" />
            Avg Position
          </span>
        </div>
      </div>
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto">
        <defs>
          <linearGradient id={gradientId || 'lineGradient'} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color || '#F7931E'} stopOpacity="0.3" />
            <stop offset="100%" stopColor={color || '#F7931E'} stopOpacity="0" />
          </linearGradient>
          <linearGradient id="lineStroke" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor={color || '#1E3A5F'} />
            <stop offset="100%" stopColor={color || '#F7931E]'} />
          </linearGradient>
        </defs>
        <polygon points={`0,{height} ${points} ${width},{height}`} fill={`url(#${gradientId || 'lineGradient'})`} className="transition-all duration-1000" style={{ opacity: animate ? 1 : 0 }} />
        <polyline points={points} fill="none" stroke="url(#lineStroke)" strokeWidth="2" className="transition-all duration-1000" style={{ strokeDasharray: width * 2, strokeDashoffset: animate ? 0 : width * 2 }} />
        {(chartData || []).map((d, i) => {
          const x = (i / (chartData.length - 1 || 1)) * width
          const y = height - ((d.value - minVal) / range) * (height - 40) - 20
          return (
            <circle key={i} cx={x} cy={y} r="3" fill={color || '#F7931E'} className="transition-all duration-500" style={{ opacity: animate ? 1 : 0 }} />
          )
        })}
        {(chartData || []).map((d, i) => (
          <text key={i} x={(i / (chartData.length - 1 || 1)) * width} y={height - 5} textAnchor="middle" className="text-[10px] fill-slate-500">{d.day}</text>
        ))}
      </svg>
    </div>
  )
}

function BarChart({ data, color, title }) {
  const [animate, setAnimate] = useState(false)
  const width = 400
  const height = 200

  useEffect(() => {
    setTimeout(() => setAnimate(true), 200)
  }, [])

  const chartData = data || []
  const maxVal = chartData.length > 0 ? Math.max(...chartData.map(d => d.value)) : 100

  return (
    <div className="glass p-5 fade-in">
      <h3 className="text-sm font-medium text-slate-300 mb-4">{title || 'Traffic Sources'}</h3>
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto">
        {(chartData || []).map((d, i) => {
          const barWidth = width / (chartData.length * 2.5)
          const x = (i * (width / chartData.length)) + (width / (chartData.length * 2))
          const barHeight = animate ? (d.value / maxVal) * (height - 40) : 0
          return (
            <g key={i}>
              <rect x={x} y={height - 20 - barHeight} width={barWidth} height={barHeight} fill={color || '#F7931E'} rx="3" className="transition-all duration-500" style={{ transitionDelay: `${i * 100}ms }} />
              <text x={x + barWidth / 2} y={height - 5} textAnchor="middle" className="text-[10px] fill-slate-500">{d.label}</text>
              <text x={x + barWidth / 2} y={height - 25 - barHeight} textAnchor="middle" className="text-[10px] fill-slate-400">{d.value}%</text>
            </g>
          )
        })}
      </svg>
    </div>
  )
}

function DataTable({ columns, data, onSort, sortConfig }) {
  const [sortField, setSortField] = useState(null)
  const [sortDirection, setSortDirection] = useState('asc')

  const handleSort = (callback) => (field) => {
    const newDirection = sortField === field && sortDirection === 'asc' ? 'desc' : 'asc'
    setSortField(field)
    setSortDirection(newDirection)
    callback && callback(field, newDirection)
  }

  const sortedData = useMemo(() => {
    const list = data || []
    if (!sortField || !list.length) return list
    return [...list].sort((a, b) => {
      if (a[sortField] < b[sortField]) return sortDirection === 'asc' ? -1 : 1
      if (a[sortField] > b[sortField]) return sortDirection === 'asc' ? 1 : -1
      return 0
    })
  }, [data, sortField, sortDirection])

  return (
    <div className="glass overflow-hidden fade-in">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/5">
              {(columns || []).map(col => (
                <th key={col.key} onClick={() => col.sortable && handleSort()(col.key)} className={`px-4 py-3 text-xs font-medium text-slate-400 text-left ${col.sortable ? 'cursor-pointer hover:text-slate-200' : ''}`}>
                  <div className="flex items-center gap-1">
                    {col.label}
                    {sortField === col.key && (
                      <span className="text-[#F7931E]">{sortDirection === 'asc' ? '↑” : '↓–'}</span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {(savedData || []).map((row, i) => (
              <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                {(columns || []).map(col => (
                  <td key={col.key} className="px-4 py-3 text-sm text-slate-300">
                    {col.render ? col.render(row[col.key], row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function DashboardContent() {
  const [kpiData, setKpiData] = useState(null)
  const [chartData, setChartData] = useState(null)
  const [activityData, setActivityData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const mockKpiData = useMemo(() => ({
    keywordsTracked: 2847,
    keywordsTrackedDelta: 12.5,
    organicTraffic: 152341,
    organicTrafficDelta: -3.2,
    backlinksBuilt: 8976,
    backlinksBuiltDelta: 8.1,
    avgPosition: 4.3,
    avgPositionDelta: -15.3
  }), [])

  const mockChartData = useMemo(() => [
    { day: 'Mon', value: 45 },
    { day: 'Tue', value: 52 },
    { day: 'Wed', value: 48 },
    { day: 'Thu', value: 61 },
    { day: 'Fri', value: 58 },
    { day: 'Sat', value: 72 },
    { day: 'Sun', value: 68 }
  ], [])

  const mockBarData = useMemo(() => [
    { label: 'Organic', value: 45 },
    { label: 'Direct', value: 25 },
    { label: 'Social', value: 18 },
    { label: 'Referral', value: 12 }
  ], [])

  const mockActivityData = useMemo(() => [
    { time: '2 min ago', action: 'Keyword update', keyword: 'organic skincare products', status: 'completed', details: 'Rank improved to #3' },
    { time: '15 min ago', action: 'Content generated', keyword: 'best face moisturizer 2024', status: 'completed', details: 'Blog post published' },
    { time: '1 hour ago', action: 'Link outreach', keyword: 'buy natural cosmetics', status: 'pending', details: 'Email sent to 5 bloggers' },
    { time: '3 hours ago', action: 'Ranking alert', keyword: 'vegan makeup brands', status: 'warning', details: 'Dropped from #2 to #5' },
    { time: '5 hours ago', action: 'Backlink found', keyword: 'organic hair products', status: 'completed', details: 'New backlink from .edu domain' }
  ], [])

  const columns = useMemo(() => [
    { key: 'time', label: 'Time', sortable: true },
    { key: 'action', label: 'Action', sortable: true },
    { key: 'keyword', label: 'Keyword', sortable: true },
    { key: 'status', label: 'Status', sortable: true, render: (val) => (
      <span className={`flex items-center gap-1 text-xs ${
        val === 'completed' ? 'text-green-400' : 
        val === 'pending' ? 'text-yellow-400' : 'text-red-400'
      }`}>
        {val === 'completed' ? <CheckCircle className="w-3 h-3" /> : 
         val === 'pending' ? <Loader2 className="w-3 h-3 animate-spin" /> : 
         <AlertCircle className="w-3 h-3" />}
        {val}
      </span>
    )},
    { key: 'details', label: 'Details', sortable: false }
  ], [])

  useEffect(() => {
    async function fetchData() {
      try {
        const [kpi, chart, activity] = await Promise.all([
          apiFetch('/api/dashboard/kpi'),
          apiFetch('/api/dashboard/chart'),
          apiFetch('/api/dashboard/activity')
        ])
        setKpiData(kpi || mockKpiData)
        setChartData(chart || mockChartData)
        setActivityData(activity || mockActivityData)
      } catch (e) {
        setError('Failed to load dashboard data')
        setKpiData(mockKpiData)
        setChartData(mockChartData)
        setActivityData(mockActivityData)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
        {[1,2,3,4].map(i => (
          <div key={i} className="glass p-5 shimmer h-32" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="glass p-6 text-center">
        <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
        <p className="text-sm text-slate-400">{error}</p>
        <button onClick={() => window.location.reload()} className="mt-3 px-4 py-2 bg-white/10 rounded-lg text-sm text-slate-400 hover:bg-white/20 transition-all">Retry</button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold gradient-text mb-1">Dashboard</h1>
        <p className="text-sm text-slate-500">Welcome back! Here's your SEO overview.</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
        <KPICard icon={Target} label="Keywords Tracked" value={kpiData?.keywordsTracked} delta={kpiData?.keywordsTrackedDelta} color="bg-blue-500/10" />
        <KPICard icon={Users} label="Organic Traffic" value={kpiData?.organicTraffic} delta={kpiData?.organicTrafficDelta} color="bg-green-500/10" />
        <KPICard icon={Globe} label="Backlinks Built" value={kpiData?.backlinksBuilt} delta={kpiData?.backlinksBuiltDelta} color="bg-purple-500/10" />
        <KPICard icon={BarChart3} label="Avg. Position" value={kpiData?.avgPosition} delta={kpiData?.avgPositionDelta} color="bg-orange-500/10" format="decimal" />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LineChart data={chartData || []} />
        <BarChart data={mockBarData} />
      </div>
      <div>
        <h3 className="text-sm font-medium text-slate-300 mb-3">Recent Activity</h3>
        <DataTable columns={columns} data={activityData || []} />
      </div>
    </div>
  )
}

function AnalyticsContent() {
  const [analyticsData, setAnalyticsData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const mockAnalyticsData = useMemo(() => ({
    topKeywords: [
      { keyword: 'organic skincare', volume: 24500, difficulty: 42, position: 3 },
      { keyword: 'vegan makeup', volume: 18900, difficulty: 58, position: 5 },
      { keyword: 'natural beauty', volume: 15300, difficulty: 35, position: 2 },
      { keyword: 'clean cosmetics', volume: 12200, difficulty: 28, position: 4 },
      { keyword: 'sustainable beauty', volume: 9800, difficulty: 45, position: 6 },
    ],
    siteHealth: 87,
    pageSpeed: 92,
    mobileScore: 78
  }), [])

  const keywordColumns = useMemo(() => [
    { key: 'keyword', label: 'Keyword', sortable: true },
    { key: 'volume', label: 'Search Volume', sortable: true },
    { key: 'difficulty', label: 'Difficulty', sortable: true, render: (val) => (
      <div className="flex items-center gap-2">
        <div className="w-20 h-1.5 bg-white/10 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-green-400 via-yellow-400 to-red-400 rounded-full" style={{ width: `${val}%` }} />
        </div>
        <span className="text-xs text-slate-400">{val}</span>
      </div>
    )},
    { key: 'position', label: 'Position', sortable: true, render: (val) => (
      <span className={`text-xs font-medium ${val <= 3 ? 'text-green-400' : val <= 5 ? 'text-yellow-400' : 'text-red-400'}`}>
        ##{val}
      </span>
    )},
  ], [])

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await apiFetch('/api/analytics')
        setAnalyticsData(data || mockAnalyticsData)
      } catch (e) {
        setAnalyticsData(mockAnalyticsData)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return <div className="space-y-6">
      {[1,2,3].map(i => <div key={i} className="glass p-5 shimmer h-32" />)}
    </div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold gradient-text mb-1">Analytics</h1>
        <p className="text-sm text-slate-500">Deep dive into your SEO performance metrics.</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass p-5 fade-in text-center">
          <p className="text-sm text-slate-400 mb-1">Site Health</p>
          <div className="text-3xl font-bold text-green-400">{analyticsData?.siteHealth || mockAnalyticsData.siteHealth}%</div>
          <div className="w-full h-2 bg-white/10 rounded-full mt-2 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-green-400 to-green-300 rounded-full" style={{ width: `${analyticsData?.siteHealth || mockAnalyticsData.siteHealth}%`}} />
          </div>
        </div>
        <div className="glass p-5 fade-in text-center">
          <p className="text-sm text-slate-400 mb-1">Page Speed</p>
          <div className="text-3xl font-bold text-blue-400">{analyticsData?.pageSpeed || mockAnalyticsData.pageSpeed}/100</div>
          <div className="w-full h-2 bg-white/10 rounded-full mt-2 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-blue-400 to-blue-300 rounded-full" style={{ width: `${analyticsData?.pageSpeed || mockAnalyticsData.pageSpeed}%`}} />
          </div>
        </div>
        <div className="glass p-5 fade-in text-center">
          <p className="text-sm text-slate-400 mb-1">Mobile Score</p>
          <div className="text-3xl font-bold text-orange-400">{analyticsData?.mobileScore || mockAnalyticsData.mobileScore}/100</div>
          <div className="w-full h-2 bg-white/10 rounded-full mt-2 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-orange-400 to-orange-300 rounded-full" style={{ width: `${analyticsData?.mobileScore || mockAnalyticsData.mobileScore}%`}} />
          </div>
        </div>
      </div>
      <div>
        <h3 className="text-sm font-medium text-slate-300 mb-3">Top Keywords</h3>
        <DataTable columns={keywordColumns} data={analyticsData?.topKeywords || mockAnalyticsData.topKeywords} />
      </div>
    </div>
  )
}
