\# Meesho Reseller Growth Analytics \& Agent Workflow



\## 1. Project Overview



This project implements a complete local workflow for analyzing \*\*Meesho reseller and category performance\*\* and turning the analysis into controlled business insights.



The workflow is divided into four Parts:



1\. \*\*Part 1 — SQL Analytics\*\*

2\. \*\*Part 2 — Growth Engine\*\*

3\. \*\*Part 3 — Narrative Generation\*\*

4\. \*\*Part 4 — Agent Workflow\*\*



The Parts are designed to work together in sequence:



```text

Raw Dataset

&#x20;   ↓

Part 1 — SQL Analytics

&#x20;   ↓

Monthly Category Revenue

&#x20;   ↓

Part 2 — Growth Engine

&#x20;   ↓

Validation + MoM Growth + Flagging

&#x20;   ↓

Part 3 — Narrative Generation

&#x20;   ↓

Context + Insight + Implication + Privacy Masking

&#x20;   ↓

Part 4 — Agent Workflow

&#x20;   ↓

Prioritize + Draft + Suppress + Escalate

&#x20;   ↓

Structured JSON

&#x20;   ↓

Human Approval

```



The complete pipeline runs \*\*locally with ZERO API keys set\*\*. It does not require external APIs, cloud services, network access, email services, or automatic message delivery.



\---



\# 2. Project Objectives



The project is designed to:



\* Analyze reseller and order data using SQL.

\* Calculate monthly category revenue and order counts.

\* Compare category performance across months.

\* Calculate month-over-month growth.

\* Detect significant positive and negative movements.

\* Validate incoming revenue feeds before processing.

\* Handle the exact threshold boundary separately.

\* Convert important movements into understandable business narratives.

\* Protect reseller identities using coded aliases.

\* Prioritize the most significant flagged categories.

\* Generate controlled drafts for human review.

\* Produce structured JSON output from the final agent workflow.



\---



\# 3. Dataset



The project uses a seeded dataset containing:



\* \*\*24 resellers\*\*

\* \*\*900 orders\*\*

\* \*\*3 months:\*\* April, May, and June 2026

\* \*\*5 product categories\*\*

\* \*\*4 regions\*\*



The data files are:



```text

data/

├── generate\_dataset.py

├── resellers.csv

├── orders.csv

└── meesho\_reseller.db

```



\### Dataset Generation



`generate\_dataset.py` creates the seeded CSV files and SQLite database used by the project.



To regenerate the dataset:



```powershell

py data/generate\_dataset.py

```



After regeneration, the Parts should be run in the order described in the \*\*Reproduction Steps\*\* section below.



\---



\# 4. Part 1 — SQL Analytics



\## Purpose



Part 1 performs the initial business analysis using SQL.



The important principle is:



> \*\*Compute the real business numbers using SQL first, then hand those numbers to the later processing stages.\*\*



This ensures that the downstream Python workflow works with calculated analytical results rather than repeatedly processing the raw order data.



\### Files



```text

part1\_sql/

├── queries.sql

├── run\_query.py

└── output/

```



\### SQL Analysis



Part 1 calculates:



\* Monthly revenue by category

\* Monthly order counts by category

\* May vs June category changes

\* Regional revenue and order counts

\* Top resellers by spend

\* Top resellers by delivered orders

\* May top 5 resellers

\* June delivered average order value

\* Resellers with zero orders



\### Monthly Category Revenue



The output:



```text

part1\_sql/output/monthly\_category\_revenue.csv

```



contains monthly revenue and order counts for each category.



This output is particularly important because it becomes the input for the growth calculations in Part 2.



\### Regional Analysis



The output:



```text

part1\_sql/output/region\_revenue\_orders.csv

```



contains total revenue and order counts by region.



\### Reseller Analysis



The project also produces:



```text

part1\_sql/output/may\_top5\_resellers.csv

part1\_sql/output/top5\_resellers\_delivered.csv

part1\_sql/output/top\_resellers\_by\_spend.csv

```



\### June Delivered AOV



The project calculates June delivered Average Order Value:



