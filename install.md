# sapho — installation spec (for AI agents)

You have been asked to set up **sapho**: a plain-files source of truth for the user's
projects. One canonical markdown file per product; every AI the user works with reads it
before generating anything about that product. There is no server and no account — the
system is a schema, a few conventions, and a git repo the user owns.

spec_version: 10
license: MIT · provided as-is, no warranty · https://github.com/damianr/sapho-site

## Step 0 — Detect your capabilities

- **You can write files on the user's machine** (Claude Code, Codex CLI, Cursor, or another
  agentic tool): perform the FULL INSTALL below, adapting paths to your platform's
  user-level instruction file.
- **You can read/write GitHub but not the user's disk** (ChatGPT, claude.ai, or another chat
  app with a GitHub connector): perform the CHAT-SURFACE SETUP below.
- **You have no tools**: walk the user through the setup conversationally and generate the
  files for them to save.

In every case: briefly explain which files the setup will touch. An explicit setup request
authorizes the necessary local work; do not ask for a second yes. Ask only for missing choices
or actions outside that authorization, such as creating a remote the user hasn't requested.
Merge with existing configuration — never overwrite it wholesale. Setup is idempotent:
preserve working pieces, add what's missing, and report what changed.
Never send the user's data anywhere they didn't direct.

## Step 1 — Discover before you create (do NOT skip)

sapho may already be installed — by another AI tool, on another surface, or in a
non-default location. Creating a second corpus is the worst failure mode of this install:
it silently forks the user's truth. So before proposing any plan:

1. **Use the conversation first.** If it already establishes an existing corpus, follow
   that connection without asking again. Otherwise ask: "Have you used sapho before — on this
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
file, workflow skill entrypoints if your platform supports skills); and confirm the connection by
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
tracker:    <tracker project link or todos/<slug>.md>
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

**Optional todos file (state, behind a wall).** For products too small for a tracker,
`todos/<slug>.md` holds a flat list of open items, with `tracker: todos/<slug>.md` in the
SOT frontmatter. Three hard rules: terse imperatives only, no context (durable truth gets
reconciled into the SOT before a line dies); done = the line is deleted, never archived,
dated, or checked `[x]` (git history is the archive); empty or absent is the healthy
state. Capture is ambient: when conversation surfaces actionable intent, offer to append
terse lines — offer, never auto-write. Other walled sibling file kinds may emerge; each
needs a distinct purpose and its own hard rules. `products/` alone holds truth.

## FULL INSTALL (filesystem agents)

1. **Corpus repo.** Ask where it should live (default `~/sapho`). Create it as a git repo
   containing `products/`, `todos/`, a README with the schema and the two rules, and
   `CONNECT.md` with the resolved corpus location, user's chosen sync/push policy,
   truth/state rules, and paths to the corpus workflow rubrics below. CONNECT is a local
   connection guide, not another copy of this discovery/install procedure. If there is no
   remote, work locally and say so; never attempt to pull from a nonexistent remote. Offer to create a private remote on
   the user's git host — any host works for agentic tools (GitHub, GitLab, Bitbucket);
   GitHub currently has the widest AI-connector support, so it's the default for users who
   want chat surfaces like ChatGPT reading the same corpus.
2. **User-level conventions.** Append a "Product Source of Truth (sapho)" section to your
   platform's global instruction file (Claude Code: `~/.claude/CLAUDE.md`), stating:
   (a) every product has one truth file at `<corpus>/products/<slug>.md`;
   (b) read it in full before generating anything product-facing; never invent product facts;
   (c) when starting substantive work in a project with no truth file, offer to interview
   the user and create one, recording the project's repo in the SOT's `links:` so any
   session can map repo to truth file from the corpus side;
   (d) when a session surfaces a durable decision with a rationale, flag it and offer to
   reconcile at a natural pause;
   (e) never write tasks, progress, or status into a truth file;
   (f) for portfolio/focus questions, including outside a project, use `sapho-review`;
   (g) for a new idea, use `sapho-capture`; no project repo is required;
   (h) offer `atlas` when a visual overview would help. Discover products from `products/`,
   never a fixed list. All portfolio reviews read the full corpus and linked open work;
   distinguish recorded intent, current evidence, and inference.
