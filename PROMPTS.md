# AI Prompts Documentation

This file contains all the prompts used during the development of the HealthLinkAI project for academic review.

---

## Project Overview
- **Project Name:** HealthLinkAI - MindWell

---

## Prompts Used


Stack (free-friendly):

 * **Frontend:** HTML, CSS, JS (Tailwind via CDN + Heroicons SVG for free icons).
 * **Backend:** **Flask** (Python) + **SQLAlchemy** + **MySQL**.
 * **DB hosting (free):** PlanetScale (MySQL) *or* PythonAnywhere MySQL (free plan).
 * **App hosting (free):** Render (free web service) *or* PythonAnywhere web app.
 * **AI (no paid APIs):** Rule-based + tiny classical ML, VADER sentiment (NLTK), hand-curated medical rules, Haversine for nearby clinics.
* **Payments (sandbox for demo):** Flutterwave/Paystack test mode (optional), or “Request Consultation” flow with admin approval.

---

# Step-by-step AI IDE Prompts

> **How to use:** Paste Prompt 1, wait for completion, test briefly, then go to Prompt 2, and so on.

---

## Prompt 1 — Project scaffold & repo

**Prompt:**

> Create a new full-stack project named **“HealthLinkAI–MindWell”** with this structure:
>
> ```
> healthlinkai/
>   backend/
>     app.py
>     models.py
>     ai/
>       symptom_rules.json
>       symptom_checker.py
>       mindwell_bot.py
>       recommend.py
>     templates/
>       base.html
>       index.html
>       symptom_checker.html
>       mindwell.html
>       providers.html
>       dashboard.html
>     static/
>       css/style.css
>       js/main.js
>       img/ (placeholders)
>     tests/
>       test_basic.py
>     requirements.txt
>     README.md
>     .env.example
>     Procfile
>     runtime.txt
>     Dockerfile
>   scripts/
>     seed_providers.sql
> ```
>
> Use **Flask + SQLAlchemy** with **MySQL**. Add Tailwind via CDN in `base.html`. Include a clean, responsive layout (max-width container, soft gray background, white cards, rounded-2xl, subtle shadows, large headings, clear CTAs). Use a **cool-gray + teal** palette and **Heroicons** SVG for icons.
> Add a visible **medical disclaimer** in the footer: “This tool provides educational information, not medical diagnosis. In emergencies call local services immediately.”
> Initialize a **git repo**, write a short `README.md` with local setup instructions, and include a `.env.example` listing: `DATABASE_URL`, `FLASK_ENV`, `SECRET_KEY`, `PAYMENT_PUBLIC_KEY`, `PAYMENT_SECRET_KEY`.

---

## Prompt 2 — Python + dependencies

**Prompt:**

> In `backend/requirements.txt`, pin these free packages:
>
> ```
> Flask==3.0.3
> python-dotenv==1.0.1
> SQLAlchemy==2.0.30
> pymysql==1.1.1
> flask-cors==4.0.1
> nltk==3.9.1
> scikit-learn==1.5.1
> numpy==2.0.1
> pandas==2.2.2
> gunicorn==22.0.0
> ```
>
> In `app.py`, set up a minimal Flask app with Jinja templates, static files, and CORS. Load env vars via `python-dotenv`. Create `/` route for home, `/symptoms`, `/mindwell`, `/providers`, `/dashboard`.

---

## Prompt 3 — Database models & schema

**Prompt:**

> Using **SQLAlchemy**, define these models in `models.py`:
>
> * `User(id, name, email, role['user','admin'], password_hash, created_at)`
> * `SymptomLog(id, user_id, symptoms_text, conditions_json, risk_level['low','medium','high'], created_at)`
> * `Assessment(id, user_id, summary, recommended_action, created_at)`
> * `Provider(id, name, type['clinic','hospital','pharmacy','counseling'], phone, email, address, city, lat, lng)`
> * `Message(id, user_id, channel['mindwell','support'], text, sentiment, alert_flag[bool], created_at)`
> * `Subscription(id, user_id, plan['free','premium'], status['active','inactive'], started_at)`
>   Add DB init code and migration-like helpers (simple `create_all` + seed). In `scripts/seed_providers.sql`, insert 8-12 realistic providers with fake coordinates around **Douala** and **Yaoundé** for demo. Expose a small admin user (hardcoded) for MVP.

---

## Prompt 4 — Connect to PlanetScale (or PythonAnywhere) MySQL

**Prompt:**

> Add `DATABASE_URL` support like:
>
> ```
> mysql+pymysql://<user>:<pass>@<host>/<db>?ssl=true
> ```
>
> Create `config_db()` that reads `DATABASE_URL` from environment. Add a CLI script section at bottom of `app.py` to run:
>
> * `python app.py --init-db` → creates tables.
> * `python app.py --seed` → runs `scripts/seed_providers.sql`.
>   Also write `README.md` instructions to set up a **free PlanetScale** database (or PythonAnywhere MySQL), and to set `DATABASE_URL` accordingly.

---

## Prompt 5 — Frontend base layout & pages

**Prompt:**

