import React, { useEffect, useState } from 'react';
import { ArrowLeft, User, TrendingUp, AlertTriangle, Users } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getParetoAnalysis } from '../../services/analyticsApi';
import ParetoChart from '../../components/analytics/ParetoChart';
import Pagination from '../../components/common/Pagination';

const ParetoPage: React.FC = () => {
    const navigate = useNavigate();
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    useEffect(() => {
        const fetch = async () => {
            try {
                // Fetch top 100 for display
                const res = await getParetoAnalysis(100);
                setData(res);
            } catch (error) {
                console.error("Failed to load pareto data", error);
            } finally {
                setLoading(false);
            }
        };
        fetch();
    }, []);

    const topCustomer = data.length > 0 ? data[0] : null;

    return (
        <div className="space-y-6 pb-12 animate-fade-in-up">
            <div className="flex items-center gap-4 mb-6">
                <button
                    onClick={() => navigate('/')}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors text-gray-600"
                >
                    <ArrowLeft size={24} />
                </button>
                <div>
                    <h1 className="text-2xl font-bold text-gray-800">Pelanggan Terbesar</h1>
                    <p className="text-gray-500 text-sm">Identifikasi pelanggan dengan konsumsi tertinggi yang mempengaruhi beban sistem.</p>
                </div>
            </div>



            {/* Chart */}
            <div className="mb-8">
                <ParetoChart data={data.slice(0, 20)} />
            </div>

            {/* Table */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                <div className="p-6 border-b border-gray-100">
                    <h3 className="font-bold text-lg text-gray-800">Daftar Pelanggan High-Value</h3>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-gray-50 text-gray-500 font-semibold border-b border-gray-200">
                            <tr>
                                <th className="px-6 py-4 w-16">Rank</th>
                                <th className="px-6 py-4">ID Pelanggan</th>
                                <th className="px-6 py-4">Nama</th>
                                <th className="px-6 py-4">Tarif/Daya</th>
                                <th className="px-6 py-4">Gardu</th>
                                <th className="px-6 py-4 text-right">Konsumsi (kWh)</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {data.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage).map((item, idx) => (
                                <tr
                                    key={item.idpel}
                                    onClick={() => navigate(`/pelanggan/${item.idpel}`)}
                                    className="hover:bg-blue-50 transition-colors cursor-pointer group"
                                >
                                    <td className="px-6 py-4 font-bold text-gray-400">#{(currentPage - 1) * itemsPerPage + idx + 1}</td>
                                    <td className="px-6 py-4 font-medium text-gray-900 group-hover:text-blue-600 transition-colors">{item.idpel}</td>
                                    <td className="px-6 py-4 text-gray-600">{item.nama}</td>
                                    <td className="px-6 py-4 text-gray-500">
                                        <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">
                                            {item.tarif}
                                        </span>
                                        <span className="ml-2 text-xs">{item.daya?.toLocaleString()} VA</span>
                                    </td>
                                    <td className="px-6 py-4 text-blue-600 font-medium">{item.gardu}</td>
                                    <td className="px-6 py-4 text-right font-bold text-emerald-600">
                                        {item.total_kwh.toLocaleString('id-ID')}
                                    </td>
                                </tr>
                            ))}
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

export default ParetoPage;
