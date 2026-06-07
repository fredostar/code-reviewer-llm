import gitlab
import httpx
from fastapi import FastAPI, HTTPException, Response

from code_reviewer.adapters.github_source import GithubSource
from code_reviewer.adapters.gitlab_source import GitlabSource
from code_reviewer.adapters.markdown_renderer import MarkdownRenderer
from code_reviewer.adapters.mistral_analyzer import MistralAnalyzer
from code_reviewer.application.review_service import ReviewService
from code_reviewer.config import Settings
from code_reviewer.domain.models import ReviewKind, ReviewRequest

settings = Settings()
renderer = MarkdownRenderer()
service = ReviewService(
    sources={
        "gitlab": GitlabSource(settings.gitlab_url, settings.gitlab_token, settings.max_files_per_review),
        "github": GithubSource(settings.github_token, settings.max_files_per_review),
    },
    analyzer=MistralAnalyzer(settings),
)

app = FastAPI(title="code-reviewer")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/reviews")
async def create_review(provider: str, project: str, ref: str, kind: ReviewKind) -> Response:
    req = ReviewRequest(provider=provider, project=project, ref=ref, kind=kind)
    try:
        report = await service.run(req)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream HTTP error: {exc.response.status_code} {exc.request.url}")
    except gitlab.exceptions.GitlabError as exc:
        raise HTTPException(status_code=502, detail=f"GitLab error: {exc}")
    return Response(content=renderer.render(report), media_type="text/markdown")