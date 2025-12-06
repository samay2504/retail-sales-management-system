/**
 * Transaction table component
 */
import type { Transaction } from '../types/api';

interface TransactionTableProps {
  transactions: Transaction[];
  isLoading?: boolean;
}

export const TransactionTable = ({
  transactions,
  isLoading = false,
}: TransactionTableProps) => {
  if (isLoading) {
    return (
      <div className="glass-card overflow-hidden">
        <div className="overflow-x-auto -mx-6 px-6 sm:mx-0 sm:px-0">
          <table className="w-full min-w-max">
            <thead className="bg-white/5 border-b border-white/10">
              <tr>
                {['ID', 'Customer', 'Phone', 'Region', 'Category', 'Qty', 'Amount', 'Payment', 'Date'].map(
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
                  {[...Array(9)].map((_, j) => (
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
              <th className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap">
                ID
              </th>
              <th className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap">
                Customer
              </th>
              <th className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap">
                Phone
              </th>
              <th className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap">
                Region
              </th>
              <th className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap">
                Category
              </th>
              <th className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap">
                Qty
              </th>
              <th className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap">
                Amount
              </th>
              <th className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap">
                Payment
              </th>
              <th className="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap">
                Date
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {transactions.map((transaction) => (
              <tr
                key={transaction.id}
                className="hover:bg-white/5 transition-colors cursor-pointer"
              >
                <td className="px-3 sm:px-4 py-3 whitespace-nowrap">
                  <span className="text-sm text-gray-300">#{transaction.id}</span>
                </td>
                <td className="px-3 sm:px-4 py-3">
                  <div className="text-sm min-w-[140px]">
                    <div className="font-medium text-gray-200">{transaction.customer_name}</div>
                    <div className="text-gray-500 text-xs">
                      {transaction.gender}, {transaction.age}y
                    </div>
                  </div>
                </td>
                <td className="px-3 sm:px-4 py-3 whitespace-nowrap">
                  <span className="text-sm text-gray-400">{transaction.phone_number}</span>
                </td>
                <td className="px-3 sm:px-4 py-3 whitespace-nowrap">
                  <span className="badge-primary text-xs">{transaction.customer_region}</span>
                </td>
                <td className="px-3 sm:px-4 py-3 whitespace-nowrap">
                  <span className="text-sm text-gray-300">{transaction.product_category}</span>
                </td>
                <td className="px-3 sm:px-4 py-3 whitespace-nowrap text-center">
                  <span className="text-sm font-medium text-gray-200">{transaction.quantity}</span>
                </td>
                <td className="px-3 sm:px-4 py-3 whitespace-nowrap">
                  <div className="text-sm">
                    <div className="font-medium text-primary">
                      ${transaction.final_amount.toFixed(2)}
                    </div>
                    {transaction.discount_percentage > 0 && (
                      <div className="text-xs text-gray-500 line-through">
                        ${transaction.total_amount.toFixed(2)}
                      </div>
                    )}
                  </div>
                </td>
                <td className="px-3 sm:px-4 py-3 whitespace-nowrap">
                  <span className="badge-cyan text-xs">{transaction.payment_method}</span>
                </td>
                <td className="px-3 sm:px-4 py-3 whitespace-nowrap">
                  <span className="text-sm text-gray-400">
                    {new Date(transaction.date).toLocaleDateString()}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
