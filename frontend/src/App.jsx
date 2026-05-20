import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import {
  LayoutDashboard,
  TrendingUp,
  FileText,
  Settings,
  Bell,
  ChevronDown,
  Search,
  ArrowUpRight,
  ArrowDownRight,
  Users,
  Eye,
  MousePointerClick,
  DollarSign,
  Loader2,
  CheckCircle2,
  XCircle,
  Clock,
  AlertCircle,
  Zap,
  Bot,
  Target,
  Link2,
  Sparkles,
  Menu,
  X,
  LogOut,
} from 'lucide-react';

const BASE = window.__BACKEND_URL__ || '';

async function apiFetch(path, opts = {}) {
  for (let i = 0; i < 5; i++) {
    try {
      const r = await fetch(BASE + path, opts);
      if (r.ok) return r.json();
    } catch (_) {}
    await new Promise(r => setTimeout(r, 1500));
  }
  return null;
}

const MOCK_KPI_DATA = [
  { label: 'Total Keywords', value: 1247, icon: Target, delta: 12.5, positive: true },
  { label: 'Page Views', value: 89432, icon: Eye, delta: 8.3, positive: true },
  { label: 'Click Rate', value: 4.7, icon: MousePointerClick, delta: -2.1, positive: false, suffix: '%' },
  { label: 'Revenue Impact', value: 28400, icon: DollarSign, delta: 15.2, positive: true, prefix: '$' },
];

const MOCK_TREND_DATA = [
  { date: 'Mon', value: 240 },
  { date: 'Tue', value: 380 },
  { date: 'Wed', value: 320 },
  { date: 'Thu', value: 510 },
  { date: 'Fri', value: 470 },
  { date: 'Sat', value: 620 },
  { date: 'Sun', value: 580 },
];

const MOCK_ACTIVITY_DATA = [
  { id: 1, action: 'Keyword Research', page: '/products/sneakers', status: 'completed', user: 'Sarah J.', time: '2 min ago', priority: 'high' },
  { id: 2, action: 'Content Generation', page: '/blog/top-10-shoes', status: 'running', user: 'Mike R.', time: '15 min ago', priority: 'medium' },
  { id: 3, action: 'Link Building', page: '/outreach', status: 'pending', user: 'Emily K.', time: '1 hr ago', priority: 'low' },
  { id: 4, action: 'SEO Audit', page: '/analytics/overview', status: 'failed', user: 'Alex P.', time: '3 hrs ago', priority: 'high' },
  { id: 5, action: 'Ranking Update', page: '/products/running', status: 'completed', user: 'Chris L.', time: '5 hrs ago', priority: 'medium' },
];

const MOCK_SEARCH_RESULTS = [
  { keyword: 'running shoes', volume: 14500, difficulty: 62, opportunity: 'high' },
  { keyword: 'best sneakers', volume: 22000, difficulty: 78, opportunity: 'medium' },
  { keyword: 'vegan leather shoes', volume: 3200, difficulty: 28, opportunity: 'high' },
];

function Counter({ target, suffix = '', prefix = '', duration = 2000 }) {
  const [count, setCount] = useState(0);
  const hasAnimated = useRef(false);

  useEffect(() => {
    if (hasAnimated.current) return;
    hasAnimated.current = true;
    const decimals = (target.toString().split('.')[1] || '').length;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      setCount(current);
    }, 16);
    return () => clearInterval(timer);
  }, [target, duration]);

  return <>{prefix}{count.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 1 })}{suffix}</>;
}

