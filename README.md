# code-reviewer

Service HTTP qui automatise la revue de code via Mistral AI. Pointez-le vers un dépôt GitHub ou GitLab, et il retourne un rapport Markdown listant les problèmes, suggestions et niveau de sévérité pour chaque fichier.

## Documentation

- [Architecture](code-reviewer/docs/architecture.md) — fonctionnement du service, décisions de conception, boucle agentique LLM
- [Référence API](code-reviewer/docs/api-reference.md) — endpoints, variables de configuration, modèles de données

## Démarrage rapide

**Prérequis** : Python 3.13+, [uv](https://docs.astral.sh/uv/)

```bash
git clone <repo-url>
cd code-reviewer-llm/code-reviewer
uv sync
```

Définissez les variables d'environnement requises :

```bash
export CR_MISTRAL_API_KEY=votre-clé-mistral

# Pour les revues GitHub
export CR_GITHUB_TOKEN=votre-token-github

# Pour les revues GitLab (instance auto-hébergée : définir aussi CR_GITLAB_URL)
export CR_GITLAB_TOKEN=votre-token-gitlab
```

Démarrez l'API :

```bash
uv run code-reviewer
# → http://localhost:8000
```

Déclenchement d'une revue :

```bash
curl -s -X POST \
  "http://localhost:8000/reviews?provider=github&project=owner/repo&ref=main&kind=code_review"
```

## Docker

```bash
docker build -t code-reviewer code-reviewer/
docker run -p 8000:8000 \
  -e CR_MISTRAL_API_KEY=... \
  -e CR_GITHUB_TOKEN=... \
  code-reviewer
```
