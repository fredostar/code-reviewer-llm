# Tutorial — Writing Guide

## What a tutorial is

A tutorial is a **learning experience**. The reader is a beginner; they don't know yet what they don't know. Your job isn't to explain everything — it's to give them a guided, hands-on experience that builds confidence and results in a tangible achievement.

Think of it like a cooking class: the instructor doesn't explain the chemistry of caramelization. They say "now stir for 3 minutes until golden." The student learns by doing, not by reading theory.

## What a tutorial is NOT

- Not a reference for all options and edge cases
- Not an explanation of why things work the way they do
- Not a list of steps for an expert user — that's a how-to guide

## Core principles

**Deliver results early and often.** The reader should see something working within the first few steps. Momentum matters. If they have to read 500 words before anything happens, they'll bounce.

**Minimize explanation.** Every sentence of explanation is a sentence that delays the next step. Save it for the explanation doc. In a tutorial, one short sentence of context per action is usually enough.

**Be specific and concrete.** Never say "run the appropriate command." Say `npm install`. Give exact values, exact file names, exact commands. The reader should be able to follow blindly and succeed.

**Make steps reversible where possible.** Prefer creating new things over modifying existing ones. If a step goes wrong, the reader should be able to undo it.

**Ensure reliable outcomes.** If the reader follows the steps exactly, they should get the same result every time. Avoid relying on state that varies between environments without explaining how to handle it.

## Structure

```markdown
# [Verb phrase — what they'll build/do, e.g., "Build a REST API with Node.js"]

Brief intro (2-4 sentences): what they'll build, what they'll learn, and what they'll have at the end.
Keep it energizing — no warnings, prerequisites buried here, or lengthy background.

## Prerequisites

- [thing they need installed or set up]
- [background knowledge assumed]

Keep this list short. If it's more than 4-5 items, the tutorial might be too advanced.

## [Step 1 title — action-oriented, e.g., "Set up the project"]

Short sentence framing what this step accomplishes.

```bash
command to run
```

Expected output or what they should see. This is important — it lets the reader confirm they're on track.

## [Step 2 title]

...

## [Final step — always produces a visible, satisfying result]

## What you've built

One paragraph summarizing what the reader achieved. Reinforce their success.

## Next steps

2-3 links to how-to guides, reference docs, or deeper tutorials — don't expand the tutorial itself.
```

## Tone

- Warm, encouraging, direct
- Use "you" throughout
- Use present tense ("Run this command", not "You will run")
- Short sentences, short paragraphs
- No jargon without a one-line definition on first use

## Common mistakes to avoid

- **Over-explaining**: "This command installs the package, which is a JavaScript runtime that..." → cut to just the command and expected output
- **Too many options**: "You can use either X or Y" → just pick one and tell them to use it
- **Vague steps**: "Configure your environment" → specify exactly what to do
- **No checkpoints**: reader has no way to know if they're on track → add expected outputs after key steps