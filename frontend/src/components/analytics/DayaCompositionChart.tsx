import React, { useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Users, Zap } from 'lucide-react';

interface DayaData {
    daya: number;
    count: number;
    total_kwh: number;
    label: string;
}

interface Props {
    data: DayaData[];
}

export const generateColor = (index: number) => {
    const hue = (index * 137.508) % 360; // Golden angle approximation for distinctiveness
    return `hsl(${hue}, 70%, 50%)`;
};

const DayaCompositionChart: React.FC<Props> = ({ data }) => {
    const [mode, setMode] = useState<'count' | 'kwh'>('count');

    // Calculate total for percentage
    const total = data.reduce((sum, item) => sum + (mode === 'count' ? item.count : item.total_kwh), 0);

    const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
        const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
        const x = cx + radius * Math.cos(-midAngle * Math.PI / 180);
        const y = cy + radius * Math.sin(-midAngle * Math.PI / 180);

        if (percent < 0.05) return null; // Hide label for small slices

        return (
            <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" className="text-[10px] font-bold">
                {`${(percent * 100).toFixed(0)}%`}
            </text>
        );
    };

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full flex flex-col">
            <div className="flex justify-between items-start mb-6">
                <div>
                    <h3 className="font-bold text-lg text-gray-800">Distribusi Beban (Daya)</h3>
                    <p className="text-gray-500 text-xs">Segmentasi pelanggan berdasarkan daya terpasang</p>
                </div>
                <div className="flex bg-gray-100 p-1 rounded-lg">
                    <button
                        onClick={(e) => { e.stopPropagation(); setMode('count'); }}
                        className={`p-1.5 rounded-md transition-all ${mode === 'count' ? 'bg-white shadow text-blue-600' : 'text-gray-400 hover:text-gray-600'}`}
                        title="Jumlah Pelanggan"
                    >
                        <Users size={16} />
                    </button>
                    <button
                        onClick={(e) => { e.stopPropagation(); setMode('kwh'); }}
                        className={`p-1.5 rounded-md transition-all ${mode === 'kwh' ? 'bg-white shadow text-amber-500' : 'text-gray-400 hover:text-gray-600'}`}
                        title="Konsumsi Energi"
                    >
                        <Zap size={16} />
                    </button>
                </div>
            </div>

            <div className="flex-1 w-full min-h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={100}
                            paddingAngle={2}
                            dataKey={mode === 'count' ? 'count' : 'total_kwh'}
                            labelLine={false}
                            label={renderCustomLabel}
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={generateColor(index)} />
                            ))}
                        </Pie>
                        <Tooltip
                            formatter={(value: number, name: string, props: any) => {
                                const val = mode === 'count' ? `${value.toLocaleString()} Pelanggan` : (value / 1e6).toFixed(2) + ' GWh';
                                return [val, props.payload.label];
                            }}
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                        />
                        <Legend
                            layout="vertical"
                            verticalAlign="middle"
                            align="right"
                            wrapperStyle={{ fontSize: '11px', fontWeight: 500 }}
                        />
                    </PieChart>
                </ResponsiveContainer>
            </div>

            <div className="mt-4 text-center">
                <p className="text-xs text-gray-400">Total: {mode === 'count' ? total.toLocaleString() + ' Pelanggan' : (total / 1e6).toFixed(2) + ' GWh'}</p>
            </div>
        </div>
    );
};

export default DayaCompositionChart;
