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
