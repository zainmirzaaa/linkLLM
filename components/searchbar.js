import React, { useState, useEffect } from 'react';

export default function SearchBar({ onSearch, placeholder, loading = false }) {
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const [minScore, setMinScore] = useState(0);
  const [limit, setLimit] = useState(10);

  const handleSubmit = (e) => {
    e.preventDefault();
    const cleanQuery = query.trim();
    if (!cleanQuery) return setError("Please enter a search term.");
    setError("");
    onSearch({ q: cleanQuery, minScore, limit });
    setQuery("");
  };

  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'Escape') setQuery('');
      if (e.key === 'Enter' && document.activeElement === document.body) {
        const clean = query.trim();
        if (clean) onSearch({ q: clean, minScore, limit });
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [query, minScore, limit, onSearch]);

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2">
      <div className="flex gap-2 items-center">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder || "Search Stack Overflow..."}
          className="border px-3 py-2 rounded w-full"
        />
        <button
          type="submit"
          disabled={!query.trim()}
          className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          Search
        </button>
        <button
          type="button"
          onClick={() => setQuery("")}
          className="bg-gray-300 text-black px-3 py-2 rounded"
        >
          Clear
        </button>
        {loading && <span className="text-sm text-gray-500">Loading...</span>}
      </div>

      <div className="flex gap-3 items-center text-sm text-gray-600">
        <label className="flex items-center gap-2">
          Min score
          <input
            type="number"
            value={minScore}
            min={0}
            max={100}
            onChange={(e) => setMinScore(Number(e.target.value))}
            className="w-16 border rounded px-2 py-1"
          />
        </label>
        <label className="flex items-center gap-2">
          Max results
          <input
            type="number"
            value={limit}
            min={1}
            max={50}
            onChange={(e) => setLimit(Number(e.target.value))}
            className="w-16 border rounded px-2 py-1"
          />
        </label>
      </div>

      {error && <p className="text-red-500 text-sm">{error}</p>}
    </form>
  );
}
