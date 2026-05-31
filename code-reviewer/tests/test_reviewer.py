import pytest

from code_reviewer.application.review_service import ReviewService
from code_reviewer.domain.models import FileAnalysis, FileToReview, Severity


class FakeFetcher:
    async def fetch_files(self, repo, branch="main"):
        return [FileToReview(path="app.py", content="print('hello')", language="python")]


class FakeAnalyzer:
    async def analyze(self, file):
        return FileAnalysis(
            path=file.path,
            summary="Code simple",
            issues=[],
            suggestions=["Ajouter un main guard"],
            severity=Severity.INFO,
        )


@pytest.mark.asyncio
async def test_review_produces_report():
    service = ReviewService(FakeFetcher(), FakeAnalyzer())
    report = await service.run("owner/repo", "main")

    assert report.repo_name == "owner/repo"
    assert report.branch == "main"
    assert len(report.files_analyzed) == 1
    assert report.files_analyzed[0].severity == Severity.INFO