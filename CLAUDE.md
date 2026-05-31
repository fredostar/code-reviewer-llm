# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

LLM-powered code review tool exposed as a FastAPI HTTP API. The Python package lives in the `code-reviewer/` subdirectory — all commands below must be run from there.

## Commands

```bash
cd code-reviewer

# Install dependencies
uv sync

# Run the API
uv run code-reviewer

# Lint / format
uv run ruff check .
uv run ruff format .

# Type check (strict)
uv run mypy .

# Tests
uv run pytest
uv run pytest path/to/test_file.py::test_name
uv run pytest --cov
```

## Architecture

- **Layout**: `src/` layout — source is under `code-reviewer/src/code_reviewer/`
- **Entry point**: `code_reviewer:main` (registered as the `code-reviewer` CLI script)
- **API framework**: FastAPI + Uvicorn
- **HTTP client**: httpx (mock with `respx` in tests)
- **Config**: pydantic-settings
- **Tests**: pytest with `asyncio_mode = "auto"` — all async tests work without `@pytest.mark.asyncio`
- **Ruff line length**: 100
- **mypy**: strict mode enabled
