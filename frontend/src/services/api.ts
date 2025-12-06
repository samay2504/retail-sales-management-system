/**
 * API client for TruEstate backend
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  Transaction,
  TransactionListResponse,
  FilterMetadata,
  TransactionFilters,
  HealthResponse,
} from '../types/api';

// Determine API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://retail-sales-management-system-96ml.onrender.com';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 45000, // Increased to 45 seconds for large datasets
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      // Enable HTTP/2 multiplexing if available
      maxRedirects: 5,
      // Connection pooling hints
      transitional: {
        clarifyTimeoutError: true,
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add request ID
        config.headers['X-Request-ID'] = this.generateRequestId();
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        // Handle errors
        if (error.response) {
          // Server responded with error
          console.error('API Error:', error.response.status, error.response.data);
        } else if (error.request) {
          // Request made but no response
          console.error('Network Error:', error.message);
        } else {
          // Something else happened
          console.error('Error:', error.message);
        }
        return Promise.reject(error);
      }
    );
  }

  private generateRequestId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Build query string from filters
   */
  private buildQueryString(filters: TransactionFilters): string {
    const params = new URLSearchParams();

    // Add search query
    if (filters.q) {
      params.append('q', filters.q);
    }

    // Add pagination
    if (filters.page) {
      params.append('page', filters.page.toString());
    }
    if (filters.limit) {
      params.append('limit', filters.limit.toString());
    }

    // Add sorting
    if (filters.sort) {
      params.append('sort', filters.sort);
    }

    // Add multi-select filters
    if (filters.customer_region) {
      filters.customer_region.forEach((region) => {
        params.append('customer_region', region);
      });
    }
    if (filters.gender) {
      filters.gender.forEach((gender) => {
        params.append('gender', gender);
      });
    }
    if (filters.product_category) {
      filters.product_category.forEach((category) => {
        params.append('product_category', category);
      });
    }
    if (filters.tags) {
      filters.tags.forEach((tag) => {
        params.append('tags', tag);
      });
    }
    if (filters.payment_method) {
      filters.payment_method.forEach((method) => {
        params.append('payment_method', method);
      });
    }

    // Add range filters
    if (filters.age_min !== undefined) {
      params.append('age_min', filters.age_min.toString());
    }
    if (filters.age_max !== undefined) {
      params.append('age_max', filters.age_max.toString());
    }
    if (filters.date_from) {
      params.append('date_from', filters.date_from);
    }
    if (filters.date_to) {
      params.append('date_to', filters.date_to);
    }

    return params.toString();
  }

  /**
   * List transactions with filters and request cancellation support
   */
  async listTransactions(
    filters: TransactionFilters = {},
    signal?: AbortSignal
  ): Promise<TransactionListResponse> {
    const requestId = this.generateRequestId();
    const queryString = this.buildQueryString(filters);
    const url = `/api/transactions${queryString ? `?${queryString}` : ''}`;
    
    // Log request start (dev only)
    if (import.meta.env.DEV) {
      console.log(`[API:${requestId}] GET ${url}`, {
        page: filters.page,
        filters: Object.keys(filters).filter(k => !['page', 'limit', 'sort'].includes(k)),
        timestamp: new Date().toISOString(),
      });
    }
    
    const startTime = performance.now();
    
    try {
      const response = await this.client.get<TransactionListResponse>(url, { signal });
      
      // Log request success (dev only)
      if (import.meta.env.DEV) {
        const duration = performance.now() - startTime;
        console.log(`[API:${requestId}] Success (${duration.toFixed(0)}ms)`, {
          total: response.data.meta.total,
          items: response.data.items.length,
        });
      }
      
      return response.data;
    } catch (error) {
      // Log request error (dev only)
      if (import.meta.env.DEV) {
        const duration = performance.now() - startTime;
        if (axios.isCancel(error)) {
          console.log(`[API:${requestId}] Cancelled (${duration.toFixed(0)}ms)`);
        } else {
          console.error(`[API:${requestId}] Error (${duration.toFixed(0)}ms)`, error);
        }
      }
      throw error;
    }
  }

  /**
   * Get a single transaction by ID
   */
  async getTransaction(id: number): Promise<Transaction> {
    const response = await this.client.get<Transaction>(`/api/transactions/${id}`);
    return response.data;
  }

  /**
   * Get filter metadata
   */
  async getFilterMetadata(): Promise<FilterMetadata> {
    const response = await this.client.get<FilterMetadata>('/api/meta/filters');
    return response.data;
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/api/health');
    return response.data;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
