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
[x] Ingredient Library: Database table for raw ingredients and their macros.

[x] Scalable Recipes: DB table for full recipes with fixed macro ratios.

[x] Scaler Logic: Algorithm to adapt portion sizes to fit specific meal/daily targets.

Phase 3: Smart Features
[x] Dietary Restrictions: Filtering for allergies or preferences (Vegan, Keto, etc.).

[x] Meal Planning: Automated suggestions based on remaining daily macros.

[ ] UX Polish: Friendly feedback (e.g., "You have 600kcal left for today").

Phase 4: Deployment & UI
[ ] API Documentation: Interactive FastAPI docs for frontend integration.

[ ] UI Design: Creating a clean, user-friendly interface.

[ ] Deployment: Hosting the backend and database on a live server.