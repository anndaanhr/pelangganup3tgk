import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertTriangle, Loader2 } from 'lucide-react';
import Pagination from '../common/Pagination';

interface AnomalyTableProps {
    zeroUsageData: any[];
    zeroPage: number;
    zeroTotalPages: number;
    zeroTotalItems: number;
    onZeroPageChange: (page: number) => void;
    zeroLoading: boolean;

    varianceData: any[];
    variancePage: number;
    varianceTotalPages: number;
    varianceTotalItems: number;
    onVariancePageChange: (page: number) => void;
    varianceLoading: boolean;
    onFilterChange: (range: { min?: number, max?: number } | null) => void;
}

const AnomalyTable: React.FC<AnomalyTableProps> = ({
    zeroUsageData, zeroPage, zeroTotalPages, zeroTotalItems, onZeroPageChange, zeroLoading,
    varianceData, variancePage, varianceTotalPages, varianceTotalItems, onVariancePageChange, varianceLoading,
    onFilterChange
}) => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = React.useState<'zero' | 'variance'>('zero');
    const [selectedFilter, setSelectedFilter] = React.useState<string>('all');

    const data = activeTab === 'zero' ? zeroUsageData : varianceData;
    const page = activeTab === 'zero' ? zeroPage : variancePage;
    const totalItems = activeTab === 'zero' ? zeroTotalItems : varianceTotalItems;
    const onPageChange = activeTab === 'zero' ? onZeroPageChange : onVariancePageChange;
    const loading = activeTab === 'zero' ? zeroLoading : varianceLoading;

    // Safety check: ensure data is an array
    const safeData = Array.isArray(data) ? data : [];
    const isEmpty = safeData.length === 0;

    const handleFilterSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const val = e.target.value;
        setSelectedFilter(val);

        let range: { min?: number, max?: number } | null = null;
        switch (val) {
            case 'drop_total': range = { max: -100 }; break;
            case 'drop_extreme': range = { max: -80 }; break;
            case 'drop_significant': range = { max: -50, min: -80 }; break;
            case 'spike_significant': range = { min: 50, max: 100 }; break;
            case 'spike_extreme': range = { min: 100 }; break;
            default: range = null;
        }
        onFilterChange(range);
    };

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${activeTab === 'zero' ? 'bg-red-100 text-red-600' : 'bg-orange-100 text-orange-600'}`}>
                        <AlertTriangle size={20} />
                    </div>
                    <div>
                        <h3 className="text-lg font-bold text-gray-800">Indikasi Anomali</h3>
                        <p className="text-sm text-gray-500">
                            {activeTab === 'zero' ? 'Pelanggan dengan pemakaian 0 kWh (3 bulan terakhir).' : 'Deteksi lonjakan atau penurunan drastis (>100% atau Drop ke 0).'}
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    {/* Range Filter Dropdown (Only visible on Variance tab) */}
                    {activeTab === 'variance' && (
                        <select
                            value={selectedFilter}
                            onChange={handleFilterSelect}
                            className="px-3 py-1.5 text-xs font-medium border border-gray-200 rounded-md bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
                        >
                            <option value="all">Semua Fluktuasi</option>
                            <option value="drop_total">📉 Drop Total (-100%)</option>
                            <option value="drop_extreme">📉 Drop Ekstrem (≤ -80%)</option>
                            <option value="drop_significant">📉 Drop Signifikan (-80% s/d -50%)</option>
                            <option value="spike_significant">📈 Kenaikan Tinggi (+50% s/d +100%)</option>
                            <option value="spike_extreme">📈 Lonjakan Ekstrem (&gt; +100%)</option>
                        </select>
                    )}

                    <div className="flex bg-gray-100 p-1 rounded-lg">
                        <button
                            onClick={() => setActiveTab('zero')}
                            className={`px-3 py-1.5 text-xs font-bold rounded-md transition-all ${activeTab === 'zero' ? 'bg-white shadow text-gray-800' : 'text-gray-500 hover:text-gray-800'}`}
                        >
                            Zero Usage
                        </button>
                        <button
                            onClick={() => setActiveTab('variance')}
                            className={`px-3 py-1.5 text-xs font-bold rounded-md transition-all ${activeTab === 'variance' ? 'bg-white shadow text-gray-800' : 'text-gray-500 hover:text-gray-800'}`}
                        >
                            Fluktuasi Ekstrem
                        </button>
                    </div>
                </div>
            </div>

            <div className="min-h-[300px] flex flex-col justify-between">
                {loading ? (
                    <div className="flex flex-col items-center justify-center h-48 text-gray-400">
                        <Loader2 className="animate-spin mb-2" size={32} />
                        <p>Memuat Data...</p>
                    </div>
                ) : isEmpty ? (
                    <div className="text-center p-8 text-gray-400 italic">Tidak ada anomali terdeteksi untuk kategori ini.</div>
                ) : (
                    <>
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm text-left">
                                <thead className="bg-gray-50 text-gray-600 font-semibold border-b border-gray-200">
                                    <tr>
                                        <th className="px-4 py-3">ID Pelanggan</th>
                                        <th className="px-4 py-3">Nama</th>
                                        <th className="px-4 py-3">Alamat</th>
                                        <th className="px-4 py-3">Info Deteksi</th>
                                        <th className="px-4 py-3">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-100">
                                    {safeData.map((row, idx) => (
                                        <tr
                                            key={`${row.idpel}-${idx}`}
                                            onClick={() => navigate(`/pelanggan/${row.idpel}`)}
                                            className="hover:bg-blue-50/50 transition-colors cursor-pointer group"
                                        >
                                            <td className="px-4 py-3 font-mono text-gray-700 group-hover:text-blue-600 transition-colors">{row.idpel}</td>
                                            <td className="px-4 py-3 font-medium text-gray-900 group-hover:text-blue-700 transition-colors">{row.nama}</td>
                                            <td className="px-4 py-3 text-gray-500 truncate max-w-xs">{row.alamat}</td>
                                            <td className={`px-4 py-3 font-medium ${activeTab === 'zero' ? 'text-red-500' : 'text-orange-500'}`}>
                                                {row.info}
                                            </td>
                                            <td className="px-4 py-3">
                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${activeTab === 'zero' ? 'bg-red-100 text-red-800' : 'bg-orange-100 text-orange-800'}`}>
                                                    Periksa
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        {/* Pagination Controls */}
                        <div className="mt-4 pt-4 border-t border-gray-100">
                            <Pagination
                                currentPage={page}
                                totalItems={totalItems}
                                itemsPerPage={10}
                                onPageChange={onPageChange}
                                showInput={false}
                                compact={false}
                            />
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default AnomalyTable;