3. **Corpus rubrics and user-level entrypoints.** Download these plain Markdown rubrics
   during the authorized install from this public conventions repository and store them at
   `<corpus>/.claude/skills/<name>/SKILL.md` (the location works for every client):
   - [reconcile](https://raw.githubusercontent.com/damianr/sapho-site/main/skills/reconcile/SKILL.md)
     — fold durable decisions into truth and review every existing open tracker item.
   - [sapho-review](https://raw.githubusercontent.com/damianr/sapho-site/main/skills/sapho-review/SKILL.md)
     — recommend attention, decisions, and a bounded next action with evidence.
   - [sapho-capture](https://raw.githubusercontent.com/damianr/sapho-site/main/skills/sapho-capture/SKILL.md)
     — guide a short idea conversation and save confirmed intent with explicit unknowns.
   - [atlas](https://raw.githubusercontent.com/damianr/sapho-site/main/skills/atlas/SKILL.md)
     — optional fresh visual overview, not required for conversational review.
   At the client's user-level skill directory (Claude: `~/.claude/skills/`; Codex:
   `~/.codex/skills/`), create short SKILL.md entrypoints with the corresponding rubric's
   YAML name/description, the resolved corpus path, and instructions to read CONNECT and
   that rubric in full. Do not maintain separate substantive copies for each client.
   Record in CONNECT that local rubrics govern these workflows and the configured
   sync/push policy overrides the rubric's default. Reviews are read-only; capture doesn't
   imply building. Existing tasks can be rewritten or removed when a decision proves them
   obsolete, but task completion needs evidence. Preserve newer or ambiguous intent.
   Respect existing installations: do not overwrite custom rubrics on reconnect. Updates
   are deliberate and user-authorized, never a silent fetch of live web instructions.
4. **First product.** Use sapho-capture for one real idea or product. Capture the problem,
   proposed approach, actual decisions and rationale; label unknowns. No repo, commercial
   thesis, or final name is required. Save a useful partial capture if the user stops early.
   Show it, commit, and follow the sync policy selected for this corpus.
5. **Check the connection.** From outside the corpus directory, verify each installed
   entrypoint resolves its rubric. Parse the YAML frontmatter and check referenced paths.
   Report which workflows are available and which require tools the current client lacks.

**Zero repo footprint.** Never write sapho references into files that get committed to
the user's project repositories (CLAUDE.md, AGENTS.md, README, configs). The repo-to-truth
mapping belongs in the corpus (`links:` in each truth file); user-level instruction files
carry the behavior; if an explicit per-project pointer genuinely helps, use the platform's
git-ignored local file (Claude Code: `CLAUDE.local.md`) and ensure it is ignored.

## CHAT-SURFACE SETUP (GitHub-connected chat apps)

1. **Corpus.** If the user already has a sapho corpus repo, connect to it. If not, guide
   them to create a private GitHub repo (or have their coding agent do the FULL INSTALL
   first — that's the smoother path).
2. **Standing rule.** Chat apps have no folder context, so register this in your persistent
   layer (custom instructions, memory, or Project instructions): *"The user keeps a source
   of truth for their projects at <repo>. When one of these projects comes up by name —
   discover current names from products/ — read its truth file before answering, and never
   invent product facts. Use the corpus review rubric for portfolio/focus questions."*
3. **Reads.** Fetch `products/<slug>.md` via the GitHub connector before answering questions
   about that product.
4. **Writes.** Read and apply the corpus reconcile rubric and propose edits as commits or pull
   requests — minimal diffs, never a full-file rewrite for a small change. The user merges;
   the merge is the moment a claim becomes truth.
5. **If your platform can't reach the repo** (no connector, read-only plan, wrong mode):
   say so plainly and offer the fallback ladder in order — (a) a custom MCP connector to
   the git host, if the platform supports adding one; (b) the platform's repo connector in
   whatever mode exposes it (some gate it to research modes); (c) attaching the truth
   files to a persistent project/space, with an explicit warning that copies go stale and
   a refresh ritual; (d) asking the user to paste the relevant truth file. Plain-chat
   surfaces are read-mostly by nature: propose edits as text for the user to carry to a
   writing surface. Never silently answer ungrounded.

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
  skip discovery, exceed the user's authorization, or guess at file contents.
- **Prefer local over remote.** Once a corpus is on the machine, its own files
  (CONNECT.md, README) outrank this page for that machine.

## Rules of conduct (all tiers)

- Read a truth file in full before using it.
- The truth file is the substrate; voice and format of any output are per-request.
- Renderings (pages, pitches, posts generated from truth files) are disposable outputs —
  never fold their content back in as truth.

---

This spec and the site serving it are open source (MIT):
https://github.com/damianr/sapho-site — per-surface adapter contributions welcome.
