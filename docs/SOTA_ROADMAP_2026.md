# SOTA platform hardening (2026 Q4)

GitHub Issues are disabled on this repository; use this checklist for portfolio tracking.

## Knowledge graph memory

- Eval harness: entity/relation extraction quality on fixed conversation sets
- Version graph snapshots; migration path for schema changes
- PII redaction before persistence; user-owned export/delete (GDPR-style)
- Optional: embed + hybrid retrieval benchmark vs flat vector RAG

## Engineering

- CI: import smoke + compile (see `.github/workflows/ci.yml`)
- Pin LangChain/provider versions; document Ollama vs cloud paths
- Observability: trace ingest → extract → graph write → query
