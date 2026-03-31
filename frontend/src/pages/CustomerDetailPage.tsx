import React from 'react';
import { User, Zap, ChevronLeft } from 'lucide-react';

interface CustomerDetailPageProps {
  data: any;
  onBack: () => void;
  searchId?: string;
}

const CustomerDetailPage: React.FC<CustomerDetailPageProps> = ({ data, onBack, searchId }) => {
  const c2025 = data?.['2025'];
  const c2024 = data?.['2024'];
  const activeData = c2025 || c2024; // Prefer 2025, fallback to 2024
  
  // Fallback if data is null but we have searchId (shouldn't happen ideally if data fetched before nav)
  const displayId = activeData?.idpel || searchId || '-';

  return (
    <div className="animate-in fade-in duration-300">
      <div className="flex items-center gap-4 mb-8">
        <button 
            onClick={onBack}
            className="p-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 text-gray-600 transition-colors shadow-sm"
        >
            <ChevronLeft size={20} />
        </button>
        <div>
            <h1 className="text-2xl font-bold text-gray-800">Detail Pelanggan</h1>
            <p className="text-gray-500 text-sm">Informasi lengkap data pelanggan</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
            {/* Identity Section */}
            <div className="mb-10">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 border border-blue-100">
                        <User size={16} />
                    </div>
                    <h3 className="font-bold text-gray-800">Informasi Identitas Pelanggan</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <div>
                        <p className="text-xs text-gray-400 mb-1 font-medium uppercase tracking-wide">ID Pelanggan</p>
                        <p className="font-bold text-gray-900 text-lg font-mono">{displayId}</p>
                    </div>
                    <div className="lg:col-span-2">
                        <p className="text-xs text-gray-400 mb-1 font-medium uppercase tracking-wide">Alamat</p>
                        <p className="font-bold text-gray-900">{activeData?.alamat || '-'}</p>
                    </div>
                     <div>
                        <p className="text-xs text-gray-400 mb-1 font-medium uppercase tracking-wide">Nama</p>
                        <p className="font-bold text-gray-900">{activeData?.nama || '-'}</p>
                    </div>
                </div>
            </div>

            <div className="border-t border-gray-100 my-8"></div>

            {/* Connection Section */}
            <div>
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-8 rounded-full bg-yellow-50 flex items-center justify-center text-yellow-600 border border-yellow-100">
                        <Zap size={16} />
                    </div>
                    <h3 className="font-bold text-gray-800">Detail Koneksi Listrik</h3>
                </div>
                
                 <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <DetailItem label="No. Meter" value={activeData?.nomor_meter || '-'} />
                    <DetailItem label="Jenis" value={activeData?.jenis || '-'} />
                    <DetailItem label="Merk KWH" value={activeData?.merk_kwh || 'ITRON'} />
                    <DetailItem label="Tarif Listrik" value={activeData?.tarif || '-'} />
                    <DetailItem label="Daya Tersambung" value={`${activeData?.daya || 0} VA`} />
                    <DetailItem label="KDDK" value={activeData?.kddk || '-'} />
                    <DetailItem label="Layanan" value={activeData?.layanan || '-'} />
                    <DetailItem label="CATER" value={activeData?.cater || '-'} />
                    <DetailItem label="Wilayah ULP" value={activeData?.unitup ? `ULP ${activeData?.unitup}` : 'Karang'} />
                    <DetailItem label="KD Prosess" value={activeData?.kd_proses || '-'} />
                    <DetailItem label="Gardu" value={activeData?.gardu || '-'} />
                </div>
            </div>
      </div>
    </div>
  );
};

const DetailItem = ({ label, value }: { label: string, value: string }) => (
    <div>
        <p className="text-xs text-gray-400 mb-1 font-medium uppercase tracking-wide">{label}</p>
        <p className="font-bold text-gray-900">{value}</p>
    </div>
);

export default CustomerDetailPage;
