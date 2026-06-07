from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class ReviewKind(str, Enum):
    CODE_REVIEW = "code_review"
    SECURITY = "security"


@dataclass(frozen=True)
class ReviewRequest:
    provider: str
    project: str
    ref: str
    kind: ReviewKind


@dataclass(frozen=True)
class FileToReview:
    path: str
    content: str
    language: str


@dataclass(frozen=True)
class FileAnalysis:
    path: str
    summary: str
    issues: list[str]
    suggestions: list[str]
    severity: Severity


@dataclass(frozen=True)
class ReviewReport:
    repo_name: str
    branch: str
    files_analyzed: list[FileAnalysis]
    overall_summary: str