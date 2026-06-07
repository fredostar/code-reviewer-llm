# Comprendre code-reviewer

## Ce que fait ce service

code-reviewer est un service HTTP qui automatise la revue de code à l'aide d'un modèle de langage. En lui fournissant un pointeur vers un dépôt Git — un fournisseur (GitHub ou GitLab), un nom de projet et une référence de branche ou de commit — il récupère les fichiers sources, envoie chacun à Mistral AI pour analyse, et retourne un rapport Markdown structuré listant les problèmes, suggestions et un résumé global.

Le service est délibérément limité dans sa portée : il ne commente pas directement les pull requests, ne s'intègre pas dans les pipelines CI, et ne conserve aucun état entre les appels. Chaque requête `POST /reviews` est entièrement autonome.

---

## Architecture hexagonale (ports et adaptateurs)

Le code suit une architecture hexagonale (ports et adaptateurs). La logique métier principale se trouve dans les couches `domain/` et `application/` et ne dépend d'aucune bibliothèque externe. Toutes les interactions avec le monde extérieur — fournisseurs VCS, l'API LLM, le format de sortie — sont médiatisées via des interfaces `Protocol` définies dans `domain/ports.py`.

Trois ports structurent l'ensemble du système :

**`RepoFetcher`** — sait comment récupérer une liste de fichiers pour une `ReviewRequest` donnée. La couche domaine ne sait pas si ces fichiers proviennent de GitHub, GitLab ou ailleurs. Deux adaptateurs l'implémentent : `GithubSource` (httpx vers l'API REST GitHub) et `GitlabSource` (SDK python-gitlab, délégué à un thread pool via `asyncio.to_thread` car le SDK est synchrone).

**`CodeAnalyzer`** — sait comment analyser un fichier unique et produire une `FileAnalysis`. Un seul adaptateur l'implémente aujourd'hui : `MistralAnalyzer`. Remplacer le LLM ne nécessite que d'écrire un nouvel adaptateur satisfaisant le protocole.

**`MarkdownRenderer`** — sait comment transformer un `ReviewReport` en chaîne de caractères. Un seul adaptateur : `MarkdownRenderer`, qui produit un document Markdown simple.

Cette structure rend la logique principale testable de façon isolée avec de simples classes Python, sans framework de mock ni appel réseau réel.

---

## Flux d'une requête

Un appel `POST /reviews` traverse quatre couches :

```
Requête HTTP
    └── Endpoint FastAPI (main.py)
            └── ReviewService.run()
                    ├── RepoFetcher.fetch_files()   → list[FileToReview]
                    ├── CodeAnalyzer.analyze()       → FileAnalysis  (une fois par fichier)
                    └── assemblage du ReviewReport
            └── MarkdownRenderer.render()
Réponse HTTP (text/markdown)
```

`ReviewService` est la seule classe de la couche application. Elle sélectionne le bon `RepoFetcher` en cherchant `request.provider` dans un dictionnaire (`{"github": GithubSource(...), "gitlab": GitlabSource(...)}`), puis récupère et analyse chaque fichier séquentiellement. Les fichiers sont analysés un par un, pas en parallèle — c'est délibéré pour éviter de saturer les limites de débit de Mistral.

---

## La boucle agentique de MistralAnalyzer

Plutôt que de demander à Mistral de retourner un objet JSON structuré en un seul appel, `MistralAnalyzer` pilote une boucle multi-tours d'appels d'outils. Le modèle dispose de trois outils :

- `report_issue(description)` — appelé une fois pour chaque bug, faille de sécurité ou code smell détecté
- `report_suggestion(description)` — appelé une fois pour chaque idée d'amélioration
- `finalize(summary, severity)` — appelé en dernier, exactement une fois, pour clore l'analyse

La boucle s'exécute jusqu'à 10 tours. Elle s'arrête prématurément quand `finalize` est appelé ou quand le modèle retourne du texte brut au lieu d'un appel d'outil (cas de repli quand le modèle décide de ne rien signaler).

Cette approche présente deux avantages par rapport à un appel à sortie structurée unique. D'abord, elle permet au modèle de "réfléchir à voix haute" sur plusieurs tours, ce qui tend à produire une analyse plus approfondie sur les fichiers complexes. Ensuite, `report_issue` et `report_suggestion` s'accumulent de façon incrémentale — le modèle n'a pas besoin de tenir toute la liste en une seule génération, ce qui réduit le risque de troncature sur les grands fichiers.

Le prompt système varie selon le `ReviewKind` : une requête `code_review` demande au modèle de chercher bugs et code smells ; une requête `security` le concentre sur les vulnérabilités, l'exposition de secrets et les failles d'autorisation.

---

## Décisions de conception à connaître

**`asyncio.to_thread` pour GitLab** — Le SDK python-gitlab est synchrone et bloque la boucle d'événements lorsqu'il est appelé directement depuis une méthode `async`. `GitlabSource` encapsule tous les appels SDK dans un unique appel `asyncio.to_thread(_fetch_sync, request)`, délégant les I/O bloquantes à un thread worker. Cela maintient la réactivité de la boucle d'événements FastAPI pendant que l'API GitLab est interrogée.

**`max_files_per_review`** — Récupérer et analyser tous les fichiers d'un grand dépôt épuiserait les limites de débit de Mistral et prendrait plusieurs minutes. La limite (par défaut : 20, configurable via `CR_MAX_FILES_PER_REVIEW`) est appliquée à l'intérieur de la boucle de récupération de chaque adaptateur, de sorte que le contenu des fichiers n'est jamais téléchargé au-delà du seuil. Elle n'est pas appliquée après récupération — cela évite de télécharger des centaines de fichiers pour en rejeter la plupart.

**Liste blanche d'extensions fixe** — Les deux adaptateurs sources ne récupèrent que les fichiers correspondant à `.py .java .kt .ts .js`. C'est une contrainte de périmètre délibérée : la revue basée sur LLM fonctionne mieux sur du code applicatif de haut niveau, et l'étendre aux fichiers de configuration, templates ou données produirait du bruit. La liste blanche est une constante de niveau module `_EXTENSIONS` dans chaque adaptateur.

**`ReviewKind` comme commutateur de prompt** — Le paramètre `kind` ne change pas les outils disponibles pour le modèle, seulement le prompt système. Une revue de sécurité et une revue de code produisent la même structure `FileAnalysis`. Cela maintient le modèle de domaine stable tout en permettant au focus du modèle de changer significativement selon ce que l'appelant recherche.

---

## Ressources associées

- [Référence API](api-reference.md) — endpoints, paramètres, variables de configuration, modèle de données
