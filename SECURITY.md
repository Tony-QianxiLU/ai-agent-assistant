# Security Policy

## Supported Versions

Security updates are applied to the `main` branch.

## Reporting a Vulnerability

Please do not open public issues for sensitive vulnerabilities.

Instead, contact the maintainer through the GitHub profile listed in this repository. Include:

- A clear description of the issue.
- Steps to reproduce.
- Potential impact.
- Suggested fix, if available.

## Security Notes

- Do not commit API keys or `.env` files.
- Use deployment-platform secret managers for production secrets.
- Treat tool outputs and LLM outputs as untrusted until reviewed.
- Add human approval before enabling tools that mutate data, spend money, send messages, or access private systems.
