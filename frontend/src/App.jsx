```jsx
import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import {
  SearchPanel, BellPanel, SettingsPanel, ChevronDownPanel, TrendingUpPanel, TrendingDownPanel,
  FileTextPanel, LinkPanel, TargetPanel, ZapPanel, BarChart3Panel, UsersPanel, ExternalLinkPanel,
  HomePanel, PieChartPanel, FileSpreadsheet, MenuPanel, XPanel, PlusPanel, RefreshCwPanel,
  ArrowUpDown, ArrowUpPanel, ArrowDownPanel, FilterPanel, DownloadPanel, EyePanel,
  CheckCircle2, AlertTrianglePanel, ClockPanel, ChevronRightPanel, GripVertical,
  GlobePanel, Sparkles, ActivityPanel, ArrowRightPanel, CopyPanel, MoreHorizontalPanel,
  MailPanel, MessageSquarePanel, Share2, StarPanel, CalendarPanel
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

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [notifications, setNotifications] = useState(3);
  const [searchQuery, setSearchQuery] = useState('');
  const [toast, setToast] = useState(null);
  const [backendData, setBackendData] = useState(null);

  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type, id: Date.now() });
    setTimeout(() => setToast(null), 3500);
  }, []);

  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = ':root { --accent: #00C9A7; --accent2: #1E3A5F; }';
      document.head.appendChild(style);
    return () => document.head.removeChild(style);
  }, []);

  useEffect(() => {
    (async () => {
      const data = await apiFetch('/api/dashboard');
      if (data) setBackendData(data);
    })();
  }, []);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: HomePanel },
    { id: 'analytics', label: 'Analytics', icon: PieChartPanel },
    { id: 'keyword-research', label: 'Keyword Research', icon: SearchPanel },
    { id: 'content', label: 'Content', icon: FileTextPanel },
    { id: 'backlinks', label: 'Backlinks', icon: LinkPanel },
    { id: 'rank-tracker', label: 'Rank Tracker', icon: BarChart3Panel },
    { id: 'reports', label: 'Reports', icon: FileSpreadsheet },
    { id: 'settings', label: 'SettingsPanel', icon: SettingsPanel },
  ];

  const kpiData = (backendData && backendData.kpiData) || [
    {
      icon: TrendingUpPanel,
      label: 'Organic Traffic',
      value: '128,450',
      delta: '+12.5%',
      positive: true,
      color: '#38BDF8',
      sparkline: [35, 42, 38, 55, 48, 62, 58, 70, 65, 78],
    },
    {
      icon: TargetPanel,
      label: 'Keywords Ranked',
      value: '3,842',
      delta: '+8.3%',
      positive: true,
      color: '#818CF8',
      sparkline: [20, 25, 28, 32, 30, 35, 40, 38, 45, 42],
    },
    {
      icon: FileTextPanel,
      label: 'Content Generated',
      value: '1,247',
      delta: '+24.1%',
      positive: true,
      color: '#22C55E',
      sparkline: [10, 15, 18, 25, 30, 28, 35, 40, 38, 45],
    },
    {
      icon: LinkPanel,
      label: 'Backlinks Acquired',
      value: '5,610',
      delta: '-3.2%',
      positive: false,
      color: '#EF4444',
      sparkline: [42, 45, 40, 38, 35, 32, 30, 28, 25, 22],
    },
  ];

  const recentActivity = (backendData && backendData.recentActivity) || [
    { id: 1, date: '2025-02-18 14:32', task: 'Keyword research completed', domain: 'stellar-shop.com', status: 'Completed', keywords: 245, difficulty: 'Medium' },
    { id: 2, date: '2025-02-18 13:15', task: 'Content brief generated', domain: 'techgear.io', status: 'Processing', keywords: 128, difficulty: 'Low' },
    { id: 3, date: '2025-02-18 11:48', task: 'Backlink outreach sent', domain: 'fashionhub.co', status: 'Pending', keywords: 56, difficulty: 'High' },
    { id: 4, date: '2025-02-18 09:22', task: 'Rank tracking update', domain: 'stellar-shop.com', status: 'Completed', keywords: 389, difficulty: 'Medium' },
    { id: 5, date: '2025-02-17 23:55', task: 'AI content generated', domain: 'organicbeauty.com', status: 'Completed', keywords: 412, difficulty: 'Low' },
  ];

  const quickActions = [
    { id: 1, label: 'New Keyword Research', icon: SearchPanel, color: 'bg-sky-500', desc: 'Analyze keywords for any domain' },
    { id: 2, label: 'Generate Content', icon: FileTextPanel, color: 'bg-indigo-500', desc: 'Create AI-optimized content briefs' },
    { id: 3, label: 'Find Backlinks', icon: LinkPanel, color: 'bg-emerald-500', desc: 'Discover link building opportunities' },
    { id: 4, label: 'Run Rank Report', icon: BarChart3Panel, color: 'bg-purple-500', desc: 'Get latest ranking positions' },
  ];

  return (
    <div className="flex h-screen overflow-hidden bg-[#0F172A] text-slate-100">
      <Sidebar
        navItems={navItems}
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />

      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          notifications={notifications}
          setNotifications={setNotifications}
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
        />

        <main className="flex-1 overflow-y-auto p-4 lg:p-6 scrollbar-thin bg-[#0F172A]">
          {currentPage === 'dashboard' && (
            <DashboardContent
              kpiData={kpiData}
              recentActivity={recentActivity}
              quickActions={quickActions}
              showToast={showToast}
            />
          )}
          {currentPage !== 'dashboard' && (
            <PagePlaceholder page={currentPage} navItems={navItems} />
          )}
        </main>
      </div>

      {toast && (
        <Toast message={toast.message} type={toast.type} id={toast.id} />
      )}
    </div>
  );
}

function Sidebar({ navItems, currentPage, setCurrentPage, sidebarOpen, setSidebarOpen }) {
  return (
    <aside
      className={`${
        sidebarOpen ? 'w-64' : 'w-20'
      } flex-shrink-0 flex flex-col border-r border-white/5 bg-white/[0.02] h-full transition-all duration-300 ease-in-out relative`}
    >
      <div className="h-14 flex items-center px-4 border-b border-white/5">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-sky-400 to-indigo-500 flex items-center justify-center flex-shrink-0">
            <ZapPanel className="w-4 h-4 text-white" />
          </div>
          {sidebarOpen && (
            <span className="font-semibold text-base whitespace-nowrap gradient-text">
              StellarSEO
            </span>
          )}
        </div>
      </div>

      <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto scrollbar-thin">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentPage(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 group relative ${
                isActive
                  ? 'bg-sky-500/15 text-sky-400 border border-sky-500/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <Icon className={`w-4 h-4 flex-shrink-0 ${isActive ? 'text-sky-400' : ''}`} />
              {sidebarOpen && (
                <span className="whitespace-nowrap truncate">{item.label}</span>
              )}
              {isActive && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-6 bg-sky-400 rounded-r-full" />
              )}
            </button>
          );
        })}
      </nav>

      <div className="p-3 border-t border-white/5">
        <div className={`glass p-3 ${!sidebarOpen && 'flex justify-center'}`}>
          {sidebarOpen ? (
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-sky-400 to-indigo-500 flex items-center justify-center flex-shrink-0">
                <span className="text-xs font-bold text-white">JD</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-slate-200 truncate">John Doe</p>
                <p className="text-[10px] text-slate-500 truncate">Enterprise Plan</p>
              </div>
              <ChevronDownPanel className="w-3 h-3 text-slate-500 flex-shrink-0" />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-sky-400 to-indigo-500 flex items-center justify-center">
              <span className="text-xs font-bold text-white">JD</span>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}

function TopBar({ searchQuery, setSearchQuery, notifications, setNotifications, sidebarOpen, setSidebarOpen }) {
  const [showNotifications, setShowNotifications] = useState(false);
  const notifRef = useRef(null);

  useEffect(() => {
    const handleClick = (e) => {
      if (notifRef.current && !notifRef.current.contains(e.target)) {
        setShowNotifications(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const dummyNotifs = [
    { id: 1, text: 'Rank tracking report is ready', time: '5m ago', unread: true },
    { id: 2, text: '3 new backlink opportunities found', time: '1h ago', unread: true },
    { id: 3, text: 'Content generation completed', time: '3h ago', unread: true },
  ];

  return (
    <header className="h-14 flex items-center justify-between px-4 lg:px-6 border-b border-white/5 flex-shrink-0 bg-[#0F172A]">
      <div className="flex items-center gap-4">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 rounded-lg hover:bg-white/5 transition-colors"
        >
          {sidebarOpen ? <XPanel className="w-4 h-4" /> : <MenuPanel className="w-4 h-4" />}
        </button>
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/5 border border-white/5 focus-within:border-sky-500/50 transition-all">
          <SearchPanel className="w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="SearchPanel domain or keyword..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="bg-transparent text-sm outline-none w-48 lg:w-64 placeholder:text-slate-600"
          />
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div ref={notifRef} className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2 rounded-lg hover:bg-white/5 transition-colors relative"
          >
            <BellPanel className="w-4 h-4" />
            {notifications > 0 && (
              <span className="absolute -top-0.5 -right-0.5 w-[18px] h-[18px] bg-sky-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center animate-pulse">
                {notifications}
              </span>
            )}
          </button>
          {showNotifications && (
            <div className="absolute right-0 top-full mt-2 w-72 glass p-2 z-50 slide-in shadow-2xl">
              <div className="flex items-center justify-between px-3 py-2">
                <p className="text-xs font-semibold text-slate-300">Notifications</p>
                <button
                  onClick={() => setNotifications(0)}
                  className="text-[10px] text-sky-400 hover:text-sky-300"
                >
                  Mark all read
                </button>
              </div>
              {(dummyNotifs || []).slice(0, notifications).map((n) => (
                <div key={n.id} className="flex items-start gap-3 p-3 hover:bg-white/5 rounded-lg transition-colors">
                  <div className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${n.unread ? 'bg-sky-500' : 'bg-slate-600'}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-slate-300 truncate">{n.text}</p>
                    <p className="text-[10px] text-slate-600 mt-0.5">{n.time}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        <button className="p-2 rounded-lg hover:bg-white/5 transition-colors">
          <SettingsPanel className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
}

function DashboardContent({ kpiData, recentActivity, quickActions, showToast }) {
  const [sortField, setSortField] = useState('date');
  const [sortDir, setSortDir] = useState('desc');
  const [animatedValues, setAnimatedValues] = useState((kpiData || []).map(() => 0));
  const animRef = useRef(false);

  const chartData = useMemo(() => [
    { day: 'Mon', organic: 45000, paid: 22000, backlinks: 1800 },
    { day: 'Tue', organic: 52000, paid: 24000, backlinks: 1950 },
    { day: 'Wed', organic: 48000, paid: 21000, backlinks: 2100 },
    { day: 'Thu', organic: 61000, paid: 28000, backlinks: 2250 },
    { day: 'Fri', organic: 58000, paid: 26000, backlinks: 2400 },
    { day: 'Sat', organic: 72000, paid: 31000, backlinks: 2600 },
    { day: 'Sun', organic: 78000, paid: 33000, backlinks: 2850 },
  ], []);

  const barData = useMemo(() => [
    { name: 'SEO', value: 65 },
    { name: 'Direct', value: 45 },
    { name: 'Social', value: 30 },
    { name: 'Referral', value: 38 },
    { name: 'Paid', value: 22 },
  ], []);

  useEffect(() => {
    if (animRef.current) return;
    animRef.current = true;
    const targets = (kpiData || []).map((k) => parseInt(k.value.replace(/,/g, '')));
    const duration = 1500;
    const steps = 60;
    let step = 0;
    const interval = setInterval(() => {
      step++;
      setAnimatedValues(targets.map((t) => Math.round((t * step) / steps)));
      if (step >= steps) clearInterval(interval);
    }, duration / steps);
    return () => clearInterval(interval);
  }, [kpiData]);

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDir('asc');
    }
  };

  const sortedActivity = useMemo(() => {
    const sorted = [...(recentActivity || [])];
    sorted.sort((a, b) => {
      let va = a[sortField];
      let vb = b[sortField];
      if (typeof va === 'string') va = va.toLowerCase();
      if (typeof vb === 'string') vb = vb.toLowerCase();
      if (va < vb) return sortDir === 'asc' ? -1 : 1;
      if (va > vb) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });
    return sorted;
  }, [recentActivity, sortField, sortDir]);

  const SortIcon = ({ field }) => {
    if (sortField !== field) return <ArrowUpDown className="w-3 h-3 inline ml-1 opacity-30" />;
    return sortDir === 'asc' ? <ArrowUpPanel className="w-3 h-3 inline ml-1 text-sky-400" /> : <ArrowDownPanel className="w-3 h-3 inline ml-1 text-sky-400" />;
  };

  const maxVal = Math.max(...chartData.map((d) => Math.max(d.organic, d.paid)));
  const maxBar = Math.max(...barData.map((d) => d.value));
  const chartWidth = 600;
  const chartHeight = 220;
  const padding = { top: 20, right: 30, bottom: 35, left: 50 };

  const pointsOrganic = chartData.map((d, i) => ({
    x: padding.left + (i / (chartData.length - 1)) * (chartWidth - padding.left - padding.right),
    y: padding.top + (1 - d.organic / (maxVal * 1.1)) * (chartHeight - padding.top - padding.bottom),
  }));
  const pointsPaid = chartData.map((d, i) => ({
    x: padding.left + (i / (chartData.length - 1)) * (chartWidth - padding.left - padding.right),
    y: padding.top + (1 - d.paid / (maxVal * 1.1)) * (chartHeight - padding.top - padding.bottom),
  }));

  const pathOrganic = `M${pointsOrganic.map((p) => `${p.x},${p.y}`).join(' L')}`;
  const pathPaid = `M${pointsPaid.map((p) => `${p.x},${p.y}`).join(' L')}`;
  const areaOrganic = `${pathOrganic} L${pointsOrganic[pointsOrganic.length - 1].x},${chartHeight - padding.bottom} L${pointsOrganic[0].x},${chartHeight - padding.bottom} Z`;
  const areaPaid = `${pathPaid} L${pointsPaid[pointsPaid.length - 1].x},${chartHeight - padding.bottom} L${pointsPaid[0].x},${chartHeight - padding.bottom} Z`;

  const yTicks = 5;
  const yTickValues = Array.from({ length: yTicks }, (_, i) => Math.round((maxVal * 1.1 * i) / (yTicks - 1)));

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold gradient-text">Dashboard</h1>
          <p className="text-sm text-slate-400 mt-1">Your SEO performance at a glance</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all">
            <CalendarPanel className="w-4 h-4" /> Last 7 days
          </button>
          <button
            onClick={() => showToast('Report exported successfully', 'success')}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-sky-500/20 border border-sky-500/30 text-sky-400 rounded-xl hover:bg-sky-500/30 transition-all"
          >
            <DownloadPanel className="w-4 h-4" /> Export
          </button>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {(kpiData || []).map((kpi, i) => {
          const Icon = kpi.icon;
          return (
            <div
              key={i}
              className="glass p-5 fade-in hover:glass-hover transition-all duration-300 cursor-pointer group"
              style={{ animationDelay: `${i * 80}ms` }}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="p-2 rounded-lg bg-white/5 group-hover:bg-white/10 transition-colors">
                  <Icon className="w-5 h-5" style={{ color: kpi.color }} />
                </div>
                <span
                  className={`flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-full ${
                    kpi.positive ? 'bg-emerald-500/15 text-emerald-400' : 'bg-red-500/15 text-red-400'
                  }`}
                >
                  {kpi.positive ? <TrendingUpPanel className="w-3 h-3" /> : <TrendingDownPanel className="w-3 h-3" />}
                  {kpi.delta}
                </span>
              </div>
              <p className="text-xs text-slate-500 mb-1">{kpi.label}</p>
              <p className="text-2xl font-bold text-slate-100 count-up">
                {animatedValues[i]?.toLocaleString() || kpi.value}
              </p>
              {/* Sparkline */}
              <svg className="w-full h-8 mt-3 opacity-50 group-hover:opacity-80 transition-opacity" viewBox={`0 0 100 20`}>
                <defs>
                  <linearGradient id={`grad-${i}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={kpi.color} stopOpacity="0.4" />
                    <stop offset="100%" stopColor={kpi.color} stopOpacity="0" />
                  </linearGradient>
                </defs>
                <path
                  d={`M${(kpi.sparkline || []).map((v, idx) => `${(idx / ((kpi.sparkline || []).length - 1)) * 100},${20 - (v / Math.max(...(kpi.sparkline || [1]))) * 18}`).join(' L')}`}
                  fill="none"
                  stroke={kpi.color}
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d={`M${(kpi.sparkline || []).map((v, idx) => `${(idx / ((kpi.sparkline || []).length - 1)) * 100},${20 - (v / Math.max(...(kpi.sparkline || [1]))) * 18}`).join(' L')} L100,20 L0,20 Z`}
                  fill={`url(#grad-${i})`}
                />
              </svg>
            </div>
          );
        })}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Area Chart */}
        <div className="lg:col-span-2 glass p-6 fade-in">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-sm font-semibold text-slate-200">Traffic Overview</h3>
              <p className="text-xs text-slate-500">Organic vs Paid traffic trends</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-sky-400" />
                <span className="text-xs text-slate-400">Organic</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-indigo-400" />
                <span className="text-xs text-slate-400">Paid</span>
              </div>
            </div>
          </div>
          <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="w-full h-auto">
            <defs>
              <linearGradient id="gradOrganic" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#38BDF8" stopOpacity="0.3" />
                <stop offset="100%" stopColor="#38BDF8" stopOpacity="0" />
              </linearGradient>
              <linearGradient id="gradPaid" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#818CF8" stopOpacity="0.3" />
                <stop offset="100%" stopColor="#818CF8" stopOpacity="0" />
              </linearGradient>
            </defs>
            {/* Grid lines */}
            {yTickValues.map((val, i) => (
              <g key={i}>
                <line
                  x1={padding.left}
                  y1={padding.top + (i / (yTicks - 1)) * (chartHeight - padding.top - padding.bottom)}
                  x2={chartWidth - padding.right}
                  y2={padding.top + (i / (yTicks - 1)) * (chartHeight - padding.top - padding.bottom)}
                  stroke="rgba(255,255,255,0.05)"
                  strokeDasharray="4 4"
                />
                <text
                  x={padding.left - 8}
                  y={padding.top + (i / (yTicks - 1)) * (chartHeight - padding.top - padding.bottom) + 4}
                  textAnchor="end"
                  className="text-[10px] fill-slate-600"
                >
                  {`${(val / 1000).toFixed(0)}k`}
                </text>
              </g>
            ))}
            {/* XPanel labels */}
            {chartData.map((d, i) => (
              <text
                key={i}
                x={padding.left + (i / (chartData.length - 1)) * (chartWidth - padding.left - padding.right)}
                y={chartHeight - 8}
                textAnchor="middle"
                className="text-[10px] fill-slate-600"
              >
                {d.day}
              </text>
            ))}
            {/* Areas */}
            <path d={areaOrganic} fill="url(#gradOrganic)" />
            <path d={areaPaid} fill="url(#gradPaid)" />
            {/* Lines */}
            <path d={pathOrganic} fill="none" stroke="#38BDF8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d={pathPaid} fill="none" stroke="#818CF8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            {/* Dots */}
            {pointsOrganic.map((p, i) => (
              <circle key={`o-${i}`} cx={p.x} cy={p.y} r="3" fill="#38BDF8" stroke="#0F172A" strokeWidth="2" />
            ))}
            {pointsPaid.map((p, i) => (
              <circle key={`p-${i}`} cx={p.x} cy={p.y} r="3" fill="#818CF8" stroke="#0F172A" strokeWidth="2" />
            ))}
          </svg>
        </div>

        {/* Bar Chart */}
        <div className="glass p-6 fade-in">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-sm font-semibold text-slate-200">Traffic Sources</h3>
              <p className="text-xs text-slate-500">Channel distribution</p>
            </div>
          </div>
          <div className="space-y-4">
            {barData.map((item, i) => (
              <div key={i} className="space-y-1.5">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">{item.name}</span>
                  <span className="text-xs font-medium text-slate-300">{item.value}%</span>
                </div>
                <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-1000 ease-out"
                    style={{
                      width: `${(item.value / maxBar) * 100}%`,
                      background: i === 0
                        ? 'linear-gradient(90deg, #38BDF8, #818CF8)'
                        : i === 1
                        ? 'linear-gradient(90deg, #818CF8, #C084FC)'
                        : i === 2
                        ? 'linear-gradient(90deg, #22C55E, #4ADE80)'
                        : i === 3
                        ? 'linear-gradient(90deg, #F59E0B, #FBBF24)'
                        : 'linear-gradient(90deg, #EF4444, #F87171)',
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Table + Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* ActivityPanel Table */}
        <div className="lg:col-span-2 glass p-6 fade-in">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-slate-200">Recent ActivityPanel</h3>
              <p className="text-xs text-slate-500">Latest SEO tasks and updates</p>
            </div>
            <button className="flex items-center gap-1 text-xs text-sky-400 hover:text-sky-300 transition-colors">
              View all <ChevronRightPanel className="w-3 h-3" />
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-white/5">
                  {[
                    { key: 'date', label: 'Date' },
                    { key: 'task', label: 'Task' },
                    { key: 'domain', label: '