---
name: sapho-review
description: Review the user's Sapho portfolio and recommend what deserves attention, needs a decision, can be delegated, or can wait. Use for portfolio questions such as "how is everything looking?" or "what should I focus on today?", including outside a project. Not a generic code review or automatic task launcher.
---

# Review the portfolio

Locate the user's existing corpus from their global instructions or the invoking skill;
do not assume the current directory is it or create another corpus. Sync according to
`CONNECT.md`, read it and the schema in `README.md`. Discover products from `products/`,
not a remembered list. Read every product file in full and its linked open work. Empty or
absent local todo files are healthy; external trackers require all relevant open pages.
Say which sources are unavailable rather than treating them as empty. Read-only by default.

## Build a grounded picture

- Use current user goals and available attention from the conversation. If missing, make a
  provisional recommendation and state the assumption; ask at most the question that would
  materially change the choice. Do not require a planning interview before being useful.
- Compare existing tasks with product decisions using the reconcile rubric. Flag clear
  drift, contradictions, and newer intent needing confirmation. A review proposes fixes;
  it does not silently reconcile or delete work.
- Separate product lifecycle (`exploring`, `building`, `live`, `paused`) from today's
  attention. Age and todo count are descriptive, never priority scores or proof of neglect.
  An old decision may remain right; a quiet live product may need no work.
- Look for commitments, consequential decisions, steps that unblock useful outcomes,
  small finishable work, and ways to reduce ongoing owner effort. Include maintenance,
  research, distribution, and personal usefulness; do not default every next step to code.
- Reconsider paused ideas only against recorded constraints and evidence of change.
  A better model announcement alone is not evidence of end-to-end feasibility. Test an
  easier approach as well as new technology. Never promote a project automatically.

## Verify the leading recommendations

Distinguish **recorded intent**, **observed state**, and **your inference**. Before saying
something is unfinished, blocked, regressing, or ready to ship, inspect the relevant current
repo, release, tracker, or analytics evidence. Map repos via `links:`; verify path and remote
before interpreting them. A commit is not proof of deployment and an intended feature is
not proof of completion. Do not run builds, mutate repos, or sweep unrelated files to answer
a status question. If evidence is inaccessible, recommend a bounded verification step and
label the conclusion provisional. Never turn a failed search into "nothing changed."

Read all corpus context, then investigate only evidence needed for the strongest candidates;
a routine review is not an exhaustive implementation audit. Follow any user time budget.
External feasibility research requires current dated sources. Cite supporting files or URLs
beside the claim, including what was actually checked and its date when relevant.

## Return an actionable brief

Lead with one recommended next action and why it outranks the alternatives. Usually keep
attention requests to three or fewer, with:

- Decisions only the user can make, explaining what each choice unlocks.
- Material drift or risks worth addressing; what can safely wait.
- For a proposed task: outcome, scope, evidence/check for done, and expected user involvement.
  Distinguish an estimate from a measured effort; do not invent availability or budgets.
- A compact coverage note: products/trackers read, external evidence checked, unresolved gaps.

Use only categories that have useful content. "Nothing requires attention" is a valid result.
A request for an overview can receive a fresh atlas (open-todo counts and freshness included),
but do not generate HTML unless the user wants a visual view. Keep findings disposable; do
not create reports, tasks, schedules, or change priorities merely because they were reviewed.
When the user asks to act on a recommendation, carry the evidence and scope into that work
and follow the existing authorization; don't make them repeat the brief or approve it twice.
