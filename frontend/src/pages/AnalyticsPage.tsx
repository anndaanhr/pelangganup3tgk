import React, { useState, useEffect } from 'react';
import { BarChart2, AlertOctagon, Zap, RefreshCw } from 'lucide-react';
import ParetoChart from '../components/analytics/ParetoChart';
import AnomalyTable from '../components/analytics/AnomalyTable';
import GarduChart from '../components/analytics/GarduChart';
import PowerChangeCard from '../components/analytics/PowerChangeCard';
import { getParetoAnalysis, getZeroUsageAnomalies, getGarduStats, getPowerChanges } from '../services/analyticsApi';

const AnalyticsPage = () => {
    const [activeTab, setActiveTab] = useState('pareto');
    const [loading, setLoading] = useState(false);

    // Data States
    const [paretoData, setParetoData] = useState([]);
    const [anomalyData, setAnomalyData] = useState([]);
    const [garduData, setGarduData] = useState([]);
    const [powerData, setPowerData] = useState(null);

    useEffect(() => {
        fetchTabContent();
    }, [activeTab]);

    const fetchTabContent = async () => {
        setLoading(true);
        try {
            if (activeTab === 'pareto' && paretoData.length === 0) {
                const data = await getParetoAnalysis();
                setParetoData(data);
            } else if (activeTab === 'anomaly' && anomalyData.length === 0) {
                const data = await getZeroUsageAnomalies();
                setAnomalyData(data);
            } else if (activeTab === 'infra' && garduData.length === 0) {
                const data = await getGarduStats();
                setGarduData(data);
            } else if (activeTab === 'lifecycle' && !powerData) {
                const data = await getPowerChanges();
                setPowerData(data);
            }
        } catch (err) {
            console.error("Failed to load analytics", err);
        } finally {
            setLoading(false);
        }
    };

    const tabs = [
        { id: 'pareto', label: 'Analisis Pareto', icon: BarChart2 },
        { id: 'anomaly', label: 'Deteksi Anomali', icon: AlertOctagon },
        { id: 'infra', label: 'Beban Infrastruktur', icon: Zap },
        { id: 'lifecycle', label: 'Mutasi Daya', icon: RefreshCw },
    ];

    return (
        <div>
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-gray-800">Analisis Lanjutan</h1>
                <p className="text-sm text-gray-500 mt-1">Laporan analitik mendalam untuk pengambilan keputusan strategis.</p>
            </div>

            {/* Tabs */}
            <div className="flex overflow-x-auto gap-2 mb-6 pb-2">
                {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${activeTab === tab.id
                                ? 'bg-blue-600 text-white shadow-md shadow-blue-200'
                                : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-100'
                                }`}
                        >
                            <Icon size={18} />
                            {tab.label}
                        </button>
                    );
                })}
            </div>

            {/* Content Area */}
            {loading ? (
                <div className="h-64 flex items-center justify-center bg-white rounded-xl border border-gray-100">
                    <p className="text-gray-400 animate-pulse">Memuat data analitik...</p>
                </div>
            ) : (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                    {activeTab === 'pareto' && <ParetoChart data={paretoData} />}
                    {activeTab === 'anomaly' && <AnomalyTable zeroUsageData={anomalyData} />}
                    {activeTab === 'infra' && <GarduChart data={garduData} />}
                    {activeTab === 'lifecycle' && <PowerChangeCard data={powerData} />}
                </div>
            )}
        </div>
    );
};

export default AnalyticsPage;
