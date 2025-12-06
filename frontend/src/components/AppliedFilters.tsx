/**
 * Applied filters component
 */
import type { TransactionFilters } from '../types/api';

interface AppliedFiltersProps {
  filters: TransactionFilters;
  onRemove: (field: keyof TransactionFilters, value?: string) => void;
}

export const AppliedFilters = ({ filters, onRemove }: AppliedFiltersProps) => {
  const filterChips: Array<{ field: keyof TransactionFilters; label: string; value?: string }> =
    [];

  // Add multi-select filters
  if (filters.customer_region) {
    filters.customer_region.forEach((value) => {
      filterChips.push({ field: 'customer_region', label: `Region: ${value}`, value });
    });
  }
  if (filters.gender) {
    filters.gender.forEach((value) => {
      filterChips.push({ field: 'gender', label: `Gender: ${value}`, value });
    });
  }
  if (filters.product_category) {
    filters.product_category.forEach((value) => {
      filterChips.push({ field: 'product_category', label: `Category: ${value}`, value });
    });
  }
  if (filters.tags) {
    filters.tags.forEach((value) => {
      filterChips.push({ field: 'tags', label: `Tag: ${value}`, value });
    });
  }
  if (filters.payment_method) {
    filters.payment_method.forEach((value) => {
      filterChips.push({ field: 'payment_method', label: `Payment: ${value}`, value });
    });
  }

  // Add range filters
  if (filters.age_min !== undefined) {
    filterChips.push({ field: 'age_min', label: `Age min: ${filters.age_min}` });
  }
  if (filters.age_max !== undefined) {
    filterChips.push({ field: 'age_max', label: `Age max: ${filters.age_max}` });
  }
  if (filters.date_from) {
    filterChips.push({ field: 'date_from', label: `From: ${filters.date_from}` });
  }
  if (filters.date_to) {
    filterChips.push({ field: 'date_to', label: `To: ${filters.date_to}` });
  }

  if (filterChips.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-wrap gap-2 items-center">
      <span className="text-sm text-gray-400">Active filters:</span>
      {filterChips.map((chip, index) => (
        <button
          key={`${chip.field}-${chip.value || index}`}
          onClick={() => onRemove(chip.field, chip.value)}
          className="inline-flex items-center space-x-2 px-3 py-1 bg-primary/20 text-primary 
                     border border-primary/30 rounded-full text-xs font-medium 
                     hover:bg-primary/30 transition-colors group"
        >
          <span>{chip.label}</span>
          <svg
            className="w-3 h-3 opacity-70 group-hover:opacity-100"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      ))}
    </div>
  );
};
