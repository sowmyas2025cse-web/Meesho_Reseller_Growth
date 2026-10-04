# Reusable Prompt Pack

## Trigger

Start this prompt when a category's `is_flagged` result is `"flagged"` based on the Part 2 growth-detection rule.

## Input list

The prompt requires these placeholder variables:

* `{category}` — the category name.
* `{previous_revenue}` — revenue for the previous month.
* `{current_revenue}` — revenue for the current month.
* `{mom_pct}` — calculated month-on-month percentage.
* `{month}` — current month.
* `{prev_month}` — previous month, used to name the comparison explicitly, such as "May vs. April".

## Prompt

Write a concise stakeholder update for a regional manager using the Context → Insight → Implication structure.

Context: State what category is being measured and the comparison period using `{category}`, `{month}`, and `{prev_month}`.

Insight: State the supplied revenue values `{previous_revenue}` and `{current_revenue}` and the supplied month-on-month result `{mom_pct}`. Label this section explicitly as a fact.

Implication: Give one specific and actionable next step for the regional manager. If a possible cause is proposed that is not directly proven by the supplied data, label it explicitly as a hypothesis.

Use only the supplied placeholder values. Never invent, calculate, estimate, round, or introduce any number that is not one of the supplied placeholders. Do not introduce unsupported causes as facts. Keep the language suitable for a regional manager rather than a technical audience.

## Checklist

Before the narrative is used, verify all of the following:

1. Every number in the draft matches one of the supplied placeholder values exactly, except for numbers that are part of an alias identifier.
2. The category, current month, and previous month exactly match the supplied placeholders.
3. The Insight section explicitly labels the numerical observation as a fact.
4. Any proposed cause that is not proven by the supplied data is explicitly labeled as a hypothesis.
5. The Implication contains a specific, actionable next step rather than a vague instruction.
6. No raw reseller name appears in an external-facing narrative; reseller references use the approved coded alias and region only.
7. The narrative contains Context, Insight, and Implication sections in that order.
