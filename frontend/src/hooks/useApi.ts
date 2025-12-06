/**
 * React Query hooks for data fetching
 */
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { useMemo } from 'react';
import { apiClient } from '../services/api';
import type {
  Transaction,
  TransactionListResponse,
  FilterMetadata,
  TransactionFilters,
} from '../types/api';

/**
 * Hook to fetch transactions list with race condition prevention
 */
export function useTransactions(
  filters: TransactionFilters
): UseQueryResult<TransactionListResponse, Error> {
  // Create stable query key to prevent unnecessary refetches
  // Stringify filters to ensure stable reference equality
  const stableQueryKey = useMemo(() => {
    // Create a sorted, stable representation of filters
    const sortedFilters = Object.keys(filters)
      .sort()
      .reduce((acc, key) => {
        const value = filters[key as keyof TransactionFilters];
        if (value !== undefined && value !== null) {
          acc[key] = value;
        }
        return acc;
      }, {} as Record<string, string | number | string[] | undefined>);
    
    return ['transactions', sortedFilters];
  }, [filters]);

  return useQuery<TransactionListResponse, Error>({
    queryKey: stableQueryKey,
    queryFn: ({ signal }) => {
      if (import.meta.env.DEV) {
        console.debug('[useTransactions] queryFn called', {
          page: filters.page,
          hasSignal: !!signal,
        });
      }
      return apiClient.listTransactions(filters, signal);
    },
    placeholderData: (previousData) => previousData, // Prevent UI flicker during page changes
    staleTime: 30000, // 30 seconds - aggressive caching for better UX
    gcTime: 600000, // 10 minutes - keep in memory longer
    retry: 2, // Retry failed requests twice
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000), // Exponential backoff
    refetchOnWindowFocus: false, // Prevent unwanted refetches
    refetchOnMount: false, // Don't refetch on component mount if data is fresh
  });
}

/**
 * Hook to fetch a single transaction
 */
export function useTransaction(id: number): UseQueryResult<Transaction, Error> {
  return useQuery({
    queryKey: ['transaction', id],
    queryFn: () => apiClient.getTransaction(id),
    enabled: !!id,
    staleTime: 60000, // 1 minute
  });
}

/**
 * Hook to fetch filter metadata
 */
export function useFilterMetadata(): UseQueryResult<FilterMetadata, Error> {
  return useQuery({
    queryKey: ['filterMetadata'],
    queryFn: () => apiClient.getFilterMetadata(),
    staleTime: Infinity, // Never automatically refetch - metadata rarely changes
    gcTime: Infinity, // Keep forever in memory
    retry: 3, // Retry 3 times for critical metadata
    retryDelay: 1000, // 1 second between retries
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    refetchOnReconnect: false,
  });
}
