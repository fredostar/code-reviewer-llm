from code_reviewer.domain.models import ReviewRequest, ReviewReport
from code_reviewer.domain.ports import SourceRepository, CodeReviewer, ReportRenderer

class ReviewService:
    def __init__(self, sources: dict[str, SourceRepository],
                 reviewer: CodeReviewer, renderer: ReportRenderer) -> None:
        self._sources = sources
        self._reviewer = reviewer
        self._renderer = renderer

    async def run(self, request: ReviewRequest) -> ReviewReport:
        source = self._sources[request.provider]   # composable, prévisible
        files = await source.fetch_files(request)
        body = await self._reviewer.review(request, files)
        return self._renderer.render(request, body)