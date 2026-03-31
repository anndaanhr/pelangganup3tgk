import { fetchWithCache } from './api';

export const getParetoAnalysis = async (limit = 50, unitup?: number) => {
    let url = `/analytics/pareto?limit=${limit}`;
    if (unitup) url += `&unitup=${unitup}`;
    return fetchWithCache(url);
};

export const getZeroUsageAnomalies = async (page = 1, limit = 10, unitup?: number) => {
    let url = `/analytics/anomalies/zero-usage?page=${page}&limit=${limit}`;
    if (unitup) url += `&unitup=${unitup}`;
    return fetchWithCache(url);
};

export const getHighVarianceAnomalies = async (
    page = 1,
    limit = 10,
    unitup?: number,
    min_pct?: number,
    max_pct?: number
) => {
    let url = `/analytics/anomalies/high-variance?page=${page}&limit=${limit}`;
    if (unitup) url += `&unitup=${unitup}`;
    if (min_pct !== undefined) url += `&min_pct=${min_pct}`;
    if (max_pct !== undefined) url += `&max_pct=${max_pct}`;

    return fetchWithCache(url);
};

export const getGarduStats = async (limit = 50, unitup?: number) => {
    let url = `/analytics/infrastructure/gardu?limit=${limit}`;
    if (unitup) url += `&unitup=${unitup}`;
    return fetchWithCache(url);
};

export const getPowerChanges = async (unitup?: number) => {
    let url = '/analytics/lifecycle/power-changes';
    if (unitup) url += `?unitup=${unitup}`;
    return fetchWithCache(url);
};

export interface DayaData {
    daya: number;
    count: number;
    total_kwh: number;
    label: string;
}

export const getDayaDistribution = async (year: number = 2025, unitup?: number): Promise<DayaData[]> => {
    let url = `/analytics/distribution/daya?year=${year}`;
    if (unitup) url += `&unitup=${unitup}`;
    return fetchWithCache(url);
};
