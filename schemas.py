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