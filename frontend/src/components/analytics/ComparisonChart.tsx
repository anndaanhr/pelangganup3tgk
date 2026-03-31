import React from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Rectangle
} from 'recharts';

interface ComparisonData {
    label: string;
    value_2024: number;
    value_2025: number;
}

interface ComparisonChartProps {
    data: ComparisonData[];
    title: string;
    subTitle?: string;
    height?: number;
}

const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
        return (
            <div className="bg-white/90 backdrop-blur-sm p-4 rounded-xl shadow-lg border border-gray-100">
                <p className="font-bold text-gray-800 mb-2">{label}</p>
                {payload.map((entry: any, index: number) => (
                    <div key={index} className="flex items-center gap-2 mb-1 text-xs">
                        <div
                            className="w-2 h-2 rounded-full"
                            style={{ backgroundColor: entry.color }}
                        />
                        <span className="text-gray-500 font-medium w-12">{entry.name}</span>
                        <span className="font-bold text-gray-700">
                            {(entry.value / 1e6).toFixed(2)} GWh
                        </span>
                    </div>
                ))}
            </div>
        );
    }
    return null;
};

const ComparisonChart: React.FC<ComparisonChartProps> = ({ data, title, subTitle, height = 300 }) => {
    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-full flex flex-col relative overflow-hidden">
            {/* Background Decoration */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50/50 rounded-bl-full -z-0 pointer-events-none" />

            <div className="mb-6 z-10 relative">
                <h3 className="font-bold text-xl text-gray-800">{title}</h3>
                {subTitle && <p className="text-xs text-gray-400 font-medium uppercase tracking-wider mt-1">{subTitle}</p>}
            </div>

            <div className="flex-1 w-full z-10 relative" style={{ minHeight: height }}>
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                        data={data}
                        margin={{ top: 10, right: 10, left: 10, bottom: 0 }}
                        barGap={8}
                        barCategoryGap="20%"
                    >
                        <defs>
                            <linearGradient id="grad2024" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor="#94a3b8" stopOpacity={0.8} />
                                <stop offset="100%" stopColor="#cbd5e1" stopOpacity={0.5} />
                            </linearGradient>
                            <linearGradient id="grad2025" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor="#3b82f6" stopOpacity={1} />
                                <stop offset="100%" stopColor="#60a5fa" stopOpacity={0.8} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                        <XAxis
                            dataKey="label"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 11, fontWeight: 600 }}
                            dy={10}
                        />
                        <YAxis
                            hide
                        />
                        <Tooltip content={<CustomTooltip />} cursor={{ fill: '#f8fafc', opacity: 0.5 }} />
                        <Legend
                            wrapperStyle={{ paddingTop: '20px' }}
                            iconType="circle"
                            formatter={(value) => <span className="text-sm font-medium text-gray-600 ml-1">{value}</span>}
                        />
                        <Bar
                            dataKey="value_2024"
                            name="2024"
                            fill="url(#grad2024)"
                            radius={[6, 6, 6, 6]}
                            barSize={16}
                            animationDuration={1500}
                        />
                        <Bar
                            dataKey="value_2025"
                            name="2025"
                            fill="url(#grad2025)"
                            radius={[6, 6, 6, 6]}
                            barSize={16}
                            animationDuration={1500}
                        // Add simple shadow effect via filter if possible, or usually just gradient is enough
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default ComparisonChart;
