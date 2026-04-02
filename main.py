from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import UserCreate, MacroResponse
from models import UserProfile, UserDB, Base
from database import engine, get_db
from calculations import calculate_tdee, calculate_macros

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