import React from "react";

export default function ResultsList({ results, loading }) {
  if (loading) {
    return <p className="text-gray-500 mt-4">Loading results...</p>;
  }

  if (!results || results.length === 0) {
    return <p className="text-gray-500 mt-4">No results found.</p>;
  }

  function highlight(text, query) {
  if (!query) return text;
  const regex = new RegExp(`(${query})`, "gi");
  return text.split(regex).map((part, i) =>
    regex.test(part) ? <mark key={i}>{part}</mark> : part
  );
}

// inside <li> replace snippet line:
<p className="text-sm text-gray-600">
  {highlight(item.snippet, item.query)}
</p>


  return (
    <ul className="mt-4 space-y-2">
      {results.map((item, idx) => (
        <li key={idx} className="p-3 border rounded hover:bg-gray-50">
          <a
            href={item.link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 font-medium"
          >
            {item.title}
          </a>
          <p className="text-sm text-gray-600">{item.snippet}</p>
        </li>
      ))}
    </ul>
  );
}