```text

AOV = Total Delivered Revenue / Number of Delivered Orders

```



Output:



```text

part1\_sql/output/june\_delivered\_aov.csv

```



\### Zero-Order Resellers



The project identifies resellers who have no orders:



```text

part1\_sql/output/zero\_order\_resellers.csv

```



It also demonstrates the difference between:



```sql

COUNT(\*)

```



and:



```sql

COUNT(order\_id)

```



when using a `LEFT JOIN`.



For a reseller with no matching orders, `COUNT(\*)` can still count the reseller row, while `COUNT(order\_id)` correctly produces zero matching orders.



\### Running Part 1



From the project root:



```powershell

py part1\_sql/run\_query.py

```



The generated CSV results are written to:



```text

part1\_sql/output/

```



\---



\# 5. Part 2 — Growth Engine



\## Purpose



Part 2 takes the analytical numbers produced by Part 1 and applies deterministic business rules.



The main files are:



```text

part2\_engine/

├── growth\_engine.py

├── test\_growth\_engine.py

└── fixtures/

```



The growth engine performs three main tasks:



1\. Validate the incoming feed.

2\. Calculate month-over-month growth.

3\. Classify the movement using the 8% threshold.



\---



\## 5.1 Month-over-Month Growth



The growth formula is:



```text

MoM Growth (%) =

((Current Revenue - Previous Revenue) / Previous Revenue) × 100

```



The result is rounded to two decimal places.



The function responsible for this is:



```text

mom\_growth()

```



For example:



```text

Previous Revenue = 100000

Current Revenue  = 108000



MoM Growth = 8.00%

```



\---



\## 5.2 Flagging Rules



The function:



```text

is\_flagged()

```



uses an 8% threshold.



The rules are:



| Absolute MoM Growth | Result                    |

| ------------------: | ------------------------- |

|     Greater than 8% | `flagged`                 |

|        Less than 8% | `not\_flagged`             |

|          Exactly 8% | `escalate\_exact\_boundary` |



Both positive and negative movements are considered.



For example:



```text

+10% → flagged

\-10% → flagged

+5%  → not\_flagged

\-5%  → not\_flagged

+8%  → escalate\_exact\_boundary

\-8%  → escalate\_exact\_boundary

```



The function returns explicit text states rather than Boolean values.



\---



\## 5.3 Feed Validation



Before calculating growth, the input CSV is validated using:



```text

validate\_feed()

```



The validator detects:



\* Missing category

\* Missing revenue

\* Non-numeric revenue

\* Negative revenue



A valid feed returns:



```text

(True, \[])

```



An invalid feed returns:



```text

(False, \[errors])

```



The project includes both a valid fixture and a deliberately corrupted fixture:



```text

part2\_engine/fixtures/

├── monthly\_category\_revenue.csv

└── corrupted\_feed.csv

```



The corrupted fixture contains missing fields and negative revenue to verify that invalid data causes the correct validation errors.



\---



\## 5.4 Running Part 2



Run:



```powershell

py -m pytest part2\_engine -v

```



The Part 2 test suite contains \*\*7 tests\*\*.



\---



\# 6. Part 3 — Narrative Generation



\## Purpose



Part 3 converts important numerical movements into understandable business narratives.



The workflow pattern is:



> \*\*Detect → Explain\*\*



Part 2 detects important movements.



Part 3 explains those movements in a structured format.



The main files are:



```text

part3\_narrative/

├── prompt\_pack.md

├── narrative\_report.md

├── masking.py

└── test\_masking.py

```



\---



\# 7. Narrative Structure



The narrative follows:



```text

Context → Insight → Implication

```



\### Context



Explains what was measured and which periods are being compared.



\### Insight



States the important numerical observation.



Numerical observations are explicitly identified as facts.



\### Implication



Provides a specific actionable recommendation.



If a possible cause is proposed without direct evidence, it is explicitly identified as a hypothesis.



\---



\# 8. Prompt Pack



The file:



```text

part3\_narrative/prompt\_pack.md

```



contains four required sections:



1\. \*\*Trigger\*\*

2\. \*\*Input List\*\*

