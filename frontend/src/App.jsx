import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { BarChart3, TrendingUp, Search, Users, Bell, Settings, LayoutDashboard, ChevronDown, ArrowUpRight, ArrowDownRight, Mail, FileText, Link, Activity } from 'lucide-react';

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

function LandingPage({ onStart }) {
  return (
    <div className="min-h-screen bg-[#06080f] text-slate-100 font-[Inter] flex flex-col">
      <header className="flex items-center justify-between px-8 py-6 border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#00C9A7] to-[#1E3A5F] flex items-center justify-center shadow-2xl shadow-[#00C9A7]/20">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">StellarRank</h1>
            <p className="text-xs text-slate-400">AI SEO Command Center</p>
          </div>
        </div>
        <button 
          onClick={onStart}
          className="px-6 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-[#00C9A7] to-[#1E3A5F] rounded-lg hover:opacity-90 transition-all duration-200 shadow-lg shadow-[#00C9A7]/20 hover:shadow-[#00C9A7]/40"
        >
          Go to Dashboard
        </button>
      </header>
      
      <main className="flex-1 flex items-center justify-center px-6 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block px-4 py-1.5 bg-[#00C9A7]/10 rounded-full text-[#00C9A7] text-sm font-medium mb-6 border border-[#00C9A7]/20">
            AI-Powered SEO Platform
          </div>
          <h2 className="text-5xl md:text-6xl font-bold leading-tight mb-6">
            <span className="gradient-text">Dominate</span> the Search Rankings<br />
            <span className="text-slate-300">with Intelligent Automation</span>
          </h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10">
            StellarRank uses advanced AI to analyze keywords, generate optimized content, 
            and build backlinks that skyrocket your organic traffic.
          </p>
          <div className="flex flex-wrap gap-4 justify-center mb-16">
            <button 
              onClick={onStart}
              className="px-8 py-3.5 text-base font-semibold text-white bg-gradient-to-r from-[#00C9A7] to-[#1E3A5F] rounded-xl hover:opacity-90 transition-all duration-200 shadow-xl shadow-[#00C9A7]/20 hover:shadow-[#00C9A7]/40"
            >
              Launch Dashboard
            </button>
            <button className="px-8 py-3.5 text-base font-medium text-slate-300 bg-white/5 rounded-xl border border-white/10 hover:bg-white/10 transition-all duration-200">
              Watch Demo
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="glass p-8 text-left">
              <Search className="w-10 h-10 text-[#00C9A7] mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Smart Keyword Research</h3>
              <p className="text-slate-400 text-sm">Discover high-value keywords with AI-powered difficulty analysis and volume predictions.</p>
            </div>
            <div className="glass p-8 text-left">
              <FileText className="w-10 h-10 text-[#00C9A7] mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Auto Content Generation</h3>
              <p className="text-slate-400 text-sm">Generate SEO-optimized articles that rank, using our proprietary AI models.</p>
            </div>
            <div className="glass p-8 text-left">
              <Link className="w-10 h-10 text-[#00C9A7] mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Backlink Building</h3>
              <p className="text-slate-400 text-sm">Automated outreach and link placement that grows your domain authority.</p>
            </div>
          </div>
        </div>
      </main>
      
      <footer className="px-8 py-6 border-t border-white/5">
        <p className="text-center text-slate-500 text-sm">© 2025 StellarRank. All rights reserved.</p>
      </footer>
    </div>
  );
}

