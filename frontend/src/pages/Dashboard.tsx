import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { Users, AlertCircle, Search, ArrowUpRight, ArrowDownRight, Zap, MapPin } from 'lucide-react';
import {
  getDashboardStats,
  getDashboardTrends,
  getCustomerDetail,
  getComparisonStats,
  SummaryStats,
  MonthlyData,
  ComparisonData
} from '../services/api';

import {
  getParetoAnalysis,
  getGarduStats,
  getPowerChanges,
  getZeroUsageAnomalies,
  getHighVarianceAnomalies,
  getDayaDistribution
} from '../services/analyticsApi';

import { getUlpOverview, UlpOverviewItem } from '../services/ulpApi';

import ParetoChart from '../components/analytics/ParetoChart';
import GarduChart from '../components/analytics/GarduChart';
import PowerChangeCard from '../components/analytics/PowerChangeCard';
import AnomalyTable from '../components/analytics/AnomalyTable';
import ComparisonChart from '../components/analytics/ComparisonChart';
import DayaCompositionChart from '../components/analytics/DayaCompositionChart';

interface DashboardProps {
  setActiveTab: (tab: string) => void;
  onShowDetail: (data: any) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ setActiveTab, onShowDetail }) => {
  const navigate = useNavigate();
  // Basic Stats
  const [stats, setStats] = useState<SummaryStats | null>(null);
  const [trends, setTrends] = useState<MonthlyData[]>([]);

  // Advanced Analytics
  const [paretoData, setParetoData] = useState<any[]>([]);
  const [garduData, setGarduData] = useState<any[]>([]);
  const [powerData, setPowerData] = useState<any>(null);
  const [anomalyData, setAnomalyData] = useState<any[]>([]);
  const [anomalyPage, setAnomalyPage] = useState(1);
  const [anomalyTotalPages, setAnomalyTotalPages] = useState(1);
  const [anomalyTotalItems, setAnomalyTotalItems] = useState(0);
  const [anomalyLoading, setAnomalyLoading] = useState(false);

  const [varianceData, setVarianceData] = useState<any[]>([]);
  const [variancePage, setVariancePage] = useState(1);
  const [varianceTotalPages, setVarianceTotalPages] = useState(1);
  const [varianceTotalItems, setVarianceTotalItems] = useState(0);
  const [varianceLoading, setVarianceLoading] = useState(false);

  const [dayaData, setDayaData] = useState<any[]>([]);

  // Comparison Data
  const [comparisonData, setComparisonData] = useState<ComparisonData | null>(null);

  const [loading, setLoading] = useState(true);

  // Search State
  const [searchId, setSearchId] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  // ULP Filter State
  const [ulps, setUlps] = useState<UlpOverviewItem[]>([]);
  const [selectedUlp, setSelectedUlp] = useState<number | undefined>(undefined);

  // Fetch ULP List on Mount
  useEffect(() => {
    getUlpOverview().then(setUlps).catch(console.error);
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Wrapper to safely fetch data without throwing
        const safeFetch = async <T,>(promise: Promise<T>, fallback: T): Promise<T> => {
          try {
            return await promise;
          } catch (error) {
            console.error("Fetch failed:", error);
            return fallback;
          }
        };

        const [
          statsData, trendsData,
          pareto, gardu, power,
          compData,
          dayaDist,
        ] = await Promise.all([
          safeFetch(getDashboardStats(selectedUlp), null),
          safeFetch(getDashboardTrends(selectedUlp), []),
          safeFetch(getParetoAnalysis(10, selectedUlp), []),
          safeFetch(getGarduStats(20, selectedUlp), []),
          safeFetch(getPowerChanges(selectedUlp), null),
          safeFetch(getComparisonStats(selectedUlp), null),
          safeFetch(getDayaDistribution(2025, selectedUlp), []),
        ]);

        if (statsData) setStats(statsData);
        if (trendsData) setTrends(trendsData);
        if (pareto) setParetoData(pareto);
        if (gardu) setGarduData(gardu);
        if (power) setPowerData(power);
        if (compData) setComparisonData(compData);
        if (dayaDist) setDayaData(dayaDist);

        // Initial Fetch for Anomalies (Page 1)
        fetchAnomalies(1);
        fetchVariance(1);

      } catch (error) {
        console.error("Dashboard Load Failed", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [selectedUlp]); // Trigger when selectedUlp changes

  // Fetch Anomaly Data
  const fetchAnomalies = async (page: number) => {
    setAnomalyLoading(true);
    try {
      const response: any = await getZeroUsageAnomalies(page, 10, selectedUlp); // Limit 10 per page
      setAnomalyData(response.data || []);
      setAnomalyTotalPages(response.pages || 1);
      setAnomalyTotalItems(response.total || 0);
      setAnomalyPage(response.page || 1);
    } catch (e) {
      console.error("Failed to fetch zero usage", e);
    } finally {
      setAnomalyLoading(false);
    }
  };

  // Filter State
  const [varianceFilter, setVarianceFilter] = useState<{ min?: number, max?: number } | null>(null);

  const fetchVariance = async (page: number, filter?: { min?: number, max?: number }) => {
    setVarianceLoading(true);
    try {
      // Use provided filter or current state (if not provided)
      const activeFilter = filter !== undefined ? filter : varianceFilter;

      const response: any = await getHighVarianceAnomalies(
        page,
        10,
        selectedUlp,
        activeFilter?.min,
        activeFilter?.max
      );
      setVarianceData(response.data || []);
      setVarianceTotalPages(response.pages || 1);
      setVarianceTotalItems(response.total || 0);
      setVariancePage(response.page || 1);
    } catch (e) {
      console.error("Failed to fetch variance", e);
    } finally {
      setVarianceLoading(false);
    }
  };

  const handleVarianceFilterChange = (range: { min?: number, max?: number } | undefined) => {
    setVarianceFilter(range || null);
    fetchVariance(1, range || undefined); // Reset to page 1 with new filter
  };


  const handleSearch = async () => {
    if (!searchId) return;
    setIsSearching(true);
    try {
      const data = await getCustomerDetail(searchId);
      onShowDetail(data); // Navigate to Detail Page
    } catch (e: any) {
      alert(`Customer ID ${searchId} not found.`);
    } finally {
      setIsSearching(false);
    }
  };

  // Prepare sorted data for chart (Top 7 + Others)
  const sortedDaya = [...dayaData].sort((a, b) => b.count - a.count);
  const top7Daya = sortedDaya.slice(0, 7);
  const othersDaya = sortedDaya.slice(7);

  const chartDayaData = othersDaya.length > 0 ? [
    ...top7Daya,
    {
      label: 'Lainnya',
      count: othersDaya.reduce((sum, item) => sum + item.count, 0),
      total_kwh: othersDaya.reduce((sum, item) => sum + item.total_kwh, 0),
      daya: 0
    }
  ] : sortedDaya;

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-gray-400">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
      <p>Memuat Analisis Dashboard...</p>
    </div>
  );

  return (
    <div className="space-y-6 pb-12">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Dashboard Analytics</h1>
          <p className="text-gray-500 text-sm mt-1">Monitoring & Analisis Energi PLN Periode 2024-2025</p>
        </div>

        <div className="flex flex-col md:flex-row gap-3 w-full md:w-auto">
          {/* ULP Filter Dropdown */}
          <div className="relative min-w-[220px]">
            <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 pointer-events-none" size={18} />
            <select
              value={selectedUlp || ''}
              onChange={(e) => setSelectedUlp(e.target.value ? Number(e.target.value) : undefined)}
              className="w-full pl-10 pr-8 py-2.5 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm appearance-none cursor-pointer hover:bg-gray-50 transition-colors"
              style={{ backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")`, backgroundPosition: `right 0.5rem center`, backgroundRepeat: `no-repeat`, backgroundSize: `1.5em 1.5em` }}
            >
              <option value="">Semua UP3 (Total)</option>
              <option disabled>──────────</option>
              {ulps.map(ulp => (
                <option key={ulp.unitup} value={ulp.unitup}>{ulp.name}</option>
              ))}
            </select>
          </div>

          {/* Simple Search */}
          <div className="relative w-full md:w-72">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input
              type="text"
              value={searchId}
              onChange={(e) => setSearchId(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Cari ID Pelanggan..."
              className="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-all"
            />
          </div>
        </div>
      </div>

      {/* Row 1: Global Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Total Pelanggan"
          value2025={stats?.total_customers_2025 || 0}
          value2024={stats?.total_customers_2024 || 0}
          unit=""
          icon={<Users size={24} className="text-blue-600" />}
          color="bg-blue-50"
        />
        <StatCard
          label="Total Konsumsi Energi"
          value2025={stats?.total_consumption_2025 || 0}
          value2024={stats?.total_consumption_2024 || 0}
          unit="kWh"
          formatCompact={true}
          icon={<Zap size={24} className="text-amber-500" />}
          color="bg-amber-50"
        />
        <div
          onClick={() => setActiveTab('new')}
          className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 cursor-pointer hover:bg-gray-50/50 hover:shadow-md transition-all flex items-center justify-between group"
        >
          <div>
            <p className="text-xs text-slate-500 font-medium mb-1 uppercase tracking-wide">Pelanggan Baru</p>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">{stats?.new_customers?.toLocaleString()}</h3>
            <p className="text-xs text-purple-600 font-medium flex items-center gap-1">Data Tahun 2025</p>
          </div>
          <div className={`w-12 h-12 rounded-xl bg-purple-50 flex items-center justify-center shrink-0 group-hover:bg-purple-100 transition-colors`}>
            <Users size={24} className="text-purple-600" />
          </div>
        </div>
        <div
          onClick={() => setActiveTab('lost')}
          className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 cursor-pointer hover:bg-gray-50/50 hover:shadow-md transition-all flex items-center justify-between group"
        >
          <div>
            <p className="text-xs text-slate-500 font-medium mb-1 uppercase tracking-wide">Churn (Hilang)</p>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">{stats?.lost_customers?.toLocaleString()}</h3>
            <p className="text-xs text-red-600 font-medium flex items-center gap-1">Data Tahun 2025</p>
          </div>
          <div className={`w-12 h-12 rounded-xl bg-red-50 flex items-center justify-center shrink-0 group-hover:bg-red-100 transition-colors`}>
            <AlertCircle size={24} className="text-red-600" />
          </div>
        </div>
      </div>

      {/* Row 2: Monthly Trends */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="font-bold text-lg text-gray-800">Tren Pemakaian Energi Bulanan</h3>
            <p className="text-xs text-gray-400">Total kWh per Bulan (2024 vs 2025)</p>
          </div>
          <div className="flex gap-4 text-xs font-medium">
            <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-gray-400"></span> 2024</div>
            <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-500"></span> 2025</div>
          </div>
        </div>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trends} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
              <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} dy={10} />
              <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} tickFormatter={(val) => `${(val / 1e6).toFixed(0)} GWh`} />
              <Tooltip
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                formatter={(val: number) => [`${(val / 1e6).toFixed(2)} GWh`, '']}
              />
              <Line type="monotone" dataKey="value_2024" stroke="#9ca3af" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="value_2025" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4, fill: '#3b82f6', strokeWidth: 0 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>



      {/* Row 3: Comparative Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div onClick={() => navigate('/analysis/comparison')} className="cursor-pointer hover:scale-[1.01] transition-transform">
          <ComparisonChart title="Analisis Tarif" subTitle="Total GWh per Golongan" data={comparisonData?.tarif || []} height={400} />
        </div>
        <div onClick={() => navigate('/analysis/comparison')} className="cursor-pointer hover:scale-[1.01] transition-transform">
          <ComparisonChart title="Analisis Jenis" subTitle="Total GWh per Jenis Pelanggan" data={comparisonData?.jenis || []} height={400} />
        </div>
        <div onClick={() => navigate('/analysis/comparison')} className="cursor-pointer hover:scale-[1.01] transition-transform">
          <ComparisonChart title="Analisis Layanan" subTitle="Total GWh Pascabayar vs Prabayar" data={comparisonData?.layanan || []} height={400} />
        </div>
      </div>

      {/* Row 4: Infrastructure & Pareto */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Gardu Chart (60%) */}
        <div className="lg:col-span-3 cursor-pointer hover:scale-[1.01] transition-transform" onClick={() => navigate('/analysis/infrastructure')}>
          <GarduChart data={garduData} />
        </div>

        {/* Pareto Chart (40%) */}
        <div className="lg:col-span-2 cursor-pointer hover:scale-[1.01] transition-transform" onClick={() => navigate('/analysis/pareto')}>
          <ParetoChart data={paretoData} />
        </div>
      </div>

      {/* Row 5: Power Analysis & Segmentasi */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12" onClick={() => navigate('/analysis/power')}>
        <div className="cursor-pointer hover:scale-[1.01] transition-transform h-[700px]">
          <DayaCompositionChart data={chartDayaData} />
        </div>
        <div className="cursor-pointer hover:scale-[1.01] transition-transform h-[700px]">
          <PowerChangeCard data={powerData} compact={true} />
        </div>
      </div>

      {/* Row 6: Anomaly Detection */}
      <div>
        <AnomalyTable
          zeroUsageData={anomalyData}
          zeroPage={anomalyPage}
          zeroTotalPages={anomalyTotalPages}
          zeroTotalItems={anomalyTotalItems}
          onZeroPageChange={fetchAnomalies}
          zeroLoading={anomalyLoading}

          varianceData={varianceData}
          variancePage={variancePage}
          varianceTotalPages={varianceTotalPages}
          varianceTotalItems={varianceTotalItems}
          onVariancePageChange={fetchVariance}
          varianceLoading={varianceLoading}
          onFilterChange={handleVarianceFilterChange}
        />
      </div>
    </div>
  );
};

const StatCard = ({ label, value2025, value2024, unit = '', icon, color, formatCompact = false }: any) => {
  const diff = value2025 - value2024;
  const percent = value2024 > 0 ? (diff / value2024) * 100 : 0;
  const isUp = diff >= 0;

  const formatValue = (val: number) => {
    if (formatCompact) {
      if (val > 1e9) return `${(val / 1e9).toFixed(2)} GWh`;
      if (val > 1e6) return `${(val / 1e6).toFixed(2)} MWh`;
      return `${val.toLocaleString()} ${unit}`;
    }
    return `${val.toLocaleString()} ${unit}`;
  };

  return (
    <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between h-full transition-all hover:bg-gray-50/50">
      <div className="flex justify-between items-start mb-2">
        <div>
          <p className="text-xs text-slate-500 font-medium mb-1 uppercase tracking-wide">{label}</p>
          <h3 className="text-2xl font-bold text-slate-800">{formatValue(value2025)}</h3>
        </div>
        <div className={`w-10 h-10 rounded-xl ${color} flex items-center justify-center shrink-0`}>
          {icon}
        </div>
      </div>

      <div className="mt-2 pt-3 border-t border-gray-50 flex items-center justify-between">
        <div className="flex flex-col">
          <span className="text-[10px] text-gray-400 font-medium">TAHUN 2024</span>
          <span className="text-xs font-semibold text-gray-600">{formatValue(value2024)}</span>
        </div>

        <div className={`flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-bold ${isUp ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`}>
          {isUp ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
          <span>{Math.abs(percent).toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
