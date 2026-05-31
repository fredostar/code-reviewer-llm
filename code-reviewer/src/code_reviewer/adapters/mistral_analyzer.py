import json

from mistralai.client.sdk import Mistral

from code_reviewer.config import Settings
from code_reviewer.domain.models import FileAnalysis, FileToReview, Severity

_MODEL = "mistral-small-latest"
_MAX_STEPS = 10

_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "report_issue",
            "description": "Signale un problème détecté dans le code (bug, faille de sécurité, code smell)",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description précise du problème",
                    }
                },
                "required": ["description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "report_suggestion",
            "description": "Propose une amélioration du code",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description de la suggestion",
                    }
                },
                "required": ["description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finalize",
            "description": "Finalise l'analyse. À appeler en dernier, une seule fois.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Résumé de l'analyse en 1-2 phrases",
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["info", "warning", "critical"],
                        "description": "critical si faille de sécurité ou bug bloquant, warning si code smell ou mauvaise pratique, info sinon",
                    },
                },
                "required": ["summary", "severity"],
            },
        },
    },
]

_SYSTEM = """Tu es un expert en revue de code. Analyse le fichier fourni étape par étape :
1. Appelle report_issue() pour chaque problème (bug, faille, code smell)
2. Appelle report_suggestion() pour chaque suggestion d'amélioration
3. Appelle finalize() en dernier avec le résumé et la sévérité globale"""


class MistralAnalyzer:
    def __init__(self, settings: Settings) -> None:
        self._client = Mistral(api_key=settings.mistral_api_key)

    async def analyze(self, file: FileToReview) -> FileAnalysis:
        messages: list = [
            {"role": "system", "content": _SYSTEM},
            {
                "role": "user",
                "content": f"Fichier : {file.path} ({file.language})\n\n```{file.language}\n{file.content}\n```",
            },
        ]

        issues: list[str] = []
        suggestions: list[str] = []
        summary = ""
        severity = Severity.INFO

        for _ in range(_MAX_STEPS):
            response = await self._client.chat.complete_async(
                model=_MODEL,
                messages=messages,
                tools=_TOOLS,
                tool_choice="auto",
            )

            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                break

            done = False
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                match call.function.name:
                    case "report_issue":
                        issues.append(args["description"])
                    case "report_suggestion":
                        suggestions.append(args["description"])
                    case "finalize":
                        summary = args["summary"]
                        severity = Severity(args["severity"])
                        done = True

                messages.append(
                    {"role": "tool", "tool_call_id": call.id, "content": "ok"}
                )

            if done:
                break

        return FileAnalysis(
            path=file.path,
            summary=summary or "Analyse terminée",
            issues=issues,
            suggestions=suggestions,
            severity=severity,
        )