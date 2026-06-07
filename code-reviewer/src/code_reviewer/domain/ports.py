from typing import Protocol

from code_reviewer.domain.models import FileToReview, FileAnalysis, ReviewReport, ReviewRequest, ReviewKind


class RepoFetcher(Protocol):
    async def fetch_files(self, request: ReviewRequest) -> list[FileToReview]: ...


class CodeAnalyzer(Protocol):
    async def analyze(self, file: FileToReview, kind: ReviewKind) -> FileAnalysis: ...


class MarkdownRenderer(Protocol):
    def render(self, report: ReviewReport) -> str: ...