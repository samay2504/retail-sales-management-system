/**
 * Sort selector component
 */

interface SortOption {
  value: string;
  label: string;
}

const SORT_OPTIONS: SortOption[] = [
  { value: 'date:desc', label: 'Date (Newest First)' },
  { value: 'date:asc', label: 'Date (Oldest First)' },
  { value: 'quantity:desc', label: 'Quantity (High to Low)' },
  { value: 'quantity:asc', label: 'Quantity (Low to High)' },
  { value: 'customer_name:asc', label: 'Customer Name (A-Z)' },
  { value: 'customer_name:desc', label: 'Customer Name (Z-A)' },
];

interface SortSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

export const SortSelector = ({ value, onChange }: SortSelectorProps) => {
  return (
    <div className="flex items-center space-x-3">
      <label htmlFor="sort" className="text-sm font-medium text-gray-300 whitespace-nowrap">
        Sort by:
      </label>
      <select
        id="sort"
        className="input-field text-sm"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        aria-label="Sort transactions"
      >
        {SORT_OPTIONS.map((option) => (
          <option key={option.value} value={option.value} className="bg-slate-900">
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};
