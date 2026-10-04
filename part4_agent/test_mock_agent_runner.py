from pathlib import Path

from part4_agent.mock_agent_runner import run
from part2_engine.growth_engine import mom_growth, is_flagged


PROJECT_ROOT = Path(__file__).resolve().parent.parent

FIXTURES = PROJECT_ROOT / "part2_engine" / "fixtures"


def test_may_scenario():
    # The Part 1 fixture contains all three months.
    # We create temporary month-specific CSV files.
    # The original Part 1 data is not modified.
    import csv
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        april_file = temp_path / "April.csv"
        may_file = temp_path / "May.csv"

        with open(
            FIXTURES / "monthly_category_revenue.csv",
            newline="",
            encoding="utf-8"
        ) as source:

            reader = csv.DictReader(source)
            rows = list(reader)

        april_rows = [
            row for row in rows
            if row["month"] == "April"
        ]

        may_rows = [
            row for row in rows
            if row["month"] == "May"
        ]

        fieldnames = [
            "month",
            "category",
            "revenue",
            "n_orders"
        ]

        with open(
            april_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(april_rows)

        with open(
            may_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(may_rows)

        result = run(
            "May",
            str(april_file),
            str(may_file)
        )

        assert result["validation_status"] == "valid"

        flagged = result["flagged_categories"]

        # Exactly the top 3 flagged categories are drafted.
        assert len(flagged) == 3

        assert [
            item["category"] for item in flagged
        ] == [
            "Ethnic Wear",
            "Western Wear",
            "Kids Wear",
        ]

        assert [
            item["mom_pct"] for item in flagged
        ] == [
            77.1,
            -23.6,
            -23.48,
        ]

        assert all(
            item["drafted"] is True
            for item in flagged
        )

        # Every drafted message must contain
        # its category and exact MoM percentage.
        for item in flagged:
            assert item["category"] in item["message"]
            assert f"{item['mom_pct']}%" in item["message"]

        # Remaining flagged categories are suppressed.
        assert set(result["suppressed_categories"]) == {
            "Beauty & Personal Care",
            "Home & Kitchen",
        }

        # No exact-boundary categories.
        assert result["escalated_categories"] == []

        assert result["action_taken"] == (
            "drafted_and_held_for_approval"
        )


def test_june_scenario():

    import csv
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        may_file = temp_path / "May.csv"
        june_file = temp_path / "June.csv"

        with open(
            FIXTURES / "monthly_category_revenue.csv",
            newline="",
            encoding="utf-8"
        ) as source:

            reader = csv.DictReader(source)
            rows = list(reader)

        may_rows = [
            row for row in rows
            if row["month"] == "May"
        ]

        june_rows = [
            row for row in rows
            if row["month"] == "June"
        ]

        fieldnames = [
            "month",
            "category",
            "revenue",
            "n_orders"
        ]

        with open(
            may_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(may_rows)

        with open(
            june_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(june_rows)

        result = run(
            "June",
            str(may_file),
            str(june_file)
        )

        assert result["validation_status"] == "valid"

        flagged = result["flagged_categories"]

        # Exactly the top 3 flagged categories are drafted.
        assert len(flagged) == 3

        assert [
            item["category"] for item in flagged
        ] == [
            "Ethnic Wear",
            "Home & Kitchen",
            "Kids Wear",
        ]

        assert [
            item["mom_pct"] for item in flagged
        ] == [
            -58.74,
            42.59,
            23.9,
        ]

        assert all(
            item["drafted"] is True
            for item in flagged
        )

        # Every drafted message must contain
        # its category and exact MoM percentage.
        for item in flagged:
            assert item["category"] in item["message"]
            assert f"{item['mom_pct']}%" in item["message"]

        # Western Wear is the fourth flagged category,
        # so it must be suppressed.
        assert result["suppressed_categories"] == [
            "Western Wear"
        ]

        # Beauty & Personal Care has only 5.67% growth,
        # so it must appear nowhere in the flagged
        # or suppressed categories.
        assert "Beauty & Personal Care" not in [
            item["category"]
            for item in flagged
        ]

        assert (
            "Beauty & Personal Care"
            not in result["suppressed_categories"]
        )

        assert result["escalated_categories"] == []

        assert result["action_taken"] == (
            "drafted_and_held_for_approval"
        )


def test_corrupted_feed_hard_stop():

    corrupted_csv = (
        FIXTURES / "corrupted_feed.csv"
    )

    result = run(
        "July",
        str(FIXTURES / "monthly_category_revenue.csv"),
        str(corrupted_csv)
    )

    # Invalid feed must cause a hard stop.
    assert result["validation_status"] == "invalid"

    assert result["action_taken"] == "hard_stop"

    # No agent processing should happen after validation fails.
    assert result["flagged_categories"] == []

    assert result["suppressed_categories"] == []

    assert result["escalated_categories"] == []

    # Exactly the 3 expected validation errors.
    assert result["validation_errors"] == [
        "line 3: negative revenue (-4200.0) "
        "for category=Western Wear",

        "line 4: missing category (month=July)",

        "line 6: missing revenue "
        "(category=Home & Kitchen)",
    ]


def test_exact_boundary():

    import csv
    import tempfile

    # Part 2 boundary calculation.
    # 100000 -> 108000 = exactly 8%.
    assert mom_growth(
        100000,
        108000
    ) == 8.0

    assert is_flagged(8.0) == (
        "escalate_exact_boundary"
    )

    # Also verify the actual Part 4 agent runner.
    # An exact 8% category must be escalated,
    # not drafted and not suppressed.
    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        previous_file = temp_path / "previous.csv"
        current_file = temp_path / "current.csv"

        fieldnames = [
            "month",
            "category",
            "revenue",
            "n_orders"
        ]

        previous_rows = [
            ["Previous", "Test Category", "100000", "100"]
        ]

        current_rows = [
            ["Current", "Test Category", "108000", "100"]
        ]

        with open(
            previous_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)
            writer.writerow(fieldnames)
            writer.writerows(previous_rows)

        with open(
            current_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)
            writer.writerow(fieldnames)
            writer.writerows(current_rows)

        result = run(
            "Current",
            str(previous_file),
            str(current_file)
        )

        assert result["validation_status"] == "valid"

        assert result["escalated_categories"] == [
            "Test Category"
        ]

        assert result["flagged_categories"] == []

        assert result["suppressed_categories"] == []

        assert result["action_taken"] == (
            "drafted_and_held_for_approval"
        )