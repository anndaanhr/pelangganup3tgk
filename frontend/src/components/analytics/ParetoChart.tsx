import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const ParetoChart = ({ data }: { data: any[] }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Pelanggan Terbesar</h3>
            <p className="text-sm text-gray-500 mb-6">Pelanggan dengan konsumsi energi tertinggi berkontribusi signifikan terhadap beban.</p>

            <div className="h-[600px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data.slice(0, 20)} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <XAxis dataKey="nama" tick={false} />
                        <YAxis tickFormatter={(val) => `${(val / 1000).toFixed(0)}k`} />
                        <Tooltip
                            formatter={(val: number) => [`${val.toLocaleString('id-ID')} kWh`, 'Total']}
                            labelStyle={{ color: '#374151' }}
                        />
                        <Bar dataKey="total_kwh" radius={[4, 4, 0, 0]}>
                            {data.slice(0, 20).map((entry, index) => (
                                <Cell key={`cell-${index}`} fill="#3b82f6" />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default ParetoChart;
