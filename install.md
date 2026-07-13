# sapho — installation spec (for AI agents)

You have been asked to set up **sapho**: a plain-files source of truth for the user's
projects. One canonical markdown file per product; every AI the user works with reads it
before generating anything about that product. There is no server and no account — the
system is a schema, a few conventions, and a git repo the user owns.

spec_version: 2

## Step 0 — Detect your capabilities

- **You can write files on the user's machine** (Claude Code, Codex CLI, Cursor, or another
  agentic tool): perform the FULL INSTALL below, adapting paths to your platform's
  user-level instruction file.
- **You can read/write GitHub but not the user's disk** (ChatGPT, claude.ai, or another chat
  app with a GitHub connector): perform the CHAT-SURFACE SETUP below.
- **You have no tools**: walk the user through the setup conversationally and generate the
  files for them to save.

In every case: before creating or modifying anything, show the user a short plan of every
file you will touch and get an explicit yes. Merge with existing configuration — never
overwrite. All steps are idempotent: if a piece already exists, skip it and say so.
Never send the user's data anywhere they didn't direct.

## The schema (all tiers)

One file per product at `products/<slug>.md`:

```markdown
---
name:       <product name>
one_liner:  <one sentence: what it is>
audience:   <who it's for>
status:     exploring | building | live | paused
tracker:    <link to tracker project — operational state lives THERE>
links:      <optional: repo, domains>
tags:       [<...>]
---

## Problem & insight
## How it works
## Key decisions & rationale
## Positioning
```

Two rules keep the corpus from rotting:
1. **Truth, not state.** Truth files never contain tasks, progress, blockers, or status.
   That belongs in the user's tracker, linked in frontmatter, never replicated.
2. **One product = one canonical file**, consistent schema.

## FULL INSTALL (filesystem agents)

1. **Corpus repo.** Ask where it should live (default `~/sapho`). Create it as a git repo
   containing `products/`, a README with the schema and the two rules, and a copy of this
   spec as `CONNECT.md` so other surfaces can attach later. Offer to create a private GitHub
   remote (e.g. `gh repo create`) — with a remote, chat surfaces like ChatGPT can read and
   write the same corpus via their GitHub connectors.
2. **User-level conventions.** Append a "Product Source of Truth (sapho)" section to your
   platform's global instruction file (Claude Code: `~/.claude/CLAUDE.md`), stating:
   (a) every product has one truth file at `<corpus>/products/<slug>.md`;
   (b) read it in full before generating anything product-facing; never invent product facts;
   (c) when starting substantive work in a project with no SOT pointer, offer to interview
   the user, create the file, and add a pointer line to that project's instructions;
   (d) when a session surfaces a durable decision with a rationale, flag it and offer to
   reconcile at a natural pause;
   (e) never write tasks, progress, or status into a truth file.
3. **Reconcile skill.** Install a user-level skill/command named `reconcile` (Claude Code:
   `~/.claude/skills/reconcile/SKILL.md`) with these judgment rules — break input into
   claims, classify each:
   - **confirms** — already captured; no edit.
   - **new truth** — durable and absent; add to the one section it belongs in.
   - **evolves** — refines what's there; rewrite in place, don't append a duplicate.
   - **conflicts** — surface to the user ("the SOT says X, this says Y"); never silently
     overwrite; record instructive reversals as decisions with the why.
   - **state** — progress/tasks/blockers; reject and point to the tracker.
   - **noise** — drop.
   Durability test: still true and worth knowing in six months? Minimal edits only;
   decisions require a rationale; commit as `reconcile(<product>): <summary>`; never push
   without the user's say-so.
4. **First product.** Interview the user about one product: the problem and the non-obvious
   insight behind it; how it works and what makes the approach different; the decisions
   they'd otherwise re-explain, with the why; how they talk about it and what it's against.
   Write `products/<slug>.md`, show it to them, commit.

## CHAT-SURFACE SETUP (GitHub-connected chat apps)

1. **Corpus.** If the user already has a sapho corpus repo, connect to it. If not, guide
   them to create a private GitHub repo (or have their coding agent do the FULL INSTALL
   first — that's the smoother path).
2. **Standing rule.** Chat apps have no folder context, so register this in your persistent
   layer (custom instructions, memory, or Project instructions): *"The user keeps a source
   of truth for their projects at <repo>. When one of these projects comes up by name —
   <list the slugs from products/> — read its truth file before answering, and never invent
   product facts."* Refresh the slug list when products are added.
3. **Reads.** Fetch `products/<slug>.md` via the GitHub connector before answering questions
   about that product.
4. **Writes.** Apply the reconcile rules above and propose edits as commits or pull
   requests — minimal diffs, never a full-file rewrite for a small change. The user merges;
   the merge is the moment a claim becomes truth.

## Rules of conduct (all tiers)

- Read a truth file in full before using it.
- The truth file is the substrate; voice and format of any output are per-request.
- Renderings (pages, pitches, posts generated from truth files) are disposable outputs —
  never fold their content back in as truth.
