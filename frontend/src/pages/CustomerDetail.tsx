import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import {
  getCustomerDetail,
  getCustomerTrends,
  MonthlyData
} from '../services/api';

function CustomerDetail() {
  const { idpel } = useParams<{ idpel: string }>();
  const navigate = useNavigate();
  const [customerData, setCustomerData] = useState<any | null>(null);
  const [trends, setTrends] = useState<MonthlyData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!idpel) return;

      setLoading(true);
      setError(null);

      try {
        const [detailData, trendsData] = await Promise.all([
          getCustomerDetail(idpel),
          getCustomerTrends(idpel)
        ]);

        setCustomerData(detailData);
        setTrends(trendsData);
      } catch (e: any) {
        const msg = e?.message || '';
        if (msg === 'Network Error' || e?.code === 'ERR_NETWORK' || !e?.response) {
          setError('Backend tidak terjangkau. Pastikan server API (port 8000) sudah jalan.');
        } else {
          setError(e?.response?.data?.detail || msg || 'Gagal memuat data pelanggan');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [idpel]);

  const calculateTotal = (year: '2024' | '2025') => {
    if (!customerData?.[year]) return 0;
    const data = customerData[year];
    const months_2024 = ['dec_2023', 'jan_2024', 'feb_2024', 'mar_2024', 'apr_2024', 'may_2024',
      'jun_2024', 'jul_2024', 'aug_2024', 'sep_2024', 'oct_2024', 'nov_2024', 'dec_2024'];
    const months_2025 = ['dec_2024', 'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
      'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025'];

    const months = year === '2024' ? months_2024 : months_2025;
    return months.reduce((sum, month) => {
      const val = data[month];
      return sum + (val ? parseFloat(val) : 0);
    }, 0);
  };

  const total2024 = calculateTotal('2024');
  const total2025 = calculateTotal('2025');
  const difference = total2025 - total2024;
  const percentageChange = total2024 > 0 ? ((difference / total2024) * 100) : 0;

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#F8F9FE]">
        <div className="flex flex-col items-center gap-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="text-gray-500 font-medium">Memuat Data Pelanggan...</p>
        </div>
      </div>
    );
  }

  if (error || !customerData) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#F8F9FE]">
        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 max-w-md">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Error</h2>
          <p className="text-gray-600 mb-6">{error || 'Pelanggan tidak ditemukan'}</p>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-[#10529d] text-white rounded-lg hover:bg-blue-800 transition-colors"
          >
            Kembali ke Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <button
          type="button"
          onClick={() => navigate(-1)}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft size={20} className="text-gray-600" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-[#1a1a1a]">Detail Pelanggan</h1>
          <p className="text-gray-500 text-sm mt-1">IDPEL: {idpel}</p>
        </div>
      </div>

      {/* Customer Info Cards */}
      <div className="grid grid-cols-2 gap-6 mb-6">
        {/* 2024 Data */}
        {customerData['2024'] && (
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex items-center gap-2 mb-4">
              <span className="w-2 h-6 bg-gray-400 rounded-full"></span>
              <h3 className="font-bold text-gray-600">Data Tahun 2024</h3>
            </div>
            <div className="space-y-3">
              <InfoRow label="Nama" value={customerData['2024'].nama || '-'} />
              <InfoRow label="Alamat" value={customerData['2024'].alamat || '-'} />
              <InfoRow label="Tarif" value={customerData['2024'].tarif || '-'} />
              <InfoRow label="Daya" value={customerData['2024'].daya ? `${customerData['2024'].daya} VA` : '-'} />
              <InfoRow label="Jenis" value={customerData['2024'].jenis || '-'} />
              <InfoRow label="Layanan" value={customerData['2024'].layanan || '-'} />
              <InfoRow label="Gardu" value={customerData['2024'].gardu || '-'} />
              <div className="pt-3 border-t border-gray-100">
                <InfoRow
                  label="Total Pemakaian"
                  value={`${total2024.toLocaleString('id-ID')} kWh`}
                />
              </div>
            </div>
          </div>
        )}

        {/* 2025 Data */}
        {customerData['2025'] && (
          <div className="bg-white p-6 rounded-xl shadow-sm border border-blue-100 bg-blue-50/30">
            <div className="flex items-center gap-2 mb-4">
              <span className="w-2 h-6 bg-[#10529d] rounded-full"></span>
              <h3 className="font-bold text-[#10529d]">Data Tahun 2025</h3>
            </div>
            <div className="space-y-3">
              <InfoRow label="Nama" value={customerData['2025'].nama || '-'} />
              <InfoRow label="Alamat" value={customerData['2025'].alamat || '-'} />
              <InfoRow label="Tarif" value={customerData['2025'].tarif || '-'} />
              <InfoRow label="Daya" value={customerData['2025'].daya ? `${customerData['2025'].daya} VA` : '-'} />
              <InfoRow label="Jenis" value={customerData['2025'].jenis || '-'} />
              <InfoRow label="Layanan" value={customerData['2025'].layanan || '-'} />
              <InfoRow label="Gardu" value={customerData['2025'].gardu || '-'} />
              <div className="pt-3 border-t border-blue-100">
                <InfoRow
                  label="Total Pemakaian"
                  value={`${total2025.toLocaleString('id-ID')} kWh`}
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Statistics Summary */}
      {customerData['2024'] && customerData['2025'] && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-6">
          <h3 className="font-bold text-lg text-gray-800 mb-4">Ringkasan Perbandingan</h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500 mb-1">2024</p>
              <p className="text-xl font-bold text-gray-800">
                {total2024.toLocaleString('id-ID')} kWh
              </p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500 mb-1">2025</p>
              <p className="text-xl font-bold text-gray-800">
                {total2025.toLocaleString('id-ID')} kWh
              </p>
            </div>
            <div className={`text-center p-4 rounded-lg ${difference >= 0 ? 'bg-green-50' : 'bg-red-50'}`}>
              <p className="text-sm text-gray-500 mb-1">Perubahan</p>
              <p className={`text-xl font-bold ${difference >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {difference >= 0 ? '+' : ''}{difference.toLocaleString('id-ID')} kWh
              </p>
              <p className={`text-sm mt-1 ${difference >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {percentageChange >= 0 ? '+' : ''}{percentageChange.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Monthly Trends Chart */}
      {trends.length > 0 && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-6">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h3 className="font-bold text-lg text-gray-800">Grafik Pemakaian Bulanan</h3>
              <p className="text-sm text-gray-500">Perbandingan Pemakaian 2024 vs 2025</p>
            </div>
            <div className="flex gap-4 text-sm">
              <div className="flex items-center gap-2">
                <span className="w-3 h-1 bg-[#10529d] rounded-full"></span>
                <span>2025</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-1 bg-gray-300 border-t border-dashed border-gray-400"></span>
                <span className="text-gray-500">2024</span>
              </div>
            </div>
          </div>

          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trends} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: '#9ca3af', fontSize: 12 }} dy={10} />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#9ca3af', fontSize: 12 }}
                  tickFormatter={(val) => {
                    if (val >= 1000) return `${(val / 1000).toFixed(1)}k kWh`;
                    return `${val} kWh`;
                  }}
                />
                <Tooltip
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  formatter={(val: number) => `${val.toLocaleString('id-ID')} kWh`}
                />
                <Line
                  type="monotone"
                  dataKey="value_2024"
                  stroke="#94a3b8"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  activeDot={{ r: 6 }}
                  name="2024"
                />
                <Line
                  type="monotone"
                  dataKey="value_2025"
                  stroke="#10529d"
                  strokeWidth={3}
                  dot={false}
                  activeDot={{ r: 8, strokeWidth: 4, stroke: '#e0f2fe' }}
                  name="2025"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      <footer className="mt-12 text-center text-xs text-gray-400">
        © 2025 PT PLN (Persero). All rights reserved. Enterprise Dashboard System v3.2
      </footer>
    </div>
  );
}

const InfoRow = ({ label, value }: { label: string, value: string | number }) => (
  <div className="flex flex-col">
    <span className="text-xs text-gray-500 uppercase tracking-wider mb-1">{label}</span>
    <span className="font-semibold text-gray-900">{value}</span>
  </div>
);

export default CustomerDetail;

