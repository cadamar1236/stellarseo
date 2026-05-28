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
    style.textContent = `
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
      :root { --accent: #00B4D8; --accent2: #1E3A5F; }
      .glass { background: rgba(255,255,255,0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; }
      .gradient-text { background: linear-gradient(135deg, #00B4D8, #1E3A5F, #6366F1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
      .shimmer { background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
      @keyframes shimmer { 0% { background-position: -200% 0 } 100% { background-position: 200% 0 } }
      @keyframes fadeIn { from { opacity:0; transform:translateY(8px) } to { opacity:1; transform:translateY(0) } }
      .fade-in { animation: fadeIn 0.3s ease forwards; }
      @keyframes slideIn { from { opacity:0; transform:translateY(-4px) } to { opacity:1; transform:translateY(0) } }
      .slide-in { animation: slideIn 0.2s ease forwards; }
      @keyframes pulse { 0%, 100% { opacity:1 } 50% { opacity:0.5 } }
      .animate-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
      .scrollbar-thin::-webkit-scrollbar { width: 4px; }
      .scrollbar-thin::-webkit-scrollbar-track { background: transparent; }
      .scrollbar-thin::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }
      .scrollbar-thin::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
    `;
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
    <div className="flex h-screen overflow-hidden bg-[#06080f] text-slate-100">
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

        <main className="flex-1 overflow-y-auto p-4 lg:p-6 scrollbar-thin bg-[#06080f]">
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
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#00B4D8] to-[#1E3A5F] flex items-center justify-center flex-shrink-0">
            <ZapPanel className="w-4 h-4 text-white" />
          </div>
          {sidebarOpen && (
            <span className="font-semibold text-base whitespace-nowrap gradient-text">
              StellarRank
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
                  ? 'bg-[#00B4D8]/15 text-[#00B4D8] border border-[#00B4D8]/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <Icon className={`w-4 h-4 flex-shrink-0 ${isActive ? 'text-[#00B4D8]' : ''}`} />
              {sidebarOpen && (
                <span className="whitespace-nowrap truncate">{item.label}</span>
              )}
              {isActive && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-6 bg-[#00B4D8] rounded-r-full" />
              )}
            </button>
          );
        })}
      </nav>

      <div className="p-3 border-t border-white/5">
        <div className={`glass p-3 ${!sidebarOpen && 'flex justify-center'}`}>
          {sidebarOpen ? (
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#00B4D8] to-[#1E3A5F] flex items-center justify-center flex-shrink-0">
                <span className="text-xs font-bold text-white">JD</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-slate-200 truncate">John Doe</p>
                <p className="text-[10px] text-slate-500 truncate">Enterprise Plan</p>
              </div>
              <ChevronDownPanel className="w-3 h-3 text-slate-500 flex-shrink-0" />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#00B4D8] to-[#1E3A5F] flex items-center justify-center">
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
    <header className="h-14 flex items-center justify-between px-4 lg:px-6 border-b border-white/5 flex-shrink-0 bg-[#06080f]">
      <div className="flex items-center gap-4">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 rounded-lg hover:bg-white/5 transition-colors"
        >
          {sidebarOpen ? <XPanel className="w-4 h-4" /> : <MenuPanel className="w-4 h-4" />}
        </button>
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/5 border border-white/5 focus-within:border-[#00B4D8]/50 transition-all">
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
              <span className="absolute -top-0.5 -right-0.5 w-[18px] h-[18px] bg-[#00B4D8] text-white text-[10px] font-bold rounded-full flex items-center justify-center animate-pulse">
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
                  className="text-[10px] text-[#00B4D8] hover:text-[#00B4D8]/80"
                >
                  Mark all read
                </button>
              </div>
              {(dummyNotifs || []).slice(0, notifications).map((n) => (
                <div key={n.id} className="flex items-start gap-3 p-3 hover:bg-white/5 rounded-lg transition-colors">
                  <div className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${n.unread ? 'bg-[#00B4D8]' : 'bg-slate-600'}`} />
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
    return sortDir === 'asc' ? <ArrowUpPanel className="w-3 h-3 inline ml-1 text-[#00B4D8]" /> : <ArrowDownPanel className="w-3 h-3 inline ml-1 text-[#00B4D8]" />;
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
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-[#00B4D8]/20 border border-[#00B4D8]/30 text-[#00B4D8] rounded-xl hover:bg-[#00B4D8]/30 transition-all"
          >
            <DownloadPanel className="w-4 h-4" /> Export
          </button>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
        {kpiData.map((kpi, idx) => (
          <div key={idx} className="glass p-5 fade-in" style={{ animationDelay: `${idx * 0.1}s` }}>
            <div className="flex items-start justify-between mb-4">
              <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center">
                <kpi.icon className="w-5 h-5" style={{ color: kpi.color }} />
              </div>
              <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                kpi.positive ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'
              }`}>
                {kpi.delta}
              </span>
            </div>
            <p className="text-2xl font-bold text-white mb-1">
              {animatedValues[idx]?.toLocaleString() || '0'}
            </p>
            <p className="text-xs text-slate-400">{kpi.label}</p>
            <div className="mt-3 h-8 flex items-end gap-0.5">
              {kpi.sparkline.map((v, i) => (
                <div
                  key={i}
                  className="flex-1 rounded-sm transition-all duration-300"
                  style={{
                    height: `${(v / Math.max(...kpi.sparkline)) * 100}%`,
                    background: kpi.color,
                    opacity: 0.3 + (v / Math.max(...kpi.sparkline)) * 0.5,
                  }}
                />
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4 mb-6">
        <div className="xl:col-span-2 glass p-5 fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-300">Traffic Overview</h3>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 rounded-full bg-[#00B4D8]" />
                <span className="text-[10px] text-slate-500">Organic</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 rounded-full bg-[#1E3A5F]" />
                <span className="text-[10px] text-slate-500">Paid</span>
              </div>
            </div>
          </div>
          <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="w-full h-auto" style={{ maxHeight: '220px' }}>
            <defs>
              <linearGradient id="organicGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#00B4D8" stopOpacity="0.3" />
                <stop offset="100%" stopColor="#00B4D8" stopOpacity="0" />
              </linearGradient>
              <linearGradient id="paidGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#1E3A5F" stopOpacity="0.3" />
                <stop offset="100%" stopColor="#1E3A5F" stopOpacity="0" />
              </linearGradient>
            </defs>
            {/* Grid lines */}
            {yTickValues.map((v, i) => (
              <g key={i}>
                <line x1={padding.left} y1={padding.top + (i / (yTicks - 1)) * (chartHeight - padding.top - padding.bottom)}
                  x2={chartWidth - padding.right} y2={padding.top + (i / (yTicks - 1)) * (chartHeight - padding.top - padding.bottom)}
                  stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
                <text x={padding.left - 8} y={padding.top + (i / (yTicks - 1)) * (chartHeight - padding.top - padding.bottom) + 3}
                  textAnchor="end" className="text-[9px]" fill="rgba(255,255,255,0.3)">
                  {v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v}
                </text>
              </g>
            ))}
            {/* XPanel axis labels */}
            {chartData.map((d, i) => (
              <text key={i} x={padding.left + (i / (chartData.length - 1)) * (chartWidth - padding.left - padding.right)}
                y={chartHeight - 8} textAnchor="middle" className="text-[9px]" fill="rgba(255,255,255,0.3)">
                {d.day}
              </text>
            ))}
            {/* Area fills */}
            <path d={areaOrganic} fill="url(#organicGrad)" className="transition-all duration-1000" />
            <path d={areaPaid} fill="url(#paidGrad)" className="transition-all duration-1000" />
            {/* Lines */}
            <path d={pathOrganic} fill="none" stroke="#00B4D8" strokeWidth="2" className="transition-all duration-1000" />
            <path d={pathPaid} fill="none" stroke="#1E3A5F" strokeWidth="2" strokeDasharray="4,2" className="transition-all duration-1000" />
            {/* Dots on organic */}
            {pointsOrganic.map((p, i) => (
              <circle key={i} cx={p.x} cy={p.y} r="3" fill="#00B4D8" stroke="#06080f" strokeWidth="1.5" />
            ))}
          </svg>
        </div>

        <div className="glass p-5 fade-in">
          <h3 className="text-sm font-semibold text-slate-300 mb-4">Traffic Sources</h3>
          <div className="space-y-3">
            {barData.map((item, i) => (
              <div key={i} className="fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-slate-400">{item.name}</span>
                  <span className="text-xs font-medium text-slate-300">{item.value}%</span>
                </div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-1000 ease-out"
                    style={{
                      width: `${(item.value / maxBar) * 100}%`,
                      background: `linear-gradient(90deg, ${['#00B4D8', '#1E3A5F', '#6366F1', '#22C55E', '#F59E0B'][i]}, ${['#38BDF8', '#2E4A7F', '#818CF8', '#4ADE80', '#FBBF24'][i]})`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent ActivityPanel Table + Quick Actions */}
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-4">
        <div className="xl:col-span-3 glass overflow-hidden fade-in">
          <div className="flex items-center justify-between p-4 border-b border-white/5">
            <h3 className="text-sm font-semibold text-slate-300">Recent ActivityPanel</h3>
            <button className="flex items-center gap-1 text-xs text-[#00B4D8] hover:text-[#00B4D8]/80 transition-colors">
              View All <ArrowRightPanel className="w-3 h-3" />
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-white/5 bg-white/[0.02]">
                  <th
                    className="text-left p-3 font-medium text-slate-500 cursor-pointer hover:text-slate-300 transition-colors"
                    onClick={() => handleSort('date')}
                  >
                    Date <SortIcon field="date" />
                  </th>
                  <th
                    className="text-left p-3 font-medium text-slate-500 cursor-pointer hover:text-slate-300 transition-colors"
                    onClick={() => handleSort('task')}
                  >
                    Task <SortIcon field="task" />
                  </th>
                  <th
                    className="text-left p-3 font-medium text-slate-500 cursor-pointer hover:text-slate-300 transition-colors"
                    onClick={() => handleSort('domain')}
                  >
                    Domain <SortIcon field="domain" />
                  </th>
                  <th
                    className="text-left p-3 font-medium text-slate-500 cursor-pointer hover:text-slate-300 transition-colors"
                    onClick={() => handleSort('status')}
                  >
                    Status <SortIcon field="status" />
                  </th>
                  <th
                    className="text-right p-3 font-medium text-slate-500 cursor-pointer hover:text-slate-300 transition-colors"
                    onClick={() => handleSort('keywords')}
                  >
                    Keywords <SortIcon field="keywords" />
                  </th>
                </tr>
              </thead>
              <tbody>
                {sortedActivity.map((row, idx) => (
                  <tr key={row.id} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                    <td className="p-3 text-slate-400 whitespace-nowrap">
                      {row.date}
                    </td>
                    <td className="p-3 text-slate-300 font-medium">{row.task}</td>
                    <td className="p-3 text-slate-400">{row.domain}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium ${
                        row.status === 'Completed' ? 'bg-emerald-500/10 text-emerald-400' :
                        row.status === 'Processing' ? 'bg-sky-500/10 text-sky-400' :
                        'bg-amber-500/10 text-amber-400'
                      }`}>
                        {row.status}
                      </span>
                    </td>
                    <td className="p-3 text-right text-slate-300">{row.keywords}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-slate-300 px-1">Quick Actions</h3>
          {quickActions.map((action, idx) => {
            const Icon = action.icon;
            return (
              <button
                key={action.id}
                onClick={() => showToast(`${action.label} initiated`,