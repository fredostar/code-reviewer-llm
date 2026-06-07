import httpx

from code_reviewer.domain.models import FileToReview, ReviewRequest

_EXTENSIONS = {".py", ".java", ".kt", ".ts", ".js"}


class GithubSource:
    def __init__(self, token: str, max_files: int = 20) -> None:
        self._token = token
        self._max_files = max_files

    async def fetch_files(self, request: ReviewRequest) -> list[FileToReview]:
        headers = {"Authorization": f"Bearer {self._token}"}
        async with httpx.AsyncClient(headers=headers) as client:
            tree_url = (
                f"https://api.github.com/repos/{request.project}"
                f"/git/trees/{request.ref}?recursive=1"
            )
            tree_resp = await client.get(tree_url)
            tree_resp.raise_for_status()

            files: list[FileToReview] = []
            for entry in tree_resp.json()["tree"]:
                if len(files) >= self._max_files:
                    break
                if entry["type"] != "blob":
                    continue
                path = entry["path"]
                ext = _extension(path)
                if ext not in _EXTENSIONS:
                    continue
                raw_url = (
                    f"https://raw.githubusercontent.com"
                    f"/{request.project}/{request.ref}/{path}"
                )
                content_resp = await client.get(raw_url)
                content_resp.raise_for_status()
                files.append(FileToReview(path=path, content=content_resp.text, language=ext.lstrip(".")))
            return files


def _extension(path: str) -> str:
    return "." + path.rsplit(".", 1)[-1] if "." in path else ""