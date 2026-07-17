# sapho — installation spec (for AI agents)

You have been asked to set up **sapho**: a plain-files source of truth for the user's
projects. One canonical markdown file per product; every AI the user works with reads it
before generating anything about that product. There is no server and no account — the
system is a schema, a few conventions, and a git repo the user owns.

spec_version: 6

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

## Step 1 — Discover before you create (do NOT skip)

sapho may already be installed — by another AI tool, on another surface, or in a
non-default location. Creating a second corpus is the worst failure mode of this install:
it silently forks the user's truth. So before proposing any plan:

1. **Ask the user first** — one question, always: "Have you used sapho before — on this
   machine, in another AI tool, or on GitHub?" Asking costs one message; forking truth
   costs the whole system.
2. **Read the user-level instruction files** on this machine (any that exist:
   `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/AGENTS.md`, editor rules files). A
   "Product Source of Truth (sapho)" section names the corpus path — follow it.
3. **Probe likely locations**: `~/sapho`, `~/Projects/sapho`, or any repo containing
   `products/*.md` alongside a README or CONNECT.md describing this schema. On chat
   surfaces, check the user's GitHub for such a repo (commonly named `sapho`).

**If you have filesystem access and find a local corpus, stop using this web page.**
Read `<corpus>/CONNECT.md` and follow it instead — it is the corpus's own connection
spec, it's newer than any cached copy of this page, and it needs no further web access
(so flaky web tooling can't break the setup).

**If a corpus exists → you are CONNECTING, not installing.** Never create a new corpus or
move the existing one. Instead: pull the latest if it has a git remote and report its
freshness (last commit date; flag truth files untouched for 45+ days as worth a re-read);
add YOUR platform's conventions pointing at the existing path (section in your instruction
file, reconcile skill if your platform supports skills); and confirm the connection by
listing the products you can now see. If the corpus has no GitHub remote yet, offer to add
one so the user's other surfaces can reach it.

**If nothing is found → proceed with a fresh install below.**

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

## Resilience rules (all tiers)

- **URL hygiene.** If fetching a URL you were given fails, strip wrapping characters
  first — markdown emphasis (`*`), angle brackets, quotes, trailing punctuation — and
  retry. Mirrors of this spec: `/install` (HTML), `/install.md` (raw text), and
  `/llms.txt` (pointer). If every fetch fails, ask the user to open the page and paste
  the spec — the install page has a "copy spec" button for exactly this.
- **Don't restart, resume.** If one step fails (a fetch, a tool error), report exactly
  which step and continue with the rest. Never respond to a tool failure by silently
  starting over or switching modes.
- **Tool failures never lower the bar.** A broken fetch or search is not a reason to
  skip discovery, skip the plan-approval step, or guess at file contents.
- **Prefer local over remote.** Once a corpus is on the machine, its own files
  (CONNECT.md, README) outrank this page for that machine.

## Rules of conduct (all tiers)

- Read a truth file in full before using it.
- The truth file is the substrate; voice and format of any output are per-request.
- Renderings (pages, pitches, posts generated from truth files) are disposable outputs —
  never fold their content back in as truth.
