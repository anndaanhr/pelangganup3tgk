import axios from 'axios';

// Dev: URL relatif → request lewat Vite proxy ke backend
// Production: pakai VITE_API_URL jika di-set, atau /api
const API_URL = import.meta.env.VITE_API_URL ?? '/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Simple memory cache
const apiCache: Record<string, { data: any, timestamp: number }> = {};
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

export async function fetchWithCache(url: string, forceRefresh = false) {
  const now = Date.now();
  if (!forceRefresh && apiCache[url] && (now - apiCache[url].timestamp < CACHE_DURATION)) {
    return apiCache[url].data;
  }
  
  const response = await api.get(url);
  apiCache[url] = { data: response.data, timestamp: now };
  return response.data;
}

export interface SummaryStats {
  total_customers_2024: number;
  total_customers_2025: number;
  active_customers: number;
  new_customers: number;
  lost_customers: number;
  total_consumption_2024: number;
  total_consumption_2025: number;

  total_revenue_2024?: number;
  total_revenue_2025?: number;
  total_energy_2024?: number;
  total_energy_2025?: number;

  avg_consumption_2024: number;
  avg_consumption_2025: number;
  consumption_change_percent: number;
}

export interface MonthlyData {
  month: string;
  value_2024: number;
  value_2025: number;
}

export interface Customer {
  idpel: number;
  nama: string;
  alamat: string;
  tarif: string;
  daya: number;
  jenis: string;
  layanan: string;
  gardu: string;
  total_consumption?: number;
  total_consumption_2024?: number;
  total_consumption_2025?: number;
}

// NOTE: All customer-related endpoints must now be prefixed with /customers

export const getDashboardStats = async (unitup?: number): Promise<SummaryStats> => {
  const url = unitup ? `/customers/dashboard?unitup=${unitup}` : '/customers/dashboard';
  return fetchWithCache(url);
};

export const getDashboardTrends = async (unitup?: number): Promise<MonthlyData[]> => {
  const url = unitup ? `/customers/dashboard/trends?unitup=${unitup}` : '/customers/dashboard/trends';
  return fetchWithCache(url);
};

export interface CustomerFilters {
  tarif?: string;
  gardu?: string;
  unitup?: string;
  daya?: number;
  jenis?: string;
  layanan?: string;
}

export const getFilterOptions = async (year: number): Promise<{ tarif: string[]; gardu: string[]; unitup: string[]; daya: number[]; jenis: string[]; layanan: string[] }> => {
  const response = await api.get(`/customers/filter-options/${year}`);
  const d = response.data;
  return {
    tarif: d.tarif || [],
    gardu: d.gardu || [],
    unitup: d.unitup || [],
    daya: d.daya || [],
    jenis: d.jenis || [],
    layanan: d.layanan || []
  };
};

function buildParams(page: number, pageSize: number, filters?: CustomerFilters): string {
  const params = new URLSearchParams();
  params.set('page', String(page));
  params.set('page_size', String(pageSize));
  if (filters?.tarif) params.set('tarif', filters.tarif);
  if (filters?.gardu) params.set('gardu', filters.gardu);
  if (filters?.unitup) params.set('unitup', filters.unitup);
  if (filters?.daya != null) params.set('daya', String(filters.daya));
  if (filters?.jenis) params.set('jenis', filters.jenis);
  if (filters?.layanan) params.set('layanan', filters.layanan);
  return params.toString();
}

export const getCustomers = async (
  page = 1,
  pageSize = 20,
  year = 2025,
  filters?: CustomerFilters
): Promise<{ items: Customer[]; total: number }> => {
  const q = buildParams(page, pageSize, filters);
  const response = await api.get(`/customers/all/${year}?${q}`);
  return response.data;
};

export const getNewCustomers = async (
  page = 1,
  pageSize = 20,
  filters?: CustomerFilters
): Promise<{ items: Customer[]; total: number }> => {
  const q = buildParams(page, pageSize, filters);
  const response = await api.get(`/customers/new?${q}`);
  return response.data;
};

export const getLostCustomers = async (
  page = 1,
  pageSize = 20,
  filters?: CustomerFilters
): Promise<{ items: Customer[]; total: number }> => {
  const q = buildParams(page, pageSize, filters);
  const response = await api.get(`/customers/lost?${q}`);
  return response.data;
};

export interface DistributionStats {
  tarif_distribution: { name: string; value: number }[];
  layanan_distribution: { label: string; value: number; percentage: number }[];
  total_revenue_2025: number;
}

export const getDistributionStats = async (unitup?: number): Promise<DistributionStats> => {
  const url = unitup ? `/customers/dashboard/distribution?unitup=${unitup}` : '/customers/dashboard/distribution';
  return fetchWithCache(url);
};

export const getCustomerDetail = async (idpel: string): Promise<any> => {
  return fetchWithCache(`/customers/${idpel}`);
};

export const getCustomerTrends = async (idpel: string): Promise<MonthlyData[]> => {
  return fetchWithCache(`/customers/${idpel}/trends`);
};

export interface ComparisonData {
  tarif: { label: string; value_2024: number; value_2025: number }[];
  jenis: { label: string; value_2024: number; value_2025: number }[];
  layanan: { label: string; value_2024: number; value_2025: number }[];
}

export const getComparisonStats = async (unitup?: number): Promise<ComparisonData> => {
  const url = unitup ? `/customers/dashboard/difference-analysis?unitup=${unitup}` : '/customers/dashboard/difference-analysis';
  return fetchWithCache(url);
};
