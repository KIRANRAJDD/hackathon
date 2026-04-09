const { useState, useEffect } = React;

const SPINNER = (
  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
);

function Login({ navigate }) {
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      navigate("dashboard");
    }, 1200);
  };

  return (
    <div className="flex justify-center items-center min-h-screen p-6">
      <div className="w-full max-w-[420px] p-10 flex flex-col gap-6 text-center bg-panel backdrop-blur-xl border border-border rounded-2xl shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)]">
        <div className="text-3xl font-semibold tracking-tight">
          <span className="inline-block animate-pulse">✨</span> AutoTest<span className="text-accent">AI</span>
        </div>
        <p className="text-gray-400 text-sm mb-4">Welcome back! Please login to your account.</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input type="email" placeholder="Email Address" required className="bg-[#1A1F29] text-[#EEF2F6] border border-border p-4 rounded-xl outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20 w-full" />
          <input type="password" placeholder="Password" required className="bg-[#1A1F29] text-[#EEF2F6] border border-border p-4 rounded-xl outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20 w-full" />
          
          <button type="submit" disabled={loading} className="mt-2 w-full p-4 rounded-xl border-none bg-gradient-to-br from-accent to-[#4a148c] text-white font-semibold flex justify-center items-center hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(124,77,255,0.4)] transition-all">
            {loading ? SPINNER : "Sign In"}
          </button>
        </form>

        <div className="mt-6 text-gray-400 text-sm">
          Don't have an account? <span onClick={() => navigate("register")} className="text-accent font-medium cursor-pointer hover:text-[#b388ff] transition">Create one</span>
        </div>
      </div>
    </div>
  );
}

function Register({ navigate }) {
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      navigate("dashboard");
    }, 1200);
  };

  return (
    <div className="flex justify-center items-center min-h-screen p-6">
      <div className="w-full max-w-[420px] p-10 flex flex-col gap-6 text-center bg-panel backdrop-blur-xl border border-border rounded-2xl shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)]">
        <div className="text-3xl font-semibold tracking-tight">
          <span className="inline-block animate-pulse">✨</span> AutoTest<span className="text-accent">AI</span>
        </div>
        <p className="text-gray-400 text-sm mb-4">Create a new account.</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input type="text" placeholder="Full Name" required className="bg-[#1A1F29] text-[#EEF2F6] border border-border p-4 rounded-xl outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20 w-full" />
          <input type="email" placeholder="Email Address" required className="bg-[#1A1F29] text-[#EEF2F6] border border-border p-4 rounded-xl outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20 w-full" />
          <input type="password" placeholder="Password" required className="bg-[#1A1F29] text-[#EEF2F6] border border-border p-4 rounded-xl outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20 w-full" />
          
          <button type="submit" disabled={loading} className="mt-2 w-full p-4 rounded-xl border-none bg-gradient-to-br from-accent to-[#4a148c] text-white font-semibold flex justify-center items-center hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(124,77,255,0.4)] transition-all">
            {loading ? SPINNER : "Sign Up"}
          </button>
        </form>

        <div className="mt-6 text-gray-400 text-sm">
          Already have an account? <span onClick={() => navigate("login")} className="text-accent font-medium cursor-pointer hover:text-[#b388ff] transition">Sign In</span>
        </div>
      </div>
    </div>
  );
}