3\. \*\*Prompt\*\*

4\. \*\*Checklist\*\*



The narrative is triggered when the Part 2 result for a category is:



```text

flagged

```



The prompt uses supplied placeholders such as:



```text

{category}

{previous\_revenue}

{current\_revenue}

{mom\_pct}

{month}

{prev\_month}

```



The prompt also requires that the generated narrative does not introduce numerical values that were not supplied.



The checklist verifies:



\* Numerical accuracy

\* Correct category and month

\* Fact and hypothesis labeling

\* Specific recommendations

\* Privacy protection

\* Correct Context → Insight → Implication structure



\---



\# 9. Worked Narrative Examples



The narrative report demonstrates significant movement in Ethnic Wear.



\### May vs April



Ethnic Wear increased by:



```text

77.1%

```



Since the absolute movement is greater than 8%, it is flagged.



\### June vs May



Ethnic Wear decreased by:



```text

58.74%

```



This is also flagged.



These examples demonstrate that the workflow detects significant changes in both directions.



The report also evaluates the narratives against:



\* Specificity

\* Audience fit

\* Completeness

\* Actionability



\---



\# 10. Privacy Masking



The file:



```text

part3\_narrative/masking.py

```



protects reseller names in business narratives.



The function:



```text

alias\_for()

```



converts reseller IDs into coded aliases.



Examples:



```text

RS019 → ALIAS-19

RS006 → ALIAS-06

```



The project also verifies that raw reseller names do not appear in the final narrative.



This creates a simple privacy boundary between internal reseller data and generated business narratives.



\---



\# 11. Running Part 3



Run:



```powershell

py -m pytest part3\_narrative -v

```



The Part 3 test suite contains \*\*3 tests\*\*.



\---



\# 12. Part 4 — Agent Workflow



\## Purpose



Part 4 combines the analytical, validation, and narrative components into a controlled agent-style workflow.



The workflow pattern is:



> \*\*Intake → Summary → Report Draft → Validate\*\*



The main files are:



```text

part4\_agent/

├── agent\_spec.md

├── mock\_agent\_runner.py

└── test\_mock\_agent\_runner.py

```



The agent is implemented locally and deterministically.



It does not call an external AI service and does not send messages automatically.



\---



\# 13. Agent Processing Flow



The agent performs the following steps.



\### Step 1 — Intake



Load the previous-month and current-month category revenue feeds.



\### Step 2 — Validate



Validate the incoming feed using the Part 2 validation logic.



If validation fails, the agent performs a:



```text

hard\_stop

```



and does not continue to business analysis.



\### Step 3 — Calculate



Calculate month-over-month growth for every category.



\### Step 4 — Classify



Apply the 8% business rule:



```text

flagged

not\_flagged

escalate\_exact\_boundary

```



\### Step 5 — Prioritize



Sort flagged categories by absolute MoM growth in descending order.



This ensures that the largest movements are considered first.



\### Step 6 — Draft



Draft narratives for at most the top three flagged categories using the Part 3 template logic.



\### Step 7 — Suppress



Flagged categories beyond the top three are recorded as suppressed rather than drafted.



\### Step 8 — Escalate



Exact ±8% movements are recorded separately as:



```text

escalate\_exact\_boundary

```



\### Step 9 — Output



The agent produces structured JSON containing:



```text

run\_month

validation\_status

validation\_errors

flagged\_categories

suppressed\_categories

escalated\_categories

action\_taken

```



For a valid run, the action is:



```text

drafted\_and\_held\_for\_approval

```



For an invalid feed:



```text

hard\_stop

```



\---



\# 14. Agent Guardrails



\## Input Guardrails



The input feed must contain valid and processable revenue data.



Invalid or corrupted data causes a hard stop.



\## Action Guardrails



The agent:



\* Does not send emails.

\* Does not send messages.

\* Does not call external services.

\* Does not require an API key.

\* Drafts at most three flagged categories.

\* Holds drafts for human approval.



\## Output Guardrails



The output must:



\* Follow the required JSON structure.

\* Preserve numerical accuracy.

\* Distinguish facts from hypotheses.

