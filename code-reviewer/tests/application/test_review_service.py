from unittest.mock import AsyncMock, MagicMock

import pytest

from code_reviewer.application.review_service import ReviewService
from code_reviewer.domain.models import ReviewKind, ReviewReport, ReviewRequest, SourceFile


class _FakeSource:
    async def fetch_files(self, request): return [SourceFile("app.py", "print('x')")]
class _FakeReviewer:
    async def review(self, request, files): return "## Findings\n- RAS"
class _MdRenderer:
    def render(self, request, body):
        from code_reviewer.domain.models import ReviewReport
        return ReviewReport(request, f"# Rapport\n\n{body}")

@pytest.mark.asyncio
async def test_produces_markdown_report():
    service = ReviewService({"gitlab": _FakeSource()}, _FakeReviewer(), _MdRenderer())
    req = ReviewRequest("gitlab", "grp/proj", "main", ReviewKind.SECURITY)
    report = await service.run(req)
    assert report.markdown.startswith("# Rapport")

@pytest.fixture
def request_() -> ReviewRequest:
    return ReviewRequest(
        provider="github",
        project="owner/repo",
        ref="main",
        kind=ReviewKind.CODE_REVIEW,
    )


@pytest.fixture
def files() -> list[SourceFile]:
    return [SourceFile(path="main.py", content="print('hello')")]


@pytest.fixture
def source_repo(files: list[SourceFile]) -> AsyncMock:
    mock = AsyncMock()
    mock.fetch_files.return_value = files
    return mock


@pytest.fixture
def code_reviewer() -> AsyncMock:
    mock = AsyncMock()
    mock.review.return_value = "## Review\nLooks good."
    return mock


@pytest.fixture
def report_renderer(request_: ReviewRequest) -> MagicMock:
    mock = MagicMock()
    mock.render.return_value = ReviewReport(
        request=request_,
        markdown="## Review\nLooks good.",
    )
    return mock


@pytest.fixture
def service(source_repo: AsyncMock, code_reviewer: AsyncMock, report_renderer: MagicMock) -> ReviewService:
    return ReviewService({"github": source_repo}, code_reviewer, report_renderer)


async def test_review_fetches_files(
    service: ReviewService, source_repo: AsyncMock, request_: ReviewRequest
) -> None:
    await service.run(request_)
    source_repo.fetch_files.assert_awaited_once_with(request_)


async def test_review_calls_reviewer_with_files(
    service: ReviewService,
    code_reviewer: AsyncMock,
    request_: ReviewRequest,
    files: list[SourceFile],
) -> None:
    await service.run(request_)
    code_reviewer.review.assert_awaited_once_with(request_, files)


async def test_review_renders_report(
    service: ReviewService,
    report_renderer: MagicMock,
    request_: ReviewRequest,
) -> None:
    await service.run(request_)
    report_renderer.render.assert_called_once_with(request_, "## Review\nLooks good.")


async def test_review_returns_rendered_report(
    service: ReviewService, report_renderer: MagicMock, request_: ReviewRequest
) -> None:
    report = await service.run(request_)
    assert report == report_renderer.render.return_value