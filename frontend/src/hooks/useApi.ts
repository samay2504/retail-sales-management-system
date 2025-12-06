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
    placeholderData: (previousData) => previousData, // Prevent UI flicker during page changes (replaces keepPreviousData in v5)
    staleTime: 5000, // 5 seconds for good UX without excessive refetches
    gcTime: 300000, // 5 minutes (previously cacheTime)
    retry: 1,
    refetchOnWindowFocus: false, // Prevent unwanted refetches
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
    staleTime: 300000, // 5 minutes
    gcTime: 600000, // 10 minutes
  });
}
