import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';

const GarduChart = ({ data, height = 600 }: { data: any[], height?: number }) => {
    // Sort data to make chart look nice
    // Revert to original behavior: Show Top 20 items.
    const sortedData = [...data].sort((a, b) => b.total_kwh - a.total_kwh).slice(0, 20);

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-bold text-gray-800 mb-2">Beban Infrastruktur</h3>
            <p className="text-sm text-gray-500 mb-6">Top 20 Gardu dengan total konsumsi energi tertinggi.</p>

            {/* Fixed height controlled by prop */}
            <div className="w-full" style={{ height: `${height}px` }}>
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                        data={sortedData}
                        layout="vertical"
                        margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                        <XAxis type="number" tickFormatter={(val) => `${(val / 1000000).toFixed(1)} GWh`} />
                        <YAxis
                            dataKey="gardu"
                            type="category"
                            width={150}
                            tick={{ fontSize: 11 }}
                            interval={0}
                        />
                        <Tooltip
                            formatter={(val: number, name: string) => [
                                `${val.toLocaleString('id-ID')} kWh`,
                                name === '2025' ? 'Beban 2025' : 'Beban 2024'
                            ]}
                            labelStyle={{ color: '#374151', fontWeight: 'bold' }}
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Bar dataKey="total_kwh_2024" name="2024" fill="#9ca3af" radius={[0, 4, 4, 0]} barSize={20} />
                        <Bar dataKey="total_kwh" name="2025" radius={[0, 4, 4, 0]} barSize={20}>
                            {sortedData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={index < 3 ? '#ef4444' : '#3b82f6'} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>

            <div className="mt-4 flex gap-6 text-sm text-gray-500 justify-center">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-gray-400 rounded-sm"></div>
                    <span>Tahun 2024</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-blue-500 rounded-sm"></div>
                    <span>Tahun 2025</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-red-500 rounded-sm"></div>
                    <span>2025 (Kritis)</span>
                </div>
            </div>
        </div>
    );
};

export default GarduChart;
