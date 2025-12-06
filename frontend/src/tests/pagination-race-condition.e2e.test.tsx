/**
 * E2E test for pagination race condition
 * Verifies that clicking page 2 doesn't snap back to page 1 when responses arrive out of order
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useTransactions } from '../hooks/useApi';
import { apiClient } from '../services/api';
import type { TransactionListResponse } from '../types/api';

// Mock API client
vi.mock('../services/api', () => ({
  apiClient: {
    listTransactions: vi.fn(),
  },
}));

describe('Pagination Race Condition E2E', () => {
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

  it('should not snap back when page 1 response arrives after page 2', async () => {
    // Setup: Create delayed responses
    let resolvePage1: (value: TransactionListResponse) => void;
    const page1Promise = new Promise<TransactionListResponse>((resolve) => {
      resolvePage1 = resolve;
    });

    const page2Response: TransactionListResponse = {
      items: [
        {
          id: 20,
          customer_name: 'Page 2 Customer',
          phone_number: '555-0020',
          customer_region: 'North',
          gender: 'Male',
          age: 30,
          product_category: 'Electronics',
          quantity: 1,
          price_per_unit: 100,
          total_amount: 100,
          discount_percentage: 0,
          final_amount: 100,
          payment_method: 'Cash',
          store_id: 'S001',
          store_location: 'Downtown',
          salesperson_id: 'EMP001',
          employee_name: 'John',
          date: '2024-01-15',
          tags: null,
          created_at: '2024-01-15',
          updated_at: '2024-01-15',
        },
      ],
      meta: {
        page: 2,
        limit: 10,
        total: 100,
        total_pages: 10,
        has_prev: true,
        has_next: true,
      },
    };

    const page1Response: TransactionListResponse = {
      items: [
        {
          id: 1,
          customer_name: 'Page 1 Customer',
          phone_number: '555-0001',
          customer_region: 'North',
          gender: 'Male',
          age: 25,
          product_category: 'Food',
          quantity: 2,
          price_per_unit: 50,
          total_amount: 100,
          discount_percentage: 0,
          final_amount: 100,
          payment_method: 'Card',
          store_id: 'S001',
          store_location: 'Downtown',
          salesperson_id: 'EMP001',
          employee_name: 'Jane',
          date: '2024-01-14',
          tags: null,
          created_at: '2024-01-14',
          updated_at: '2024-01-14',
        },
      ],
      meta: {
        page: 1,
        limit: 10,
        total: 100,
        total_pages: 10,
        has_prev: false,
        has_next: true,
      },
    };

    // Mock: Page 1 is slow, Page 2 is fast
    vi.mocked(apiClient.listTransactions).mockImplementation(async (filters) => {
      if (filters?.page === 1) {
        // Slow response - will arrive after page 2
        return page1Promise;
      } else {
        // Fast response
        await new Promise((resolve) => setTimeout(resolve, 10));
        return page2Response;
      }
    });

    // 1. Start with page 1
    const { result, rerender } = renderHook(
      ({ page }) => useTransactions({ page, limit: 10, sort: 'date:desc' }),
      {
        wrapper,
        initialProps: { page: 1 },
      }
    );

    // 2. Quickly switch to page 2 before page 1 completes
    await new Promise((resolve) => setTimeout(resolve, 20));
    rerender({ page: 2 });

    // 3. Wait for page 2 to load (fast)
    await waitFor(
      () => {
        expect(result.current.data?.meta.page).toBe(2);
      },
      { timeout: 200 }
    );

    const page2Data = result.current.data;
    expect(page2Data?.items[0]?.id).toBe(20);
    expect(page2Data?.items[0]?.customer_name).toBe('Page 2 Customer');

    // 4. Now resolve page 1 (stale response arrives late)
    resolvePage1!(page1Response);

    // 5. Wait to ensure stale response doesn't override
    await new Promise((resolve) => setTimeout(resolve, 100));

    // 6. Verify we're still on page 2 (React Query's built-in signal handling prevents override)
    expect(result.current.data?.meta.page).toBe(2);
    expect(result.current.data?.items[0]?.id).toBe(20);
    expect(result.current.data?.items[0]?.customer_name).toBe('Page 2 Customer');
  });

  it('should use stable query keys to prevent unnecessary refetches', async () => {
    const mockResponse: TransactionListResponse = {
      items: [],
      meta: {
        page: 1,
        limit: 10,
        total: 0,
        total_pages: 0,
        has_prev: false,
        has_next: false,
      },
    };

    vi.mocked(apiClient.listTransactions).mockResolvedValue(mockResponse);

    // Render with same filters but different object reference
    const { rerender } = renderHook(
      ({ filters }) => useTransactions(filters),
      {
        wrapper,
        initialProps: {
          filters: { page: 1, limit: 10, sort: 'date:desc', customer_region: ['North'] },
        },
      }
    );

    await waitFor(() => {
      expect(apiClient.listTransactions).toHaveBeenCalledTimes(1);
    });

    // Re-render with semantically identical filters (different object reference)
    rerender({
      filters: { page: 1, limit: 10, sort: 'date:desc', customer_region: ['North'] },
    });

    // Should not trigger new fetch (stable query key)
    await new Promise((resolve) => setTimeout(resolve, 100));
    expect(apiClient.listTransactions).toHaveBeenCalledTimes(1);
  });
});
