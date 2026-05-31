import gitlab
from code_reviewer.domain.models import ReviewRequest, SourceFile

class GitlabSource:
    def __init__(self, url: str, token: str) -> None:
        self._gl = gitlab.Gitlab(url, private_token=token)

    async def fetch_files(self, request: ReviewRequest) -> list[SourceFile]:
        project = self._gl.projects.get(request.project)
        tree = project.repository_tree(ref=request.ref, recursive=True, all=True)
        files: list[SourceFile] = []
        for item in tree:
            if item["type"] == "blob" and item["path"].endswith((".py", ".java")):
                raw = project.files.get(item["path"], ref=request.ref)
                files.append(SourceFile(item["path"], raw.decode().decode("utf-8")))
        return files