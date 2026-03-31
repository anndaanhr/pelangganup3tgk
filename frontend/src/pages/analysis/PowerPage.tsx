import React, { useEffect, useState } from 'react';
import { ArrowLeft, Activity, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getDayaDistribution, getPowerChanges } from '../../services/analyticsApi';
import DayaCompositionChart, { generateColor } from '../../components/analytics/DayaCompositionChart';
import PowerChangeCard from '../../components/analytics/PowerChangeCard';
import Pagination from '../../components/common/Pagination';

const PowerPage: React.FC = () => {
    const navigate = useNavigate();
    const [year, setYear] = useState<number>(2025);
    const [dayaData, setDayaData] = useState<any[]>([]);
    const [changeData, setChangeData] = useState<any>(null);
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetch = async () => {
            setLoading(true);
            try {
                const [dData, cData] = await Promise.all([
                    getDayaDistribution(year),
                    getPowerChanges() // Power changes might be year-agnostic or always current
                ]);
                setDayaData(dData);
                setChangeData(cData);
            } catch (error) {
                console.error("Failed to load power data", error);
            } finally {
                setLoading(false);
            }
        };
        fetch();
    }, [year]);

    const totalCustomers = dayaData.reduce((acc, curr) => acc + curr.count, 0);
    const totalEnergy = dayaData.reduce((acc, curr) => acc + curr.total_kwh, 0);

    // Prepare sorted data for chart (Top 7 + Others) to avoid UI clutter
    const sortedData = [...dayaData].sort((a, b) => b.count - a.count);
    const top7 = sortedData.slice(0, 7);
    const others = sortedData.slice(7);

    const chartData = others.length > 0 ? [
        ...top7,
        {
            label: 'Lainnya',
            count: others.reduce((sum, item) => sum + item.count, 0),
            total_kwh: others.reduce((sum, item) => sum + item.total_kwh, 0),
            daya: 0 // Dummy value
        }
    ] : sortedData;

    const handleRowClick = (daya: number) => {
        navigate(`/pelanggan/semua?year=${year}&daya=${daya}`);
    };

    if (loading) return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-gray-400">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p>Memuat Analisis Daya...</p>
        </div>
    );

    return (
        <div className="space-y-6 pb-12 animate-fade-in-up">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => navigate('/')}
                        className="p-2 hover:bg-gray-100 rounded-lg transition-colors text-gray-600"
                    >
                        <ArrowLeft size={24} />
                    </button>
                    <div>
                        <h1 className="text-2xl font-bold text-gray-800">Analisis Distribusi Daya</h1>
                        <p className="text-gray-500 text-sm">Segmentasi pelanggan berdasarkan batas daya dan dinamika perubahan daya.</p>
                    </div>
                </div>

                <div className="flex bg-gray-100 p-1 rounded-lg">
                    {[2024, 2025].map((y) => (
                        <button
                            key={y}
                            onClick={() => setYear(y)}
                            className={`px-4 py-2 text-sm font-bold rounded-md transition-all ${year === y
                                ? 'bg-white shadow text-blue-600'
                                : 'text-gray-500 hover:text-gray-800'
                                }`}
                        >
                            {y}
                        </button>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
                {/* Visualizations */}
                <div className="space-y-6 flex flex-col lg:h-full">
                    {/* Explicit height for chart container */}
                    <div className="h-[400px] flex-shrink-0">
                        <DayaCompositionChart key={year} data={chartData} />
                    </div>
                    <div className="flex-1 min-h-0">
                        <PowerChangeCard data={changeData} />
                    </div>
                </div>

                {/* Table Breakdown */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 lg:h-full flex flex-col">
                    <div className="flex items-center justify-between mb-6 flex-shrink-0">
                        <h3 className="font-bold text-lg text-gray-800">Detail Sebaran Daya</h3>
                    </div>
                    <div className="overflow-hidden rounded-xl border border-gray-100 flex-1 relative">
                        <div className="absolute inset-0 overflow-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-gray-50 text-gray-500 font-semibold border-b border-gray-200 sticky top-0 bg-white z-10">
                                    <tr>
                                        <th className="px-4 py-3 bg-gray-50">Golongan Daya</th>
                                        <th className="px-4 py-3 text-right bg-gray-50">Pelanggan</th>
                                        <th className="px-4 py-3 text-right bg-gray-50">Total (kWh)</th>
                                        <th className="px-4 py-3 text-right bg-gray-50">Rata-rata (kWh)</th>
                                        <th className="px-4 py-3 text-right bg-gray-50">Kontribusi</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-100">
                                    {dayaData.map((item, idx) => {
                                        const avg = item.count > 0 ? item.total_kwh / item.count : 0;
                                        const contribution = totalEnergy > 0 ? (item.total_kwh / totalEnergy) * 100 : 0;

                                        return (
                                            <tr
                                                key={idx}
                                                onClick={() => handleRowClick(item.daya)}
                                                className="hover:bg-blue-50 transition-colors cursor-pointer group"
                                            >
                                                <td className="px-4 py-3 font-medium text-gray-800 flex items-center">
                                                    <span className="inline-block w-3 h-3 rounded-full mr-2" style={{ backgroundColor: generateColor(idx) }}></span>
                                                    {item.label}
                                                    <ArrowUpRight size={14} className="ml-2 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                                                </td>
                                                <td className="px-4 py-3 text-right">{item.count.toLocaleString()}</td>
                                                <td className="px-4 py-3 text-right font-bold text-gray-700">{item.total_kwh.toLocaleString('id-ID', { maximumFractionDigits: 0 })}</td>
                                                <td className="px-4 py-3 text-right text-gray-500">{avg.toLocaleString('id-ID', { maximumFractionDigits: 1 })}</td>
                                                <td className="px-4 py-3 text-right">
                                                    <div className="flex items-center justify-end gap-2">
                                                        <span className="text-xs text-gray-500">{contribution.toFixed(1)}%</span>
                                                        <div className="w-10 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                                            <div className="h-full bg-gray-300 rounded-full" style={{ width: `${contribution}%`, backgroundColor: generateColor(idx) }}></div>
                                                        </div>
                                                    </div>
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PowerPage;
