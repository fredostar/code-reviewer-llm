# Understanding code-reviewer

## What this service does

code-reviewer is an HTTP service that automates code review using a language model. Given a pointer to a Git repository — a provider (GitHub or GitLab), a project name, and a branch or commit reference — it fetches the source files, sends each one to Mistral AI for analysis, and returns a structured Markdown report listing issues, suggestions, and an overall summary.

The service is intentionally narrow: it does not comment on pull requests directly, it does not integrate with CI pipelines, and it does not retain state between calls. Each `POST /reviews` request is fully self-contained.

---

## Hexagonal architecture (ports and adapters)

The codebase follows a hexagonal (ports and adapters) architecture. The core business logic lives in the `domain/` and `application/` layers and depends on no external library. All interactions with the outside world — VCS providers, the LLM API, the output format — are mediated through `Protocol` interfaces defined in `domain/ports.py`.

Three ports structure the entire system:

**`RepoFetcher`** — knows how to retrieve a list of files for a given `ReviewRequest`. The domain doesn't know whether those files come from GitHub, GitLab, or anywhere else. Two adapters implement it: `GithubSource` (httpx against the GitHub REST API) and `GitlabSource` (python-gitlab SDK, offloaded to a thread pool via `asyncio.to_thread` because the SDK is synchronous).

**`CodeAnalyzer`** — knows how to analyze a single file and produce a `FileAnalysis`. One adapter implements it today: `MistralAnalyzer`. Swapping in a different LLM requires only writing a new adapter that satisfies the protocol.

**`MarkdownRenderer`** — knows how to turn a `ReviewReport` into a string. One adapter: `MarkdownRenderer`, which produces a straightforward Markdown document.

This structure makes the core logic testable in isolation using plain Python classes, with no mocking framework and no real network calls.

---

## Request flow

A `POST /reviews` call travels through four layers:

```
HTTP request
    └── FastAPI endpoint (main.py)
            └── ReviewService.run()
                    ├── RepoFetcher.fetch_files()   → list[FileToReview]
                    ├── CodeAnalyzer.analyze()       → FileAnalysis  (once per file)
                    └── assemble ReviewReport
            └── MarkdownRenderer.render()
HTTP response (text/markdown)
```

`ReviewService` is the only application-layer class. It selects the right `RepoFetcher` by looking up `request.provider` in a dictionary (`{"github": GithubSource(...), "gitlab": GitlabSource(...)}`), then sequentially fetches and analyzes each file. Files are analyzed one at a time, not in parallel — this is intentional to avoid hammering the Mistral rate limits.

---

## The MistralAnalyzer agentic loop

Rather than asking Mistral to return a structured JSON object in a single call, `MistralAnalyzer` drives a multi-turn tool-calling loop. The model is given three tools:

- `report_issue(description)` — call once for each bug, security flaw, or code smell detected
- `report_suggestion(description)` — call once for each improvement idea
- `finalize(summary, severity)` — call last, exactly once, to close the analysis

The loop runs for up to 10 turns. It exits early when `finalize` is called or when the model returns plain text instead of a tool call (a fallback for cases where the model decides it has nothing to report).

This approach has two advantages over a single structured-output call. First, it lets the model "think out loud" across multiple turns, which tends to produce more thorough analysis on complex files. Second, `report_issue` and `report_suggestion` accumulate incrementally — the model doesn't need to hold the entire list in one generation, which reduces truncation risk on large files.

The system prompt varies by `ReviewKind`: a `code_review` request instructs the model to look for bugs and code smells; a `security` request focuses it on vulnerabilities, secret exposure, and authorization flaws.

---

## Design decisions worth knowing

**`asyncio.to_thread` for GitLab** — The python-gitlab SDK is synchronous and blocks the event loop when called directly from an `async` method. `GitlabSource` wraps all SDK calls in a single `asyncio.to_thread(_fetch_sync, request)` call, offloading the blocking I/O to a worker thread. This keeps the FastAPI event loop responsive while the GitLab API is queried.

**`max_files_per_review`** — Fetching and analyzing every file in a large repository would exhaust Mistral's rate limit and take minutes. The limit (default: 20, configurable via `CR_MAX_FILES_PER_REVIEW`) is applied inside each adapter's fetch loop, so file content is never downloaded beyond the cap. It is not applied after fetching — this avoids downloading hundreds of files only to discard most of them.

**Fixed file extension allowlist** — Both source adapters only fetch files matching `.py .java .kt .ts .js`. This is a deliberate scope constraint: LLM-based review works best on high-level application code, and extending to configuration files, templates, or data files would produce noise. The allowlist lives as a module-level constant `_EXTENSIONS` in each adapter.

**`ReviewKind` as a prompt switch** — The `kind` parameter doesn't change the tools available to the model, only the system prompt. A security review and a code review produce the same `FileAnalysis` shape. This keeps the domain model stable while allowing the model's focus to shift significantly depending on what the caller cares about.

---

## Related resources

- [API Reference](api-reference.md) — endpoints, parameters, configuration variables, data model
