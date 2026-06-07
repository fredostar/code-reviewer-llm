# code-reviewer — Référence API

## Endpoints

### `GET /health`

Retourne l'état de santé du service.

**Réponse**

`200 OK`

```json
{"status": "ok"}
```

---

### `POST /reviews`

Déclenche une revue de code pour un dépôt à une référence Git donnée. Récupère les fichiers sources depuis le fournisseur VCS, analyse chacun d'eux, et retourne un rapport au format Markdown.

**Paramètres de requête**

| Paramètre | Type | Requis | Description |
|---|---|---|---|
| `provider` | `"github" \| "gitlab"` | Oui | Fournisseur VCS depuis lequel récupérer les fichiers |
| `project` | string | Oui | Identifiant du projet. Pour GitHub : `owner/repo`. Pour GitLab : ID numérique du projet ou `namespace/path` |
| `ref` | string | Oui | Nom de branche, tag ou SHA de commit |
| `kind` | `"code_review" \| "security"` | Oui | Type de revue. Détermine le prompt d'analyse envoyé au LLM |

**Réponse**

`200 OK` — `Content-Type: text/markdown`

Un document Markdown structuré comme suit :

```markdown
# Code Review — {project} @ {ref}

## Summary

{overall_summary}

## `{file_path}` — {severity}

{file_summary}

### Issues
- {description du problème}

### Suggestions
- {description de la suggestion}
```

**Erreurs**

| Code | Condition |
|---|---|
| `422` | Paramètre de requête manquant ou invalide |
| `502` | Erreur HTTP en amont (l'API GitHub ou Mistral a retourné un statut non-2xx) |
| `502` | Erreur API GitLab (échec d'authentification, projet introuvable, etc.) |

---

## Configuration

Tous les paramètres sont lus depuis des variables d'environnement préfixées par `CR_`. Aucun fichier de configuration n'est requis.

| Variable | Type | Défaut | Description |
|---|---|---|---|
| `CR_GITHUB_TOKEN` | string | `""` | Token d'accès personnel GitHub. Requis quand `provider=github` |
| `CR_GITLAB_URL` | string | `"https://gitlab.com"` | URL de base de l'instance GitLab. À surcharger pour les instances auto-hébergées |
| `CR_GITLAB_TOKEN` | string | `""` | Token privé GitLab. Requis quand `provider=gitlab` |
| `CR_MISTRAL_API_KEY` | string | `""` | Clé API Mistral AI. Requise pour toutes les requêtes de revue |
| `CR_MAX_FILES_PER_REVIEW` | integer | `20` | Nombre maximum de fichiers récupérés et analysés par requête. Les fichiers au-delà de cette limite sont silencieusement ignorés |

---

## Modèles de données

### `ReviewKind`

| Valeur | Description |
|---|---|
| `code_review` | Revue de code générale : bugs, code smells, mauvaises pratiques |
| `security` | Revue axée sécurité : vulnérabilités, exposition de secrets, failles d'autorisation |

---

### `Severity`

| Valeur | Signification |
|---|---|
| `info` | Aucun problème significatif trouvé |
| `warning` | Code smells, mauvaises pratiques ou problèmes mineurs |
| `critical` | Vulnérabilité de sécurité ou bug bloquant |

La sévérité d'une `FileAnalysis` est déterminée par le LLM lors de l'appel à l'outil `finalize`, en fonction de ce qui a été trouvé dans ce fichier.

---

### `FileAnalysis`

Produit pour chaque fichier analysé. Intégré dans le `ReviewReport`.

| Champ | Type | Description |
|---|---|---|
| `path` | string | Chemin du fichier relatif à la racine du dépôt |
| `summary` | string | Résumé en 1 à 2 phrases de l'analyse du fichier |
| `issues` | `list[string]` | Problèmes trouvés (bugs, failles de sécurité, code smells). Peut être vide |
| `suggestions` | `list[string]` | Suggestions d'amélioration. Peut être vide |
| `severity` | `Severity` | Sévérité globale pour ce fichier |

---

### `ReviewReport`

L'objet de niveau supérieur assemblé par `ReviewService` et rendu en Markdown.

| Champ | Type | Description |
|---|---|---|
| `repo_name` | string | Valeur du paramètre de requête `project` |
| `branch` | string | Valeur du paramètre de requête `ref` |
| `files_analyzed` | `list[FileAnalysis]` | Une entrée par fichier récupéré et analysé |
| `overall_summary` | string | Concaténation des résumés de chaque fichier, séparés par des sauts de ligne |

---

## Extensions de fichiers supportées

Les deux adaptateurs sources (GitHub et GitLab) ne récupèrent que les fichiers correspondant aux extensions suivantes. Les fichiers avec d'autres extensions sont silencieusement ignorés lors de la phase de récupération.

| Extension | Langage |
|---|---|
| `.py` | Python |
| `.java` | Java |
| `.kt` | Kotlin |
| `.ts` | TypeScript |
| `.js` | JavaScript |
