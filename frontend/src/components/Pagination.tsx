/**
 * Pagination controls component
 */
import type { PaginationMeta } from '../types/api';

interface PaginationProps {
  meta: PaginationMeta;
  onPageChange: (page: number) => void;
}

export const Pagination = ({ meta, onPageChange }: PaginationProps) => {
  const { page, total_pages, has_prev, has_next, total, limit } = meta;

  const startItem = (page - 1) * limit + 1;
  const endItem = Math.min(page * limit, total);

  // Generate page numbers to display
  const getPageNumbers = () => {
    const pages: (number | string)[] = [];
    const maxVisible = 7;

    if (total_pages <= maxVisible) {
      // Show all pages if total is small
      for (let i = 1; i <= total_pages; i++) {
        pages.push(i);
      }
    } else {
      // Show first, last, current, and nearby pages
      pages.push(1);

      if (page > 3) {
        pages.push('...');
      }

      for (let i = Math.max(2, page - 1); i <= Math.min(page + 1, total_pages - 1); i++) {
        pages.push(i);
      }

      if (page < total_pages - 2) {
        pages.push('...');
      }

      pages.push(total_pages);
    }

    return pages;
  };

  return (
    <div className="glass-card px-6 py-4">
      <div className="flex flex-col sm:flex-row items-center justify-between space-y-4 sm:space-y-0">
        {/* Results info */}
        <div className="text-sm text-gray-400">
          Showing <span className="font-medium text-gray-200">{startItem}</span> to{' '}
          <span className="font-medium text-gray-200">{endItem}</span> of{' '}
          <span className="font-medium text-gray-200">{total}</span> results
        </div>

        {/* Page controls */}
        <div className="flex items-center space-x-2">
          {/* Previous button */}
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={!has_prev}
            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              has_prev
                ? 'bg-white/10 text-gray-200 hover:bg-white/20'
                : 'bg-white/5 text-gray-600 cursor-not-allowed'
            }`}
            aria-label="Previous page"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
          </button>

          {/* Page numbers */}
          <div className="hidden sm:flex items-center space-x-1">
            {getPageNumbers().map((pageNum, index) => {
              if (pageNum === '...') {
                return (
                  <span key={`ellipsis-${index}`} className="px-3 py-2 text-gray-500">
                    ...
                  </span>
                );
              }

              const isActive = pageNum === page;
              return (
                <button
                  key={pageNum}
                  onClick={() => onPageChange(pageNum as number)}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-gradient-cta text-white shadow-glow-cyan'
                      : 'bg-white/10 text-gray-200 hover:bg-white/20'
                  }`}
                >
                  {pageNum}
                </button>
              );
            })}
          </div>

          {/* Mobile page indicator */}
          <div className="sm:hidden px-3 py-2 bg-white/10 rounded-lg text-sm font-medium text-gray-200">
            {page} / {total_pages}
          </div>

          {/* Next button */}
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={!has_next}
            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              has_next
                ? 'bg-white/10 text-gray-200 hover:bg-white/20'
                : 'bg-white/5 text-gray-600 cursor-not-allowed'
            }`}
            aria-label="Next page"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};