function Dashboard({ navigate }) {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [activeTab, setActiveTab] = useState("summary");

  const handleGenerate = async () => {
    if (!code.trim()) {
      alert("Please paste some code first!");
      return;
    }
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language })
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Failed to generate tests");
      }

      const data = await response.json();
      setResults(data.results);
      setActiveTab("summary");
    } catch (error) {
      alert("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const target = e.target;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      target.value = target.value.substring(0, start) + "    " + target.value.substring(end);
      target.selectionStart = target.selectionEnd = start + 4;
      setCode(target.value);
    }
  };

  return (
    <div className="flex flex-col h-screen p-6 gap-6 max-w-[1600px] mx-auto">
      <header className="flex items-baseline justify-between p-4 px-8 bg-panel backdrop-blur-xl border border-border rounded-2xl">
        <div className="flex items-baseline gap-4">
          <div className="text-2xl font-semibold tracking-tight">
            <span className="inline-block animate-pulse">✨</span> AutoTest<span className="text-accent">AI</span>
          </div>
          <p className="text-gray-400 text-sm">Intelligent Test Suite Generation <span className="ml-2 px-2 py-0.5 bg-accent/20 text-accent rounded-full text-xs font-mono">REACT</span></p>
        </div>
        <button onClick={() => navigate("login")} className="text-sm text-gray-400 hover:text-white transition">Sign Out</button>
      </header>

      <main className="flex flex-1 gap-6 min-h-0">
        {/* Left Panel */}
        <section className="flex-1 flex flex-col bg-panel backdrop-blur-xl border border-border rounded-2xl overflow-hidden group hover:border-white/20 transition duration-300">
          <div className="flex justify-between items-center p-4 px-6 border-b border-border">
            <h2 className="text-lg font-medium">Input Source Code</h2>
            <select value={language} onChange={(e) => setLanguage(e.target.value)} className="bg-[#1A1F29] text-white border border-border px-4 py-2 rounded-lg outline-none cursor-pointer">
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="java">Java</option>
              <option value="go">Go</option>
            </select>
          </div>
          <textarea 
            value={code} 
            onChange={(e) => setCode(e.target.value)} 
            onKeyDown={handleKeyDown}
            placeholder="Paste your source code here..." 
            className="flex-1 bg-[#1A1F29] text-[#A9B7C6] font-mono text-sm p-6 resize-none outline-none"
          ></textarea>
          <button 
            onClick={handleGenerate} 
            disabled={loading}
            className="m-6 mt-0 p-4 rounded-xl border-none bg-gradient-to-br from-accent to-[#4a148c] text-white font-semibold flex justify-center items-center hover:-translate-y-0.5 hover:shadow-[0_8px_20px_rgba(124,77,255,0.4)] transition-all disabled:opacity-50 disabled:transform-none"
          >
            {loading ? SPINNER : "Generate Test Suite"}
          </button>
        </section>

        {/* Right Panel */}
        <section className="flex-1 flex flex-col bg-panel backdrop-blur-xl border border-border rounded-2xl overflow-hidden group hover:border-white/20 transition duration-300">
          <div className="flex justify-between items-center p-4 px-6 border-b border-border">
            <h2 className="text-lg font-medium">Generated Tests</h2>
          </div>
          
          {!results ? (
            <div className="flex flex-col flex-1 items-center justify-center text-gray-400 text-center">
              <div className="w-16 h-16 rounded-full bg-accent/20 flex items-center justify-center mb-6 animate-pulse shadow-[0_0_30px_rgba(124,77,255,0.3)]">
                <span className="text-accent text-3xl">✨</span>
              </div>
              <h3 className="text-white text-xl font-medium mb-2">Ready to analyze.</h3>
              <p>Paste code on the left and hit generate.</p>
            </div>
          ) : (
             <div className="flex flex-col flex-1 min-h-0">
              <div className="flex border-b border-border bg-black/20">
                {['summary', 'unit', 'integration', 'edge'].map(tab => (
                  <button 
                    key={tab} 
                    onClick={() => setActiveTab(tab)}
                    className={`flex-1 p-4 font-medium capitalize border-b-2 transition ${activeTab === tab ? 'text-accent border-accent bg-accent/5' : 'text-gray-400 border-transparent hover:text-white'}`}
                  >
                    {tab === 'unit' ? 'Unit Tests' : tab === 'edge' ? 'Edge Cases' : tab}
                  </button>
                ))}
              </div>

              <div className="flex-1 overflow-y-auto">
                {activeTab === 'summary' && (
                  <div className="p-6">
                    <h3 className="text-accent font-medium mb-2">Code Analysis</h3>
                    <div className="p-6 text-gray-300 leading-relaxed border-b border-border mb-6">
                      <p>{results.summary}</p>
                    </div>
                    <h3 className="text-accent font-medium mb-4">Identified Scenarios</h3>
                    <ul className="list-disc pl-8 text-gray-300 leading-loose">
                      {(results.scenarios || []).map((sc, i) => <li key={i}>{sc}</li>)}
                    </ul>
                  </div>
                )}
                {activeTab === 'unit' && (
                  <div className="flex flex-col h-full">
                    <div className="bg-[#11151c] px-4 py-2 text-xs font-mono text-gray-400 border-b border-border">test_unit.py</div>
                    <pre className="p-6 font-mono text-sm text-[#A9B7C6] bg-[#1A1F29] flex-1 outline-none">{results.unit_tests || 'No unit tests generated.'}</pre>
                  </div>
                )}
                {activeTab === 'integration' && (
                  <div className="flex flex-col h-full">
                    <div className="bg-[#11151c] px-4 py-2 text-xs font-mono text-gray-400 border-b border-border">test_integration.py</div>
                    <pre className="p-6 font-mono text-sm text-[#A9B7C6] bg-[#1A1F29] flex-1 outline-none">{results.integration_tests || 'No integration tests generated.'}</pre>
                  </div>
                )}
                {activeTab === 'edge' && (
                  <div className="flex flex-col h-full">
                    <div className="bg-[#11151c] px-4 py-2 text-xs font-mono text-gray-400 border-b border-border">test_edge_cases.py</div>
                    <pre className="p-6 font-mono text-sm text-[#A9B7C6] bg-[#1A1F29] flex-1 outline-none">{results.edge_cases || 'No edge cases generated.'}</pre>
                  </div>
                )}
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

function App() {
  const [route, setRoute] = useState("login");

  if (route === "login") return <Login navigate={setRoute} />;
  if (route === "register") return <Register navigate={setRoute} />;
  if (route === "dashboard") return <Dashboard navigate={setRoute} />;
  return null;
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
