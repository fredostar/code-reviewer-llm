# Reference Documentation — Writing Guide

## What reference docs are

Reference documentation is **technical truth**. The reader has a specific question: what does this parameter do? what are the valid values? what does this function return? They consult it, find the answer, and leave. They don't read it cover to cover.

Think of it like a dictionary: objective, consistent, complete, no opinions.

## What reference docs are NOT

- Not a tutorial — don't include step-by-step instructions
- Not a how-to — don't frame content around user goals
- Not an explanation — no "this was designed this way because..."

## Core principles

**Description only.** Describe what things are and how they behave. Don't tell the reader what to do with them, don't opine about best practices, don't embed workflow guidance.

**Mirror the product's structure.** If the product has endpoints, document endpoints. If it has commands, document commands. The structure of the reference docs should map 1:1 to the structure of the thing being documented. When the product changes, the docs change in lockstep.

**Consistent patterns.** Every endpoint, every function, every flag should use the same template. Predictability is what makes reference docs fast to use — the reader knows exactly where to look.

**Austere tone.** No enthusiasm, no encouragement. "Returns a 404 if not found" not "Uh oh — you'll get a 404 if not found."

**Examples are good — as illustration, not instruction.** A code snippet showing a parameter in use is helpful. Just don't let it become a how-to guide in disguise.

## Structures by type

### API Endpoint

```markdown
## `GET /users/{id}`

Returns a single user by ID.

### Path parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Unique identifier of the user |

### Query parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `include` | string | — | Comma-separated list of relations to include (e.g., `profile,roles`) |

### Response

`200 OK`

```json
{
  "id": "usr_123",
  "email": "alice@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Errors

| Code | Meaning |
|---|---|
| `404` | User not found |
| `401` | Missing or invalid authentication |
```

### CLI Command

```markdown
## `mytool deploy`

Deploys the application to the configured environment.

**Usage**

```
mytool deploy [options]
```

**Options**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--env` | string | `staging` | Target environment (`staging`, `production`) |
| `--dry-run` | boolean | `false` | Print what would be deployed without deploying |
| `--timeout` | integer | `300` | Deployment timeout in seconds |

**Exit codes**

| Code | Meaning |
|---|---|
| `0` | Deployment succeeded |
| `1` | Deployment failed (see stderr for details) |
| `2` | Invalid configuration |

**Example**

```bash
mytool deploy --env production --timeout 600
```
```

### Function / Method

```markdown
## `createUser(options)`

Creates a new user record and returns it.

**Parameters**

| Name | Type | Required | Description |
|---|---|---|---|
| `options.email` | string | Yes | Email address. Must be unique. |
| `options.role` | `"admin" \| "member"` | No | Default: `"member"` |

**Returns**

`Promise<User>` — the created user object.

**Throws**

- `ValidationError` — if `email` is not a valid email address
- `ConflictError` — if a user with this email already exists

**Example**

```js
const user = await createUser({ email: "alice@example.com", role: "admin" });
```
```

### Configuration file

```markdown
## `database`

Database connection configuration.

```yaml
database:
  host: localhost
  port: 5432
  name: mydb
  pool_size: 10
```

| Key | Type | Required | Default | Description |
|---|---|---|---|---|
| `host` | string | Yes | — | Database hostname or IP |
| `port` | integer | No | `5432` | PostgreSQL port |
| `name` | string | Yes | — | Database name |
| `pool_size` | integer | No | `10` | Maximum number of connections in the pool |
```

## Tone

- Neutral, factual, impersonal
- Present tense: "Returns" not "Will return"
- Third person or direct object: "The `--env` flag sets..." not "You can use `--env` to..."
- No hedging: "Returns a user" not "Should return a user"

## Common mistakes to avoid

- **Mixed-in how-to**: "To authenticate, first call..." → that belongs in a how-to guide
- **Opinions**: "The recommended approach is..." → remove or move to explanation
- **Inconsistent templates**: endpoint A documents errors, endpoint B doesn't → pick a template and apply it everywhere
- **Missing defaults**: always document the default value for optional parameters
- **Vague types**: "a value" → be specific: `string`, `integer`, `boolean`, `"option1" | "option2"`