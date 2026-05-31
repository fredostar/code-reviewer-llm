import pytest
from code_reviewer.domain.models import FileToReview, FileAnalysis, Severity, ReviewReport
from code_reviewer.review.reviewer import CodeReviewer

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

class FakeWriter:
    def __init__(self):
        self.last_report = None
    def write(self, report, output_path):
        self.last_report = report
        return output_path

@pytest.mark.asyncio
async def test_review_produces_report():
    writer = FakeWriter()
    reviewer = CodeReviewer(FakeFetcher(), FakeAnalyzer(), writer)

    path = await reviewer.review("owner/repo", "main", "out.md")

    assert path == "out.md"
    assert writer.last_report is not None
    assert len(writer.last_report.files_analyzed) == 1
    assert writer.last_report.files_analyzed[0].severity == Severity.INFO