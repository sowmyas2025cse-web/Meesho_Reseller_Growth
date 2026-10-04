# Part 4 — Agentic Workflow Specification

## 4.1 Agent Specification

### Goal

Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with every drafted message held for human approval before it is considered sent.

### Tools

The monitoring agent uses the following project functions:

* `validate_feed` from Part 2 — validates the current monthly revenue feed before any other processing.
* `mom_growth` from Part 2 — calculates month-on-month revenue growth.
* `is_flagged` from Part 2 — classifies the growth result as `flagged`, `not_flagged`, or `escalate_exact_boundary`.
* Part 3 prompt-pack template-fill logic — creates a stakeholder narrative from the supplied category, revenue, month, previous month, and MoM values without inventing numbers.

### Memory / State

Between runs, the agent must retain or receive the previous month's revenue per category so that the current month's revenue can be compared against the correct previous month. The current run also maintains the flagged, suppressed, and escalated category lists.

### Planner

The agent follows these ordered subtasks:

1. Load the monthly revenue feed and run `validate_feed`.
2. If validation fails, Hard Stop and report all validation errors.
3. If validation succeeds, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by `abs(mom_pct)` in descending order.
6. Draft a message using the Part 3 prompt-pack template for at most the top 3 flagged categories.
7. Log any remaining flagged categories beyond the top-3 cap as `suppressed, review manually` without drafting a message.
   7b. Separately log every category whose result is `escalate_exact_boundary` into `escalated_categories` without drafting a message.
8. Emit one structured JSON object for the run.

### Feedback Loop

Every drafted message is held for human approval. The mock runner does not send email, call an external service, or automatically deliver a message. A drafted message is considered only a proposed action until a human approves it.

## Guardrails

### Input Guardrail

`validate_feed` must pass before any MoM calculation, flag classification, sorting, or message drafting occurs. An invalid feed causes an immediate Hard Stop.

### Action Guardrail

No message is ever automatically sent. Messages are only drafted and held for human approval.

### Output Guardrail

Every number in a drafted message must trace directly to a Part 1 or Part 2 value supplied to the workflow. The agent must not invent, estimate, or introduce unsupported numerical figures.

## Success and Error Stopping Conditions

### Success

A run succeeds when the feed is valid and the agent produces the correctly ordered drafts, or correctly produces zero drafts when no category crosses the threshold. Every number in every drafted message must be traceable to a Part 1 or Part 2 value.

### Error / Hard Stop

If `validate_feed` returns `False`, the agent performs a Hard Stop. The validation errors are surfaced in `validation_errors`. No MoM computation or message drafting is attempted.

## Required Given-When-Then Agent Specifications

1. **GIVEN** April→May Ethnic Wear revenue moves from 104520.77 to 185107.61, **WHEN** `mom_growth` then `is_flagged` run on it, **THEN** `mom_growth` returns `77.1` and `is_flagged` returns `"flagged"`.

2. **GIVEN** May→June Beauty & Personal Care revenue moves from 35542.11 to 37559.07, **WHEN** evaluated, **THEN** `mom_growth` returns `5.67` and `is_flagged` returns `"not_flagged"`.

3. **GIVEN** a synthetic pair `previous=100000, current=108000` (chosen so the growth is exactly on the threshold boundary), **WHEN** evaluated, **THEN** `mom_growth` returns exactly `8.0` and `is_flagged` returns `"escalate_exact_boundary"` — not `"flagged"` and not `"not_flagged"`.

4. **GIVEN** the corrupted feed fixture below, **WHEN** `validate_feed` runs on it, **THEN** it returns `(False, errors)` where `errors` has **exactly 3** entries, matching (in order): the negative-revenue row, the missing-category row, and the missing-revenue row.

## 4.2 Ordered Workflow

The planner processes one run in the following order:

1. Load and validate the current feed.
2. Hard Stop if validation fails.
3. Calculate MoM growth for every category.
4. Classify every category using `is_flagged`.
5. Sort flagged categories by absolute MoM percentage in descending order.
6. Draft messages for at most the top 3 flagged categories.
7. Suppress additional flagged categories and log them for manual review.
   7b. Record exact-boundary categories separately in `escalated_categories`.
8. Emit one structured JSON object.

## 4.3 Output Contract

Every run emits exactly one JSON object with these top-level fields:

* `run_month`
* `validation_status`
* `validation_errors`
* `flagged_categories`
* `suppressed_categories`
* `escalated_categories`
* `action_taken`

For a valid run, `action_taken` is:

`"drafted_and_held_for_approval"`

For an invalid run, `action_taken` is:

`"hard_stop"`
