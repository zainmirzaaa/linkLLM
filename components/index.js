const [dark, setDark] = useState(false);

return (
  <div className={dark ? "bg-gray-900 text-white min-h-screen" : "bg-white text-black min-h-screen"}>
    <button
      onClick={() => setDark(!dark)}
      className="absolute top-2 right-2 px-3 py-1 border rounded"
    >
      {dark ? "Light Mode" : "Dark Mode"}
    </button>

    {/* rest of your app here */}
  </div>
);