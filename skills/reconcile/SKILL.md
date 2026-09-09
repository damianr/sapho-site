---
name: reconcile
description: Fold new durable truth about a product back into its SOT file in products/. Use when a conversation, work session, or pasted note surfaces a decision, positioning shift, changed audience, killed assumption, or corrected fact about a product. Takes raw input (or reads it from the conversation), classifies it against the SOT, and applies the minimal edit. Also use when asked to reconcile todo drift against product decisions. Routine tasks and progress belong in the linked tracker, not product truth.
---

# Reconcile: fold new truth into an SOT

Input: raw material about a product — the user's words in this conversation, a pasted note,
or an explicit statement. Work in the user's canonical corpus, not the current project's
repo. Read `CONNECT.md` and sync as directed before reading product truth (`git pull
--ff-only` for a remote-backed corpus). Read the relevant `products/<slug>.md` in full
and all open work in its frontmatter `tracker` before editing.
For local todos, read the whole file; an absent or empty file is healthy. For an external
tracker, include all pages of open items. If access is unavailable, continue any supported
truth edit but report the tracker review as incomplete; never claim it is consistent.

## Classify before editing

Break the input into individual claims. For each claim, classify it against the SOT:

- **confirms** — already captured. No edit. Don't restate existing truth in new words.
- **new truth** — durable and absent. Add it to the one section where it belongs.
- **evolves** — refines something present (sharper positioning, narrowed audience). Rewrite
  that passage in place; don't append a second version alongside the old one.
- **conflicts** — contradicts the SOT. Never silently overwrite: surface the conflict to the
  user ("the SOT says X, this says Y"). If the user has already explicitly decided the
  reversal, apply it; otherwise ask which is now true. If the new version wins,
  replace the old — and if the *reversal itself* is instructive, record it as a decision
  with the why.
- **state** — progress, tasks, blockers, "next steps," anything with a shelf life of weeks.
  Reject from the SOT; route it to the linked tracker. Offer to capture new tasks unless
  the user has already authorized their addition; do not generate a backlog from a decision.
  State in the SOT is the failure mode that killed the predecessor system.
- **noise** — not about durable product truth at all. Drop it.

## The durability test

Before writing anything, ask: *will this still be true and worth knowing in six months?*
- "We decided X because Y" → truth (decision + rationale).
- "We shipped X" → state, unless it changed what the product *is* — then capture what it is
  now, not the shipping event.
- "X is blocked on Y" → state, always.

## Check decision consequences

Every reconciliation includes the tracker review, even when the incoming truth merely
confirms what is already recorded. A requested drift cleanup uses the same review.

Read the resulting truth file for other passages invalidated by the decision. Rewrite
superseded current claims; retain historical rationale only when clearly labeled as history.
Then classify every existing open item against the resulting decisions. Count todo items,
not headings or blank lines; split compound intent only when needed to preserve unfinished
clauses. Partial completion is a rewrite, not deletion of the whole item:

- **Keep:** still compatible, including explicitly deferred work. Age, inactivity, or
  absence from the SOT is not evidence that a task is obsolete.
- **Rewrite:** the outcome survives but the required approach changed. Preserve its intent
  and any surviving clauses; do not turn a small correction into new scope.
- **Remove as superseded:** an explicit adopted decision eliminates the work. Cite that
  decision in the reconciliation summary; do not describe the work as completed.
- **Remove as completed:** session or implementation evidence establishes completion.
  A proposed design or intended capability in the SOT is not proof it has shipped.
  Match evidence to the actual outcome: a feature branch does not prove a release, source
  changes do not prove deployment, and local configuration does not prove account setup
  or device verification. Inspect only the supporting evidence needed for the item.
- **Unresolved:** evidence conflicts, intent is unclear, or a newer task may reflect a
  decision missing from the SOT. Keep it and surface the specific uncertainty. Never let
  an older truth file automatically erase newer work.

Cleaning existing local todos is part of an authorized reconciliation; no separate approval
is needed for consequences clearly established by the decision. External tracker mutations
must stay within the user's authorization; otherwise report the exact proposed changes.
Before deleting any item, preserve durable rationale in the SOT if it remains applicable
and is not already captured. Done or superseded = delete the line, never archive or check
it off. Make surviving task text terse and imperative without losing its requirements.
Do not normalize unrelated items or execute the tasks during reconciliation.

## Editing rules

- Make the **minimal edit**: touch the claim and any passages or existing todos it invalidates.
  Keep the schema (frontmatter + Problem & insight / How it works / Key decisions & rationale / Positioning).
- Decisions go in "Key decisions & rationale" only with a *why*. No dated changelog tables.
- Update frontmatter when the claim is about it (`status`, `audience`, `one_liner`).
- **Sync**: follow `CONNECT.md` and the user's configured commit/push policy. For a
  remote-backed corpus, pull with `--ff-only` before reading; a local-only corpus has no
  remote to pull or push. Other surfaces cannot see unpushed changes.
- After editing, show the user a short summary: what was added/changed, what was rejected as
  state or noise and why. Report tracker coverage and counts kept/rewritten/removed/unresolved;
  explain changes and unresolved items with their evidence. Commit related SOT and local
  todo edits together so other surfaces receive the same decision. Commit with message
  `reconcile(<product>): <one-line summary>`, then sync as configured.
