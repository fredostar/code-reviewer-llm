import pytest

from code_reviewer.application.review_service import ReviewService
from code_reviewer.domain.models import FileAnalysis, FileToReview, Severity


class _FakeFetcher:
    async def fetch_files(self, repo, branch="main"):
        return [FileToReview(path="app.py", content="print('x')", language="python")]


class _FakeAnalyzer:
    async def analyze(self, file):
        return FileAnalysis(
            path=file.path,
            summary="Looks good",
            issues=[],
            suggestions=[],
            severity=Severity.INFO,
        )


@pytest.mark.asyncio
async def test_produces_report_with_analyzed_files():
    service = ReviewService(_FakeFetcher(), _FakeAnalyzer())
    report = await service.run("owner/repo", "main")
    assert report.repo_name == "owner/repo"
    assert report.branch == "main"
    assert len(report.files_analyzed) == 1
    assert report.files_analyzed[0].path == "app.py"