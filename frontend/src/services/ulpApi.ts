import { api } from './api';

export interface UlpOverviewItem {
    unitup: number;
    name: string;
    customer_count_2025: number;
    customer_count_2024: number;
    total_kwh_2025: number;
    total_kwh_2024: number;
    kwh_growth_percent: number;
    customer_growth_percent: number;
}

export const getUlpOverview = async (): Promise<UlpOverviewItem[]> => {
    const response = await api.get('/analytics/ulp/overview');
    return response.data;
};


