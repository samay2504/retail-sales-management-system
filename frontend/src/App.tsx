/**
 * Main App component
 */
import { useState, useMemo, useCallback, useRef, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Header } from './components/Header';
import { SearchBar } from './components/SearchBar';
import { SortSelector } from './components/SortSelector';
import { FilterPanel } from './components/FilterPanel';
import { TransactionTable } from './components/TransactionTable';
import { Pagination } from './components/Pagination';
import { AppliedFilters } from './components/AppliedFilters';
import { useTransactions, useFilterMetadata } from './hooks/useApi';
import type { TransactionFilters } from './types/api';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function TransactionsPage() {
  const [filters, setFilters] = useState<TransactionFilters>({
    page: 1,
    limit: 10,
    sort: 'date:desc',
  });

  // Create stable filter key for comparison (prevents unnecessary page resets)
  const filtersKey = useMemo(() => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { page, limit, sort, ...filterValues } = filters;
    return JSON.stringify(filterValues);
  }, [filters]);

  // Track previous filter key to detect actual changes
  const prevFiltersKeyRef = useRef(filtersKey);

  // Debug logging (development only)
  useEffect(() => {
    if (import.meta.env.DEV) {
      console.debug('[Pagination Debug]', {
        page: filters.page,
        filtersKey,
        filtersChanged: prevFiltersKeyRef.current !== filtersKey,
        timestamp: Date.now(),
      });
    }
  }, [filters.page, filtersKey]);

  // Fetch data
  const { data: transactionsData, isLoading: isLoadingTransactions, error: transactionsError } = useTransactions(filters);
  const { data: filterMetadata, isLoading: isLoadingMetadata, error: metadataError } = useFilterMetadata();

  const handleSearchChange = useCallback((q: string) => {
    setFilters((prev) => ({
      ...prev,
      q: q || undefined,
      page: 1, // Reset to first page on search
    }));
  }, []);

  const handleSortChange = useCallback((sort: string) => {
    setFilters((prev) => ({
      ...prev,
      sort,
      page: 1, // Reset to first page on sort
    }));
  }, []);

  const handleFiltersChange = useCallback((newFilters: TransactionFilters) => {
    setFilters((prev) => {
      // Only reset page if actual filter values changed (not page/limit/sort)
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { page: prevPage, limit: prevLimit, sort: prevSort, ...prevFilterValues } = prev;
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { page: newPage, limit: newLimit, sort: newSort, ...newFilterValues } = newFilters;
      const filtersChanged = JSON.stringify(prevFilterValues) !== JSON.stringify(newFilterValues);
      
      if (import.meta.env.DEV) {
        console.debug('[handleFiltersChange]', {
          filtersChanged,
          prevFilterValues,
          newFilterValues,
        });
      }
      
      return {
        ...newFilters,
        page: filtersChanged ? 1 : (newFilters.page ?? prev.page),
      };
    });
  }, []);

  const handlePageChange = useCallback((newPage: number) => {
    if (import.meta.env.DEV) {
      console.debug('[handlePageChange]', { page: newPage, timestamp: Date.now() });
    }
    setFilters((prev) => ({
      ...prev,
      page: newPage,
    }));
  }, []);

  const handleClearFilters = useCallback(() => {
    setFilters((prev) => ({
      page: 1,
      limit: 10,
      sort: prev.sort,
      q: prev.q,
    }));
  }, []);

  const handleRemoveFilter = useCallback((field: keyof TransactionFilters, value?: string) => {
    setFilters((prev) => {
      const newFilters = { ...prev };

      if (value && Array.isArray(newFilters[field])) {
        // Remove specific value from array
        const arr = newFilters[field] as string[];
        const filtered = arr.filter((v) => v !== value);
        if (filtered.length === 0) {
          delete newFilters[field];
        } else {
          (newFilters as Record<string, unknown>)[field] = filtered;
        }
      } else {
        // Remove entire field
        delete newFilters[field];
      }

      return { ...newFilters, page: 1 };
    });
  }, []);

  return (
    <div className="min-h-screen bg-slate-950">
      <Header />
      
      <main className="container mx-auto px-4 sm:px-6 py-8 max-w-screen-2xl">
        <div className="flex flex-col lg:flex-row gap-6 lg:gap-8">
          {/* Filter Panel - Left Side */}
          <aside className="lg:w-80 flex-shrink-0">
            {isLoadingMetadata ? (
              <div className="glass-card p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="skeleton h-6 w-24 rounded"></div>
                  <div className="skeleton h-5 w-16 rounded-full"></div>
                </div>
                <div className="space-y-4">
                  {[...Array(8)].map((_, i) => (
                    <div key={i} className="space-y-2">
                      <div className="skeleton h-4 w-20 rounded"></div>
                      <div className="space-y-2">
                        {[...Array(3)].map((_, j) => (
                          <div key={j} className="skeleton h-6 w-full rounded"></div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : metadataError ? (
              <div className="glass-card p-6 text-center">
                <div className="text-red-400 mb-2">⚠️ Failed to load filters</div>
                <button
                  onClick={() => window.location.reload()}
                  className="text-sm text-primary hover:text-primary/80 transition-colors"
                >
                  Reload page
                </button>
              </div>
            ) : filterMetadata ? (
              <FilterPanel
                metadata={filterMetadata}
                filters={filters}
                onChange={handleFiltersChange}
                onClear={handleClearFilters}
              />
            ) : null}
          </aside>

          {/* Main Content */}
          <div className="flex-1 space-y-6">
            {/* Error State */}
            {transactionsError && (
              <div className="glass-card p-6 text-center">
                <div className="text-red-400 text-lg mb-2">⚠️ Failed to load transactions</div>
                <p className="text-gray-400 text-sm mb-4">
                  {transactionsError.message || 'An error occurred while fetching data'}
                </p>
                <button
                  onClick={() => window.location.reload()}
                  className="btn-primary"
                >
                  Retry
                </button>
              </div>
            )}
            {/* Search and Sort Bar */}
            <div className="glass-card p-6">
              <div className="flex flex-col md:flex-row gap-4 items-stretch md:items-center">
                <div className="flex-1">
                  <SearchBar
                    value={filters.q || ''}
                    onChange={handleSearchChange}
                  />
                </div>
                <div className="flex-shrink-0">
                  <SortSelector
                    value={filters.sort || 'date:desc'}
                    onChange={handleSortChange}
                  />
                </div>
              </div>

              {/* Applied Filters */}
              {Object.keys(filters).filter(k => !['page', 'limit', 'sort', 'q'].includes(k)).length > 0 && (
                <div className="mt-4 pt-4 border-t border-white/10">
                  <AppliedFilters filters={filters} onRemove={handleRemoveFilter} />
                </div>
              )}
            </div>

            {/* Results Summary with Loading State */}
            <div className="flex items-center justify-between text-sm text-gray-400">
              <div>
                {filters.q && (
                  <span>
                    Search results for <span className="text-primary font-medium">"{filters.q}"</span>
                  </span>
                )}
              </div>
              <div className="flex items-center gap-3">
                {isLoadingTransactions && (
                  <div className="flex items-center gap-2 text-primary">
                    <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Loading...</span>
                  </div>
                )}
                {transactionsData && (
                  <span>
                    {transactionsData.meta.total.toLocaleString()} result{transactionsData.meta.total !== 1 ? 's' : ''} found
                  </span>
                )}
              </div>
            </div>

            {/* Transactions Table */}
            <TransactionTable
              transactions={transactionsData?.items || []}
              isLoading={isLoadingTransactions}
            />

            {/* Pagination */}
            {transactionsData && transactionsData.meta.total > 0 && (
              <Pagination
                meta={transactionsData.meta}
                onPageChange={handlePageChange}
              />
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-8 mt-16 border-t border-white/10">
        <div className="text-center text-sm text-gray-500">
          <p>TruEstate Retail Sales Management System</p>
          <p className="mt-2">Built with FastAPI, React, and Tailwind CSS</p>
        </div>
      </footer>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TransactionsPage />
    </QueryClientProvider>
  );
}

export default App;
