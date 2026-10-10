# CortexKG

CortexKG is a local-first Streamlit application that turns conversations into a persistent, explorable knowledge graph. It extracts entities and relationships from chat, stores the graph as portable JSON, and can inject graph context into later conversations.

## Supported providers

- Ollama
- OpenAI
- Google Gemini
- OpenAI-compatible endpoints such as OpenRouter, LM Studio, vLLM, and ArvanCloud

## Quick start

A new developer can run the application in under 15 minutes.

```bash
git clone https://github.com/massoudsh/CortexKG.git
cd CortexKG
python3.12 -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
python -m pip install --requirement requirements.txt
python main.py
```

Open the address shown by Streamlit. Select a provider in **Settings**, enter its model configuration and API key, then begin chatting. To explore the UI without model credentials, select **Load Sample Knowledge Graph** under **Graph Memory**.

Use the pinned Python version in `.python-version`. Runtime configuration is created locally as `app_config.json`; use `.env.example` only as a reference for non-secret deployment paths. Do not commit API keys, generated configuration, or graph exports.

## How it works

1. The user sends a chat message to the selected provider.
2. CortexKG optionally adds the current graph as context.
3. The response and/or user input are converted into structured entities and relationships.
4. The graph is saved locally and rendered interactively.
5. The graph can be exported as JSON and imported later.

See [Architecture](docs/ARCHITECTURE.md) for the data flow and component map.

## Testing

```bash
python -m unittest discover -v
node --test CortexKG/graph.test.js
```

Pull requests and updates to `main` run dependency installation, Python compilation, both test suites, CodeQL analysis, and secret scanning in GitHub Actions. Dependabot checks Python and GitHub Actions dependencies weekly.

## Security and AI evaluation

Read [Security notes and threat model](docs/SECURITY.md) before using CortexKG with sensitive conversations. Provider keys and graph data are local files; protect the device and storage where they reside.

Entity and relationship extraction is probabilistic. Review important facts and links before using the graph for operational, legal, security, financial, or personnel decisions.

## License

MIT
