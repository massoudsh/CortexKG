# Security notes and threat model

## Assets

- Provider API keys configured in the local application settings.
- Chat messages and derived knowledge-graph data.
- Exported and imported graph JSON files.

## Trust boundaries

- The browser/Streamlit UI is trusted only for the local user running the application.
- LLM providers receive the messages submitted for completion and, when enabled, graph context.
- Imported JSON files are external input and can contain untrusted text.

## Main risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Secret disclosure through source control | `app_config.json`, `.env`, and runtime graph data are gitignored; CI runs Gitleaks on pushes and pull requests. |
| Vulnerable dependencies | Exact dependency versions are maintained in `requirements.txt`; Dependabot opens update proposals weekly. |
| Unsafe code changes | Pull requests run compilation, unit tests, mock graph tests, and CodeQL analysis. |
| Provider data exposure | Select providers deliberately and do not place secrets or sensitive personal data in prompts unless the provider's handling policy is acceptable. |
| Malformed imported graph | Import failures are handled without replacing the active graph; review third-party JSON before importing. |

## Operational guidance

1. Keep the local configuration and graph files on encrypted storage if they contain sensitive context.
2. Use a restricted provider key with only the permissions required for inference.
3. Rotate provider credentials if a local device or configuration file is exposed.
4. Review GitHub Actions results before merging dependency or security changes.

## AI evaluation

Knowledge extraction is probabilistic. Validate important links before relying on them for decisions, especially relationships involving people, dates, ownership, risks, or compliance obligations. The sample graph is illustrative and not evidence about a real project.
