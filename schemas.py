from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

# This is what the user SENDS to the API
class UserCreate(BaseModel):
    name: str
    sex: str = Field(..., pattern="^(male|female)$") # Only 'male' or 'female'
    height: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    age: int = Field(..., gt=0, lt=120)
    activity_level: str  # "1", "2", "3", etc.
    goal_choice: str     # "1", "2", "3", etc.

# This is what the API SENDS BACK to the user
class MacroResponse(BaseModel):
    daily_kcal: int
    protein: int
    fat: int
    carbs: int
    p_multiplier_used: float
    messages: list[str] = []


class UserRead(BaseModel):
    id: int
    name: str
    sex: str
    height: float
    weight: float
    age: int
    activity_level: str
    goal_choice: str
    daily_kcal: int
    protein: int
    fat: int
    carbs: int
    model_config = ConfigDict(from_attributes=True)


class UserPlanRequest(BaseModel):
    diet: str | None = None
    meals: int = Field(3, ge=1, le=4)
    split: list[float] | None = None


# --- Ingredients ---
class IngredientCreate(BaseModel):
    name: str
    kcal_per_100g: float = Field(..., ge=0)
    protein_per_100g: float = Field(..., ge=0)
    fat_per_100g: float = Field(..., ge=0)
    carbs_per_100g: float = Field(..., ge=0)

class IngredientRead(IngredientCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- Recipes ---
class RecipeItemCreate(BaseModel):
    ingredient_id: int
    grams: float = Field(..., gt=0)

class RecipeItemRead(BaseModel):
    ingredient_id: int
    ingredient_name: str
    grams: float
    model_config = ConfigDict(from_attributes=True)

class RecipeCreate(BaseModel):
    name: str
    servings: int = Field(1, gt=0)
    instructions: str | None = None
    items: list[RecipeItemCreate]

class PlanRequest(BaseModel):
    daily_kcal: int = Field(..., gt=0)
    protein: int = Field(..., ge=0)
    fat: int = Field(..., ge=0)
    carbs: int = Field(..., ge=0)
    diet: str | None = None
    meals: int = Field(3, ge=1, le=4)
    split: list[float] | None = None


class RecipeRead(BaseModel):
    id: int
    name: str
    servings: int
    instructions: str | None = None
    items: list[RecipeItemRead]
    total_kcal: float
    total_protein: float
    total_fat: float
    total_carbs: float
    model_config = ConfigDict(from_attributes=True)


class ScaledRecipeRead(RecipeRead):
    scale_factor: float


# --- Plan response ---
class PlanTotals(BaseModel):
    total_kcal: float
    total_protein: float
    total_fat: float
    total_carbs: float


class PlanLeftover(BaseModel):
    kcal: float
    protein: float
    fat: float
    carbs: float


class PlanMealSlot(BaseModel):
    slot: str
    recipe: ScaledRecipeRead


class PlanItem(BaseModel):
    score: float
    meals: list[PlanMealSlot]
    totals: PlanTotals
    leftover: PlanLeftover
    messages: list[str] = []


class PlanTarget(BaseModel):
    daily_kcal: int
    protein: int
    fat: int
    carbs: int


class PlanResponse(BaseModel):
    target: PlanTarget | None = None
    plans: list[PlanItem]
    error: str | None = None


class UserSummary(BaseModel):
    profile: UserRead
    messages: list[str]
    suggested_plan: PlanResponse


# --- Food log ---
class DailyTotals(BaseModel):
    kcal: float
    protein: float
    fat: float
    carbs: float


class MealLogCreate(BaseModel):
    recipe_id: int
    scale_factor: float = Field(1.0, gt=0)
    eaten_at: datetime | None = None
    note: str | None = None


class MealLogRead(BaseModel):
    id: int
    user_id: int
    recipe_id: int | None
    recipe_name: str | None
    scale_factor: float
    eaten_at: datetime
    kcal: float
    protein: float
    fat: float
    carbs: float
    note: str | None
    model_config = ConfigDict(from_attributes=True)


class TodayResponse(BaseModel):
    date: str
    targets: PlanTarget
    consumed: DailyTotals
    remaining: DailyTotals
    messages: list[str]
    logs: list[MealLogRead]