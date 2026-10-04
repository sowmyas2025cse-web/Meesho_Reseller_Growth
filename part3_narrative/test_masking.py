from part3_narrative.masking import (
    alias_for,
    assert_no_raw_names_leak
)


TOP_RESELLER_NAMES = [
    "Mumbai Reseller 1",
    "Mumbai Reseller 4",
    "Hyderabad Reseller 6",
    "Lucknow Reseller 6",
    "Jaipur Reseller 5",
]


FINAL_TOP_RESELLER_NARRATIVE = """
Context:
The Part 1 HAVING query identified a top reseller in the West region
with coded reseller identifier ALIAS-19.

Insight — Fact:
The coded reseller generated INR 75295.09 in total spend and was one
of the five resellers returned by the Part 1 HAVING query.

Implication — Hypothesis:
The regional manager should review this coded reseller's recent
category and order activity before deciding whether the reseller's
performance should inform regional follow-up.
"""


def test_alias_for_rs019():
    assert alias_for("RS019") == "ALIAS-19"


def test_final_narrative_has_no_raw_names():
    assert assert_no_raw_names_leak(
        FINAL_TOP_RESELLER_NARRATIVE,
        TOP_RESELLER_NAMES
    ) is True


def test_raw_name_is_detected():
    leaked_version = """
    Mumbai Reseller 1 generated INR 75295.09 in total spend.
    """

    assert assert_no_raw_names_leak(
        leaked_version,
        TOP_RESELLER_NAMES
    ) is False