import React, { useEffect, useState } from 'react';
import { ArrowLeft, Zap, AlertCircle, BarChart2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getGarduStats } from '../../services/analyticsApi';
import GarduChart from '../../components/analytics/GarduChart';
import Pagination from '../../components/common/Pagination';

const InfrastructurePage: React.FC = () => {
    const navigate = useNavigate();
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    useEffect(() => {
        const fetch = async () => {
            try {
                // Fetch top 50 for chart, but maybe table can use same data for now
                // In real app, we might want pagination, but client agreed on top 500 limit for now
                const res = await getGarduStats(100);
                setData(res);
            } catch (error) {
                console.error("Failed to load infrastructure data", error);
            } finally {
                setLoading(false);
            }
        };
        fetch();
    }, []);

    const totalEnergy = data.reduce((acc, curr) => acc + (curr.total_kwh || 0), 0);
    const maxLoadGardu = data.length > 0 ? data[0] : null;
    
    const displayedData = data.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

    return (
        <div className="space-y-6 pb-12 animate-fade-in-up">
            {/* Header */}
            <div className="flex items-center gap-4 mb-6">
                <button
                    onClick={() => navigate('/')}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors text-gray-600"
                >
                    <ArrowLeft size={24} />
                </button>
                <div>
                    <h1 className="text-2xl font-bold text-gray-800">Analisis Beban Infrastruktur</h1>
                    <p className="text-gray-500 text-sm">Detail beban gardu distribusi dan tren pemakaian energi.</p>
                </div>
            </div>

            {/* Key Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center justify-between">
                    <div>
                        <p className="text-xs text-gray-500 uppercase font-semibold mb-1">Total Energi (Top 100)</p>
                        <h3 className="text-2xl font-bold text-blue-600">{(totalEnergy / 1e6).toFixed(1)} GWh</h3>
                    </div>
                    <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center text-blue-500">
                        <Zap size={24} />
                    </div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center justify-between">
                    <div>
                        <p className="text-xs text-gray-500 uppercase font-semibold mb-1">Gardu Terpadat</p>
                        <h3 className="text-lg font-bold text-gray-800">{maxLoadGardu?.gardu || '-'}</h3>
                        <p className="text-xs text-gray-400">{(maxLoadGardu?.total_kwh / 1000).toFixed(0)} MWh</p>
                    </div>
                    <div className="w-12 h-12 bg-amber-50 rounded-xl flex items-center justify-center text-amber-500">
                        <AlertCircle size={24} />
                    </div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center justify-between">
                    <div>
                        <p className="text-xs text-gray-500 uppercase font-semibold mb-1">Total Gardu Dipantau</p>
                        <h3 className="text-2xl font-bold text-emerald-600">{data.length}</h3>
                    </div>
                    <div className="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-500">
                        <BarChart2 size={24} />
                    </div>
                </div>
            </div>

            {/* Main Chart */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="font-bold text-lg text-gray-800">Visualisasi Beban (Top 20)</h3>
                    <div className="px-3 py-1 bg-gray-50 text-xs text-gray-500 rounded-lg">
                        Diurutkan berdasarkan total konsumsi 2025
                    </div>
                </div>
                {/* Scrollable container for the chart if 50 items are too squeezed */}
                {/* Chart container */}
                <div className="w-full">
                    <GarduChart data={data} height={800} />
                </div>
            </div>

            {/* Detailed Table */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                <div className="p-6 border-b border-gray-100">
                    <h3 className="font-bold text-lg text-gray-800">Data Detail Gardu</h3>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-gray-50 text-gray-500 font-semibold border-b border-gray-200">
                            <tr>
                                <th className="px-6 py-4 w-16">#</th>
                                <th className="px-6 py-4">Kode Gardu</th>
                                <th className="px-6 py-4 text-right">Beban 2024 (kWh)</th>
                                <th className="px-6 py-4 text-right">Beban 2025 (kWh)</th>
                                <th className="px-6 py-4 text-center">Pertumbuhan</th>
                                <th className="px-6 py-4 text-center">Kontribusi</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {displayedData.map((item, idx) => {
                                const growth = item.total_kwh - item.total_kwh_2024;
                                const percent = item.total_kwh_2024 > 0 ? (growth / item.total_kwh_2024) * 100 : 100;
                                const contribution = (item.total_kwh / totalEnergy) * 100;

                                return (
                                    <tr key={idx} className="hover:bg-gray-50/50 transition-colors group">
                                        <td className="px-6 py-4 text-gray-400 font-medium">{(currentPage - 1) * itemsPerPage + idx + 1}</td>
                                        <td className="px-6 py-4 font-semibold text-blue-600">{item.gardu}</td>
                                        <td className="px-6 py-4 text-right text-gray-500">{item.total_kwh_2024.toLocaleString('id-ID')}</td>
                                        <td className="px-6 py-4 text-right font-bold text-gray-800">{item.total_kwh.toLocaleString('id-ID')}</td>
                                        <td className="px-6 py-4 flex justify-center">
                                            <span className={`px-2 py-1 rounded text-xs font-bold ${percent >= 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`}>
                                                {percent > 0 ? '+' : ''}{percent.toFixed(1)}%
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                                                    <div
                                                        className="h-full bg-blue-500 rounded-full"
                                                        style={{ width: `${contribution * 5}%` }} // Scaling for visibility
                                                    ></div>
                                                </div>
                                                {/* <span className="text-xs text-gray-400 w-10 text-right">{contribution.toFixed(1)}%</span> */}
                                            </div>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                    <div className="px-6 pb-6">
                        <Pagination
                            currentPage={currentPage}
                            totalItems={data.length}
                            itemsPerPage={itemsPerPage}
                            onPageChange={setCurrentPage}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default InfrastructurePage;
