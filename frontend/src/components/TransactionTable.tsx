/**
 * Transaction table component with dynamic columns
 */
import { useMemo } from 'react';
import type { Transaction } from '../types/api';

interface TransactionTableProps {
  transactions: Transaction[];
  isLoading?: boolean;
}

// Column configuration for display
const COLUMN_CONFIG: Record<string, { label: string; format?: (val: unknown) => string; priority: number }> = {
  transaction_id: { label: 'TXN ID', priority: 1 },
  id: { label: 'ID', priority: 2 },
  customer_id: { label: 'CUST ID', priority: 3 },
  customer_name: { label: 'Customer', priority: 4 },
  phone_number: { label: 'Phone', priority: 5 },
  customer_region: { label: 'Region', priority: 6 },
  customer_type: { label: 'Type', priority: 7 },
  gender: { label: 'Gender', priority: 8 },
  age: { label: 'Age', priority: 9 },
  product_id: { label: 'PROD ID', priority: 10 },
  product_name: { label: 'Product', priority: 11 },
  brand: { label: 'Brand', priority: 12 },
  product_category: { label: 'Category', priority: 13 },
  quantity: { label: 'Qty', priority: 14 },
  price_per_unit: { label: 'Unit Price', format: (v) => `$${(v as number).toFixed(2)}`, priority: 15 },
  discount_percentage: { label: 'Discount %', format: (v) => `${v}%`, priority: 16 },
  final_amount: { label: 'Amount', format: (v) => `$${(v as number).toFixed(2)}`, priority: 17 },
  payment_method: { label: 'Payment', priority: 18 },
  order_status: { label: 'Status', priority: 19 },
  delivery_type: { label: 'Delivery', priority: 20 },
  date: { label: 'Date', format: (v) => new Date(v as string).toLocaleDateString(), priority: 21 },
  store_location: { label: 'Store', priority: 22 },
};

export const TransactionTable = ({
  transactions,
  isLoading = false,
}: TransactionTableProps) => {
  // Extract columns dynamically from first transaction
  const columns = useMemo(() => {
    if (transactions.length === 0) return [];
    const firstRow = transactions[0];
    return Object.keys(firstRow)
      .filter(key => COLUMN_CONFIG[key] && !['created_at', 'updated_at', 'tags', 'total_amount', 'store_id', 'salesperson_id', 'employee_name'].includes(key))
      .sort((a, b) => COLUMN_CONFIG[a].priority - COLUMN_CONFIG[b].priority)
      .slice(0, 15); // Show top 15 most important columns
  }, [transactions]);

  if (isLoading) {
    return (
      <div className="glass-card overflow-hidden">
        <div className="overflow-x-auto -mx-6 px-6 sm:mx-0 sm:px-0">
          <table className="w-full min-w-max">
            <thead className="bg-white/5 border-b border-white/10">
              <tr>
                {['TXN ID', 'ID', 'CUST ID', 'Customer', 'Phone', 'Region', 'Type', 'PROD ID', 'Product', 'Brand', 'Category', 'Qty', 'Amount', 'Payment', 'Date'].map(
                  (header) => (
                    <th
                      key={header}
                      className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap"
                    >
                      {header}
                    </th>
                  )
                )}
              </tr>
            </thead>
            <tbody>
              {[...Array(5)].map((_, i) => (
                <tr key={i} className="border-b border-white/5">
                  {[...Array(15)].map((_, j) => (
                    <td key={j} className="px-3 sm:px-4 py-3">
                      <div className="skeleton h-4 w-20 rounded"></div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  if (transactions.length === 0) {
    return (
      <div className="glass-card p-12 text-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center">
            <svg
              className="w-8 h-8 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-medium text-gray-300">No transactions found</h3>
            <p className="text-sm text-gray-500">Try adjusting your search or filters</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card overflow-hidden">
      <div className="overflow-x-auto -mx-6 px-6 sm:mx-0 sm:px-0">
        <table className="w-full min-w-max">
          <thead className="bg-white/5 border-b border-white/10">
            <tr>
              {columns.map((col) => (
                <th
                  key={col}
                  className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap"
                >
                  {COLUMN_CONFIG[col]?.label || col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {transactions.map((transaction) => (
              <tr
                key={transaction.id}
                className="hover:bg-white/5 transition-colors cursor-pointer"
              >
                {columns.map((col) => {
                  const value = transaction[col as keyof Transaction];
                  const formatter = COLUMN_CONFIG[col]?.format;
                  const displayValue = formatter && value !== null && value !== undefined
                    ? formatter(value)
                    : String(value || '-');

                  // Special styling for specific columns
                  const cellClass = 'px-3 sm:px-4 py-3 whitespace-nowrap text-sm';
                  let contentClass = 'text-gray-300';

                  if (col === 'transaction_id' || col === 'id' || col === 'customer_id' || col === 'product_id') {
                    contentClass = 'text-primary font-mono text-xs';
                  } else if (col === 'final_amount' || col === 'price_per_unit') {
                    contentClass = 'text-primary font-semibold';
                  } else if (col === 'customer_region' || col === 'customer_type' || col === 'payment_method' || col === 'order_status' || col === 'delivery_type') {
                    contentClass = 'badge-primary text-xs inline-block';
                  } else if (col === 'customer_name' || col === 'product_name') {
                    contentClass = 'text-gray-200 font-medium';
                  } else if (col === 'brand') {
                    contentClass = 'text-cyan-400';
                  }

                  return (
                    <td key={col} className={cellClass}>
                      <span className={contentClass}>
                        {displayValue}
                      </span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
