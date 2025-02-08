export default function handler(req, res) {
  const { q } = req.query;
  // for now just echo back the query
  res.status(200).json({
    results: [
      { 
        title: "Sample Result", 
        link: "https://stackoverflow.com", 
        snippet: `Query: ${q}` 
      }
    ]
  });
}
