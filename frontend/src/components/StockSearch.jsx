import React, { useState } from "react";

const StockSearch = () => {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const fetchStockPrice = async () => {
    if (!query) {
      setError("Please enter a company name or stock symbol!");
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/market/live/?query=${query}`);
      const data = await response.json();

      if (response.ok) {
        setResult(data);
        setError("");
      } else {
        setError(data.error || "Failed to fetch stock price.");
      }
    } catch (err) {
      setError("Error fetching stock price.");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-lg font-bold">Search Stock Prices</h2>
      <input
        type="text"
        placeholder="Enter company name or stock symbol"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="border p-2 rounded"
      />
      <button onClick={fetchStockPrice} className="ml-2 bg-blue-500 text-white p-2 rounded">
        Get Price
      </button>

      {result && (
        <div className="mt-4">
          <p><strong>Company:</strong> {result.company}</p>
          <p><strong>Stock Symbol:</strong> {result.symbol}</p>
          <p><strong>Price:</strong> ${result.price}</p>
          <p><strong>Source:</strong> {result.source}</p>
        </div>
      )}

      {error && <p className="mt-2 text-red-500">{error}</p>}
    </div>
  );
};

export default StockSearch;
