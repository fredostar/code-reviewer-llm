from code_reviewer.domain.models import ReviewReport, ReviewRequest
from code_reviewer.domain.ports import RepoFetcher, CodeAnalyzer


class ReviewService:
    def __init__(self, sources: dict[str, RepoFetcher], analyzer: CodeAnalyzer) -> None:
        self._sources = sources
        self._analyzer = analyzer

    async def run(self, request: ReviewRequest) -> ReviewReport:
        fetcher = self._sources[request.provider]
        files = await fetcher.fetch_files(request)
        analyses = [await self._analyzer.analyze(f, request.kind) for f in files]
        overall_summary = "\n".join(a.summary for a in analyses)
        return ReviewReport(
            repo_name=request.project,
            branch=request.ref,
            files_analyzed=analyses,
            overall_summary=overall_summary,
        )