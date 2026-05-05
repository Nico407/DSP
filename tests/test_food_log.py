from food_log import daily_messages


def test_empty_day_message():
    msgs = daily_messages({"kcal": 2200, "protein": 150, "fat": 70, "carbs": 240}, num_logs=0)
    assert len(msgs) == 1
    assert "Nothing logged" in msgs[0]


def test_on_target_within_50_kcal():
    msgs = daily_messages({"kcal": 30, "protein": 0, "fat": 0, "carbs": 0}, num_logs=3)
    assert any("on target" in m.lower() for m in msgs)


def test_kcal_remaining_message():
    msgs = daily_messages({"kcal": 600, "protein": 0, "fat": 0, "carbs": 0}, num_logs=2)
    assert any("600 kcal left" in m for m in msgs)


def test_over_kcal_message():
    msgs = daily_messages({"kcal": -200, "protein": 0, "fat": 0, "carbs": 0}, num_logs=4)
    assert any("200 kcal over" in m for m in msgs)


def test_protein_short_nudge():
    msgs = daily_messages({"kcal": 600, "protein": 50, "fat": 0, "carbs": 0}, num_logs=2)
    assert any("protein" in m.lower() and "to go" in m for m in msgs)


def test_protein_over_nudge():
    msgs = daily_messages({"kcal": 0, "protein": -40, "fat": 0, "carbs": 0}, num_logs=2)
    assert any("protein" in m.lower() and "over" in m.lower() for m in msgs)


def test_protein_within_threshold_no_nudge():
    msgs = daily_messages({"kcal": 0, "protein": 5, "fat": 0, "carbs": 0}, num_logs=2)
    # Only the "on target" line, no protein nudge
    assert not any("protein" in m.lower() for m in msgs)
