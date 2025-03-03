export default function handler(req, res) {
  try {
    const { q } = req.query;
    if (!q) {
      return res.status(400).json({ error: "Missing query" });
    }
    res.status(200).json({
      results: [
        { title: "Sample Result", link: "https://stackoverflow.com", snippet: `Query: ${q}` }
      ]
    });
  } catch (err) {
    res.status(500).json({ error: "Server error" });
  }
}

res.status(200).json({
  results: [
    { 
      title: "Sample Result", 
      link: "https://stackoverflow.com", 
      snippet: `Query: ${q}` 
    }
  ],
  timestamp: Date.now()
});

let requestCount = 0;

export default async function handler(req, res) {
  requestCount++;
  console.log(`Request #${requestCount} received`);

  // existing code...
}

