---
name: diataxis-doc-writer
description: >
  Write technical documentation following the Diátaxis framework. Use this skill whenever
  the user wants to write, improve, or restructure documentation — tutorials, how-to guides,
  API or CLI reference docs, conceptual explanations, READMEs, internal runbooks, onboarding
  guides, or any technical writing about software. Trigger on: "write docs for X", "document
  this function/API/CLI", "create a tutorial", "write a guide for", "write a readme", "explain
  how X works", "add documentation", "create reference docs", "write a how-to", "document this
  feature", "help me write the docs", or any request to produce technical writing. Also trigger
  when the user pastes undocumented code and asks to document it, or shares existing docs and
  asks to improve them.
---

# Diátaxis Documentation Writer

Diátaxis organizes documentation into four distinct types, each serving a different user need. Mixing types is the most common documentation mistake — a tutorial that explains too much, a how-to that teaches instead of directing, a reference that gives opinions. Your job is to keep each piece of documentation pure to its type.

## Step 1 — Diagnose the documentation type

Before writing anything, ask these questions if the user hasn't already answered them:

1. **What are you documenting?** (a feature, an API endpoint, a CLI tool, a concept, a workflow...)
2. **Who is the reader?** (a beginner who has never used this, an experienced user who knows what they want, someone looking up a specific fact, someone trying to understand why something works the way it does)
3. **What will the reader do right after reading this?** (follow steps, accomplish a specific task, look up a value, gain understanding)

Use the answers to map to one of the four types:

| If the reader wants to… | And they are… | → Write a… |
|---|---|---|
| Learn by doing | A beginner, new to the topic | **Tutorial** |
| Accomplish a specific task | Someone who already knows the basics | **How-to guide** |
| Look up facts, values, syntax | Someone with a specific question | **Reference** |
| Understand the why/how | Someone seeking deeper context | **Explanation** |

If the user already names the type ("write me a tutorial for X"), skip the diagnosis and go straight to writing.

If the content genuinely needs multiple types (e.g., a full README), write each section as its own pure Diátaxis block. Label sections clearly.

## Step 2 — Read the type-specific guide

Once you've identified the type, read the corresponding reference file before writing:

- Tutorial → `references/tutorial.md`
- How-to guide → `references/how-to.md`
- Reference documentation → `references/reference.md`
- Explanation → `references/explanation.md`

These files contain the principles, structure, tone guidelines, and a template for each type.

## Step 3 — Write the documentation

Follow the guidance in the reference file. Produce clean Markdown output ready to paste into a `.md` file or a doc site (Docusaurus, MkDocs, Sphinx, etc.).

After writing, do a quick self-check:
- Does this doc stay true to its type? (no tutorial explanation in a how-to, no opinions in a reference, no step-by-step instructions in an explanation)
- Does the title signal the type? (tutorials start with a verb like "Build…" or "Create…"; how-tos with "How to…"; reference uses the thing's name; explanations use "Understanding…" or "About…")
- Is the audience's assumed knowledge level consistent throughout?

If the user shares existing documentation to improve, first identify its current type (or types), note where it violates Diátaxis principles, then rewrite it cleanly.