from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_token: str = ""
    gitlab_url: str = "https://gitlab.com"
    gitlab_token: str = ""
    mistral_api_key: str = ""
    max_files_per_review: int = 20

    model_config = {"env_prefix": "CR_"}
