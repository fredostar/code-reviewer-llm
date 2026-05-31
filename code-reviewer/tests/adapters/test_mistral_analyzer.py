import json

import httpx
import respx

from code_reviewer.adapters.mistral_analyzer import MistralAnalyzer
from code_reviewer.config import Settings
from code_reviewer.domain.models import FileToReview, Severity

_CHAT_URL = "https://api.mistral.ai/v1/chat/completions"


def _tool_call_response(name: str, args: dict, call_id: str) -> dict:
    return {
        "id": "chat-1",
        "object": "chat.completion",
        "created": 1700000000,
        "model": "mistral-small-latest",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": call_id,
                    "type": "function",
                    "function": {"name": name, "arguments": json.dumps(args)},
                }],
            },
            "finish_reason": "tool_calls",
        }],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }


def _text_response(content: str) -> dict:
    return {
        "id": "chat-2",
        "object": "chat.completion",
        "created": 1700000000,
        "model": "mistral-small-latest",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": content, "tool_calls": None},
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }


@respx.mock
async def test_analyze_collects_issues_and_finalizes():
    respx.post(_CHAT_URL).mock(side_effect=[
        httpx.Response(200, json=_tool_call_response(
            "report_issue", {"description": "Variable non typée"}, "c1"
        )),
        httpx.Response(200, json=_tool_call_response(
            "report_suggestion", {"description": "Ajouter des annotations de type"}, "c2"
        )),
        httpx.Response(200, json=_tool_call_response(
            "finalize", {"summary": "Code fonctionnel mais non typé", "severity": "warning"}, "c3"
        )),
    ])

    analyzer = MistralAnalyzer(Settings(mistral_api_key="fake-key"))
    file = FileToReview(path="app.py", content="x = 1", language="python")

    result = await analyzer.analyze(file)

    assert result.path == "app.py"
    assert result.issues == ["Variable non typée"]
    assert result.suggestions == ["Ajouter des annotations de type"]
    assert result.summary == "Code fonctionnel mais non typé"
    assert result.severity == Severity.WARNING


@respx.mock
async def test_analyze_stops_early_on_text_response():
    respx.post(_CHAT_URL).mock(return_value=httpx.Response(
        200, json=_text_response("Rien à signaler.")
    ))

    analyzer = MistralAnalyzer(Settings(mistral_api_key="fake-key"))
    file = FileToReview(path="ok.py", content="pass", language="python")

    result = await analyzer.analyze(file)

    assert result.summary == "Analyse terminée"
    assert result.issues == []
    assert result.severity == Severity.INFO