\* Protect reseller identities.

\* Handle exact-boundary cases separately.



\---



\# 15. Human-in-the-Loop Approval



The final workflow does not automatically communicate the generated insights.



Instead, successful runs use:



```text

drafted\_and\_held\_for\_approval

```



This means the system prepares the report draft, but a human must review and approve it before any real-world communication.



This makes the workflow suitable for controlled business reporting.



\---



\# 16. Running Part 4



Run:



```powershell

py -m pytest part4\_agent -v

```



The Part 4 test suite contains \*\*4 tests\*\* covering:



\* May scenario

\* June scenario

\* Corrupted feed hard stop

\* Exact 8% boundary



\---



\# 17. Workflow Pattern Mapping



Each Part implements a specific workflow pattern.



\## Part 1 → Part 2



\*\*Pattern: Compute real numbers via SQL first, then hand off.\*\*



Part 1 performs the authoritative aggregation of the raw order data using SQL.



The resulting monthly category revenue is then handed to Part 2, which performs growth calculations and applies business rules.



This separates:



```text

Data analysis

```



from:



```text

Business-rule processing

```



\---



\## Part 2 → Part 3



\*\*Pattern: Detect → Explain.\*\*



Part 2 determines which category movements are important.



Part 3 takes those important movements and turns them into understandable business narratives.



Therefore:



```text

Part 2 = What changed?

Part 3 = How should the change be explained?

```



\---



\## Part 3 → Part 4



\*\*Pattern: Generate → Protect → Hand off.\*\*



Part 3 provides:



\* The narrative template

\* Fact/hypothesis structure

\* Actionable recommendation format

\* Reseller privacy masking



Part 4 uses these components when creating controlled report drafts.



\---



\## Part 4



\*\*Pattern: Intake → Summary → Report Draft → Validate.\*\*



The agent:



```text

Intake

&#x20; ↓

Validate input

&#x20; ↓

Summarize category movements

&#x20; ↓

Prioritize important movements

&#x20; ↓

Draft reports

&#x20; ↓

Suppress lower-priority items

&#x20; ↓

Escalate exact-boundary cases

&#x20; ↓

Validate structured output

&#x20; ↓

Hold for human approval

```



This mirrors a controlled reporting workflow rather than an unrestricted autonomous agent.



\---



\# 18. Complete Reproduction Steps



The complete project should be run in the following order.



\## Step 1 — Generate the Dataset



From the project root:



```powershell

py data/generate\_dataset.py

```



This creates/regenerates the seeded reseller and order data.



\---



\## Step 2 — Run Part 1



```powershell

py part1\_sql/run\_query.py

```



This executes the SQL analysis and produces the required CSV outputs in:



```text

part1\_sql/output/

```



\---



\## Step 3 — Run Part 2



```powershell

py -m pytest part2\_engine -v

```



This verifies:



\* Growth calculation

\* Threshold classification

\* Exact boundary behavior

\* Feed validation

\* Growth tables



\---



\## Step 4 — Run Part 3



```powershell

py -m pytest part3\_narrative -v

```



This verifies:



\* Alias generation

\* Raw-name detection

\* Final narrative privacy



\---



\## Step 5 — Run Part 4



```powershell

py -m pytest part4\_agent -v

```



This verifies:



\* Valid monthly scenarios

\* Corrupted-feed hard stop

\* Exact-boundary escalation

\* Agent output behavior



\---



\## Step 6 — Run the Complete Test Suite



After Parts 1–4 have been executed:



```powershell

py -m pytest part2\_engine part3\_narrative part4\_agent -v

```



Expected test count:



```text

Part 2 → 7 tests

Part 3 → 3 tests

Part 4 → 4 tests



Total → 14 tests

```



Expected result:



```text

14 passed

```



\---



\# 19. Zero API Key Requirement



\## The complete pipeline runs with ZERO API keys set.



No API key needs to be created, configured, or stored.



The project does not require:



\* OpenAI API keys

\* Gemini API keys

\* Other AI API keys

\* Cloud credentials

\* Network access

\* External APIs

\* Email credentials

\* Messaging credentials



