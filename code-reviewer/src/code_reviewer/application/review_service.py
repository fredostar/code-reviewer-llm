from code_reviewer.domain.models import ReviewReport
from code_reviewer.domain.ports import RepoFetcher, CodeAnalyzer


class ReviewService:
    def __init__(self, fetcher: RepoFetcher, analyzer: CodeAnalyzer) -> None:
        self._fetcher = fetcher
        self._analyzer = analyzer

    async def run(self, repo: str, branch: str = "main") -> ReviewReport:
        files = await self._fetcher.fetch_files(repo, branch)
        analyses = [await self._analyzer.analyze(f) for f in files]
        overall_summary = "\n".join(a.summary for a in analyses)
        return ReviewReport(
            repo_name=repo,
            branch=branch,
            files_analyzed=analyses,
            overall_summary=overall_summary,
        )