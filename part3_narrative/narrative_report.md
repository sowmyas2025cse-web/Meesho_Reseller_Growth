# Part 3 — Reliable AI Narrative & Prompt-Pack Report

## 3.2 Worked Narrative Reports

### May — Ethnic Wear

**Context:**
This measures Ethnic Wear revenue from April to May.

**Insight — Fact:**
Ethnic Wear revenue increased from INR 104520.77 in April to INR 185107.61 in May, producing a month-on-month growth of exactly 77.1%. Part 2 classifies this movement as flagged.

**Implication — Hypothesis:**
A practical next step is to check May's Ethnic Wear order volume and reseller activity against April and review whether the increase was concentrated in particular regions or resellers. A possible explanation could be increased demand or stronger reseller activity, but the available revenue data alone does not prove the cause.

### June — Ethnic Wear

**Context:**
This measures Ethnic Wear revenue from May to June.

**Insight — Fact:**
Ethnic Wear revenue decreased from INR 185107.61 in May to INR 76371.53 in June, producing a month-on-month change of exactly -58.74%. Part 2 classifies this movement as flagged.

**Implication — Hypothesis:**
A practical next step is to check June's Ethnic Wear order volume and reseller activity against May and identify whether the decline was concentrated in particular regions or resellers. A possible explanation could be weaker demand or reduced reseller activity, but the available revenue data alone does not prove the cause.

## Narrative Self-Score

### Specificity — Pass

The narratives identify the exact category, comparison months, revenue values, and required MoM percentages of 77.1% and -58.74%.

### Audience Fit — Pass

The narratives focus on business meaning and concrete actions for a regional manager rather than implementation details for a data engineer.

### Completeness — Pass

Both narratives contain Context, an explicitly labelled Fact-based Insight, and an actionable Implication.

### Actionability — Pass

Both narratives recommend checking order volume, reseller activity, and regional or reseller concentration rather than giving a vague instruction to investigate the category.

---

## 3.3 Chart-Choice Justification

### 1. Which month had the highest total revenue?

**Recommended chart: Column chart.**

This is a univariate comparison of total revenue across the three months, with month as the categorical dimension and revenue as the measured value. A column chart makes the highest month immediately visible within 10 seconds. The y-axis should start at zero so the differences are not exaggerated, and no 3D effect is needed. Because there is only one series, a legend is unnecessary. The supplied totals are April = INR 419417.43, May = INR 444594.25, and June = INR 398055.24, so the chart directly supports comparison of the three monthly totals.

### 2. What percentage share does Ethnic Wear represent of April's total revenue?

**Recommended chart: Donut chart.**

This is a univariate part-to-whole question: Ethnic Wear's April revenue of INR 104520.77 represents 24.92% of April's total revenue of INR 419417.43. A donut chart communicates a single category's share of a whole quickly and clearly. It should remain a simple 2-part visual rather than using unnecessary 3D effects. Since there are not multiple data series, a legend is not required if the segments are directly labelled.

### 3. How do the four regions compare on total revenue?

**Recommended chart: Horizontal bar chart.**

This is a univariate comparison across the categorical dimension of region and the measured value of total revenue. A horizontal bar chart allows North, West, South, and East to be compared quickly using a common zero baseline. The y-axis/value axis should start at zero, 3D should be avoided, and a legend is unnecessary because there is only one revenue series. The Part 1 totals are North = INR 337125.46, West = INR 333106.33, South = INR 316736.68, and East = INR 275098.45.

---

## 3.4 Masked Top-Reseller Narrative

**Context:**
The Part 1 `HAVING` query identified a top reseller in the West region with coded reseller identifier `ALIAS-19`.

**Insight — Fact:**
The coded reseller generated INR 75295.09 in total spend and was one of the five resellers returned by the Part 1 `HAVING` query.

**Implication — Hypothesis:**
The regional manager should review this coded reseller's recent category and order activity before deciding whether the reseller's performance should inform regional follow-up. Any explanation for the reseller's spend should be treated as a hypothesis unless supported by additional data.

This narrative intentionally references the reseller only through its region and coded alias. It does not expose the raw reseller name.
