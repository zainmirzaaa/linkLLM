import React, { useState } from 'react';

export default function SearchBar({ onSearch, placeholder }) {
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const cleanQuery = query.trim();
    if (!cleanQuery) {
      setError("Please enter a search term.");
      return;
    }
    setError("");
    onSearch(cleanQuery);
    setQuery(""); // reset input after submit
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2">
      <div className="flex gap-2">
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
      </div>
      {error && <p className="text-red-500 text-sm">{error}</p>}
    </form>
  );
}
