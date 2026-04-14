from itertools import permutations
from models import Recipe
from recipes import compute_totals, scale_recipe

DEFAULT_SPLITS = {
    1: [1.0],
    2: [0.5, 0.5],
    3: [0.3, 0.4, 0.3],
    4: [0.25, 0.35, 0.25, 0.15],
}
MEAL_NAMES = ["breakfast", "lunch", "dinner", "snack"]


def _matches_diet(recipe, required_tags):
    if not required_tags:
        return True
    return all(
        all(req in {t.name for t in item.ingredient.tags} for req in required_tags)
        for item in recipe.items
    )


def _score(totals, target):
    # Lower is better. Kcal error has smaller unit scale, so weight macros equally.
    return (
        abs(totals["total_protein"] - target["protein"])
        + abs(totals["total_fat"]     - target["fat"])
        + abs(totals["total_carbs"]   - target["carbs"])
    )


def build_plans(db, target, diet=None, meals=3, split=None, top_n=2):
    required = [t.strip() for t in diet.split(",")] if diet else []
    split = split or DEFAULT_SPLITS.get(meals, [1.0 / meals] * meals)
    if len(split) != meals:
        raise ValueError("split length must equal meals count")

    candidates = [
        r for r in db.query(Recipe).all()
        if _matches_diet(r, required) and compute_totals(r)["total_kcal"] > 0
    ]
    if len(candidates) < meals:
        return {
            "error": f"Not enough recipes matching diet (have {len(candidates)}, need {meals}).",
            "plans": [],
        }

    meal_kcal = [target["daily_kcal"] * s for s in split]

    # Enumerate permutations of `meals` distinct recipes. Each permutation assigns
    # a recipe to a slot, so order matters (recipe A at breakfast != at dinner).
    scored = []
    for combo in permutations(candidates, meals):
        scaled = [scale_recipe(r, target_kcal=meal_kcal[i]) for i, r in enumerate(combo)]
        totals = {
            "total_kcal":    round(sum(s["total_kcal"]    for s in scaled), 1),
            "total_protein": round(sum(s["total_protein"] for s in scaled), 1),
            "total_fat":     round(sum(s["total_fat"]     for s in scaled), 1),
            "total_carbs":   round(sum(s["total_carbs"]   for s in scaled), 1),
        }
        scored.append((_score(totals, target), combo, scaled, totals))

    scored.sort(key=lambda x: x[0])

    # Keep plans with distinct recipe *sets* so the top-N aren't reorderings.
    plans = []
    seen_sets = set()
    for score, combo, scaled, totals in scored:
        key = frozenset(r.id for r in combo)
        if key in seen_sets:
            continue
        seen_sets.add(key)
        plans.append({
            "score": round(score, 1),
            "meals": [
                {"slot": MEAL_NAMES[i] if i < len(MEAL_NAMES) else f"meal_{i+1}",
                 "recipe": s}
                for i, s in enumerate(scaled)
            ],
            "totals": totals,
            "leftover": {
                "kcal":    round(target["daily_kcal"] - totals["total_kcal"], 1),
                "protein": round(target["protein"]    - totals["total_protein"], 1),
                "fat":     round(target["fat"]        - totals["total_fat"], 1),
                "carbs":   round(target["carbs"]      - totals["total_carbs"], 1),
            },
        })
        if len(plans) >= top_n:
            break
    return {"target": target, "plans": plans}
