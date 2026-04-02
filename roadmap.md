# DSP Project Roadmap

### Frontend
FastAPI
- Will be done in further steps (outside of this framework)

### Backend
contains the following files:

backend/
├── main.py          <-- The "entry point" that connects everything
├── database.py      <-- Database connection setup
├── models.py        <-- Database table definitions (User, Recipe)
├── schemas.py       <-- Data validation (what the API expects to receive)
├── calculations.py  <-- The "Math" (BMR, TDEE, Macros...?)
└── recipes.db       <-- local database file

Phase 1: Core
✔    - User Logic (Inputs like weight, age etc...)
✔    - Preferences and activity levels
✔    - Max kCal calculation and prefernce adjustments
✔    - DB insertion

Phase 2: Recipe Ecosystem
X     - DB Table with Ingredients
X     - DB Table with scalable Recipes
X     - Scaler Logic, adapt portions to meal/daily intake

Phase 3: Features
X     - Dietary Restrictions
X     - Meal Planning suggestions
X     - Aestetics (renaming stuff like "you have 600kcal left")

Phase 4:
X     - API Documentation
X     - UI Design
X     - Webpage Deplyoment