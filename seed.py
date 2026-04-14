from database import engine, SessionLocal
from models import Base, Ingredient, Tag, Recipe, RecipeItem

Base.metadata.create_all(bind=engine)

# (name, kcal, protein, fat, carbs, [tags])  — per 100g
INGREDIENTS = [
    ("chicken breast",    165, 31.0,  3.6,  0.0, ["gluten_free", "dairy_free", "nut_free", "carnivore"]),
    ("salmon",            208, 20.0, 13.0,  0.0, ["gluten_free", "dairy_free", "nut_free", "carnivore"]),
    ("ground beef 90/10", 176, 20.0, 10.0,  0.0, ["gluten_free", "dairy_free", "nut_free", "carnivore"]),
    ("egg",               143, 12.6,  9.5,  0.7, ["vegetarian", "gluten_free", "dairy_free", "nut_free", "carnivore"]),
    ("greek yogurt 0%",    59, 10.0,  0.4,  3.6, ["vegetarian", "gluten_free", "nut_free", "carnivore"]),
    ("white rice cooked", 130,  2.7,  0.3, 28.0, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("oats dry",          389, 16.9,  6.9, 66.3, ["vegan", "vegetarian", "dairy_free", "nut_free"]),
    ("whole wheat bread", 247, 13.0,  3.4, 41.0, ["vegan", "vegetarian", "dairy_free", "nut_free"]),
    ("potato",             77,  2.0,  0.1, 17.0, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("broccoli",           34,  2.8,  0.4,  7.0, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("olive oil",         884,  0.0,100.0,  0.0, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("almonds",           579, 21.2, 49.9, 21.6, ["vegan", "vegetarian", "gluten_free", "dairy_free"]),
    ("banana",             89,  1.1,  0.3, 22.8, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("cheddar cheese",    403, 23.0, 33.0,  3.1, ["vegetarian", "gluten_free", "nut_free", "carnivore"]),
    # --- phase 3 additions ---
    ("tofu firm",         144, 17.0,  9.0,  3.0, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("lentils cooked",    116,  9.0,  0.4, 20.0, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("black beans cooked",132,  8.9,  0.5, 23.7, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("tuna canned water", 116, 25.5,  0.8,  0.0, ["gluten_free", "dairy_free", "nut_free", "carnivore"]),
    ("shrimp",             99, 24.0,  0.3,  0.2, ["gluten_free", "dairy_free", "nut_free", "carnivore"]),
    ("spinach",            23,  2.9,  0.4,  3.6, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("sweet potato",       86,  1.6,  0.1, 20.0, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("quinoa cooked",     120,  4.4,  1.9, 21.3, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("avocado",           160,  2.0, 14.7,  8.5, ["vegan", "vegetarian", "gluten_free", "dairy_free", "nut_free"]),
    ("milk whole",         61,  3.2,  3.3,  4.8, ["vegetarian", "gluten_free", "nut_free", "carnivore"]),
]

RECIPES = [
    # (name, servings, instructions, [(ingredient_name, grams), ...])
    ("oatmeal banana bowl", 1, "Cook oats with milk, top with banana and almonds.", [
        ("oats dry", 60), ("milk whole", 200), ("banana", 100), ("almonds", 15),
    ]),
    ("salmon & sweet potato", 1, "Bake salmon and sweet potato, steam broccoli, drizzle olive oil.", [
        ("salmon", 180), ("sweet potato", 250), ("broccoli", 150), ("olive oil", 10),
    ]),
    ("tofu quinoa stir-fry", 1, "Pan-fry tofu, serve on quinoa with spinach and olive oil.", [
        ("tofu firm", 200), ("quinoa cooked", 200), ("spinach", 100), ("olive oil", 10),
    ]),
    ("beef burrito bowl", 1, "Brown beef, combine with rice, beans, and avocado.", [
        ("ground beef 90/10", 150), ("white rice cooked", 200), ("black beans cooked", 120), ("avocado", 60),
    ]),
    ("egg avocado toast", 1, "Toast bread, top with mashed avocado and fried eggs.", [
        ("egg", 120), ("whole wheat bread", 80), ("avocado", 50), ("olive oil", 5),
    ]),
    ("tuna spinach salad", 1, "Toss tuna with spinach, avocado, olive oil.", [
        ("tuna canned water", 120), ("spinach", 150), ("avocado", 80), ("olive oil", 10),
    ]),
    ("greek yogurt bowl", 1, "Mix yogurt with banana, oats, almonds.", [
        ("greek yogurt 0%", 200), ("banana", 100), ("oats dry", 30), ("almonds", 15),
    ]),
    ("lentil soup bowl", 1, "Simmer lentils with potato and spinach, finish with olive oil.", [
        ("lentils cooked", 250), ("potato", 150), ("spinach", 100), ("olive oil", 10),
    ]),
    ("black bean quinoa bowl", 1, "Combine quinoa, black beans, avocado, and broccoli.", [
        ("quinoa cooked", 200), ("black beans cooked", 150), ("avocado", 70), ("broccoli", 100),
    ]),
    ("sweet potato lentil bowl", 1, "Roast sweet potato, top with lentils, spinach, olive oil.", [
        ("sweet potato", 250), ("lentils cooked", 200), ("spinach", 80), ("olive oil", 10),
    ]),
]

db = SessionLocal()

def get_or_create_tag(name):
    tag = db.query(Tag).filter(Tag.name == name).first()
    if not tag:
        tag = Tag(name=name)
        db.add(tag); db.flush()
    return tag

added_ing = 0
added_tag_links = 0
for name, kcal, p, f, c, tag_names in INGREDIENTS:
    ing = db.query(Ingredient).filter(Ingredient.name == name).first()
    if not ing:
        ing = Ingredient(
            name=name, kcal_per_100g=kcal,
            protein_per_100g=p, fat_per_100g=f, carbs_per_100g=c,
        )
        db.add(ing); db.flush()
        added_ing += 1
    existing = {t.name for t in ing.tags}
    for tn in tag_names:
        if tn not in existing:
            ing.tags.append(get_or_create_tag(tn))
            added_tag_links += 1

db.commit()

added_recipes = 0
for rname, servings, instructions, items in RECIPES:
    if db.query(Recipe).filter(Recipe.name == rname).first():
        continue
    recipe = Recipe(name=rname, servings=servings, instructions=instructions)
    for ing_name, grams in items:
        ing = db.query(Ingredient).filter(Ingredient.name == ing_name).first()
        if not ing:
            raise RuntimeError(f"Missing ingredient for recipe '{rname}': {ing_name}")
        recipe.items.append(RecipeItem(ingredient_id=ing.id, grams=grams))
    db.add(recipe)
    added_recipes += 1
db.commit()

print(f"Seeded {added_ing} new ingredients, {added_tag_links} new tag links, {added_recipes} new recipes.")
print(f"Totals — ingredients: {db.query(Ingredient).count()}, tags: {db.query(Tag).count()}, recipes: {db.query(Recipe).count()}.")
db.close()
