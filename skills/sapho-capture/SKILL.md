---
name: sapho-capture
description: Guide a new or unfinished product idea from a natural description into the user's existing Sapho corpus. Use for "I have an idea", "help me shape this", or requests to capture or park an idea. Start with the problem and proposed solution, preserve unknowns, and avoid treating capture as a commitment to build.
---

# Capture an idea

Locate the existing corpus using the user's global instructions or the invoking skill,
regardless of the current directory. Follow `CONNECT.md` for sync; read it and `README.md`.
Discover existing products and their names/links before choosing a new slug. Read any likely
match in full so a renamed product, feature, or returning idea does not become a duplicate.
Do not require a project repo, a remote, a commercial thesis, or a final name to capture an
idea. Do not create a second corpus or a project repo during capture.

## Interview only for what's missing

First reflect the idea back briefly, using the user's words. Extract what the conversation
already establishes; don't ask it again. Then ask one useful question at a time, prioritizing:

1. The problem: who experiences it, a concrete occasion, and what they do today.
2. The desired outcome: what would improve if this were solved.
3. The imagined solution: what the user pictures, what matters about that shape, and what
   is flexible. Preserve the idea without presenting its feasibility as established.
4. The most consequential assumption: access, reliability, owner effort, cost, demand, or
   another condition that could invalidate the approach.
5. The smallest useful experiment or the condition for reconsidering it later.

This is a guide, not a form to complete. Adapt the order to what is known and allow an early
stop. Ask for missing preferences rather than inventing numerical effort/reliability budgets.
If the user supplies no idea yet, ask for the problem; don't create an empty product. Use a
working name derived from their words if naming would otherwise block useful capture.

## Save confirmed intent, label hypotheses

A request to capture/save an idea authorizes recording what the user supplied; don't add a
second confirmation ceremony. If they only want to discuss, stay in the conversation.
Use `products/<slug>.md` with the existing schema, normally `status: exploring` and
`tracker: todos/<slug>.md`; omit nonexistent repo links. The four sections can be short:

- **Problem & insight:** confirmed problem, audience, and desired improvement.
- **How it works:** the user's proposed approach, explicitly described as a hypothesis;
  say when implementation or feasibility is unverified.
- **Key decisions & rationale:** only actual choices with a known why. Say no decisions
  are established yet if needed; don't manufacture decisions to fill the section.
- **Positioning:** confirmed framing or an explicit unknown; no invented market research.

Incomplete is acceptable; unsupported certainty is not. Confirmed interest is product intent,
not a build commitment. An existing product gets a minimal reconcile, not a replacement file.
If the user explicitly shelves it, use `paused`; preserve the durable rationale where it
belongs. A dated feasibility assessment or temporary blocker is operational state, not truth:
use the linked tracker if it supports context; for bare todos keep a terse reassessment action
and leave the detailed assessment in the conversation. Don't invent another file convention
or schedule a review. Point out if the user wants durable evidence storage beyond this scope.

Keep tasks out of truth. Offer a small next action in the linked tracker unless its capture
was already requested; never generate an implementation backlog by default. An absent todo
file is fine. Show the saved path and a short readback distinguishing confirmed intent from
unknowns, commit as `reconcile(<product>): capture product intent`, and sync as CONNECT directs.
If the user pauses the interview after providing enough intent, save that useful partial
capture when capture was requested; don't hold it hostage to unanswered questions.
