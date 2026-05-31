import pytest

from code_reviewer.application.review_service import ReviewService
from code_reviewer.domain.models import ReviewKind, ReviewRequest, SourceFile


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