> Build `templates/base.html` with a responsive nav: **Logo** (“HealthLinkAI”), links to Home, Symptom Checker, MindWell, Providers, Dashboard, and a **Get Premium** button. Use Tailwind CDN and Heroicons. Include a cookie banner for analytics consent (client-side only).
> Implement pages:
>
> * `index.html`: hero section with 2 CTAs: “Check Symptoms” and “Talk to MindWell”. Three feature cards (AI triage, mental health support, nearby providers). A section showing sample screenshots (use placeholders).
> * `symptom_checker.html`: a multi-step form (chips for common symptoms + free-text). Results card shows **possible conditions** + **risk level** + **next steps**.
> * `mindwell.html`: chat UI (left: messages, right: quick tips and helplines placeholder). Input box with send button and disclaimer.
> * `providers.html`: interactive list + map placeholder (no paid map). For MVP, show distance text using Haversine; allow filter by type and city.
> * `dashboard.html`: simple user dashboard—recent assessments, MindWell alerts, subscription status, and button to request a tele-consultation.
>   Add accessible HTML (labels, aria-attributes) and mobile-first responsive design.

---

## Prompt 6 — Symptom rules & checker (AI without paid APIs)

**Prompt:**

> In `ai/symptom_rules.json`, store a minimal ruleset mapping common symptoms to possible conditions and risk levels. Example entries:
>
> * fever + chills → malaria/infection (risk medium-high if >3 days)
> * headache + sensitivity to light → migraine
> * cough + fever + shortness of breath → pneumonia (risk high)
> * diarrhea + dehydration signs → gastroenteritis (risk medium)
> * sore throat + runny nose → common cold (risk low)
> * chest pain + radiating arm pain → possible cardiac issue (risk high → emergency)
>   In `ai/symptom_checker.py`, implement:
> * `analyze_symptoms(text:str, selected:list)-> dict` that:
>
>   * normalizes text, matches keywords, aggregates conditions, assigns a **risk score** (0-100) and risk band (low/medium/high),
>   * returns `{"conditions":[...], "advice":[...], "risk":"high"}`.
>     Add conservative defaults: if **red-flag** terms are present (e.g., “severe chest pain”, “fainting”, “bleeding”), set risk=high with emergency advice. Include clear **safety disclaimers** in the return.

---

## Prompt 7 — MindWell (NLP companion)

**Prompt:**

> In `ai/mindwell_bot.py`:
>
> * Use **NLTK VADER** for sentiment (free). Download needed lexicon on first run.
> * Implement `mindwell_reply(user_text)-> dict` that:
>
>   * Analyzes sentiment & detects intents from keyword lists (stress, anxiety, sleep, exam pressure, bullying, loneliness).
>   * Returns empathetic, **non-clinical** responses, **guided breathing** steps, and resource suggestions.
>   * If self-harm indicators are detected (“want to end it”, etc.), return a **crisis message** prompting to contact local helplines or a trusted adult; **do not** provide instructions or judgment.
> * Log each message with `Message` model including `alert_flag` when risk is detected.
>   Add 6–8 **guided exercises** (box breathing, grounding 5-4-3-2-1, journaling prompt, short routine). Keep everything stigma-free and supportive.

---

## Prompt 8 — Provider recommendations (Haversine + filters)

**Prompt:**

> In `ai/recommend.py`, implement:
>
> * `nearest_providers(lat, lng, type=None, limit=5)`:
>
>   * Compute distances using Haversine formula from DB coordinates.
>   * Return nearest N providers, optionally filtered by `type`.
>     In `providers.html`, use **browser geolocation API** (with permission) to get user location; fallback to manual city select (Douala/Yaoundé). Display a ranked list with contact buttons (tel: and mailto:).

---

## Prompt 9 — Flask routes & forms

**Prompt:**

> Implement Flask routes:
>
> * `GET/POST /symptoms` → renders form and on submit runs `ai.symptom_checker.analyze_symptoms(...)`, saves a `SymptomLog`, displays results with risk badge and next steps (self-care vs seek care).
> * `GET/POST /mindwell` → chat page that posts to `/api/mindwell`, appends responses live (use fetch).
> * `GET /providers` with optional `?type=&city=&lat=&lng=` calls `nearest_providers`.
> * `GET /dashboard` → show recent logs, alerts, subscription.
> * `POST /subscribe` → switches plan to `premium` (no real charge yet).
>   Build a small `/admin` page (basic auth with the hardcoded admin) to view alerts and mark consultations as handled.

---

## Prompt 10 — Frontend interactivity & polish

**Prompt:**

> In `static/js/main.js`:
>
> * Add progressive enhancement: async fetch for MindWell chat (`/api/mindwell`), message bubbles, auto-scroll, loading indicator.
> * Multi-step symptom flow with **chips** for common symptoms; on submit, show a skeleton loader then render results with icons (exclamation for risk high, shield for advice, map pin for providers).
> * Providers page: obtain geolocation, then fetch nearest list and render cards with distance (km).
>   In `static/css/style.css`, add small custom styles on top of Tailwind: soft shadows, hover states, focus rings, and a simple **teal accent**.

---

## Prompt 11 — Monetization hooks (freemium now, payments later)

**Prompt:**

> Implement **Freemium** now:
>
> * Free: symptom checks, basic MindWell chat, 3 provider lookups/day.
> * Premium (demo): unlimited checks, priority MindWell, “Request doctor callback” button.
>   Add `/subscribe` (no payment yet) and a **Premium upsell modal** explaining benefits.
>   Add a `payments.md` with instructions for **Flutterwave/Paystack sandbox** integration for later (test keys only).


---
