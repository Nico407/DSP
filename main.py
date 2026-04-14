from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import (
    UserCreate, MacroResponse,
    IngredientCreate, IngredientRead,
    RecipeCreate, PlanRequest,
)
from models import UserProfile, UserDB, Base, Ingredient, Recipe, RecipeItem, Tag
from database import engine, get_db
from calculations import calculate_tdee, calculate_macros
from recipes import serialize_recipe, scale_recipe
from planner import build_plans

#creates DB File if none existing
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Macro API is online."}

# We use @app.post because we are SENDING data to the server
@app.post("/calculate", response_model=MacroResponse)
def get_macros_api(user_data: UserCreate, db: Session = Depends(get_db)):
    
    # 1. Map the Schema data to your Logic Class (UserProfile)
    user_logic = UserProfile(
        name=user_data.name,
        sex=user_data.sex,
        height=user_data.height,
        weight=user_data.weight,
        age=user_data.age,
        activity_level=user_data.activity_level
    )
    
    # 2. Run your existing math
    tdee = calculate_tdee(user_logic)
    results = calculate_macros(user_logic, tdee, user_data.goal_choice)
    
    # 3. Save to Database
    new_user = UserDB(
        name = user_data.name,
        sex = user_data.sex,
        height = user_data.height,
        weight = user_data.weight,
        age = user_data.age,
        activity_level = user_data.activity_level,
        goal_choice = user_data.goal_choice,
        daily_kcal = results["daily_kcal"],
        protein = results["protein"],
        fat = results["fat"],
        carbs = results["carbs"]
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user) #gives object Id from DB

    return results


@app.post("/ingredients", response_model=IngredientRead)
def create_ingredient(data: IngredientCreate, db: Session = Depends(get_db)):
    if db.query(Ingredient).filter(Ingredient.name == data.name).first():
        raise HTTPException(400, f"Ingredient '{data.name}' already exists.")
    ing = Ingredient(**data.model_dump())
    db.add(ing); db.commit(); db.refresh(ing)
    return ing


@app.get("/ingredients", response_model=list[IngredientRead])
def list_ingredients(db: Session = Depends(get_db)):
    return db.query(Ingredient).all()


@app.post("/recipes")
def create_recipe(data: RecipeCreate, db: Session = Depends(get_db)):
    recipe = Recipe(name=data.name, servings=data.servings, instructions=data.instructions)
    for item in data.items:
        if not db.query(Ingredient).get(item.ingredient_id):
            raise HTTPException(404, f"Ingredient id {item.ingredient_id} not found.")
        recipe.items.append(RecipeItem(ingredient_id=item.ingredient_id, grams=item.grams))
    db.add(recipe); db.commit(); db.refresh(recipe)
    return serialize_recipe(recipe)


@app.get("/tags")
def list_tags(db: Session = Depends(get_db)):
    return [t.name for t in db.query(Tag).order_by(Tag.name).all()]


# GET /recipes?diet=vegan,gluten_free
# A recipe matches iff EVERY ingredient carries EVERY requested tag.
@app.get("/recipes")
def list_recipes(diet: str | None = None, db: Session = Depends(get_db)):
    required = [t.strip() for t in diet.split(",")] if diet else []
    results = []
    for recipe in db.query(Recipe).all():
        if required:
            ok = all(
                all(req in {t.name for t in item.ingredient.tags} for req in required)
                for item in recipe.items
            )
            if not ok:
                continue
        results.append(serialize_recipe(recipe))
    return results


@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).get(recipe_id)
    if not recipe:
        raise HTTPException(404, "Recipe not found.")
    return serialize_recipe(recipe)


@app.post("/plan")
def plan_day(req: PlanRequest, db: Session = Depends(get_db)):
    target = {
        "daily_kcal": req.daily_kcal,
        "protein": req.protein,
        "fat": req.fat,
        "carbs": req.carbs,
    }
    return build_plans(db, target, diet=req.diet, meals=req.meals, split=req.split)


@app.get("/recipes/{recipe_id}/scale")
def scale_recipe_endpoint(
    recipe_id: int,
    target_kcal: float | None = None,
    target_protein: float | None = None,
    db: Session = Depends(get_db),
):
    recipe = db.query(Recipe).get(recipe_id)
    if not recipe:
        raise HTTPException(404, "Recipe not found.")
    return scale_recipe(recipe, target_kcal=target_kcal, target_protein=target_protein)