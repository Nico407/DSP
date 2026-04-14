from pydantic import BaseModel, Field

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


# --- Ingredients ---
class IngredientCreate(BaseModel):
    name: str
    kcal_per_100g: float = Field(..., ge=0)
    protein_per_100g: float = Field(..., ge=0)
    fat_per_100g: float = Field(..., ge=0)
    carbs_per_100g: float = Field(..., ge=0)

class IngredientRead(IngredientCreate):
    id: int
    class Config:
        from_attributes = True


# --- Recipes ---
class RecipeItemCreate(BaseModel):
    ingredient_id: int
    grams: float = Field(..., gt=0)

class RecipeItemRead(BaseModel):
    ingredient_id: int
    ingredient_name: str
    grams: float
    class Config:
        from_attributes = True

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
    class Config:
        from_attributes = True