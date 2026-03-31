import React from 'react';
import { Treemap, Tooltip, ResponsiveContainer } from 'recharts';

const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload;
        return (
            <div className="bg-white p-3 border border-gray-200 shadow-xl rounded-lg">
                <p className="font-bold text-gray-800">{data.gardu}</p>
                <p className="text-sm text-blue-600">Total: {data.total_kwh.toLocaleString('id-ID')} kWh</p>
                <p className="text-xs text-gray-500">Pelanggan: {data.customer_count}</p>
            </div>
        );
    }
    return null;
};

const GarduTreemap = ({ data }: { data: any[] }) => {
    // Transform data for Treemap (needs name/size or children)
    // Recharts Treemap data format: [{name: 'A', size: 100}, ...]
    const treeData = data.map(d => ({
        name: d.gardu,
        size: d.total_kwh,
        ...d
    }));

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-bold text-gray-800 mb-2">Peta Beban Infrastruktur (Gardu)</h3>
            <p className="text-sm text-gray-500 mb-6">Ukuran kotak merepresentasikan total beban kWh pada Gardu tersebut.</p>

            <div className="h-[400px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <Treemap
                        data={treeData}
                        dataKey="size"
                        aspectRatio={4 / 3}
                        stroke="#fff"
                        fill="#3b82f6"
                    >
                        <Tooltip content={<CustomTooltip />} />
                    </Treemap>
                </ResponsiveContainer>
            </div>
            <div className="mt-4 flex gap-4 text-sm text-gray-500 justify-center">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-blue-500 rounded-sm"></div>
                    <span>Beban Tinggi</span>
                </div>
            </div>
        </div>
    );
};

export default GarduTreemap;
