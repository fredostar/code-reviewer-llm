from mistralai import Mistral
from code_reviewer.domain.models import ReviewRequest, SourceFile, ReviewKind

_PROMPTS = {
    ReviewKind.CODE_REVIEW: "Tu es un relecteur senior. Analyse qualité/lisibilité/SOLID.",
    ReviewKind.SECURITY:    "Tu es un expert sécurité. Repère les vulnérabilités (OWASP).",
}

class MistralReviewer:
    def __init__(self, api_key: str, model: str = "mistral-large-latest") -> None:
        self._client = Mistral(api_key=api_key)
        self._model = model

    async def review(self, request: ReviewRequest, files: list[SourceFile]) -> str:
        bundle = "\n\n".join(f"### {f.path}\n```\n{f.content}\n```" for f in files)
        resp = await self._client.chat.complete_async(
            model=self._model,
            messages=[
                {"role": "system", "content": _PROMPTS[request.kind] +
                                              " Réponds en Markdown structuré (titres, listes)."},
                {"role": "user", "content": bundle},
            ],
        )
        return resp.choices[0].message.content