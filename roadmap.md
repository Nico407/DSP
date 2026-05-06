# Roadmap

## Project layout

```text
.
├── main.py            # FastAPI app — API + UI routes
├── database.py        # SQLAlchemy engine + session
├── models.py          # User, Ingredient, Recipe, RecipeItem, Tag, MealLog
├── schemas.py         # Pydantic request/response schemas
├── calculations.py    # BMR / TDEE / macros + friendly messages
├── recipes.py         # Recipe totals + scaler
├── planner.py         # Meal-plan suggester
├── food_log.py        # Food-log helpers
├── seed.py            # One-shot DB seeder
├── templates/         # Jinja2 templates for the UI
├── tests/             # Pytest suite (38 tests)
├── Dockerfile         # Container image
├── fly.toml           # Fly.io launch config
├── serve_public.sh    # Quick Cloudflare tunnel
├── serve_named.sh     # Named Cloudflare tunnel
└── recipes.db         # SQLite database
```

## Phase 1 — Core engine

- [x] User logic: handling inputs (weight, height, age, sex)
- [x] Activity & goals: levels and goal-based adjustments
- [x] BMR + TDEE calculations
- [x] Persistence: user profile storage in SQLite

## Phase 2 — Recipe ecosystem

- [x] Ingredient library (per-100g macros + diet tags)
- [x] Scalable recipes (Recipe + RecipeItem with grams)
- [x] Scaler logic: scale a recipe to hit a target kcal or protein

## Phase 3 — Smart features

- [x] Dietary restrictions (Tag model + filter on `/recipes` and `/plan`)
- [x] Meal planning (`build_plans` with permutation scoring)
- [x] UX polish: friendly feedback throughout
  - `/calculate` returns goal-aware messages and protein-bump notes for 40+/50+
  - `/plan` returns "You have N kcal left" / "Protein N g over" lines per plan
  - `/users/{id}/today` returns real-time consumption-driven messages
    ("Nothing logged yet today — start with breakfast.")

## Phase 4 — Deployment & UI

- [x] API documentation: Swagger UI at `/docs` with full `response_model` typing
- [x] UI design: server-rendered pages at `/app/*`
  - Home (3-card intro)
  - Calculate form
  - Users list
  - User dashboard (target/consumed/remaining + log form + today's log)
  - Suggested meal plan view
- [ ] Production deployment: Dockerfile + fly.toml are ready, hosting is the
      remaining decision (Fly requires a card; Render free needs a Postgres
      switch; Cloudflare quick tunnel works as an interim demo)

## Beyond the original roadmap

Things that were not on the plan but ended up in the codebase:

- [x] User identity loop (`GET /users`, `GET /users/{id}`, `POST /users/{id}/plan`,
      `GET /users/{id}/summary`) — closes the loop so stored users aren't write-only
- [x] Food log (`MealLog` table + log/list/delete endpoints + `/today`) — the
      table that makes "kcal left for today" truthful instead of plan-relative
- [x] 38-test pytest suite for pure logic
- [x] Pydantic v3 / SQLAlchemy 2.0 deprecation cleanup
- [x] UTF-8 requirements.txt (was UTF-16, broke `pip install -r`)

## Honest gaps

- No authentication. Anyone with a tunnel URL can read/write all data. Fine
  for a class demo, not for a public deployment.
- No user delete / edit endpoints.
- No admin view of all logs across users (deliberate: not the use case).
- No timezone handling on `MealLog.eaten_at` — uses server UTC. "Today"
  is the server's today, not the user's.
- No food-log history page in the UI (the API has it, the UI does not).
