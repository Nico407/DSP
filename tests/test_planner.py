from planner import _score, _friendly_messages


def test_score_zero_when_perfect():
    totals = {"total_kcal": 2000, "total_protein": 150, "total_fat": 60, "total_carbs": 200}
    target = {"daily_kcal": 2000, "protein": 150, "fat": 60, "carbs": 200}
    assert _score(totals, target) == 0


def test_score_sums_absolute_macro_errors():
    totals = {"total_kcal": 2000, "total_protein": 140, "total_fat": 70, "total_carbs": 195}
    target = {"daily_kcal": 2000, "protein": 150, "fat": 60, "carbs": 200}
    # |140-150| + |70-60| + |195-200| = 10 + 10 + 5
    assert _score(totals, target) == 25


def test_score_ignores_kcal_dimension():
    # kcal differs but macros match -> score 0
    totals = {"total_kcal": 9999, "total_protein": 150, "total_fat": 60, "total_carbs": 200}
    target = {"daily_kcal": 2000, "protein": 150, "fat": 60, "carbs": 200}
    assert _score(totals, target) == 0


def test_friendly_kcal_left_message():
    msgs = _friendly_messages({"kcal": 600, "protein": 0, "fat": 0, "carbs": 0})
    assert any("600 kcal left" in m for m in msgs)


def test_friendly_on_target_message():
    msgs = _friendly_messages({"kcal": 20, "protein": 0, "fat": 0, "carbs": 0})
    assert any("On target" in m for m in msgs)


def test_friendly_over_kcal_message():
    msgs = _friendly_messages({"kcal": -300, "protein": 0, "fat": 0, "carbs": 0})
    assert any("300 kcal over" in m for m in msgs)


def test_friendly_protein_short_message():
    msgs = _friendly_messages({"kcal": 0, "protein": 30, "fat": 0, "carbs": 0})
    assert any("protein" in m.lower() and "hit" in m for m in msgs)
