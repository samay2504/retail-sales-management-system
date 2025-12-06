/**
 * Type definitions for TruEstate API
 */

export interface Transaction {
  id: number;
  customer_name: string;
  phone_number: string;
  customer_region: string;
  gender: string;
  age: number;
  date: string;
  quantity: number;
  price_per_unit: number;
  discount_percentage: number;
  total_amount: number;
  final_amount: number;
  product_category: string;
  tags: string | null;
  payment_method: string;
  store_id: string;
  store_location: string;
  salesperson_id: string;
  employee_name: string;
  created_at?: string;
  updated_at?: string;
}

export interface PaginationMeta {
  total: number;
  page: number;
  limit: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface TransactionListResponse {
  items: Transaction[];
  meta: PaginationMeta;
}

export interface FilterOption {
  value: string;
  count: number;
}

export interface FilterMetadata {
  customer_regions: FilterOption[];
  genders: FilterOption[];
  product_categories: FilterOption[];
  tags: FilterOption[];
  payment_methods: FilterOption[];
  age_range: {
    min: number;
    max: number;
  };
  date_range: {
    min: string | null;
    max: string | null;
  };
}

export interface TransactionFilters {
  q?: string;
  page?: number;
  limit?: number;
  sort?: string;
  customer_region?: string[];
  gender?: string[];
  product_category?: string[];
  tags?: string[];
  payment_method?: string[];
  age_min?: number;
  age_max?: number;
  date_from?: string;
  date_to?: string;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}
