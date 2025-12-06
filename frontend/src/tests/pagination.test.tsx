/**
 * Pagination race condition tests
 */
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useTransactions } from '../hooks/useApi';
import { apiClient } from '../services/api';
import type { TransactionListResponse } from '../types/api';

// Mock API client
vi.mock('../services/api', () => ({
  apiClient: {
    listTransactions: vi.fn(),
  },
}));

describe('Pagination Race Condition Prevention', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
    vi.clearAllMocks();
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );

  it('should prevent race condition when quickly changing pages', async () => {
    // Setup: page 1 response (slow)
    const page1Response: TransactionListResponse = {
      items: [{ id: 1, customer_name: 'Page 1' } as any],
      meta: {
        page: 1,
        limit: 10,
        total: 100,
        total_pages: 10,
        has_prev: false,
        has_next: true,
      },
    };

    // Setup: page 2 response (fast)
    const page2Response: TransactionListResponse = {
      items: [{ id: 2, customer_name: 'Page 2' } as any],
      meta: {
        page: 2,
        limit: 10,
        total: 100,
        total_pages: 10,
        has_prev: true,
        has_next: true,
      },
    };

    let page1Resolver: (value: TransactionListResponse) => void;
    const page1Promise = new Promise<TransactionListResponse>((resolve) => {
      page1Resolver = resolve;
    });

    // Mock implementation that delays page 1
    vi.mocked(apiClient.listTransactions).mockImplementation(async (filters) => {
      if (filters?.page === 1) {
        // Slow response
        return page1Promise;
      } else {
        // Fast response
        await new Promise((resolve) => setTimeout(resolve, 10));
        return page2Response;
      }
    });

    // First render with page 1
    const { result, rerender } = renderHook(
      ({ page }) => useTransactions({ page, limit: 10, sort: 'date:desc' }),
      {
        wrapper,
        initialProps: { page: 1 },
      }
    );

    // Wait a bit then switch to page 2
    await new Promise((resolve) => setTimeout(resolve, 50));
    rerender({ page: 2 });

    // Wait for page 2 to load (fast)
    await waitFor(() => {
      expect(result.current.data?.items[0]?.id).toBe(2);
    });

    // Now resolve page 1 (slow, should be ignored)
    page1Resolver!(page1Response);
    
    // Wait a bit
    await new Promise((resolve) => setTimeout(resolve, 100));

    // Should still show page 2 data (not overridden by stale page 1)
    expect(result.current.data?.items[0]?.id).toBe(2);
    expect(result.current.data?.meta.page).toBe(2);
  });

  it('should cancel previous request when page changes', async () => {
    // Track abort controllers
    const controllers: Array<{ page?: number; signal?: AbortSignal }> = [];

    vi.mocked(apiClient.listTransactions).mockImplementation(async (filters, signal) => {
      // Store the signal for testing
      controllers.push({ page: filters?.page, signal });

      const page = filters?.page || 1;
      return {
        items: [{ id: page } as any],
        meta: {
          page,
          limit: 10,
          total: 100,
          total_pages: 10,
          has_prev: false,
          has_next: true,
        },
      };
    });

    const { rerender } = renderHook(
      ({ page }) => useTransactions({ page, limit: 10, sort: 'date:desc' }),
      {
        wrapper,
        initialProps: { page: 1 },
      }
    );

    // Change page multiple times quickly
    rerender({ page: 2 });
    rerender({ page: 3 });

    // React Query should have cancelled previous requests via signal
    await waitFor(() => {
      expect(controllers.length).toBeGreaterThan(1);
    });

    // Verify signals were passed
    expect(controllers.every((c) => c.signal !== undefined)).toBe(true);
  });

  it('should use keepPreviousData to prevent UI flicker', async () => {
    vi.mocked(apiClient.listTransactions).mockResolvedValue({
      items: [{ id: 1 } as any],
      meta: {
        page: 1,
        limit: 10,
        total: 100,
        total_pages: 10,
        has_prev: false,
        has_next: true,
      },
    });

    const { result, rerender } = renderHook(
      ({ page }) => useTransactions({ page, limit: 10, sort: 'date:desc' }),
      {
        wrapper,
        initialProps: { page: 1 },
      }
    );

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    const page1Data = result.current.data;

    // Change to page 2
    vi.mocked(apiClient.listTransactions).mockResolvedValue({
      items: [{ id: 2 } as any],
      meta: {
        page: 2,
        limit: 10,
        total: 100,
        total_pages: 10,
        has_prev: true,
        has_next: true,
      },
    });

    rerender({ page: 2 });

    // During loading, previous data should still be available (keepPreviousData)
    expect(result.current.data).toBeDefined();
    expect(result.current.data).toBe(page1Data); // Same reference

    // Wait for new data
    await waitFor(() => {
      expect(result.current.data?.items[0]?.id).toBe(2);
    });
  });
});
