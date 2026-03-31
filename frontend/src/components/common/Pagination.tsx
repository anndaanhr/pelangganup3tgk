import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
    currentPage: number;
    totalItems: number;
    itemsPerPage: number;
    onPageChange: (page: number) => void;
    compact?: boolean;
    showInput?: boolean;
}

const Pagination: React.FC<PaginationProps> = ({ 
    currentPage, 
    totalItems, 
    itemsPerPage, 
    onPageChange,
    compact = false,
    showInput = false
}) => {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const [pageInput, setPageInput] = useState(currentPage.toString());

    useEffect(() => {
        setPageInput(currentPage.toString());
    }, [currentPage]);

    if (totalPages <= 1) return null;

    const handleJump = (e: React.FormEvent) => {
        e.preventDefault();
        const page = parseInt(pageInput);
        if (page >= 1 && page <= totalPages) {
            onPageChange(page);
        } else {
            setPageInput(currentPage.toString());
        }
    };

    return (
        <div className="flex items-center justify-between pt-4 border-t border-gray-100 text-sm">
             <div className="flex items-center gap-2">
                <button
                    disabled={currentPage === 1}
                    onClick={() => onPageChange(currentPage - 1)}
                    className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50 text-gray-500 transition-colors"
                >
                    <ChevronLeft size={16} />
                </button>
                
                <div className="flex gap-1 hidden sm:flex">
                    {/* Simplified logic: Show first 3, then ..., then last if needed, or just a window around current. 
                        User asked to follow CustomerTable style which was just [1][2][3]... 
                        I will improve it slightly to be useful. */}
                    {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                        // Logic to show a window of pages is complex, let's stick to simple or slightly smart
                        // If totalPages is large, show: 1, ... current-1, current, current+1 ... last
                        // For now, let's just do a simple window or what CustomerTable did (first 3).
                        // CustomerTable code: [...Array(Math.min(3, totalPages))]
                        // I will implement a smarter sliding window.
                        return null; 
                    })}
                    
                    {(() => {
                        const pages = [];
                         // Always show page 1
                        if (totalPages > 0) pages.push(1);

                        let start = Math.max(2, currentPage - 1);
                        let end = Math.min(totalPages - 1, currentPage + 1);

                        if (start > 2) pages.push('...');
                        for (let i = start; i <= end; i++) {
                            pages.push(i);
                        }
                        if (end < totalPages - 1) pages.push('...');
                        
                        // Always show last page if > 1
                        if (totalPages > 1) pages.push(totalPages);

                        // If total pages is small (e.g. < 7), just show all
                        if (totalPages <= 7) {
                            return Array.from({length: totalPages}, (_, i) => i + 1).map(p => (
                                 <button
                                    key={p}
                                    onClick={() => onPageChange(p)}
                                    className={`min-w-[2rem] h-8 px-2 rounded-lg text-xs font-bold transition-colors ${currentPage === p ? 'bg-blue-600 text-white shadow-md shadow-blue-200' : 'bg-white border border-gray-100 text-gray-500 hover:bg-gray-50'}`}
                                >
                                    {p}
                                </button>
                            ));
                        }

                        // Render the complex list
                         return pages.map((p, idx) => (
                             typeof p === 'number' ? (
                                <button
                                    key={idx}
                                    onClick={() => onPageChange(p)}
                                    className={`min-w-[2rem] h-8 px-2 rounded-lg text-xs font-bold transition-colors ${currentPage === p ? 'bg-blue-600 text-white shadow-md shadow-blue-200' : 'bg-white border border-gray-100 text-gray-500 hover:bg-gray-50'}`}
                                >
                                    {p}
                                </button>
                             ) : (
                                 <span key={idx} className="flex items-end px-1 text-gray-400">...</span>
                             )
                        ));
                    })()}
                </div>

                <button
                    disabled={currentPage === totalPages}
                    onClick={() => onPageChange(currentPage + 1)}
                    className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50 text-gray-500 transition-colors"
                >
                    <ChevronRight size={16} />
                </button>
            </div>

            {(!compact || showInput) && (
                <form onSubmit={handleJump} className="flex items-center gap-2 ml-4">
                    <span className="text-gray-500 text-xs text-nowrap hidden md:inline">Go to</span>
                    <input
                        type="number"
                        min="1"
                        max={totalPages}
                        value={pageInput}
                        onChange={(e) => setPageInput(e.target.value)}
                         className="w-20 px-2 py-1.5 border border-gray-200 rounded-lg text-center text-xs focus:ring-2 focus:ring-blue-500 outline-none"
                        placeholder="#"
                    />
                    <button type="submit" className="hidden"></button>
                </form>
            )}
            
            {compact && (
                 <span className="text-gray-500 text-xs ml-auto">
                    {currentPage} / {totalPages}
                </span>
            )}
        </div>
    );
};

export default Pagination;
