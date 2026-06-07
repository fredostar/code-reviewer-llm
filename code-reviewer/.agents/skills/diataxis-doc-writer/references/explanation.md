# Explanation — Writing Guide

## What an explanation is

An explanation deepens **understanding**. The reader isn't trying to do anything right now — they want to understand how or why something works, the thinking behind a design decision, the tradeoffs between approaches, or the broader context of a concept.

Think of it like an essay or a chapter in a good technical book: discursive, thoughtful, willing to explore alternatives and nuance. It's the documentation you read away from the keyboard, to deepen your mental model.

## What an explanation is NOT

- Not a tutorial — don't guide the reader through steps
- Not a how-to — don't frame it around accomplishing a task
- Not a reference — don't list facts exhaustively; explore meaning

## Core principles

**Explain the why.** This is the documentation type where "why" belongs. Why was this decision made? Why does this constraint exist? Why is this the recommended approach? Reference docs say what; explanations say why.

**Provide context and connections.** Weave concepts together. Relate this thing to other things the reader might know. Acknowledge the history or evolution of an approach when relevant.

**Acknowledge alternatives and tradeoffs.** Explanation is the right place to say "approach A trades X for Y; approach B does the opposite." This is not opinion — it's honest, balanced treatment.

**Read comfortably without a terminal open.** An explanation should make sense without running any commands. It's conceptual territory. If the reader needs to do something, link to the how-to or tutorial instead.

**Maintain clear boundaries.** The most common failure mode for explanations is "tutorial creep" — suddenly giving step-by-step instructions because it feels helpful. Resist. Link to the relevant how-to instead.

## Structure

Unlike tutorials and how-to guides, explanations don't follow a rigid template — they're prose-driven. But they benefit from clear signposting:

```markdown
# [Understanding/About] [topic — e.g., "Understanding authentication flows" or "About connection pooling"]

## Overview / What this is

1-2 paragraphs introducing the concept and why it matters. What problem does this solve? What mental model should the reader build?

## [Core concept or dimension 1]

Prose exploration. Use diagrams, analogies, or examples to illuminate, not to instruct.

## [Core concept or dimension 2]

...

## [Tradeoffs / Alternatives / When to use which]

Honest comparison of approaches. Not "use X" but "X works well when... Y is better when..."

## [Common misconceptions] (optional)

Useful when there's a widespread wrong mental model worth correcting.

## Related resources

- [Tutorial: hands-on introduction to this topic](link)
- [How to: do specific task related to this](link)
- [Reference: full technical details](link)
```

## Using analogies

Analogies are powerful in explanations. A good analogy transfers understanding from something the reader already knows to something they don't. A few guidelines:
- Introduce the analogy explicitly ("Think of it like...")
- Acknowledge where the analogy breaks down (every analogy does)
- Don't overload a single analogy — switch to a different one or drop to direct explanation

## Tone

- Thoughtful, discursive, conversational — more like an essay than a manual
- First person is acceptable ("We chose this approach because...")
- Allow for nuance: "it depends", "in most cases", "historically"
- Don't moralize or lecture — explain and illuminate

## Common mistakes to avoid

- **Instruction creep**: "To understand this, first run..." → link to the how-to instead
- **Reference in disguise**: an explanation that just lists all the config options → move to reference
- **No perspective**: explanation that only says "here is what X is" without saying why it matters or what alternatives exist
- **Too narrow**: a good explanation connects concepts — if it only covers one tiny detail, it might belong in the reference docs as a note
- **Unbalanced tradeoffs**: presenting only one approach without acknowledging alternatives makes an explanation feel like marketing copy