function KPICard({ data, index }) {
  const [loaded, setLoaded] = useState(false);
  const Icon = data.icon;

  useEffect(() => {
    const t = setTimeout(() => setLoaded(true), index * 100);
    return () => clearTimeout(t);
  }, [index]);

  return (
    <div className={`glass p-5 fade-in transition-all duration-300 hover:bg-white/[0.06] hover:border-white/20 cursor-pointer`} style={{ animationDelay: `${index * 0.1}s` }}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{data.label}</span>
        <div className="p-2 rounded-lg bg-white/[0.05]">
          <Icon className="w-4 h-4 text-yellow-400" />
        </div>
      </div>
      <div className="flex items-end justify-between">
        <div className="text-3xl font-bold text-white">
          {loaded ? <Counter target={data.value} suffix={data.suffix || ''} prefix={data.prefix || ''} /> : '0'}
        </div>
        <div className={`flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-full ${data.positive ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}`}>
          {data.positive ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
          {data.delta}%
        </div>
      </div>
    </div>
  );
}

function LineChart({ data, height = 200, color = '#F59E0B' }) {
  const [animated, setAnimated] = useState(false);
  const svgRef = useRef(null);

  useEffect(() => {
    requestAnimationFrame(() => setAnimated(true));
  }, []);

  const maxVal = Math.max(...(data || []).map(d => d.value));
  const points = (data || []).map((d, i) => ({
    x: (i / ((data || []).length - 1)) * 100,
    y: ((maxVal - d.value) / maxVal) * height,
  }));

  const linePath = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');

  const areaPath = `${linePath} L 100 ${height} L 0 ${height} Z`;

  return (
    <svg ref={svgRef} viewBox={`0 0 100 ${height}`} className="w-full h-full" preserveAspectRatio="none">
      <defs>
        <linearGradient id="lineGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.3" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      <path d={areaPath} fill="url(#lineGradient)" opacity={animated ? 0.8 : 0} style={{ transition: 'opacity 0.8s ease' }} />
      <path
        d={linePath}
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeDasharray={animated ? '1000' : '0'}
        strokeDashoffset="0"
        style={{ transition: 'stroke-dasharray 1.5s ease-in-out' }}
      />
      {animated && points.slice(0).map((p, i) => (
        <circle
          key={i}
          cx={p.x}
          cy={p.y}
          r="2"
          fill="#06080f"
          stroke={color}
          strokeWidth="2"
          style={{ animation: `fadeIn 0.3s ease ${i * 0.1}s forwards`, opacity: 0 }}
        />
      ))}
    </svg>
  );
}

function BarChart({ data, height = 150, color = '#1E3A8A' }) {
  const [animated, setAnimated] = useState(false);

  useEffect(() => {
    requestAnimationFrame(() => setAnimated(true));
  }, []);

  const maxVal = Math.max(...(data || []).map(d => d.value));

  return (
    <div className="flex items-end gap-2 h-full" style={{ height }}>
      {(data || []).map((d, i) => {
        const pct = (d.value / maxVal) * 100;
        return (
          <div key={i} className="flex-1 flex flex-col items-center gap-1">
            <div
              className="w-full rounded-t-md transition-all duration-700 ease-out"
              style={{
                height: animated ? `${pct}%` : '0%',
                background: `linear-gradient(180deg, ${color}, ${color}88)`,
                transitionDelay: `${i * 0.1}s`,
              }}
            />
            <span className="text-[10px] text-slate-500">{d.date}</span>
          </div>
        );
      })}
    </div>
  );
}

function DataTable({ data, columns }) {
  const [sortKey, setSortKey] = useState(null);
  const [sortDir, setSortDir] = useState('asc');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  const filteredData = useMemo(() => {
    let items = (data || []).filter(item => {
      if (filterStatus !== 'all' && item.status !== filterStatus) return false;
      if (searchTerm) {
        return Object.values(item).some(v =>
          String(v).toLowerCase().includes(searchTerm.toLowerCase())
        );
      }
      return true;
    });

    if (sortKey) {
      items = [...items].sort((a, b) => {
        const aVal = a[sortKey];
        const bVal = b[sortKey];
        if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
        return 0;
      });
    }
    return items;
  }, [data, searchTerm, filterStatus, sortKey, sortDir]);

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  };

  const statusColors = {
    completed: 'bg-emerald-500/10 text-emerald-400',
    running: 'bg-blue-500/10 text-blue-400',
    pending: 'bg-yellow-500/10 text-yellow-400',
    failed: 'bg-red-500/10 text-red-400',
  };

  const statusIcons = {
    completed: CheckCircle2,
    running: Loader2,
    pending: Clock,
    failed: XCircle,
  };

  return (
    <div>
      <div className="flex items-center gap-4 mb-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search activity..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white/[0.04] border border-white/10 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-yellow-500/50 focus:ring-1 focus:ring-yellow-500/20"
          />
        </div>
        <select
          value={filterStatus}
          onChange={e => setFilterStatus(e.target.value)}
          className="px-3 py-2 bg-white/[0.04] border border-white/10 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-yellow-500/50"
        >
          <option value="all">All Status</option>
          <option value="completed">Completed</option>
          <option value="running">Running</option>
          <option value="pending">Pending</option>
          <option value="failed">Failed</option>
        </select>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/5">
              {(columns || []).map(col => (
                <th
                  key={col.key}
                  onClick={() => handleSort(col.key)}
                  className={`text-left py-3 px-3 text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:text-slate-200 transition-colors ${col.sortable ? '' : ''}`}
                >
                  <div className="flex items-center gap-1">
                    {col.label}
                    {col.sortable && sortKey === col.key && (
                      <span className="text-yellow-400">{sortDir === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {(filteredData || []).map((row, i) => {
              const Icon = statusIcons[row.status] || AlertCircle;
              return (
                <tr key={row.id} className="border-b border-white/[0.02] hover:bg-white/[0.02] transition-colors">
                  <td className="py-3 px-3 text-slate-300">{row.action}</td>
                  <td className="py-3 px-3 text-slate-400">{row.page}</td>
                  <td className="py-3 px-3">
                    <span className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium ${statusColors[row.status] || 'bg-slate-500/10 text-slate-400'}`}>
                      <Icon className={`w-3 h-3 ${row.status === 'running' ? 'animate-spin' : ''}`} />
                      {row.status}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-400">{row.user}</td>
                  <td className="py-3 px-3 text-slate-500">{row.time}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Sidebar({ activePage, setActivePage }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 flex-shrink-0 flex flex-col border-r border-white/5 bg-white/[0.02] h-full">
      <div className="h-14 flex items-center gap-2 px-5 border-b border-white/5">
        <Sparkles className="w-6 h-6 text-yellow-400" />
        <span className="font-semibold text-lg">
          <span className="gradient-text">Stellar</span>
          <span className="text-slate-200">SEO</span>
        </span>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = activePage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-blue-900/30 text-yellow-400 border border-blue-800/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/[0.04]'
              }`}
            >
              <Icon className="w-4 h-4" />
              {item.label}
            </button>
          );
        })}
      </nav>
      <div className="px-3 py-4 border-t border-white/5">
        <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-slate-200 hover:bg-white/[0.04] transition-all duration-200">
          <LogOut className="w-4 h-4" />
          Sign Out
        </button>
      </div>
    </aside>
  );
}

function TopBar({ onToggleSidebar }) {
  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-white/5 flex-shrink-0">
      <div className="flex items-center gap-4">
        <button onClick={onToggleSidebar} className="lg:hidden p-2 hover:bg-white/[0.04] rounded-lg">
          <Menu className="w-5 h-5 text-slate-400" />
        </button>
        <h1 className="text-lg font-semibold text-slate-100">Dashboard</h1>
      </div>
      <div className="flex items-center gap-4">
        <button className="relative p-2 hover:bg-white/[0.04] rounded-lg transition-colors">
          <Bell className="w-5 h-5 text-slate-400" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-yellow-400 rounded-full"></span>
        </button>
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-600 to-yellow-500 flex items-center justify-center text-xs font-semibold text-white">
            JD
          </div>
          <ChevronDown className="w-4 h-4 text-slate-500" />
        </div>
      </div>
    </header>
  );
}

function QuickActions() {
  const actions = [
    { label: 'Run Keyword Scan', icon: Target, color: 'text-blue-400' },
    { label: 'Generate Content', icon: Bot, color: 'text-emerald-400' },
    { label: 'Start Outreach', icon: Link2, color: 'text-purple-400' },
    { label: 'View Rankings', icon: TrendingUp, color: 'text-yellow-400' },
  ];

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Quick Actions</h3>
      <div className="space-y-2">
        {actions.map((action, i) => {
          const Icon = action.icon;
          return (
            <button
              key={i}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-lg glass hover:bg-white/[0.06] hover:border-white/20 transition-all duration-200 text-sm"
            >
              <Icon className={`w-4 h-4 ${action.color}`} />
              <span className="text-slate-300">{action.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

function KeywordSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = useCallback(async () => {
    if (!query.trim()) return;
    setLoading(true);
    // Simulate API call
    await new Promise(r => setTimeout(r, 800));
    setResults(MOCK_SEARCH_RESULTS.filter(r => r.keyword.includes(query.toLowerCase())));
    setLoading(false);
  }, [query]);

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSearch()}
          placeholder="Search keywords..."
          className="flex-1 px-4 py-2 bg-white/[0.04] border border-white/10 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-yellow-500/50"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 text-white text-sm font-medium rounded-lg transition-all duration-200 disabled:opacity-50"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Search'}
        </button>
      </div>
      <div className="space-y-2">
        {(results || []).map((r, i) => (
          <div key={i} className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-white/[0.04] transition-colors">
            <div className="flex items-center gap-2">
              <Target className="w-3 h-3 text-yellow-400" />
              <span className="text-sm text-slate-300">{r.keyword}</span>
            </div>
            <div className="flex items-center gap-4 text-xs text-slate-500">
              <span>{r.volume.toLocaleString()} vol</span>
              <span className={`px-2 py-0.5 rounded-full ${
                r.opportunity === 'high' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-yellow-500/10 text-yellow-400'
              }`}>
                {r.opportunity}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [kpiData, setKpiData] = useState(null);
  const [trendData, setTrendData] = useState(null);
  const [activity, setActivity] = useState(null);
  const [toast, setToast] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // CSS injection
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
      :root {
        --accent: #1E3A8A;
        --accent2: #F59E0B;
      }
      .glass {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
      }
      .gradient-text {
        background: linear-gradient(135deg, #1E3A8A, #F59E0B, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }
      .shimmer {
        background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
      }
      @keyframes shimmer {
        0% { background-position: -200% 0 }
        100% { background-position: 200% 0 }
      }
      @keyframes fadeIn {
        from { opacity:0; transform:translateY(8px) }
        to { opacity:1; transform:translateY(0) }
      }
      .fade-in { animation: fadeIn 0.3s ease forwards; }
      * { transition: all 0.2s ease; }
    `;
    document.head.appendChild(style);
    return () => style.remove();
  }, []);

  // Fetch data
  useEffect(() => {
    async function load() {
      const kpi = await apiFetch('/api/kpi');
      setKpiData(kpi || MOCK_KPI_DATA);
      const trend = await apiFetch('/api/trends');
      setTrendData(trend || MOCK_TREND_DATA);
      const act = await apiFetch('/api/activity');
      setActivity(act || MOCK_ACTIVITY_DATA);
    }
    load();
  }, []);

  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  }, []);

  const columns = useMemo(() => [
    { key: 'action', label: 'Action', sortable: true },
    { key: 'page', label: 'Page', sortable: true },
    { key: 'status', label: 'Status', sortable: true },
    { key: 'user', label: 'User', sortable: true },
    { key: 'time', label: 'Time', sortable: true },
  ], []);

  // ALL hooks before any conditional return
  const kpis = kpiData || MOCK_KPI_DATA;
  const trends = trendData || MOCK_TREND_DATA;
  const activities = activity || MOCK_ACTIVITY_DATA;

  return (
    <div className="flex h-screen overflow-hidden bg-[#06080f] text-slate-100">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed lg:relative z-50 h-full transition-transform duration-300 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
        <Sidebar activePage={activePage} setActivePage={(p) => { setActivePage(p); setSidebarOpen(false); }} />
      </div>

      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />

        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            <div className="mb-8">
              <h2 className="text-2xl font-bold gradient-text mb-1">StellarSEO Dashboard</h2>
              <p className="text-slate-400 text-sm">AI-powered SEO that drives e-commerce brands to the top of Google</p>
            </div>

            {/* KPI Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
              {(kpis || []).map((kpi, i) => (
                <KPICard key={kpi.label} data={kpi} index={i} />
              ))}
            </div>

            {/* Main content area */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
              {/* Trend Chart */}
              <div className="lg:col-span-2 glass p-5 fade-in">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">7-Day Traffic Trend</h3>
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded-full bg-yellow-400"></span>
                    <span className="text-xs text-slate-500">Page Views</span>
                  </div>
                </div>
                <div className="h-48">
                  <LineChart data={trends} />
                </div>
              </div>

              {/* Right panel */}
              <div className="space-y-6">
                <div className="glass p-5 fade-in">
                  <QuickActions />
                </div>
                <div className="glass p-5 fade-in">
                  <KeywordSearch />
                </div>
              </div>
            </div>

            {/* Activity Table */}
            <div className="glass p-5 fade-in mb-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Recent Activity</h3>
                <button
                  onClick={() => showToast('Activity refreshed successfully!', 'success')}
                  className="px-3 py-1.5 bg-yellow-500/10 text-yellow-400 text-xs font-medium rounded-lg hover:bg-yellow-500/20 transition-colors"
                >
                  Refresh
                </button>
              </div>
              <DataTable data={activities} columns={columns} />
            </div>

            {/* Stats bars */}
            <div className="glass p-5 fade-in">
              <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-4">Keyword Difficulty</h3>
              <div className="h-32">
                <BarChart data={trends} />
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Toast notification */}
      {toast && (
        <div className={`fixed bottom-6 right-6 z-50 flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg fade-in ${
          toast.type === 'success' ? 'bg-emerald-900/90 border border-emerald-700/50' : 'bg-red-900/90 border border-red-700/50'
        }`}>
          {toast.type === 'success' ? (
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          ) : (
            <XCircle className="w-5 h-5 text-red-400" />
          )}
          <span className="text-sm text-slate-200">{toast.message}</span>
        </div>
      )}
    </div>
  );
}