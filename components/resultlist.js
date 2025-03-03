import React from "react";

export default function ResultsList({ results, loading }) {
    if (loading) return <p>Loading results...</p>;
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

function estimateTime(text) {
  const words = text.split(/\s+/).length;
  const minutes = Math.max(1, Math.ceil(words / 200));
  return `${minutes} min read`;
}

// inside list item
<p className="text-xs text-gray-400">
  {estimateTime(item.snippet)}
</p>
}









// inside <li> replace snippet line:
<p className="text-sm text-gray-600">
  {highlight(item.snippet, item.query)}
</p>

  if (loading) return <p className="text-gray-500 mt-4">Loading results...</p>;
  if (!results || results.length === 0) return <p className="text-gray-500 mt-4">No results found.</p>;
  
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
        <li key={idx} className="p-3 border rounded hover:bg-gray-50">
    <span className="mr-2 text-gray-500">#{idx + 1}</span>
    <a href={item.link} target="_blank" rel="noopener noreferrer"
        className="text-blue-600 font-medium">
        {item.title}
    </a>
    <p className="text-sm text-gray-600">{item.snippet}</p>
    </li>
    {results.length > 0 && (
    <button
        onClick={() => results.forEach(r => window.open(r.link, "_blank"))}
        className="mb-2 bg-green-500 text-white px-3 py-1 rounded"
    >
        Open All
    </button>
    )}

      <button
  onClick={() => navigator.clipboard.writeText(item.link)}
  className="ml-2 text-xs text-blue-500 underline"
>
  Copy Link
</button>

    </ul>
  );
}
