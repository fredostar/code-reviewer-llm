from typing import Protocol

from code_reviewer.domain.models import FileToReview, FileAnalysis, ReviewReport

class RepoFetcher(Protocol):
    """Récupère les fichiers d'un dépôt distant."""
    async def fetch_files(self, repo: str, branch: str = "main") -> list[FileToReview]: ...

class CodeAnalyzer(Protocol):
    """Analyse un fichier via un LLM et retourne un diagnostic."""
    async def analyze(self, file: FileToReview) -> FileAnalysis: ...

class ReportWriter(Protocol):
    """Produit le rapport final dans un format donné."""
    def write(self, report: ReviewReport, output_path: str) -> str: ...