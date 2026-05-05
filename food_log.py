def serialize_log(log):
    return {
        "id": log.id,
        "user_id": log.user_id,
        "recipe_id": log.recipe_id,
        "recipe_name": log.recipe.name if log.recipe else None,
        "scale_factor": log.scale_factor,
        "eaten_at": log.eaten_at,
        "kcal": log.kcal,
        "protein": log.protein,
        "fat": log.fat,
        "carbs": log.carbs,
        "note": log.note,
    }


def daily_messages(remaining, num_logs):
    if num_logs == 0:
        return ["Nothing logged yet today — start with breakfast."]
    msgs = []
    k = remaining["kcal"]
    if abs(k) <= 50:
        msgs.append(f"You're on target — only {abs(k):.0f} kcal off your daily goal.")
    elif k > 0:
        msgs.append(f"You have {k:.0f} kcal left for today.")
    else:
        msgs.append(f"You're {abs(k):.0f} kcal over your daily goal.")
    p = remaining["protein"]
    if p > 20:
        msgs.append(f"Still {p:.0f} g protein to go — pick a high-protein next meal.")
    elif p < -20:
        msgs.append(f"Protein is {abs(p):.0f} g over target.")
    return msgs
