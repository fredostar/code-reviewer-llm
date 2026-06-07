import uvicorn


def main() -> None:
    uvicorn.run("code_reviewer.main:app", host="0.0.0.0", port=8000, reload=True)