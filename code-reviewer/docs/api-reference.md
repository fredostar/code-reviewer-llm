# code-reviewer — API Reference

## Endpoints

### `GET /health`

Returns the service health status.

**Response**

`200 OK`

```json
{"status": "ok"}
```

---

### `POST /reviews`

Triggers a code review for a repository at a given Git reference. Fetches source files from the VCS provider, analyzes each one, and returns a Markdown-formatted report.

**Query parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `provider` | `"github" \| "gitlab"` | Yes | VCS provider to fetch files from |
| `project` | string | Yes | Project identifier. For GitHub: `owner/repo`. For GitLab: numeric project ID or `namespace/path` |
| `ref` | string | Yes | Branch name, tag, or commit SHA |
| `kind` | `"code_review" \| "security"` | Yes | Review type. Determines the analysis prompt sent to the LLM |

**Response**

`200 OK` — `Content-Type: text/markdown`

A Markdown document structured as follows:

```markdown
# Code Review — {project} @ {ref}

## Summary

{overall_summary}

## `{file_path}` — {severity}

{file_summary}

### Issues
- {issue description}

### Suggestions
- {suggestion description}
```

**Errors**

| Code | Condition |
|---|---|
| `422` | Missing or invalid query parameter |
| `502` | Upstream HTTP error (GitHub or Mistral API returned a non-2xx status) |
| `502` | GitLab API error (authentication failure, project not found, etc.) |

---

## Configuration

All settings are read from environment variables prefixed with `CR_`. No configuration file is required.

| Variable | Type | Default | Description |
|---|---|---|---|
| `CR_GITHUB_TOKEN` | string | `""` | GitHub personal access token. Required when `provider=github` |
| `CR_GITLAB_URL` | string | `"https://gitlab.com"` | GitLab instance base URL. Override for self-hosted instances |
| `CR_GITLAB_TOKEN` | string | `""` | GitLab private token. Required when `provider=gitlab` |
| `CR_MISTRAL_API_KEY` | string | `""` | Mistral AI API key. Required for all review requests |
| `CR_MAX_FILES_PER_REVIEW` | integer | `20` | Maximum number of files fetched and analyzed per request. Files beyond this limit are silently skipped |

---

## Data models

### `ReviewKind`

| Value | Description |
|---|---|
| `code_review` | General code review: bugs, code smells, bad practices |
| `security` | Security-focused review: vulnerabilities, secret exposure, authorization flaws |

---

### `Severity`

| Value | Meaning |
|---|---|
| `info` | No significant issues found |
| `warning` | Code smells, bad practices, or minor issues |
| `critical` | Security vulnerability or blocking bug |

The severity of a `FileAnalysis` is determined by the LLM during the `finalize` tool call, based on what was found in that file.

---

### `FileAnalysis`

Produced for each file analyzed. Embedded in the `ReviewReport`.

| Field | Type | Description |
|---|---|---|
| `path` | string | File path relative to repository root |
| `summary` | string | 1–2 sentence summary of the file's analysis |
| `issues` | `list[string]` | Issues found (bugs, security flaws, code smells). May be empty |
| `suggestions` | `list[string]` | Improvement suggestions. May be empty |
| `severity` | `Severity` | Overall severity for this file |

---

### `ReviewReport`

The top-level object assembled by `ReviewService` and rendered to Markdown.

| Field | Type | Description |
|---|---|---|
| `repo_name` | string | Value of the `project` query parameter |
| `branch` | string | Value of the `ref` query parameter |
| `files_analyzed` | `list[FileAnalysis]` | One entry per file that was fetched and analyzed |
| `overall_summary` | string | Concatenation of each file's summary, separated by newlines |

---

## Supported file extensions

Both source adapters (GitHub and GitLab) only fetch files matching the following extensions. Files with other extensions are silently ignored during the fetch phase.

| Extension | Language |
|---|---|
| `.py` | Python |
| `.java` | Java |
| `.kt` | Kotlin |
| `.ts` | TypeScript |
| `.js` | JavaScript |
