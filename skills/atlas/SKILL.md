---
name: atlas
description: Generate a fresh visual atlas of the Sapho portfolio when the user asks for a visual overview, dashboard artifact, or atlas. For conversational status or focus advice, use sapho-review. The atlas is a disposable read-only rendering, never current truth.
---

# Atlas: the inward view of the corpus

Use `../sapho-review/SKILL.md` for evidence gathering and judgment. Read **every** product
and its linked open work, plus `git log` per file (last touch, recent reconciles). Then generate one self-contained HTML file and publish it (artifact or local
preview). The atlas is a disposable rendering: regenerate at will, never treat it as input.

## What it shows

1. **Overview**: one card per product — name, one_liner, status chip, tags, frontmatter
   completeness, gap count, and open-todo signal for products with a `todos/<slug>.md`
   (open item count + age of the oldest line via git blame; empty file = healthy, show
   nothing; older items show their age, without inferring urgency or obsolescence). A summary strip (statuses, corpus age, most common gap) and a
   cross-project insights panel (strategic connections between products, shared audiences,
   portfolio threads, all-corpus patterns).
2. **Detail per product** (click a card): frontmatter, the four sections condensed
   faithfully (no invented facts), last-touched date and last reconcile commit, and a
   **gaps panel**.
3. **Gaps** are where the value is. Two kinds, labeled:
   - *corpus gaps* — mechanical: malformed metadata, unreadable tracker references, or
     broken known links. Optional missing repo links, absent/empty local todos, and young
     ideas with explicit unknowns are healthy. Age alone does not establish staleness.
   - *worth deciding* — editorial judgment: threads mentioned without a rationale,
     truth dropped in a migration that may still be live, assumptions old enough to
     re-confirm.
   Every gap gets a **copyable prompt** the user can paste into any AI session to close it
   (usually an interview + reconcile). The atlas never edits truth itself.

## Style

sopt aesthetic: dark `#08080b`, DM Mono, white-alpha cards/borders, purple
`rgb(168,155,232)` accent, teal reads / coral highlights. Stamp the build: date + corpus
commit hash. Title: `sapho atlas`.

## Rules

- Facts only from the files; judgments clearly framed as judgments.
- Read-only: writes route through reconcile prompts, never through the atlas.
- Output to `renderings/atlas.html` (overwrite freely — it's disposable).
