from mistralai import Mistral

from code_reviewer.domain.models import FileToReview, FileAnalysis, Severity

_SYSTEM_PROMPT = """Tu es un expert en revue de code. Analyse le fichier fourni et retourne :
- Un résumé en 2-3 phrases
- Une liste de problèmes détectés (bugs, code smells, violations SOLID/CUPID)
- Une liste de suggestions d'amélioration
- Un niveau de sévérité global : info, warning ou critical

Réponds en JSON strict avec les clés : summary, issues, suggestions, severity"""

class MistralCodeAnalyzer:
    def __init__(self, api_key: str, model: str = "mistral-large-latest") -> None:
        self._client = Mistral(api_key=api_key)
        self._model = model

    async def analyze(self, file: FileToReview) -> FileAnalysis:
        user_prompt = f"Fichier: {file.path} ({file.language})\n\n```{file.language}\n{file.content}\n```"
        response = await self._client.chat.complete_async(
            model=self._model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        import json
        data = json.loads(response.choices[0].message.content)
        return FileAnalysis(
            path=file.path,
            summary=data["summary"],
            issues=data.get("issues", []),
            suggestions=data.get("suggestions", []),
            severity=Severity(data.get("severity", "info")),
        )