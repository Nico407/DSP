# Contributing

Thanks for your interest in working on Macro Tracker. This guide gets you from
a fresh clone to your first pull request.

## 1. Set up your environment

```bash
git clone <repo-url>
cd DSP
python3 -m venv .venv && source .venv/bin/activate    # optional but recommended
pip install -r requirements.txt
```

Python 3.12+ is recommended. The `requirements.txt` is now plain UTF-8 — if
your tooling ever complains about encoding, re-save it as UTF-8.

## 2. Seed the database

The repo ships with an empty schema. To get a usable set of ingredients and
recipes for development:

```bash
python3 seed.py
```

This is idempotent — re-running it adds anything missing without duplicating.

## 3. Run the app locally

```bash
uvicorn main:app --reload
```

Then open:
- <http://127.0.0.1:8000/app> — the UI
- <http://127.0.0.1:8000/docs> — the interactive API reference

`--reload` picks up Python and template changes without restarting.

## 4. Run the tests

```bash
python3 -m pytest -q
```

The suite covers pure logic (calculations, recipe scaling, planner scoring,
food-log messages). New backend logic should come with a test in `tests/`.

## 5. Add an ingredient or recipe via the API

The fastest way is via the Swagger UI at `/docs` → "Try it out".

Programmatically:

```bash
# 1. Add an ingredient (per-100g macros)
curl -X POST http://127.0.0.1:8000/ingredients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "rolled oats",
    "kcal_per_100g": 379,
    "protein_per_100g": 13.2,
    "fat_per_100g": 6.5,
    "carbs_per_100g": 67.7
  }'

# 2. Add a recipe that references existing ingredient ids
curl -X POST http://127.0.0.1:8000/recipes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "oats with milk",
    "servings": 1,
    "instructions": "Cook oats in milk for 5 minutes.",
    "items": [
      {"ingredient_id": 1, "grams": 60},
      {"ingredient_id": 2, "grams": 200}
    ]
  }'
```

For permanent additions, add the ingredient/recipe to `seed.py` so other
contributors get it on a fresh DB.

## 6. Branch naming

Use one of these prefixes so the intent of a branch is obvious:

- `feature/<short-description>` — new functionality (e.g. `feature/timezone-support`)
- `fix/<short-description>` — bug fixes (e.g. `fix/scale-factor-rounding`)
- `docs/<short-description>` — docs-only changes (e.g. `docs/contributing-guide`)

Keep the description short and lowercase, dashes between words.

## 7. Open a pull request

1. Branch off `main`:
   ```bash
   git checkout -b feature/your-thing
   ```
2. Make your change. Keep commits focused; one logical change per commit
   is ideal.
3. Run the tests locally before pushing:
   ```bash
   python3 -m pytest -q
   ```
4. Push and open a PR against `main` via GitHub. CI runs the same test
   suite on every PR (`.github/workflows/test.yml`); the PR can be merged
   once CI is green.
5. In the PR description, briefly note:
   - **What** changed (one sentence)
   - **Why** it was needed (link the issue if there is one)
   - **How to verify** (the manual or automated check that proves it works)

## House rules

- Don't break the `pytest` suite. Add a test if you add logic.
- Keep `response_model` set on every new FastAPI endpoint.
- Don't commit `recipes.db` changes — the file is for local use; production
  deploys seed their own copy.
- Match the existing style: flat module layout, type hints where useful,
  no comments that just restate the code.
