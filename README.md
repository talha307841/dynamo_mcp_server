# Dynamo MCP 🚀

<p align="center">
  <img src="assets/logo.png" alt="Dynamo MCP Logo" width="200"/>
</p>

<p align="center">
  <b>The Self-Extending MCP Server</b><br/>
  One MCP server to build them all ⚡
</p>

---

## 🌟 Why Dynamo MCP?

Most MCP servers are **static**: you code tools once, deploy, and that’s it.  
**Dynamo MCP is different** — it’s the **world’s first self-extending MCP server**.  

- 🧠 **LLM-powered tool generation** → Missing a tool? Dynamo asks an LLM to create one.  
- 📂 **Persistent registry** → Every generated tool is saved & reusable forever.  
- 🔌 **Plug-and-play for AIs** → Any AI (Claude, GPT, local models) can request tools.  
- 🛡️ **Sandbox-ready** → Tools run in safe environments.  
- 🌍 **Global utility hub** → From time zones to PDF generation — one server, infinite growth.  

---

## 📊 System Architecture

```mermaid
graph TD
    A[AI Client] -->|Request Tool| B[Dynamo MCP Server]
    B -->|Check| C[Tool Registry]
    C -->|Exists| D[Return Tool]
    C -->|Missing| E[LLM Generator]
    E -->|Generate| F[Dynamic Loader]
    F -->|Register| C
    D -->|Execute| G[Result Back to Client]


sequenceDiagram
    participant AI as AI Client
    participant D as Dynamo MCP
    participant R as Tool Registry
    participant L as LLM Generator

    AI->>D: Request "time_in_timezone"
    D->>R: Check tool
    R-->>D: Tool Found
    D-->>AI: Return result ✅

    AI->>D: Request "text_to_pdf"
    D->>R: Check tool
    R-->>D: Not Found ❌
    D->>L: Generate tool
    L-->>D: Returns code
    D->>R: Save + Register tool
    D-->>AI: Return result ✅



Quick Start
1️⃣ Clone the repo
git clone https://github.com/yourname/dynamo-mcp.git
cd dynamo-mcp

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the server
python main.py



4️⃣ Connect to your AI

Claude Desktop → add dynamo-mcp in config

OpenAI client → use MCP stdio transport

Or call the HTTP endpoint directly

⚙️ Example Usage

AI asks:

"What’s the time in Tokyo?"

✔️ Dynamo finds time_in_timezone → returns instantly.

AI asks:

"Convert this text into a PDF."

❌ Tool not found →
⚡ Dynamo generates text_to_pdf with an LLM, saves it, and returns the PDF.
✔️ Next time → tool is already available.

📈 Roadmap

 Core MCP server

 Persistent registry of tools

 Sandbox execution (Docker/WASM isolation)

 Web dashboard with tool marketplace

 Tool versioning + rollback

 Global “Dynamo Hub” for shared tools

🤝 Contributing

We welcome your PRs! 🚀 Build new core features, improve security, or design amazing logos/UX.

Fork it

Create feature branch (git checkout -b feature/awesome)

Commit (git commit -m "Add awesome feature")

Push & PR

📜 License

MIT License © 2025 Talha Yousaf

💡 Tagline

Dynamo MCP — The last MCP server you’ll ever need.


---

Now for the **logo** 🎨:  
Do you want me to generate a **techy neon-style AI logo** or a **minimal clean flat logo** for Dynamo MCP?
