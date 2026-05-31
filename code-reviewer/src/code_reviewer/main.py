from fastapi import FastAPI, Response
from code_reviewer.config import Settings
from code_reviewer.domain.models import ReviewRequest, ReviewKind
from code_reviewer.application.review_service import ReviewService
from code_reviewer.adapters.gitlab_source import GitlabSource
from code_reviewer.adapters.github_source import GithubSource
from code_reviewer.adapters.mistral_reviewer import MistralReviewer
from code_reviewer.adapters.markdown_renderer import MarkdownRenderer

settings = Settings()
service = ReviewService(
    sources={
        "gitlab": GitlabSource(settings.gitlab_url, settings.gitlab_token),
        "github": GithubSource(settings.github_token),
    },
    reviewer=MistralReviewer(settings.mistral_api_key),
    renderer=MarkdownRenderer(),
)

app = FastAPI(title="code-reviewer")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/reviews")
async def create_review(provider: str, project: str, ref: str, kind: ReviewKind) -> Response:
    req = ReviewRequest(provider, project, ref, kind)
    report = await service.run(req)
    return Response(content=report.markdown, media_type="text/markdown")