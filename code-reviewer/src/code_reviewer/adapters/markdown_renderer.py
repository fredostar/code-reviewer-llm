from code_reviewer.domain.models import ReviewReport


class MarkdownRenderer:
    def render(self, report: ReviewReport) -> str:
        lines = [
            f"# Code Review — {report.repo_name} @ {report.branch}",
            "",
            "## Summary",
            "",
            report.overall_summary,
            "",
        ]
        for analysis in report.files_analyzed:
            lines += [
                f"## `{analysis.path}` — {analysis.severity.value}",
                "",
                analysis.summary,
                "",
            ]
            if analysis.issues:
                lines.append("### Issues")
                lines += [f"- {issue}" for issue in analysis.issues]
                lines.append("")
            if analysis.suggestions:
                lines.append("### Suggestions")
                lines += [f"- {s}" for s in analysis.suggestions]
                lines.append("")
        return "\n".join(lines)