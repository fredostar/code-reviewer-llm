import asyncio

import gitlab

from code_reviewer.domain.models import FileToReview, ReviewRequest

_EXTENSIONS = {".py", ".java", ".kt", ".ts", ".js"}


class GitlabSource:
    def __init__(self, url: str, token: str, max_files: int = 20) -> None:
        self._gl = gitlab.Gitlab(url, private_token=token)
        self._max_files = max_files

    async def fetch_files(self, request: ReviewRequest) -> list[FileToReview]:
        return await asyncio.to_thread(self._fetch_sync, request)

    def _fetch_sync(self, request: ReviewRequest) -> list[FileToReview]:
        project = self._gl.projects.get(request.project)
        tree = project.repository_tree(ref=request.ref, recursive=True, all=True)
        files: list[FileToReview] = []
        for item in tree:
            if len(files) >= self._max_files:
                break
            path = item["path"]
            ext = _extension(path)
            if item["type"] == "blob" and ext in _EXTENSIONS:
                raw = project.files.get(path, ref=request.ref)
                files.append(FileToReview(
                    path=path,
                    content=raw.decode().decode("utf-8"),
                    language=ext.lstrip("."),
                ))
        return files


def _extension(path: str) -> str:
    return "." + path.rsplit(".", 1)[-1] if "." in path else ""