def compute_totals(recipe):
    kcal = protein = fat = carbs = 0.0
    for item in recipe.items:
        factor = item.grams / 100.0
        ing = item.ingredient
        kcal    += ing.kcal_per_100g    * factor
        protein += ing.protein_per_100g * factor
        fat     += ing.fat_per_100g     * factor
        carbs   += ing.carbs_per_100g   * factor
    return {
        "total_kcal":    round(kcal, 1),
        "total_protein": round(protein, 1),
        "total_fat":     round(fat, 1),
        "total_carbs":   round(carbs, 1),
    }


def serialize_recipe(recipe):
    totals = compute_totals(recipe)
    return {
        "id": recipe.id,
        "name": recipe.name,
        "servings": recipe.servings,
        "instructions": recipe.instructions,
        "items": [
            {
                "ingredient_id": it.ingredient_id,
                "ingredient_name": it.ingredient.name,
                "grams": it.grams,
            }
            for it in recipe.items
        ],
        **totals,
    }


# Scale all ingredient grams by `factor` so the recipe hits a target macro.
# Returns a dict shaped like serialize_recipe but with scaled grams + totals.
def scale_recipe(recipe, target_kcal=None, target_protein=None):
    totals = compute_totals(recipe)

    if target_kcal is not None and totals["total_kcal"] > 0:
        factor = target_kcal / totals["total_kcal"]
    elif target_protein is not None and totals["total_protein"] > 0:
        factor = target_protein / totals["total_protein"]
    else:
        factor = 1.0

    scaled_items = [
        {
            "ingredient_id": it.ingredient_id,
            "ingredient_name": it.ingredient.name,
            "grams": round(it.grams * factor, 1),
        }
        for it in recipe.items
    ]
    return {
        "id": recipe.id,
        "name": recipe.name,
        "servings": recipe.servings,
        "instructions": recipe.instructions,
        "scale_factor": round(factor, 3),
        "items": scaled_items,
        "total_kcal":    round(totals["total_kcal"]    * factor, 1),
        "total_protein": round(totals["total_protein"] * factor, 1),
        "total_fat":     round(totals["total_fat"]     * factor, 1),
        "total_carbs":   round(totals["total_carbs"]   * factor, 1),
    }
