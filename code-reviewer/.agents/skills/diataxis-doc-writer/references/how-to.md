# How-to Guide — Writing Guide

## What a how-to guide is

A how-to guide helps a **competent user accomplish a specific, real-world task**. The reader already knows the basics — they've done a tutorial or have relevant experience. They have a concrete goal and want efficient, direct guidance to reach it.

Think of it like a recipe: the reader knows how to cook. They don't need to be taught what a knife is. They just want to know: how do I make this particular dish?

## What a how-to guide is NOT

- Not a tutorial — it doesn't teach; it guides action
- Not a reference — it doesn't exhaustively document all options
- Not an explanation — it doesn't explore background or theory

## Core principles

**Stay problem-focused.** The title and focus should reflect what the user is trying to accomplish, not what the tool does. "How to migrate from v1 to v2" is good. "Using the migrate command" is a reference entry.

**Assume competence.** Skip the basics. Don't explain what a terminal is, don't define common terms. The reader knows their stuff — respect that.

**No digression.** Every sentence should move the reader toward their goal. No "by the way" context, no side notes, no teaching moments. If something needs explaining, link to the explanation doc instead.

**Acknowledge real-world variation.** Unlike tutorials (which have a single controlled path), how-to guides can note that "if you're using X, do Y instead" — because experienced users operate in varied environments.

**Only necessary steps.** If a step is optional, mark it clearly or leave it out. If a step is only needed in a specific scenario, say so.

## Structure

```markdown
# How to [verb phrase — the concrete goal, e.g., "How to deploy to production with Docker"]

One sentence: what this guide helps you do. Optionally, what conditions apply (e.g., "if you're using X version or later").

## Prerequisites

- [specific tool, version, or state required]
- [access or permission required]

Be precise. "Admin access to the cluster" not just "cluster access".

## [First action — verb-first heading, e.g., "Configure the database connection"]

Command or action. Minimal explanation.

```bash
exact command
```

Any important note about variation: "If you're on Windows, use `...` instead."

## [Next action]

...

## [Final action]

## Verify

How the reader can confirm it worked. This is especially important when there's no obvious success signal.
```

## Tone

- Direct, efficient, professional
- No hand-holding, no encouragement — just clear direction
- Use imperative voice: "Run", "Set", "Open", "Replace"
- Short steps, each focused on one action

## How-to vs. Tutorial — the key distinction

| | How-to | Tutorial |
|---|---|---|
| Reader | Competent practitioner | Beginner |
| Goal | Accomplish a task | Learn a skill |
| Explanation | Minimal | Contextual, brief |
| Path | Often flexible | Single prescribed path |
| Scope | Specific task | Guided experience |

## Common mistakes to avoid

- **Teaching instead of directing**: "The reason we configure this is..." → remove it or link to explanation
- **Tutorial creep**: starting from zero when the reader is already competent
- **Vague goals**: "Working with authentication" → pick one concrete task
- **Missing prerequisites**: reader gets halfway through and discovers they need something not listed upfront