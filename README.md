# Macro Tracker — DSP Project

Module: *Designing Software as Product* (ZHAW)

A nutrition-tracking web app. Calculate your daily kcal + macro target from
body stats and goals, log what you eat, see what's left, and get suggested
meals that fit your remaining macros.

## What's in here

- **FastAPI backend** with full REST API (Swagger at `/docs`).
- **Server-rendered UI** at `/app` (HTMX + Jinja2 + Pico.css).
- **SQLite** storage with seeded ingredients and recipes.
- **Pytest** suite covering pure logic (38 tests).
- **Cloudflare tunnel scripts** to expose the local app to the public internet.
- **Dockerfile + fly.toml** ready for cloud deployment when you want it.

## Quick start (local)

```bash
pip install -r requirements.txt
python3 seed.py                       # populates ingredients + recipes
uvicorn main:app --reload
```

Then open:
- <http://127.0.0.1:8000/app> — the UI
- <http://127.0.0.1:8000/docs> — the interactive API reference

## Public demo (no signup, random URL)

```bash
brew install cloudflared              # one-time
./serve_public.sh
```

Cloudflare prints a `https://<random>.trycloudflare.com` URL. Anyone with
the link can hit your local app for as long as the script is running.
Ctrl+C tears it down.

## Public demo at your own domain (one free Cloudflare account)

See the header of [serve_named.sh](serve_named.sh) for the one-time
DNS + tunnel setup, then:

```bash
./serve_named.sh
```

## Cloud deployment (when laptop-as-server isn't enough)

`fly.toml` + `Dockerfile` are ready. See the comments at the top of
[fly.toml](fly.toml) for the launch sequence.

## How to use the app

1. **`/app/calculate`** — enter your stats and goal. The app saves you as
   a user and takes you to your dashboard.
2. **`/app/users/{id}`** — your dashboard. Shows daily target, what you've
   consumed today, and what's remaining (with friendly messages like
   "You have 600 kcal left for today"). Log meals from the recipe dropdown.
3. **`/app/users/{id}/plan`** — get 3-meal plans that fit your remaining
   macros for today.

## Activity levels and goals

| Activity | | | Goal | |
|---|---|---|---|---|
| 1 | sedentary | 1.2× | 1 | strong gain (+0.5 kg/wk) |
| 2 | light | 1.375× | 2 | mild gain (+0.25 kg/wk) |
| 3 | moderate | 1.55× | 3 | maintain |
| 4 | active | 1.725× | 4 | mild loss (-0.25 kg/wk) |
| 5 | extreme | 1.9× | 5 | strong loss (-0.5 kg/wk) |

Protein gets a +0.2× bump for users 40+ and +0.3× for 50+ (anabolic resistance).

## Project structure

```
.
├── main.py            # FastAPI app — API + UI routes
├── database.py        # SQLAlchemy engine + session
├── models.py          # SQLAlchemy models: User, Ingredient, Recipe, MealLog, Tag
├── schemas.py         # Pydantic request/response schemas
├── calculations.py    # BMR / TDEE / macro math + friendly messages
├── recipes.py         # Recipe totals + scaler
├── planner.py         # Meal-plan suggester (permutations + scoring)
├── food_log.py        # Food-log helpers (serialization, daily messages)
├── seed.py            # One-shot DB seeder (ingredients + recipes)
├── templates/         # Jinja2 templates for the UI
├── tests/             # Pytest suite for pure logic
├── Dockerfile         # Container image for cloud deploys
├── fly.toml           # Fly.io launch config
├── serve_public.sh    # Quick Cloudflare tunnel (no account)
└── serve_named.sh     # Named Cloudflare tunnel (custom domain)
```

## Running the tests

```bash
python3 -m pytest -q
```

## Roadmap status

See [roadmap.md](roadmap.md) — Phases 1–3 fully delivered, Phase 4
(deployment + UI) shipped except for production hosting.
