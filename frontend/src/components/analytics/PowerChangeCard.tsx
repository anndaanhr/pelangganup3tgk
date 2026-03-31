import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Zap } from 'lucide-react';
import Pagination from '../common/Pagination';

const StatCard = ({ title, value, sub, icon: Icon, color, compact }: any) => (
    <div className={`bg-white rounded-xl border border-gray-100 shadow-sm flex items-center justify-between ${compact ? 'p-5' : 'p-5'}`}>
        <div>
            <p className="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-1">{title}</p>
            <h4 className={`font-bold text-gray-800 ${compact ? 'text-2xl' : 'text-2xl'}`}>{value}</h4>
            <p className={`text-xs ${color ? 'text-' + color + '-600' : 'text-gray-400'}`}>{sub}</p>
        </div>
        <div className={`rounded-full bg-${color}-50 text-${color}-600 ${compact ? 'p-3' : 'p-3'}`}>
            <Icon size={compact ? 24 : 24} />
        </div>
    </div>
);

const PaginatedList = ({ items, title, icon: Icon, color, compact, showInput = false }: any) => {
    // User requested "pake scroll gausa pagination" for both Dashboard and Power Page relative to this component.
    // So we remove pagination logic and just show scrollable list.
    
    return (
        <div className={`bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex flex-col ${compact ? 'h-full min-h-[400px]' : 'h-[600px]'}`}>
            <div className="flex justify-between items-center mb-4">
                <h4 className="font-bold text-gray-800 flex items-center gap-2">
                    <Icon size={18} className={`text-${color}-600`} />
                    {title} <span className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full">{items.length}</span>
                </h4>
            </div>

            <div className={`flex-1 overflow-y-auto space-y-3 pr-2 mb-4 scrollbar-thin`}>
                {items.map((u: any, idx: number) => (
                    <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg text-sm hover:bg-gray-100 transition-colors">
                        <div>
                            <p className="font-semibold text-gray-700">{u.nama}</p>
                            <p className="text-xs text-gray-500">{u.idpel}</p>
                        </div>
                        <div className="text-right">
                            <p className={`font-bold text-${color}-600`}>
                                {u.daya_2024} → {u.daya_2025} VA
                            </p>
                            <p className={`text-xs text-${color}-700`}>{u.diff > 0 ? '+' : ''}{u.diff} VA</p>
                        </div>
                    </div>
                ))}
                {items.length === 0 && <p className="text-gray-400 text-center py-10">Tidak ada data</p>}
            </div>
        </div>
    );
};

const PowerChangeCard = ({ data, compact = false }: { data: any, compact?: boolean }) => {
    if (!data) return null;
    const { summary, upgrades, downgrades } = data;

    return (
        <div className={`flex flex-col gap-6 ${compact ? 'h-full py-4' : 'h-full gap-8 pt-12'}`}>
            <div className={`grid grid-cols-1 md:grid-cols-3 gap-4 flex-shrink-0`}>
                <StatCard
                    title="Tambah Daya"
                    value={summary.total_upgrades}
                    sub={`+${Math.round(summary.total_kva_added)} kVA Added`}
                    icon={TrendingUp}
                    color="green"
                    compact={compact}
                />
                <StatCard
                    title="Turun Daya"
                    value={summary.total_downgrades}
                    sub={`-${Math.round(summary.total_kva_reduced)} kVA Reduced`}
                    icon={TrendingDown}
                    color="red"
                    compact={compact}
                />
                <StatCard
                    title="Net Perubahan"
                    value={`${(summary.total_kva_added - summary.total_kva_reduced).toFixed(1)} kVA`}
                    sub="Total Kapasitas"
                    icon={Zap}
                    color="blue"
                    compact={compact}
                />
            </div>

            <div className={`grid grid-cols-1 lg:grid-cols-2 gap-6 flex-1 min-h-0`}>
                <PaginatedList items={upgrades} title="Daftar Penambahan Daya" icon={TrendingUp} color="green" compact={compact} showInput={true} />
                <PaginatedList items={downgrades} title="Daftar Penurunan Daya" icon={TrendingDown} color="red" compact={compact} showInput={true} />
            </div>
        </div>
    );
};

export default PowerChangeCard;
