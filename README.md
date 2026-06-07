# code-reviewer

HTTP service that automates code review using Mistral AI. Point it at a GitHub or GitLab repository, and it returns a Markdown report listing issues, suggestions, and severity for each file.

## Documentation

- [Architecture](code-reviewer/docs/architecture.md) — how the service works, design decisions, the LLM agentic loop
- [API Reference](code-reviewer/docs/api-reference.md) — endpoints, configuration variables, data models

## Quick start

**Prerequisites**: Python 3.13+, [uv](https://docs.astral.sh/uv/)

```bash
git clone <repo-url>
cd code-reviewer-llm/code-reviewer
uv sync
```

Set the required environment variables:

```bash
export CR_MISTRAL_API_KEY=your-mistral-key

# For GitHub reviews
export CR_GITHUB_TOKEN=your-github-token

# For GitLab reviews (self-hosted: also set CR_GITLAB_URL)
export CR_GITLAB_TOKEN=your-gitlab-token
```

Start the API:

```bash
uv run code-reviewer
# → http://localhost:8000
```

Trigger a review:

```bash
curl -s -X POST \
  "http://localhost:8000/reviews?provider=github&project=owner/repo&ref=main&kind=code_review"
```

## Docker

```bash
docker build -t code-reviewer code-reviewer/
docker run -p 8000:8000 \
  -e CR_MISTRAL_API_KEY=... \
  -e CR_GITHUB_TOKEN=... \
  code-reviewer
```