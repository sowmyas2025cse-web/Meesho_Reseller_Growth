from part2_engine.growth_engine import mom_growth, is_flagged, validate_feed


def test_ethnic_wear_may_growth():
    # GIVEN April -> May Ethnic Wear revenue
    previous = 104520.77
    current = 185107.61

    # WHEN evaluated
    growth = mom_growth(previous, current)

    # THEN
    assert growth == 77.1
    assert is_flagged(growth) == "flagged"


def test_beauty_personal_care_june_growth():
    # GIVEN May -> June Beauty & Personal Care revenue
    previous = 35542.11
    current = 37559.07

    # WHEN evaluated
    growth = mom_growth(previous, current)

    # THEN
    assert growth == 5.67
    assert is_flagged(growth) == "not_flagged"


def test_exact_boundary():
    # GIVEN exactly 8% growth
    previous = 100000
    current = 108000

    # WHEN evaluated
    growth = mom_growth(previous, current)

    # THEN
    assert growth == 8.0
    assert is_flagged(growth) == "escalate_exact_boundary"


def test_corrupted_feed():
    # GIVEN corrupted feed
    result, errors = validate_feed(
        "part2_engine/fixtures/corrupted_feed.csv"
    )

    # THEN validation fails with exactly 3 errors
    assert result is False

    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]


def test_valid_part1_feed():
    # GIVEN the valid Part 1 feed
    result, errors = validate_feed(
        "part2_engine/fixtures/monthly_category_revenue.csv"
    )

    # THEN validation passes
    assert result is True
    assert errors == []


def test_may_growth_table():
    # GIVEN Part 1 revenue values
    april = {
        "Ethnic Wear": 104520.77,
        "Western Wear": 113866.15,
        "Kids Wear": 59847.27,
        "Home & Kitchen": 100446.23,
        "Beauty & Personal Care": 40737.01,
    }

    may = {
        "Ethnic Wear": 185107.61,
        "Western Wear": 86998.18,
        "Kids Wear": 45793.78,
        "Home & Kitchen": 91152.57,
        "Beauty & Personal Care": 35542.11,
    }

    expected = {
        "Ethnic Wear": 77.1,
        "Western Wear": -23.6,
        "Kids Wear": -23.48,
        "Home & Kitchen": -9.25,
        "Beauty & Personal Care": -12.75,
    }

    for category in april:
        growth = mom_growth(april[category], may[category])
        assert growth == expected[category]
        assert is_flagged(growth) == "flagged"


def test_june_growth_table():
    # GIVEN Part 1 revenue values
    may = {
        "Ethnic Wear": 185107.61,
        "Western Wear": 86998.18,
        "Kids Wear": 45793.78,
        "Home & Kitchen": 91152.57,
        "Beauty & Personal Care": 35542.11,
    }

    june = {
        "Ethnic Wear": 76371.53,
        "Western Wear": 97415.64,
        "Kids Wear": 56737.78,
        "Home & Kitchen": 129971.22,
        "Beauty & Personal Care": 37559.07,
    }

    expected = {
        "Ethnic Wear": -58.74,
        "Western Wear": 11.97,
        "Kids Wear": 23.9,
        "Home & Kitchen": 42.59,
        "Beauty & Personal Care": 5.67,
    }

    for category in may:
        growth = mom_growth(may[category], june[category])
        assert growth == expected[category]

        if category == "Beauty & Personal Care":
            assert is_flagged(growth) == "not_flagged"
        else:
            assert is_flagged(growth) == "flagged"