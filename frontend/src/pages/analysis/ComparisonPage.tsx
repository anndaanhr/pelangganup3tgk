import React, { useEffect, useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getComparisonStats } from '../../services/api';
import ComparisonChart from '../../components/analytics/ComparisonChart';

const ComparisonPage: React.FC = () => {
    const navigate = useNavigate();
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetch = async () => {
            try {
                const res = await getComparisonStats();
                setData(res);
            } catch (error) {
                console.error("Failed to load comparison data", error);
            } finally {
                setLoading(false);
            }
        };
        fetch();
    }, []);

    return (
        <div className="space-y-8 pb-12 animate-fade-in-up">
            <div className="flex items-center gap-4 mb-2">
                <button
                    onClick={() => navigate('/')}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors text-gray-600"
                >
                    <ArrowLeft size={24} />
                </button>
                <div>
                    <h1 className="text-2xl font-bold text-gray-800">Analisis Komparatif</h1>
                    <p className="text-gray-500 text-sm">Perbandingan performa 2024 vs 2025 berdasarkan Tarif, Jenis, dan Layanan.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 gap-8">
                <div className="bg-white p-1 rounded-2xl shadow-sm border border-gray-100">
                    <ComparisonChart
                        title="Analisis Golongan Tarif"
                        subTitle="Perbandingan total penggunaan energi antar golongan tarif."
                        data={data?.tarif || []}
                        height={400}
                    />
                </div>

                <div className="bg-white p-1 rounded-2xl shadow-sm border border-gray-100">
                    <ComparisonChart
                        title="Analisis Jenis Pelanggan"
                        subTitle="Perbandingan berdasarkan jenis peruntukan (Swasta, Dinas, dll)."
                        data={data?.jenis || []}
                        height={400}
                    />
                </div>

                <div className="bg-white p-1 rounded-2xl shadow-sm border border-gray-100">
                    <ComparisonChart
                        title="Analisis Layanan"
                        subTitle="Perbandingan Pascabayar vs Prabayar."
                        data={data?.layanan || []}
                        height={400}
                    />
                </div>
            </div>
        </div>
    );
};

export default ComparisonPage;
