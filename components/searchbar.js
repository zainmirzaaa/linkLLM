import React, { useState } from 'react';

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

const handleSubmit = (e) => {
  e.preventDefault();
  const cleanQuery = query.trim();
  if (cleanQuery) {
    onSearch(cleanQuery);
    setQuery(""); // reset input after submit
  }
};




  // add a prop so we can customize the placeholder later
<input
  type="text"
  value={query}
  onChange={(e) => setQuery(e.target.value)}
  placeholder={placeholder || "Search..."}
  className="border px-3 py-2 rounded w-full"
/>







  return (
    
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search Stack Overflow..."
        className="border px-3 py-2 rounded w-full"
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Search
      </button>
        <button 
    type="submit" 
    disabled={!query.trim()}
    className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
    >
    Search
    </button>

    </form>
    
    
  );
}

export default function handler(req, res) {
  const { q } = req.query;
  // for now just echo back the query
  res.status(200).json({
    results: [
      { title: "Sample Result", link: "https://stackoverflow.com", snippet: `Query: ${q}` }
    ]
  });
}