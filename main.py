from datetime import datetime, date, time, timezone
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import (
    UserCreate, MacroResponse, UserRead, UserPlanRequest, UserSummary,
    IngredientCreate, IngredientRead,
    RecipeCreate, RecipeRead, ScaledRecipeRead,
    PlanRequest, PlanResponse,
    MealLogCreate, MealLogRead, TodayResponse,
)
from models import UserProfile, UserDB, Base, Ingredient, Recipe, RecipeItem, Tag, MealLog
from database import engine, get_db
from calculations import calculate_tdee, calculate_macros, build_macro_messages
from recipes import serialize_recipe, scale_recipe, compute_totals
from planner import build_plans
from food_log import serialize_log, daily_messages

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

    results["messages"] = build_macro_messages(user_logic, user_data.goal_choice, results)
    return results


@app.get("/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(404, f"User id {user_id} not found.")
    return user


@app.post("/users/{user_id}/plan", response_model=PlanResponse)
def plan_for_user(user_id: int, req: UserPlanRequest, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(404, f"User id {user_id} not found.")
    target = {
        "daily_kcal": user.daily_kcal,
        "protein":    user.protein,
        "fat":        user.fat,
        "carbs":      user.carbs,
    }
    return build_plans(db, target, diet=req.diet, meals=req.meals, split=req.split)


@app.post("/users/{user_id}/log", response_model=MealLogRead)
def log_meal(user_id: int, data: MealLogCreate, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(404, f"User id {user_id} not found.")
    recipe = db.get(Recipe, data.recipe_id)
    if not recipe:
        raise HTTPException(404, f"Recipe id {data.recipe_id} not found.")

    totals = compute_totals(recipe)
    f = data.scale_factor
    log = MealLog(
        user_id=user_id,
        recipe_id=recipe.id,
        scale_factor=f,
        eaten_at=data.eaten_at or datetime.now(timezone.utc),
        kcal=round(totals["total_kcal"]    * f, 1),
        protein=round(totals["total_protein"] * f, 1),
        fat=round(totals["total_fat"]      * f, 1),
        carbs=round(totals["total_carbs"]   * f, 1),
        note=data.note,
    )
    db.add(log); db.commit(); db.refresh(log)
    return serialize_log(log)


@app.get("/users/{user_id}/log", response_model=list[MealLogRead])
def list_logs(user_id: int, db: Session = Depends(get_db)):
    if not db.get(UserDB, user_id):
        raise HTTPException(404, f"User id {user_id} not found.")
    logs = (
        db.query(MealLog)
        .filter(MealLog.user_id == user_id)
        .order_by(MealLog.eaten_at.desc())
        .all()
    )
    return [serialize_log(l) for l in logs]


@app.delete("/log/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.get(MealLog, log_id)
    if not log:
        raise HTTPException(404, f"Log id {log_id} not found.")
    db.delete(log); db.commit()
    return {"deleted": log_id}


@app.get("/users/{user_id}/today", response_model=TodayResponse)
def today_status(user_id: int, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(404, f"User id {user_id} not found.")

    today = date.today()
    start = datetime.combine(today, time.min)
    end = datetime.combine(today, time.max)
    logs = (
        db.query(MealLog)
        .filter(
            MealLog.user_id == user_id,
            MealLog.eaten_at >= start,
            MealLog.eaten_at <= end,
        )
        .order_by(MealLog.eaten_at)
        .all()
    )

    consumed = {
        "kcal":    round(sum(l.kcal    for l in logs), 1),
        "protein": round(sum(l.protein for l in logs), 1),
        "fat":     round(sum(l.fat     for l in logs), 1),
        "carbs":   round(sum(l.carbs   for l in logs), 1),
    }
    remaining = {
        "kcal":    round(user.daily_kcal - consumed["kcal"],    1),
        "protein": round(user.protein    - consumed["protein"], 1),
        "fat":     round(user.fat        - consumed["fat"],     1),
        "carbs":   round(user.carbs      - consumed["carbs"],   1),
    }
    return {
        "date": today.isoformat(),
        "targets": {
            "daily_kcal": user.daily_kcal,
            "protein":    user.protein,
            "fat":        user.fat,
            "carbs":      user.carbs,
        },
        "consumed": consumed,
        "remaining": remaining,
        "messages": daily_messages(remaining, len(logs)),
        "logs": [serialize_log(l) for l in logs],
    }


@app.get("/users/{user_id}/summary", response_model=UserSummary)
def user_summary(user_id: int, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(404, f"User id {user_id} not found.")
    targets = {
        "daily_kcal": user.daily_kcal,
        "protein":    user.protein,
        "fat":        user.fat,
        "carbs":      user.carbs,
    }
    messages = build_macro_messages(user, user.goal_choice, targets)
    suggested_plan = build_plans(db, targets, meals=3)
    return {"profile": user, "messages": messages, "suggested_plan": suggested_plan}


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


@app.post("/recipes", response_model=RecipeRead)
def create_recipe(data: RecipeCreate, db: Session = Depends(get_db)):
    recipe = Recipe(name=data.name, servings=data.servings, instructions=data.instructions)
    for item in data.items:
        if not db.get(Ingredient, item.ingredient_id):
            raise HTTPException(404, f"Ingredient id {item.ingredient_id} not found.")
        recipe.items.append(RecipeItem(ingredient_id=item.ingredient_id, grams=item.grams))
    db.add(recipe); db.commit(); db.refresh(recipe)
    return serialize_recipe(recipe)


@app.get("/tags", response_model=list[str])
def list_tags(db: Session = Depends(get_db)):
    return [t.name for t in db.query(Tag).order_by(Tag.name).all()]


# GET /recipes?diet=vegan,gluten_free
# A recipe matches iff EVERY ingredient carries EVERY requested tag.
@app.get("/recipes", response_model=list[RecipeRead])
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


@app.get("/recipes/{recipe_id}", response_model=RecipeRead)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(404, "Recipe not found.")
    return serialize_recipe(recipe)


@app.post("/plan", response_model=PlanResponse)
def plan_day(req: PlanRequest, db: Session = Depends(get_db)):
    target = {
        "daily_kcal": req.daily_kcal,
        "protein": req.protein,
        "fat": req.fat,
        "carbs": req.carbs,
    }
    return build_plans(db, target, diet=req.diet, meals=req.meals, split=req.split)


@app.get("/recipes/{recipe_id}/scale", response_model=ScaledRecipeRead)
def scale_recipe_endpoint(
    recipe_id: int,
    target_kcal: float | None = None,
    target_protein: float | None = None,
    db: Session = Depends(get_db),
):
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(404, "Recipe not found.")
    return scale_recipe(recipe, target_kcal=target_kcal, target_protein=target_protein)