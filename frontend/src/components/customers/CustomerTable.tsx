import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Eye, Edit2, Trash2 } from 'lucide-react';
import { getCustomers, getNewCustomers, getLostCustomers, Customer, getCustomerDetail, getFilterOptions } from '../../services/api';
import Pagination from '../common/Pagination';

interface CustomerTableProps {
  mode: 'all' | 'new' | 'lost';
  onShowDetail?: (data: any) => void;
}

const CustomerTable: React.FC<CustomerTableProps> = ({ mode, onShowDetail }) => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const initialYear = parseInt(searchParams.get('year') || '2025');
  const initialDaya = searchParams.get('daya') || '';

  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [selectedYear, setSelectedYear] = useState(initialYear);

  // Sync state with URL params
  useEffect(() => {
    const yearParam = parseInt(searchParams.get('year') || '2025');
    if (yearParam !== selectedYear) {
      setSelectedYear(yearParam);
    }
    const dayaParam = searchParams.get('daya') || '';
    if (dayaParam !== filterDaya) {
      setFilterDaya(dayaParam);
    }
  }, [searchParams]);

  // Filter state
  const [filterGardu, setFilterGardu] = useState<string>('');
  const [filterUnitUp, setFilterUnitUp] = useState<string>('');
  const [filterTarif, setFilterTarif] = useState<string>('');
  const [filterDaya, setFilterDaya] = useState<string>(initialDaya);
  const [filterJenis, setFilterJenis] = useState<string>('');
  const [filterLayanan, setFilterLayanan] = useState<string>('');

  const [filterOptions, setFilterOptions] = useState<{ tarif: string[]; gardu: string[]; unitup: string[]; daya: number[]; jenis: string[]; layanan: string[] } | null>(null);

  const pageSize = 30;

  const filterYear = mode === 'all' ? selectedYear : mode === 'new' ? 2025 : 2024;

  useEffect(() => {
    getFilterOptions(filterYear)
      .then((opts) => setFilterOptions({ ...opts, unitup: opts.unitup || [], daya: opts.daya || [] }))
      .catch(() => setFilterOptions(null));
  }, [mode, selectedYear, filterYear]);

  useEffect(() => {
    fetchData();
  }, [mode, page, selectedYear, filterGardu, filterUnitUp, filterTarif, filterDaya, filterJenis, filterLayanan]);

  useEffect(() => {
    setPage(1);
  }, [mode, filterGardu, filterUnitUp, filterTarif, filterDaya, filterJenis, filterLayanan]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const filters = {
        tarif: filterTarif || undefined,
        gardu: filterGardu || undefined,
        unitup: filterUnitUp || undefined,
        daya: filterDaya ? parseInt(filterDaya, 10) : undefined,
        jenis: filterJenis || undefined,
        layanan: filterLayanan || undefined
      };

      let response;
      if (mode === 'new') {
        response = await getNewCustomers(page, pageSize, filters);
      } else if (mode === 'lost') {
        response = await getLostCustomers(page, pageSize, filters);
      } else {
        response = await getCustomers(page, pageSize, selectedYear, filters);
      }

      if (response) {
        setCustomers(response.items);
        setTotalItems(response.total);
        setTotalPages(Math.ceil(response.total / pageSize) || 1);
      }
    } catch (error) {
      console.error("Failed to fetch customers", error);
      setCustomers([]);
      setTotalItems(0);
      setTotalPages(1);
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetail = (idpel: number) => {
    navigate(`/pelanggan/${idpel}`);
  };

  const getTitle = () => {
    if (mode === 'new') return 'Daftar Pelanggan Baru';
    if (mode === 'lost') return 'Daftar Pelanggan Hilang';
    return 'Daftar Pelanggan';
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">{getTitle()}</h1>
          <p className="text-gray-500 text-sm mt-1">
            {mode === 'all' ? 'Semua Data Pelanggan' : (mode === 'new' ? 'Periode Tahun 2025' : 'Periode Tahun 2024 ke 2025')}
          </p>
        </div>
        {mode === 'all' && (
          <div className="flex bg-gray-100 p-1 rounded-lg">
            <button
              onClick={() => setSelectedYear(2024)}
              className={`px-3 py-1 text-xs font-bold rounded-md transition-all ${selectedYear === 2024 ? 'bg-white shadow text-blue-600' : 'text-gray-500 hover:text-gray-800'}`}
            >
              2024
            </button>
            <button
              onClick={() => setSelectedYear(2025)}
              className={`px-3 py-1 text-xs font-bold rounded-md transition-all ${selectedYear === 2025 ? 'bg-white shadow text-blue-600' : 'text-gray-500 hover:text-gray-800'}`}
            >
              2025
            </button>
          </div>
        )}
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        {/* Filters */}
        <div className="flex flex-wrap items-center gap-4 mb-6">
          <h3 className="font-bold text-gray-800 whitespace-nowrap">Filter</h3>

          <select
            value={filterGardu}
            onChange={(e) => setFilterGardu(e.target.value)}
            className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 min-w-[140px]"
          >
            <option value="">Semua Gardu</option>
            {(filterOptions?.gardu || []).map((g) => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select>

          <select
            value={filterUnitUp}
            onChange={(e) => setFilterUnitUp(e.target.value)}
            className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 min-w-[140px]"
          >
            <option value="">Semua Unit ULP</option>
            {(filterOptions?.unitup || []).map((u) => (
              <option key={u} value={u}>{u}</option>
            ))}
          </select>

          <select
            value={filterTarif}
            onChange={(e) => setFilterTarif(e.target.value)}
            className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 min-w-[140px]"
          >
            <option value="">Semua Tarif</option>
            {(filterOptions?.tarif || []).map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>

          <select
            value={filterJenis}
            onChange={(e) => setFilterJenis(e.target.value)}
            className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 min-w-[140px]"
          >
            <option value="">Semua Jenis</option>
            {(filterOptions?.jenis || []).map((j) => (
              <option key={j} value={j}>{j}</option>
            ))}
          </select>

          <select
            value={filterLayanan}
            onChange={(e) => setFilterLayanan(e.target.value)}
            className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 min-w-[140px]"
          >
            <option value="">Semua Layanan</option>
            {(filterOptions?.layanan || []).map((l) => (
              <option key={l} value={l}>{l}</option>
            ))}
          </select>

          <select
            value={filterDaya}
            onChange={(e) => setFilterDaya(e.target.value)}
            className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 min-w-[120px]"
          >
            <option value="">Semua Daya</option>
            {(filterOptions?.daya || []).map((d) => (
              <option key={d} value={String(d)}>{d} VA</option>
            ))}
          </select>

          {(filterGardu || filterUnitUp || filterTarif || filterDaya || filterJenis || filterLayanan) && (
            <button
              type="button"
              onClick={() => {
                setFilterGardu('');
                setFilterUnitUp('');
                setFilterTarif('');
                setFilterDaya('');
                setFilterJenis('');
                setFilterLayanan('');
              }}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              Hapus filter
            </button>
          )}
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-gray-400 uppercase bg-transparent border-b border-gray-100">
              <tr>
                <th className="px-4 py-3 font-semibold">ID Pelanggan</th>
                <th className="px-4 py-3 font-semibold">Nama</th>
                <th className="px-4 py-3 font-semibold">Jenis</th>
                <th className="px-4 py-3 font-semibold">Layanan</th>
                <th className="px-4 py-3 font-semibold">Tarif</th>
                <th className="px-4 py-3 font-semibold">Daya</th>
                <th className="px-4 py-3 font-semibold">Gardu</th>
                <th className="px-4 py-3 font-semibold">Pemakaian (kWh)</th>
                <th className="px-4 py-3 font-semibold text-center">Aksi</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {loading ? (
                <tr><td colSpan={9} className="px-4 py-8 text-center text-gray-400">Memuat data...</td></tr>
              ) : customers.length > 0 ? (
                customers.map((row, idx) => (
                  <tr key={idx} className="hover:bg-gray-50/50 transition-colors group">
                    <td className="px-4 py-4 font-mono text-gray-600">{row.idpel}</td>
                    <td className="px-4 py-4 font-medium text-gray-800">{row.nama}</td>
                    <td className="px-4 py-4 text-gray-600 font-medium text-xs">{row.jenis}</td>
                    <td className="px-4 py-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${(row.layanan || '').toLowerCase().includes('pra')
                        ? 'bg-yellow-50 text-yellow-700 border-yellow-200'
                        : 'bg-blue-50 text-blue-700 border-blue-200'
                        }`}>
                        {row.layanan}
                      </span>
                    </td>
                    <td className="px-4 py-4">
                      <span className="font-mono text-xs bg-gray-100 px-2 py-1 rounded text-gray-600 font-semibold">
                        {row.tarif}
                      </span>
                    </td>
                    <td className="px-4 py-4 text-gray-600">{row.daya} VA</td>
                    <td className="px-4 py-4 text-gray-500 text-xs">{row.gardu || '-'}</td>
                    <td className="px-4 py-4 font-medium text-gray-800">
                      {(() => {
                        const value = mode === 'lost' || mode === 'new' ? row.total_consumption : (row.total_consumption ?? row.total_consumption_2025 ?? row.total_consumption_2024);
                        return value != null ? `${Number(value).toLocaleString('id-ID')}` : '-';
                      })()}
                    </td>
                    <td className="px-4 py-4">
                      <div className="flex items-center justify-center gap-2">
                        <button
                          onClick={() => handleViewDetail(row.idpel)}
                          className="p-1.5 text-blue-500 hover:bg-blue-50 rounded-lg transition-colors"
                          title="Lihat Detail"
                        >
                          <Eye size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr><td colSpan={9} className="px-4 py-8 text-center text-gray-400 italic">Tidak ada data ditemukan</td></tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="mt-6 pt-4 border-t border-gray-100">
           <Pagination 
              currentPage={page} 
              totalItems={totalItems} 
              itemsPerPage={pageSize}
              onPageChange={setPage} 
              showInput={true} 
           />
        </div>
      </div>
    </div>
  );
};

export default CustomerTable;
