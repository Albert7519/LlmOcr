# Contributing to LlmOcr

Thank you for considering a contribution to LlmOcr.

This is currently a single-maintainer project, so the contribution process is intentionally lightweight. Issues, bug reports, documentation fixes, and focused pull requests are welcome when they include enough context to reproduce or review the change.

## Good contribution areas

- Docker and deployment fixes.
- Documentation improvements.
- Prompt improvements for invoice extraction.
- More robust CSV parsing and export behavior.
- UI improvements for upload, error handling, and downloads.
- Tests for parsing and export logic.

## Development setup

1. Fork and clone the repository.
2. Create a feature branch.
3. Create a local `.env` file from `.env.example`.
4. Set `QWEN_API_KEY` in your environment or `.env` file.
5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Run the app:

   ```bash
   streamlit run app.py
   ```

## Pull request guidelines

- Keep changes focused.
- Explain why the change is useful.
- Include reproduction steps for bug fixes.
- Update README documentation when setup or behavior changes.
- Do not commit API keys, real `.env` files, private invoices, or sensitive business documents.

## Issue guidelines

When opening an issue, please include:

- Operating system and deployment method.
- Whether you used Docker Compose, Docker Run, or local Python.
- Steps to reproduce.
- Expected behavior and actual behavior.
- Error logs or screenshots when available.
- Sanitized or synthetic sample inputs when they help reproduce the issue.

## Security and privacy

Do not upload real API keys, private invoices, identity documents, or confidential business data to issues or pull requests. Use synthetic or anonymized examples only.
