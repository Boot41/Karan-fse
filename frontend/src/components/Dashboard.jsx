import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();

  // Dummy data for demonstration
  const [portfolio, setPortfolio] = useState({
    stocks: [
      { symbol: 'AAPL', name: 'Apple Inc.', quantity: 10, purchasePrice: 150, currentPrice: 175 },
      { symbol: 'GOOGL', name: 'Alphabet Inc.', quantity: 5, purchasePrice: 2800, currentPrice: 2950 },
      { symbol: 'MSFT', name: 'Microsoft Corp.', quantity: 15, purchasePrice: 280, currentPrice: 310 },
      { symbol: 'AMZN', name: 'Amazon.com Inc.', quantity: 8, purchasePrice: 3200, currentPrice: 3400 },
    ],
    pieData: [
      { name: 'Technology', value: 45 },
      { name: 'Healthcare', value: 25 },
      { name: 'Finance', value: 20 },
      { name: 'Consumer', value: 10 },
    ],
    trendData: [
      { date: '2025-02-01', value: 150 },
      { date: '2025-02-02', value: 155 },
      { date: '2025-02-03', value: 160 },
      { date: '2025-02-04', value: 158 },
      { date: '2025-02-05', value: 165 },
      { date: '2025-02-06', value: 170 },
      { date: '2025-02-07', value: 175 },
    ],
  });

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="space-y-6">
      {/* Navigation Bar */}
      <div className="flex justify-between items-center bg-gray-800 p-4 rounded-lg shadow-md mb-6">
        <h1 className="text-3xl font-bold text-white">Investment Portfolio</h1>
        <div className="flex space-x-4">
          <button 
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-transform transform hover:scale-105"
            onClick={() => navigate('/dashboard')} // Navigate to the Dashboard page
          >
            Dashboard
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Portfolio Allocation */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Portfolio Allocation</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={portfolio.pieData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {portfolio.pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Holdings Overview */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Holdings Overview</h2>
          <div className="space-y-4">
            {portfolio.stocks.map((stock) => {
              const totalValue = stock.quantity * stock.currentPrice;
              const profit = (stock.currentPrice - stock.purchasePrice) * stock.quantity;
              const profitPercentage = ((stock.currentPrice - stock.purchasePrice) / stock.purchasePrice) * 100;
              
              return (
                <div key={stock.symbol} className="border-b pb-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold">{stock.name}</h3>
                      <p className="text-sm text-gray-500">{stock.symbol}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold">${totalValue.toLocaleString()}</p>
                      <div className={`flex items-center ${profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {profit >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                        <span className="ml-1">{profitPercentage.toFixed(2)}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Recent Transactions */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Recent Transactions</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {/* Example Transaction Rows */}
              <tr className="hover:bg-gray-100">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2024-03-15</td>
                <td className="px-6 py-4 whitespace-nowrap">AAPL</td>
                <td className="px-6 py-4 whitespace-nowrap text-green-600 font-semibold">Buy</td>
                <td className="px-6 py-4 whitespace-nowrap">10</td>
                <td className="px-6 py-4 whitespace-nowrap">$1750</td>
              </tr>
              <tr className="hover:bg-gray-100">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2024-03-16</td>
                <td className="px-6 py-4 whitespace-nowrap">GOOGL</td>
                <td className="px-6 py-4 whitespace-nowrap text-red-600 font-semibold">Sell</td>
                <td className="px-6 py-4 whitespace-nowrap">5</td>
                <td className="px-6 py-4 whitespace-nowrap">$14750</td>
              </tr>
              {/* Add more rows here */}
            </tbody>
          </table>
        </div>
      </div>

      {/* Trend Analysis */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Trend Analysis of Your Stocks</h2>
        <p>This graph shows the trend of your stock values over the past week:</p>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={portfolio.trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
