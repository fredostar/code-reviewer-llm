import httpx

from code_reviewer.domain.models import FileToReview
from code_reviewer.config import Settings

# Extensions à analyser
_EXTENSIONS = {".py", ".java", ".kt", ".ts", ".js"}

class GitHubRepoFetcher:
    """Récupère l'arborescence d'un repo GitHub via l'API REST."""

    def __init__(self, settings: Settings) -> None:
        self._token = settings.github_token
        self._base_url = "https://api.github.com"

    async def fetch_files(self, repo: str, branch: str = "main") -> list[FileToReview]:
        headers = {"Authorization": f"Bearer {self._token}"}
        async with httpx.AsyncClient(headers=headers) as client:
            # 1. Récupérer l'arborescence récursive
            tree_url = f"{self._base_url}/repos/{repo}/git/trees/{branch}?recursive=1"
            tree_resp = await client.get(tree_url)
            tree_resp.raise_for_status()
            entries = tree_resp.json()["tree"]

            files: list[FileToReview] = []
            for entry in entries:
                if entry["type"] != "blob":
                    continue
                path = entry["path"]
                ext = _extension(path)
                if ext not in _EXTENSIONS:
                    continue

                # 2. Récupérer le contenu brut
                raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
                content_resp = await client.get(raw_url)
                content_resp.raise_for_status()
                files.append(FileToReview(
                    path=path,
                    content=content_resp.text,
                    language=ext.lstrip("."),
                ))
            return files

def _extension(path: str) -> str:
    return "." + path.rsplit(".", 1)[-1] if "." in path else ""