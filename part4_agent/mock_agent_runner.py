import csv
import json
import sys
from pathlib import Path

# Allow this file to import Part 2 functions.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from part2_engine.growth_engine import (
    validate_feed,
    mom_growth,
    is_flagged,
)


def fill_prompt_template(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str,
) -> str:
    """
    Part 3 prompt-pack template-fill logic.

    Only supplied values are used in the drafted message.
    """

    return (
        f"Context: {category} revenue is being compared from "
        f"{prev_month} to {month}.\n"
        f"Insight — Fact: {category} revenue moved from "
        f"INR {previous_revenue} in {prev_month} to "
        f"INR {current_revenue} in {month}, with a month-on-month "
        f"change of {mom_pct}%.\n"
        f"Implication — Hypothesis: Review {category} order volume "
        f"and reseller activity for the affected period before "
        f"taking follow-up action."
    )


def load_revenue_by_category(
    csv_path: str
) -> tuple[str, dict[str, float]]:
    """
    Load the month name and revenue for each category
    from a monthly CSV file.
    """

    revenue_by_category = {}
    month_name = ""

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            month_name = row["month"]
            revenue_by_category[row["category"]] = float(
                row["revenue"]
            )

    return month_name, revenue_by_category


def run(
    month: str,
    previous_month_csv: str,
    current_month_csv: str,
) -> dict:
    """
    Run the complete mock monitoring agent workflow.
    """

    # 1. Validate the current feed before anything else.
    is_valid, validation_errors = validate_feed(
        current_month_csv
    )

    # 2. Hard Stop if the feed is invalid.
    if not is_valid:
        result = {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

        print(json.dumps(result, indent=2))
        return result

    # 3. Load previous and current month revenue.
    prev_month, previous_revenue = load_revenue_by_category(
        previous_month_csv
    )

    current_month, current_revenue = load_revenue_by_category(
        current_month_csv
    )

    flagged = []
    suppressed = []
    escalated = []

    # 4. Compute MoM and classify every category.
    for category, current_value in current_revenue.items():

        previous_value = previous_revenue[category]

        mom_pct = mom_growth(
            previous_value,
            current_value
        )

        status = is_flagged(mom_pct)

        if status == "flagged":

            flagged.append({
                "category": category,
                "mom_pct": mom_pct,
                "previous_revenue": previous_value,
                "current_revenue": current_value,
            })

        elif status == "escalate_exact_boundary":

            # Exact 8% boundary is handled separately.
            escalated.append(category)

    # 5. Sort flagged categories by absolute MoM
    # magnitude in descending order.
    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True
    )

    # 6. Draft messages for at most the top 3.
    drafted_flagged = []

    for index, item in enumerate(flagged):

        if index < 3:

            item["drafted"] = True

            item["message"] = fill_prompt_template(
                category=item["category"],
                previous_revenue=item["previous_revenue"],
                current_revenue=item["current_revenue"],
                mom_pct=item["mom_pct"],
                month=month,
                prev_month=prev_month,
            )

            drafted_flagged.append(item)

        else:

            # 7. Suppress additional flagged categories.
            suppressed.append(item["category"])

    # 8. Emit one structured JSON object.
    result = {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted_flagged,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }

    print(json.dumps(result, indent=2))

    return result