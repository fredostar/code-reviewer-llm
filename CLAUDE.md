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

Hexagonal (ports & adapters) design. The domain layer defines three `Protocol` ports in `domain/ports.py`:

- **`RepoFetcher`** — fetches files from a VCS provider; adapters: `GithubSource`, `GitlabSource`
- **`CodeAnalyzer`** — analyzes a single file and returns a `FileAnalysis`; adapter: `MistralAnalyzer`
- **`MarkdownRenderer`** — renders a `ReviewReport` to a markdown string; adapter: `MarkdownRenderer`

**Request flow**: `POST /reviews?provider=&project=&ref=&kind=` → `ReviewService.run()` → picks the right `RepoFetcher` by `provider` string → fetches files one-by-one → analyzes each with `CodeAnalyzer` → assembles `ReviewReport` → renderer returns `text/markdown`.

**`MistralAnalyzer`** drives an agentic loop (up to 10 steps) using Mistral tool-calling. The LLM calls three tools — `report_issue`, `report_suggestion`, `finalize` — and the loop exits when `finalize` is called or the model returns plain text.

**Source adapters** filter files to a fixed extension allowlist: `.py .java .kt .ts .js`. `GithubSource` uses raw httpx against the GitHub REST API. `GitlabSource` uses the `python-gitlab` SDK (synchronous SDK called from an async method — no `await`).

**Config** (`config.py`): all settings are `pydantic-settings` fields prefixed `CR_` (e.g. `CR_MISTRAL_API_KEY`, `CR_GITHUB_TOKEN`, `CR_GITLAB_TOKEN`, `CR_GITLAB_URL`).

**Test strategy**: service tests use plain `_Fake*` classes; adapter tests for `MistralAnalyzer` use `respx` to mock `https://api.mistral.ai/v1/chat/completions`.

- **Layout**: `src/` layout — source is under `code-reviewer/src/code_reviewer/`
- **Entry point**: `code_reviewer:main` (registered as the `code-reviewer` CLI script)
- **API framework**: FastAPI + Uvicorn
- **HTTP client**: httpx (mock with `respx` in tests)
- **Tests**: pytest with `asyncio_mode = "auto"` — all async tests work without `@pytest.mark.asyncio`
- **Ruff line length**: 100
- **mypy**: strict mode enabled

## Skills

Reusable agent skills are in `code-reviewer/.agents/skills/`. Invoke them from Claude Code with their `name` field.

| Skill | Description |
|-------|-------------|
| `pytest-coverage` | Run pytest with annotated coverage, find uncovered lines (`!`), add tests until 100% coverage |
| `github-copilot-starter` | Scaffold a full GitHub Copilot config (instructions, skills, agents, optional Actions workflow) for a new project |
| `dataverse-python-production-code` | Generate production Python code for the PowerPlatform Dataverse SDK (error handling, retry, OData) |
| `dataverse-python-advanced-patterns` | Advanced Dataverse SDK patterns: batch ops, metadata, file upload, Pandas integration |
| `diataxis-doc-writer` | Write technical documentation following the Diátaxis framework (tutorials, how-to guides, reference, explanation) |