function Sidebar({ activeView, onNavigate }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 flex-shrink-0 flex flex-col border-r border-white/5 bg-white/[0.02] h-full">
      <div className="p-6 border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#00C9A7] to-[#1E3A5F] flex items-center justify-center">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-white">StellarRank</h1>
            <p className="text-xs text-slate-400">AI SEO Command Center</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group ${
                isActive
                  ? 'bg-[#1E3A5F]/40 text-white border border-[#00C9A7]/20'
                  : 'text-slate-400 hover:text-white hover:bg-white/5'
              }`}
            >
              <Icon className={`w-5 h-5 transition-colors ${
                isActive ? 'text-[#00C9A7]' : 'text-slate-500 group-hover:text-slate-300'
              }`} />
              {item.label}
            </button>
          );
        })}
      </nav>
      <div className="p-4 border-t border-white/5">
        <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-white/[0.02]">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#00C9A7] to-[#1E3A5F] flex items-center justify-center">
            <Users className="w-4 h-4 text-white" />
          </div>
          <div>
            <p className="text-sm font-medium text-white">Sarah Chen</p>
            <p className="text-xs text-slate-400">Enterprise Plan</p>
          </div>
        </div>
      </div>
    </aside>
  );
}

function TopBar({ notificationCount }) {
  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-white/5 flex-shrink-0 bg-white/[0.02]">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-slate-300">StellarRank</span>
          <span className="text-xs text-slate-500">/</span>
          <span className="text-sm text-slate-400">Dashboard</span>
        </div>
        <div className="hidden md:flex items-center gap-2 bg-white/5 rounded-lg px-3 py-1.5 border border-white/5">
          <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input type="text" placeholder="Search keywords, projects..." className="bg-transparent text-sm text-slate-300 placeholder-slate-500 outline-none w-48" />
        </div>
      </div>
      <div className="flex items-center gap-4">
        <button className="relative p-2 rounded-lg hover:bg-white/5 transition-all duration-200">
          <Bell className="w-5 h-5 text-slate-400" />
          {notificationCount > 0 && (
            <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-[#00C9A7] rounded-full text-[10px] font-bold text-white flex items-center justify-center">
              {notificationCount}
            </span>
          )}
        </button>
        <div className="flex items-center gap-3 pl-4 border-l border-white/5">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#00C9A7] to-[#1E3A5F] flex items-center justify-center">
            <span className="text-sm font-semibold text-white">SC</span>
          </div>
          <ChevronDown className="w-4 h-4 text-slate-400" />
        </div>
      </div>
    </header>
  );
}

function KPICard({ icon: Icon, label, value, delta, prefix = '', suffix = '', delay = 0 }) {
  const [count, setCount] = useState(0);
  const target = value;

  useEffect(() => {
    const timeout = setTimeout(() => {
      const duration = 1500;
      const steps = 60;
      const increment = target / steps;
      let current = 0;
      const interval = setInterval(() => {
        current += increment;
        if (current >= target) {
          setCount(target);
          clearInterval(interval);
        } else {
          setCount(Math.floor(current));
        }
      }, duration / steps);
      return () => clearInterval(interval);
    }, delay * 200);
    return () => clearTimeout(timeout);
  }, [target, delay]);

  const isPositive = delta >= 0;
  return (
    <div className="glass p-5 fade-in" style={{ animationDelay: `${delay * 0.1}s` }}>
      <div className="flex items-center justify-between mb-3">
        <div className="p-2 rounded-lg bg-white/5">
          <Icon className="w-5 h-5 text-[#00C9A7]" />
        </div>
        <span className={`flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full ${
          isPositive ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'
        }`}>
          {isPositive ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
          {Math.abs(delta)}%
        </span>
      </div>
      <p className="text-sm text-slate-400 mb-1">{label}</p>
      <p className="text-2xl font-bold text-white">{prefix}{count.toLocaleString()}{suffix}</p>
    </div>
  );
}

function LineChart() {
  const data = useMemo(() => [
    { day: 'Mon', value: 820 },
    { day: 'Tue', value: 945 },
    { day: 'Wed', value: 1100 },
    { day: 'Thu', value: 1280 },
    { day: 'Fri', value: 1430 },
    { day: 'Sat', value: 1510 },
    { day: 'Sun', value: 1680 },
  ], []);

  const svgWidth = 400;
  const svgHeight = 200;
  const padding = 30;
  const chartWidth = svgWidth - padding * 2;
  const chartHeight = svgHeight - padding * 2;

  const maxValue = Math.max(...data.map(d => d.value));
  const minValue = Math.min(...data.map(d => d.value));
  const valueRange = maxValue - minValue || 1;

  const points = data.map((d, i) => ({
    x: padding + (i / (data.length - 1)) * chartWidth,
    y: padding + chartHeight - ((d.value - minValue) / valueRange) * chartHeight,
  }));

  const pathD = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
  const areaD = `${pathD} L ${points[points.length - 1].x} ${padding + chartHeight} L ${points[0].x} ${padding + chartHeight} Z`;

  return (
    <div className="glass p-5 fade-in">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-slate-300">Ranking Trend (7 Days)</h3>
        <span className="text-xs text-[#00C9A7] bg-[#00C9A7]/10 px-2 py-0.5 rounded-full">+12.4%</span>
      </div>
      <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`} className="w-full h-48">
        <defs>
          <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#00C9A7" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#00C9A7" stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d={areaD} fill="url(#chartGradient)" className="animate-pulse" />
        <path d={pathD} fill="none" stroke="#00C9A7" strokeWidth="2" strokeLinecap="round" className="animate-dash" />
        {points.map((p, i) => (
          <circle key={i} cx={p.x} cy={p.y} r="3" fill="#00C9A7" className="animate-ping" style={{ animationDelay: `${i * 0.1}s` }} />
        ))}
        {data.map((d, i) => (
          <text key={i} x={points[i].x} y={svgHeight - 5} textAnchor="middle" fill="#64748b" fontSize="10">
            {d.day}
          </text>
        ))}
      </svg>
    </div>
  );
}

