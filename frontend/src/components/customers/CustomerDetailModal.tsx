import React from 'react';
import { X, User, Zap, MapPin } from 'lucide-react';

interface CustomerDetailModalProps {
  data: any;
  onClose: () => void;
  searchId: string;
}

const CustomerDetailModal: React.FC<CustomerDetailModalProps> = ({ data, onClose, searchId }) => {
  const c2025 = data['2025'];
  const c2024 = data['2024'];
  const activeData = c2025 || c2024; // Prefer 2025, fallback to 2024

  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-200">
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-5xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="px-8 py-6 border-b border-gray-100 flex justify-between items-center sticky top-0 bg-white/95 backdrop-blur z-10">
            <div>
                <h2 className="text-xl font-bold text-gray-800">Detail Pelanggan</h2>
            </div>
            <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full text-gray-400 transition-colors">
                <X size={24} />
            </button>
        </div>

        <div className="p-8">
            {/* Identity Section */}
            <div className="mb-8">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                        <User size={16} />
                    </div>
                    <h3 className="font-bold text-gray-800">Informasi Identitas Pelanggan</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
                    <div>
                        <p className="text-xs text-gray-400 mb-1">ID Pelanggan</p>
                        <p className="font-bold text-gray-800 text-lg">{activeData?.idpel || searchId}</p>
                    </div>
                    <div>
                        <p className="text-xs text-gray-400 mb-1">Alamat</p>
                        <p className="font-bold text-gray-800">{activeData?.alamat || '-'}</p>
                    </div>
                     <div>
                        <p className="text-xs text-gray-400 mb-1">Nama</p>
                        <p className="font-bold text-gray-800">{activeData?.nama || '-'}</p>
                    </div>
                </div>
            </div>

            <div className="border-t border-gray-100 my-8"></div>

            {/* Connection Section */}
            <div>
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-8 rounded-full bg-yellow-100 flex items-center justify-center text-yellow-600">
                        <Zap size={16} />
                    </div>
                    <h3 className="font-bold text-gray-800">Detail Koneksi Listrik</h3>
                </div>
                
                 <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
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
    </div>
  );
};

const DetailItem = ({ label, value }: { label: string, value: string }) => (
    <div>
        <p className="text-xs text-gray-400 mb-1">{label}</p>
        <p className="font-bold text-gray-800">{value}</p>
    </div>
);

export default CustomerDetailModal;
