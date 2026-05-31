from dataclasses import dataclass
from enum import Enum

class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

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