function BarChart() {
  const data = useMemo(() => [
    { label: 'Product A', value: 85, color: '#00C9A7' },
    { label: 'Product B', value: 72, color: '#00C9A7' },
    { label: 'Product C', value: 95, color: '#1E3A5F' },
    { label: 'Product D', value: 65, color: '#00C9A7' },
    { label: 'Product E', value: 78, color: '#1E3A5F' },
  ], []);

  const maxValue = 100;
  const barHeight = 200;

  return (
    <div className="glass p-5 fade-in">
      <h3 className="text-sm font-medium text-slate-300 mb-4">Keyword Difficulty Score</h3>
      <div className="flex items-end justify-between gap-4 h-48">
        {data.map((item, i) => (
          <div key={i} className="flex-1 flex flex-col items-center gap-2">
            <span className="text-xs text-slate-400 font-medium">{item.value}%</span>
            <div
              className="w-full rounded-t-lg transition-all duration-1000"
              style={{
                height: `${(item.value / maxValue) * barHeight}px`,
                background: `linear-gradient(to top, ${item.color}, ${item.color}88)`,
                opacity: 0.8 + (item.value / 100) * 0.2,
              }}
            />
            <span className="text-xs text-slate-500 truncate w-full text-center">{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function DataTable() {
  const [data, setData] = useState([
    { keyword: 'organic skincare', volume: 14200, difficulty: 45, position: 3, trend: 'up' },
    { keyword: 'natural face serum', volume: 8300, difficulty: 62, position: 7, trend: 'down' },
    { keyword: 'vegan moisturizer', volume: 5600, difficulty: 38, position: 1, trend: 'up' },
    { keyword: 'clean beauty routine', volume: 12400, difficulty: 71, position: 12, trend: 'up' },
    { keyword: 'sustainable cosmetics', volume: 9800, difficulty: 55, position: 5, trend: 'down' },
  ]);
  const [sortKey, setSortKey] = useState('position');
  const [sortDir, setSortDir] = useState('asc');

  const sortedData = useMemo(() => {
    return [...data].sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      if (typeof aVal === 'string') {
        return sortDir === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
      }
      return sortDir === 'asc' ? aVal - bVal : bVal - aVal;
    });
  }, [data, sortKey, sortDir]);

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir(prev => prev === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  };

  return (
    <div className="glass p-5 fade-in overflow-hidden">
      <h3 className="text-sm font-medium text-slate-300 mb-4">Keyword Rankings</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/5">
              {['keyword', 'volume', 'difficulty', 'position', 'trend'].map((col) => (
                <th
                  key={col}
                  onClick={() => handleSort(col)}
                  className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:text-white transition-colors"
                >
                  <div className="flex items-center gap-1">
                    {col}
                    {sortKey === col && (
                      <span className="text-[#00C9A7]">{sortDir === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {(sortedData || []).map((row, i) => (
              <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                <td className="px-4 py-3 text-white font-medium">{row.keyword}</td>
                <td className="px-4 py-3 text-slate-300">{row.volume.toLocaleString()}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-16 h-1.5 bg-white/10 rounded-full overflow-hidden">
                      <div className="h-full rounded-full bg-[#00C9A7]" style={{ width: `${row.difficulty}%` }} />
                    </div>
                    <span className="text-slate-400 text-xs">{row.difficulty}%</span>
                  </div>
                </td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                    row.position <= 3 ? 'bg-green-500/10 text-green-400' :
                    row.position <= 10 ? 'bg-yellow-500/10 text-yellow-400' :
                    'bg-red-500/10 text-red-400'
                  }`}>
                    #{row.position}
                  </span>
                </td>
                <td className="px-4 py-3">
                  {row.trend === 'up' ? (
                    <ArrowUpRight className="w-4 h-4 text-green-400" />
                  ) : (
                    <ArrowDownRight className="w-4 h-4 text-red-400" />
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function QuickActions() {
  return (
    <div className="glass p-5 fade-in">
      <h3 className="text-sm font-medium text-slate-300 mb-4">Quick Actions</h3>
      <div className="space-y-3">
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-white/5 hover:bg-white/10 transition-all duration-200 group">
          <Search className="w-5 h-5 text-[#00C9A7] group-hover:scale-110 transition-transform" />
          <div className="text-left">
            <p className="text-sm font-medium text-white">New Keyword Research</p>
            <p className="text-xs text-slate-400">Discover untapped opportunities</p>
          </div>
        </button>
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-white/5 hover:bg-white/10 transition-all duration-200 group">
          <FileText className="w-5 h-5 text-[#00C9A7] group-hover:scale-110 transition-transform" />
          <div className="text-left">
            <p className="text-sm font-medium text-white">Generate Content</p>
            <p className="text-xs text-slate-400">AI-powered SEO articles</p>
          </div>
        </button>
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-white/5 hover:bg-white/10 transition-all duration-200 group">
          <Link className="w-5 h-5 text-[#00C9A7] group-hover:scale-110 transition-transform" />
          <div className="text-left">
            <p className="text-sm font-medium text-white">Build Backlinks</p>
            <p className="text-xs text-slate-400">Outreach & link building</p>
          </div>
        </button>
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-white/5 hover:bg-white/10 transition-all duration-200 group">
          <Mail className="w-5 h-5 text-[#00C9A7] group-hover:scale-110 transition-transform" />
          <div className="text-left">
            <p className="text-sm font-medium text-white">Send Report</p>
            <p className="text-xs text-slate-400">Share with stakeholders</p>
          </div>
        </button>
      </div>
    </div>
  );
}

export default function App() {
  const [activeView, setActiveView] = useState('dashboard');
  const [notificationCount, setNotificationCount] = useState(0);
  const [cssInjected, setCssInjected] = useState(false);
  const [showLanding, setShowLanding] = useState(true);

  useEffect(() => {
    if (!cssInjected) {
      const style = document.createElement('style');
      style.textContent = `
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        :root { --accent: #00C9A7; --accent2: #1E3A5F; }
        .glass { background: rgba(255,255,255,0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; }
        .gradient-text { background: linear-gradient(135deg, #00C9A7, #1E3A5F, #6366F1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .shimmer { background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
        @keyframes shimmer { 0% { background-position: -200% 0 } 100% { background-position: 200% 0 } }
        @keyframes fadeIn { from { opacity:0; transform:translateY(8px) } to { opacity:1; transform:translateY(0) } }
        .fade-in { animation: fadeIn 0.3s ease forwards; }
        @keyframes dash { to { stroke-dashoffset: 0; } }
        .animate-dash { stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: dash 2s ease forwards; }
      `;
      document.head.appendChild(style);
      setCssInjected(true);
    }
  }, [cssInjected]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await apiFetch('/api/notifications');
      if (result && result.count !== undefined) {
        setNotificationCount(result.count);
      } else {
        setNotificationCount(5);
      }
    };
    fetchData();
  }, []);

  if (showLanding) {
    return <LandingPage onStart={() => setShowLanding(false)} />;
  }

  return (
    <div className="flex h-screen overflow-hidden bg-[#06080f] text-slate-100 font-[Inter]">
      <Sidebar activeView={activeView} onNavigate={setActiveView} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar notificationCount={notificationCount} />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold gradient-text">SEO Command Center</h2>
                <p className="text-sm text-slate-400 mt-1">AI-driven insights for your e-commerce rankings</p>
              </div>
              <div className="flex items-center gap-3">
                <button className="px-4 py-2 text-sm font-medium text-white bg-[#00C9A7] hover:bg-[#00C9A7]/90 rounded-lg transition-all duration-200">
                  Run Audit
                </button>
                <button className="px-4 py-2 text-sm font-medium text-slate-300 bg-white/5 hover:bg-white/10 rounded-lg border border-white/5 transition-all duration-200">
                  Export
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
              <KPICard icon={Search} label="Keywords Tracked" value={2847} delta={12.5} delay={0} />
              <KPICard icon={TrendingUp} label="Avg. Position" value={3.2} delta={8.3} prefix=" #" suffix="" delay={1} />
              <KPICard icon={BarChart3} label="Content Generated" value={156} delta={22.1} delay={2} />
              <KPICard icon={Users} label="Backlinks Built" value={892} delta={-3.7} delay={3} />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
              <div className="lg:col-span-2">
                <LineChart />
              </div>
              <div>
                <BarChart />
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div className="lg:col-span-2">
                <DataTable />
              </div>
              <div>
                <QuickActions />
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}