from typing import Protocol
from .models import ReviewRequest, ReviewReport, SourceFile

class SourceRepository(Protocol):
    async def fetch_files(self, request: ReviewRequest) -> list[SourceFile]: ...

class CodeReviewer(Protocol):
    async def review(self, request: ReviewRequest,
                     files: list[SourceFile]) -> str: ...   # renvoie le corps markdown

class ReportRenderer(Protocol):
    def render(self, request: ReviewRequest, body: str) -> ReviewReport: ...