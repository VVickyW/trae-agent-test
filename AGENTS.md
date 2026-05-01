# Trae Agent - Development Guide

## Overview

Trae Agent is an LLM-based CLI agent for software engineering tasks, built with Python 3.12+ and managed by `uv`. The entry point is `trae-cli`.

## Cursor Cloud specific instructions

### Quick Reference

- **Install deps**: `uv sync --all-extras` (or `make install-dev` which also creates the venv)
- **Activate venv**: `source .venv/bin/activate`
- **Run tests**: `make uv-test` (skips Ollama/OpenRouter/Google tests that need live APIs)
- **Lint**: `uv run ruff check .` and `uv run ruff format --check .`
- **Fix formatting**: `make fix-format`
- **Run CLI**: `uv run trae-cli --help`

### Important Notes

- The `trae-cli run` and `trae-cli interactive` commands require a valid `trae_config.yaml` with at least one LLM provider API key. Without it, `show-config` errors with "Config file not found". Copy `trae_config.yaml.example` to `trae_config.yaml` and add your API key.
- Tests are designed to run without any external LLM services — the Makefile test targets set `SKIP_OLLAMA_TEST=true SKIP_OPENROUTER_TEST=true SKIP_GOOGLE_TEST=true` to skip tests requiring live API connections.
- Pre-commit hooks are configured in `.pre-commit-config.yaml` and include: trailing-whitespace, end-of-file-fixer, check-yaml, check-toml, check-added-large-files, detect-private-key, ruff, ruff-format, codespell, and mypy.
- The project uses `hatchling` as the build backend. `uv sync --all-extras` installs the project in editable mode, so code changes are immediately available via `trae-cli`.
- Python version requirement is 3.12+ (specified in `.python-version` and `pyproject.toml`).
