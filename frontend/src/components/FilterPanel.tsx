/**
 * Filter panel component
 */
import { memo } from 'react';
import type { FilterMetadata, TransactionFilters } from '../types/api';

interface FilterPanelProps {
  metadata: FilterMetadata;
  filters: TransactionFilters;
  onChange: (filters: TransactionFilters) => void;
  onClear: () => void;
}

export const FilterPanel = memo(({
  metadata,
  filters,
  onChange,
  onClear,
}: FilterPanelProps) => {
  const handleMultiSelectChange = (field: keyof TransactionFilters, value: string) => {
    const currentValues = (filters[field] as string[]) || [];
    const newValues = currentValues.includes(value)
      ? currentValues.filter((v) => v !== value)
      : [...currentValues, value];
    
    onChange({
      ...filters,
      [field]: newValues.length > 0 ? newValues : undefined,
    });
  };

  const handleRangeChange = (field: keyof TransactionFilters, value: string) => {
    onChange({
      ...filters,
      [field]: value ? (field.includes('age') ? parseInt(value) : value) : undefined,
    });
  };

  const activeFilterCount = [
    filters.customer_region?.length || 0,
    filters.customer_type?.length || 0,
    filters.gender?.length || 0,
    filters.product_category?.length || 0,
    filters.brand?.length || 0,
    filters.tags?.length || 0,
    filters.payment_method?.length || 0,
    filters.order_status?.length || 0,
    filters.delivery_type?.length || 0,
    filters.age_min !== undefined ? 1 : 0,
    filters.age_max !== undefined ? 1 : 0,
    filters.date_from ? 1 : 0,
    filters.date_to ? 1 : 0,
  ].reduce((sum, count) => sum + count, 0);

  return (
    <div className="glass-card p-6 space-y-6 h-fit sticky top-24">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-100">Filters</h2>
        {activeFilterCount > 0 && (
          <div className="flex items-center space-x-2">
            <span className="badge-primary">{activeFilterCount} active</span>
            <button
              onClick={onClear}
              className="text-xs text-gray-400 hover:text-primary transition-colors"
            >
              Clear all
            </button>
          </div>
        )}
      </div>

      {/* Region Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Region</h3>
        <div className="space-y-2 max-h-40 overflow-y-auto">
          {metadata.customer_regions.map((option) => (
            <label key={option.value} className="flex items-center space-x-2 cursor-pointer group">
              <input
                type="checkbox"
                className="rounded border-gray-600 bg-white/5 text-primary focus:ring-primary focus:ring-offset-slate-950"
                checked={filters.customer_region?.includes(option.value) || false}
                onChange={() => handleMultiSelectChange('customer_region', option.value)}
              />
              <span className="text-sm text-gray-400 group-hover:text-gray-200 flex-1">
                {option.value}
              </span>
              <span className="text-xs text-gray-500">({option.count})</span>
            </label>
          ))}
        </div>
      </div>

      {/* Customer Type Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Customer Type</h3>
        <div className="space-y-2">
          {metadata.customer_types.map((option) => (
            <label key={option.value} className="flex items-center space-x-2 cursor-pointer group">
              <input
                type="checkbox"
                className="rounded border-gray-600 bg-white/5 text-primary focus:ring-primary focus:ring-offset-slate-950"
                checked={filters.customer_type?.includes(option.value) || false}
                onChange={() => handleMultiSelectChange('customer_type', option.value)}
              />
              <span className="text-sm text-gray-400 group-hover:text-gray-200 flex-1">
                {option.value}
              </span>
              <span className="text-xs text-gray-500">({option.count})</span>
            </label>
          ))}
        </div>
      </div>

      {/* Gender Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Gender</h3>
        <div className="space-y-2">
          {metadata.genders.map((option) => (
            <label key={option.value} className="flex items-center space-x-2 cursor-pointer group">
              <input
                type="checkbox"
                className="rounded border-gray-600 bg-white/5 text-primary focus:ring-primary focus:ring-offset-slate-950"
                checked={filters.gender?.includes(option.value) || false}
                onChange={() => handleMultiSelectChange('gender', option.value)}
              />
              <span className="text-sm text-gray-400 group-hover:text-gray-200 flex-1">
                {option.value}
              </span>
              <span className="text-xs text-gray-500">({option.count})</span>
            </label>
          ))}
        </div>
      </div>

      {/* Category Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Category</h3>
        <div className="space-y-2 max-h-40 overflow-y-auto">
          {metadata.product_categories.map((option) => (
            <label key={option.value} className="flex items-center space-x-2 cursor-pointer group">
              <input
                type="checkbox"
                className="rounded border-gray-600 bg-white/5 text-primary focus:ring-primary focus:ring-offset-slate-950"
                checked={filters.product_category?.includes(option.value) || false}
                onChange={() => handleMultiSelectChange('product_category', option.value)}
              />
              <span className="text-sm text-gray-400 group-hover:text-gray-200 flex-1">
                {option.value}
              </span>
              <span className="text-xs text-gray-500">({option.count})</span>
            </label>
          ))}
        </div>
      </div>

      {/* Brand Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Brand</h3>
        <div className="space-y-2 max-h-40 overflow-y-auto">
          {metadata.brands.map((option) => (
            <label key={option.value} className="flex items-center space-x-2 cursor-pointer group">
              <input
                type="checkbox"
                className="rounded border-gray-600 bg-white/5 text-primary focus:ring-primary focus:ring-offset-slate-950"
                checked={filters.brand?.includes(option.value) || false}
                onChange={() => handleMultiSelectChange('brand', option.value)}
              />
              <span className="text-sm text-gray-400 group-hover:text-gray-200 flex-1">
                {option.value}
              </span>
              <span className="text-xs text-gray-500">({option.count})</span>
            </label>
          ))}
        </div>
      </div>

      {/* Payment Method Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Payment Method</h3>
        <div className="space-y-2">
          {metadata.payment_methods.map((option) => (
            <label key={option.value} className="flex items-center space-x-2 cursor-pointer group">
              <input
                type="checkbox"
                className="rounded border-gray-600 bg-white/5 text-primary focus:ring-primary focus:ring-offset-slate-950"
                checked={filters.payment_method?.includes(option.value) || false}
                onChange={() => handleMultiSelectChange('payment_method', option.value)}
              />
              <span className="text-sm text-gray-400 group-hover:text-gray-200 flex-1">
                {option.value}
              </span>
              <span className="text-xs text-gray-500">({option.count})</span>
            </label>
          ))}
        </div>
      </div>

      {/* Order Status Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Order Status</h3>
        <div className="space-y-2">
          {metadata.order_statuses.map((option) => (
            <label key={option.value} className="flex items-center space-x-2 cursor-pointer group">
              <input
                type="checkbox"
                className="rounded border-gray-600 bg-white/5 text-primary focus:ring-primary focus:ring-offset-slate-950"
                checked={filters.order_status?.includes(option.value) || false}
                onChange={() => handleMultiSelectChange('order_status', option.value)}
              />
              <span className="text-sm text-gray-400 group-hover:text-gray-200 flex-1">
                {option.value}
              </span>
              <span className="text-xs text-gray-500">({option.count})</span>
            </label>
          ))}
        </div>
      </div>

      {/* Delivery Type Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Delivery Type</h3>
        <div className="space-y-2">
          {metadata.delivery_types.map((option) => (
            <label key={option.value} className="flex items-center space-x-2 cursor-pointer group">
              <input
                type="checkbox"
                className="rounded border-gray-600 bg-white/5 text-primary focus:ring-primary focus:ring-offset-slate-950"
                checked={filters.delivery_type?.includes(option.value) || false}
                onChange={() => handleMultiSelectChange('delivery_type', option.value)}
              />
              <span className="text-sm text-gray-400 group-hover:text-gray-200 flex-1">
                {option.value}
              </span>
              <span className="text-xs text-gray-500">({option.count})</span>
            </label>
          ))}
        </div>
      </div>

      {/* Age Range Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Age Range</h3>
        <div className="grid grid-cols-2 gap-2">
          <input
            type="number"
            className="input-field text-sm"
            placeholder={`Min (${metadata.age_range.min})`}
            value={filters.age_min || ''}
            onChange={(e) => handleRangeChange('age_min', e.target.value)}
            min={metadata.age_range.min}
            max={metadata.age_range.max}
          />
          <input
            type="number"
            className="input-field text-sm"
            placeholder={`Max (${metadata.age_range.max})`}
            value={filters.age_max || ''}
            onChange={(e) => handleRangeChange('age_max', e.target.value)}
            min={metadata.age_range.min}
            max={metadata.age_range.max}
          />
        </div>
      </div>

      {/* Date Range Filter */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-300">Date Range</h3>
        <div className="space-y-2">
          <input
            type="date"
            className="input-field text-sm w-full"
            placeholder="From"
            value={filters.date_from || ''}
            onChange={(e) => handleRangeChange('date_from', e.target.value)}
          />
          <input
            type="date"
            className="input-field text-sm w-full"
            placeholder="To"
            value={filters.date_to || ''}
            onChange={(e) => handleRangeChange('date_to', e.target.value)}
          />
        </div>
      </div>
    </div>
  );
});
