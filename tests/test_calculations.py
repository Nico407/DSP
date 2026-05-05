from types import SimpleNamespace

import pytest

from calculations import (
    calculate_bmr,
    calculate_tdee,
    calculate_macros,
    build_macro_messages,
    GOAL_LABELS,
)


def make_user(sex="male", height=180, weight=80, age=30, activity_level="3"):
    return SimpleNamespace(
        name="t", sex=sex, height=height, weight=weight,
        age=age, activity_level=activity_level,
    )


# --- BMR (Mifflin-St Jeor) -------------------------------------------------

def test_bmr_male():
    # 10*80 + 6.25*180 - 5*30 + 5 = 800 + 1125 - 150 + 5 = 1780
    assert calculate_bmr(make_user()) == 1780


def test_bmr_female():
    # 10*60 + 6.25*165 - 5*25 - 161 = 600 + 1031.25 - 125 - 161 = 1345.25
    assert calculate_bmr(make_user(sex="female", weight=60, height=165, age=25)) == pytest.approx(1345.25)


# --- TDEE multipliers ------------------------------------------------------

@pytest.mark.parametrize("level,mult", [
    ("1", 1.2), ("2", 1.375), ("3", 1.55), ("4", 1.725), ("5", 1.9),
])
def test_tdee_each_level(level, mult):
    u = make_user(activity_level=level)
    assert calculate_tdee(u) == pytest.approx(1780 * mult)


def test_tdee_unknown_level_falls_back_to_sedentary():
    u = make_user(activity_level="not-a-real-level")
    assert calculate_tdee(u) == pytest.approx(1780 * 1.2)


# --- Macros ---------------------------------------------------------------

def test_macros_maintain_30yo():
    u = make_user(age=30)
    tdee = calculate_tdee(u)
    res = calculate_macros(u, tdee, "3")
    # daily kcal = tdee + 0
    assert res["daily_kcal"] == round(tdee)
    # protein = weight * 1.0
    assert res["protein"] == 80
    assert res["p_multiplier_used"] == 1.0


def test_macros_age_40_bumps_protein():
    u = make_user(age=42)
    res = calculate_macros(u, calculate_tdee(u), "3")
    # base 1.0 + 0.2 for 40+
    assert res["p_multiplier_used"] == 1.2
    assert res["protein"] == round(80 * 1.2)


def test_macros_age_50_bumps_protein_more():
    u = make_user(age=55)
    res = calculate_macros(u, calculate_tdee(u), "3")
    # base 1.0 + 0.3 for 50+
    assert res["p_multiplier_used"] == 1.3


def test_macros_strong_loss_subtracts_500():
    u = make_user()
    tdee = calculate_tdee(u)
    res = calculate_macros(u, tdee, "5")
    assert res["daily_kcal"] == round(tdee - 500)


def test_macros_unknown_goal_defaults_to_maintain():
    u = make_user()
    tdee = calculate_tdee(u)
    res_unknown = calculate_macros(u, tdee, "bogus")
    res_maintain = calculate_macros(u, tdee, "3")
    assert res_unknown == res_maintain


def test_macros_carbs_never_negative():
    # tiny target with lots of protein/fat could push remaining kcal negative
    u = make_user(weight=200, age=30)  # large protein/fat draw
    res = calculate_macros(u, 1500, "5")  # aggressive deficit
    assert res["carbs"] >= 0


# --- Friendly messages ----------------------------------------------------

def test_macro_messages_include_goal_label():
    u = make_user(age=30)
    results = {"daily_kcal": 2000, "protein": 150, "fat": 60, "carbs": 200}
    msgs = build_macro_messages(u, "4", results)
    assert any(GOAL_LABELS["4"] in m for m in msgs)
    assert any("2000 kcal" in m for m in msgs)


def test_macro_messages_age_50_mentions_anabolic_resistance():
    u = make_user(age=55)
    results = {"daily_kcal": 2000, "protein": 150, "fat": 60, "carbs": 200}
    msgs = build_macro_messages(u, "3", results)
    assert any("50+" in m or "anabolic" in m.lower() for m in msgs)


def test_macro_messages_age_40_mentions_protein_bump():
    u = make_user(age=42)
    results = {"daily_kcal": 2000, "protein": 150, "fat": 60, "carbs": 200}
    msgs = build_macro_messages(u, "3", results)
    assert any("40+" in m for m in msgs)


def test_macro_messages_young_user_no_age_bump():
    u = make_user(age=25)
    results = {"daily_kcal": 2000, "protein": 150, "fat": 60, "carbs": 200}
    msgs = build_macro_messages(u, "3", results)
    assert not any("40+" in m or "50+" in m for m in msgs)
