import React from "react";

export default function ResultsList({ results }) {
  if (!results || results.length === 0) {
    return <p className="text-gray-500 mt-4">No results found.</p>;
  }

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
