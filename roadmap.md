# DSP Project Roadmap


### Backend
contains the following files:

backend/
├── main.py          <-- The "entry point" that connects everything
├── database.py      <-- Database connection setup
├── models.py        <-- Database table definitions (User, Recipe)
├── schemas.py       <-- Data validation (what the API expects to receive)
├── calculations.py  <-- The "Math" (BMR, TDEE, Macros...?)
└── recipes.db       <-- local database file

### Project Phases

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




# backend logic

```text
backend/
├── main.py          # The "entry point" that connects everything
├── database.py      # Database connection setup
├── models.py        # Database table definitions (User, Recipe)
├── schemas.py       # Data validation (Pydantic models)
├── calculations.py  # The "Math" (BMR, TDEE, Macros, Anabolic Resistance)
└── recipes.db       # Local SQLite database file

Phase 1: Core Engine
[x] User Logic: Handling inputs (weight, height, age, sex).

[x] Activity & Goals: Integration of activity levels and goal-based adjustments.

[x] The Math: Basal Metabolic Rate (BMR) and TDEE calculations.

[x] Persistence: Database insertion and user profile storage.

Phase 2: Recipe Ecosystem
[ ] Ingredient Library: Database table for raw ingredients and their macros.

[ ] Scalable Recipes: DB table for full recipes with fixed macro ratios.

[ ] Scaler Logic: Algorithm to adapt portion sizes to fit specific meal/daily targets.

Phase 3: Smart Features
[ ] Dietary Restrictions: Filtering for allergies or preferences (Vegan, Keto, etc.).

[ ] Meal Planning: Automated suggestions based on remaining daily macros.

[ ] UX Polish: Friendly feedback (e.g., "You have 600kcal left for today").

Phase 4: Deployment & UI
[ ] API Documentation: Interactive FastAPI docs for frontend integration.

[ ] UI Design: Creating a clean, user-friendly interface.

[ ] Deployment: Hosting the backend and database on a live server.