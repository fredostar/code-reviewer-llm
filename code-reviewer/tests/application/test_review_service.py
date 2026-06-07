from code_reviewer.application.review_service import ReviewService
from code_reviewer.domain.models import FileAnalysis, FileToReview, ReviewKind, ReviewRequest, Severity


class _FakeFetcher:
    async def fetch_files(self, request: ReviewRequest) -> list[FileToReview]:
        return [FileToReview(path="app.py", content="print('x')", language="python")]


class _FakeAnalyzer:
    async def analyze(self, file: FileToReview, kind: ReviewKind) -> FileAnalysis:
        return FileAnalysis(
            path=file.path,
            summary="Looks good",
            issues=[],
            suggestions=[],
            severity=Severity.INFO,
        )


async def test_produces_report_with_analyzed_files() -> None:
    service = ReviewService({"github": _FakeFetcher()}, _FakeAnalyzer())
    request = ReviewRequest(provider="github", project="owner/repo", ref="main", kind=ReviewKind.CODE_REVIEW)
    report = await service.run(request)
    assert report.repo_name == "owner/repo"
    assert report.branch == "main"
    assert len(report.files_analyzed) == 1
    assert report.files_analyzed[0].path == "app.py"