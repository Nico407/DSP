from types import SimpleNamespace

from recipes import compute_totals, scale_recipe


def make_ingredient(name, kcal, p, f, c):
    return SimpleNamespace(
        name=name, kcal_per_100g=kcal,
        protein_per_100g=p, fat_per_100g=f, carbs_per_100g=c,
    )


def make_item(ingredient, grams, ingredient_id=1):
    return SimpleNamespace(ingredient=ingredient, ingredient_id=ingredient_id, grams=grams)


def make_recipe(items, name="t", id=1, servings=1, instructions=None):
    return SimpleNamespace(items=items, id=id, name=name, servings=servings, instructions=instructions)


def test_totals_sums_per_100g_correctly():
    chicken = make_ingredient("chicken", 165, 31, 3.6, 0)
    rice = make_ingredient("rice", 130, 2.7, 0.3, 28)
    recipe = make_recipe([
        make_item(chicken, 200, 1),
        make_item(rice, 150, 2),
    ])
    t = compute_totals(recipe)
    # chicken: 165*2 + rice: 130*1.5 = 330 + 195 = 525
    assert t["total_kcal"] == 525.0
    # protein: 31*2 + 2.7*1.5 = 62 + 4.05 = 66.05 (banker's rounding -> 66.0)
    assert t["total_protein"] == 66.0


def test_totals_empty_recipe():
    recipe = make_recipe([])
    t = compute_totals(recipe)
    assert t == {"total_kcal": 0, "total_protein": 0, "total_fat": 0, "total_carbs": 0}


def test_scale_by_target_kcal_doubles_when_target_doubled():
    chicken = make_ingredient("chicken", 165, 31, 3.6, 0)
    recipe = make_recipe([make_item(chicken, 100, 1)])
    # base totals: 165 kcal — request 330 -> factor 2
    out = scale_recipe(recipe, target_kcal=330)
    assert out["scale_factor"] == 2.0
    assert out["items"][0]["grams"] == 200.0
    assert out["total_kcal"] == 330.0


def test_scale_by_target_protein():
    chicken = make_ingredient("chicken", 165, 31, 3.6, 0)
    recipe = make_recipe([make_item(chicken, 100, 1)])
    # base protein 31 g, target 62 -> factor 2
    out = scale_recipe(recipe, target_protein=62)
    assert out["scale_factor"] == 2.0


def test_scale_no_target_returns_factor_one():
    chicken = make_ingredient("chicken", 165, 31, 3.6, 0)
    recipe = make_recipe([make_item(chicken, 100, 1)])
    out = scale_recipe(recipe)
    assert out["scale_factor"] == 1.0


def test_scale_kcal_takes_precedence_over_protein():
    chicken = make_ingredient("chicken", 165, 31, 3.6, 0)
    recipe = make_recipe([make_item(chicken, 100, 1)])
    out = scale_recipe(recipe, target_kcal=330, target_protein=999)
    # kcal-based factor 2 wins
    assert out["scale_factor"] == 2.0