All processing is performed locally using the project files, Python, SQL/SQLite, and pytest.



\---



\# 20. Final Project Structure



```text

Meesho\_Reseller\_Growth/

│

├── README.md

│

├── data/

│   ├── generate\_dataset.py

│   ├── resellers.csv

│   ├── orders.csv

│   └── meesho\_reseller.db

│

├── part1\_sql/

│   ├── queries.sql

│   ├── run\_query.py

│   └── output/

│       ├── june\_delivered\_aov.csv

│       ├── may\_june\_category\_change.csv

│       ├── may\_top5\_resellers.csv

│       ├── monthly\_category\_revenue.csv

│       ├── region\_revenue\_orders.csv

│       ├── top5\_resellers\_delivered.csv

│       ├── top\_resellers\_by\_spend.csv

│       ├── zero\_order\_count\_demo.csv

│       └── zero\_order\_resellers.csv

│

├── part2\_engine/

│   ├── growth\_engine.py

│   ├── test\_growth\_engine.py

│   └── fixtures/

│       ├── corrupted\_feed.csv

│       └── monthly\_category\_revenue.csv

│

├── part3\_narrative/

│   ├── prompt\_pack.md

│   ├── narrative\_report.md

│   ├── masking.py

│   └── test\_masking.py

│

└── part4\_agent/

&#x20;   ├── agent\_spec.md

&#x20;   ├── mock\_agent\_runner.py

&#x20;   └── test\_mock\_agent\_runner.py

```



\---



\# 21. Final Summary



The project implements a complete progression:



```text

Raw Data

&#x20;  ↓

SQL Analytics

&#x20;  ↓

Validated Growth Metrics

&#x20;  ↓

Business Narratives

&#x20;  ↓

Agent Prioritization

&#x20;  ↓

Structured Report Draft

&#x20;  ↓

Human Approval

```



The key workflow patterns are:



\* \*\*Part 1 → Part 2:\*\* Compute real numbers via SQL first, then hand off.

\* \*\*Part 2 → Part 3:\*\* Detect important movements, then explain them.

\* \*\*Part 3 → Part 4:\*\* Generate structured narratives while protecting sensitive reseller names.

\* \*\*Part 4:\*\* Intake → Summary → Report Draft → Validate, with human approval before external action.



The complete pipeline is locally reproducible and runs with \*\*zero API keys set\*\*.

\# 22. Academic Integrity and Documentation References



This project is individual work.



During implementation, official Python standard-library documentation was used as a reference where needed, particularly for Python file handling, CSV processing, SQLite/database access, and JSON processing.



Referenced official Python documentation:



\* Python `csv` module documentation

\* Python `sqlite3` module documentation

\* Python `json` module documentation

\* Python `pathlib` module documentation

\* Python `unittest`/testing-related standard-library documentation where applicable



All project logic and implementation files in this repository are part of the submitted project.



No paid service, API key, hosted AI service, or account-gated service is required.



\---



\# 23. Part-to-Part Data Flow



The Parts are connected through concrete outputs rather than being independent exercises.



```text

Part 1

SQL queries

&#x20;   ↓

part1\_sql/output/monthly\_category\_revenue.csv

&#x20;   ↓

Part 2

Growth Engine

&#x20;   ↓

Validated feed + MoM growth + flagging

&#x20;   ↓

Part 3

Narrative templates and privacy masking

&#x20;   ↓

Part 4

Agent runner

&#x20;   ↓

Prioritized structured report draft

```



Specifically:



\* \*\*Part 1's SQL output feeds Part 2's growth engine.\*\*

\* \*\*Part 2's engine provides the flagged category movements used by Part 3's narrative templates.\*\*

\* \*\*Part 2's validation and growth logic is also reused by Part 4's agent runner.\*\*

\* \*\*Part 3's narrative/template logic is used by Part 4 when creating report drafts.\*\*

\* \*\*Part 4 combines the earlier Parts into a controlled workflow with validation, prioritization, suppression, escalation, and human approval.\*\*



The entire workflow can therefore be reproduced locally from dataset generation through final agent output without an external AI service.



