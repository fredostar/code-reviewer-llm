from dataclasses import dataclass
from enum import Enum

class ReviewKind(str, Enum):
    CODE_REVIEW = "code_review"
    SECURITY = "security"

@dataclass(frozen=True, slots=True)
class ReviewRequest:
    provider: str          # "gitlab" | "github"
    project: str           # "group/project" ou "owner/repo"
    ref: str               # branche ou SHA
    kind: ReviewKind

@dataclass(frozen=True, slots=True)
class SourceFile:
    path: str
    content: str

@dataclass(frozen=True, slots=True)
class ReviewReport:
    request: ReviewRequest
    markdown: str