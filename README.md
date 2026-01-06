# Feature Flag Service

A backend service that allows teams to control feature releases using
runtime-configurable feature flags and percentage-based rollouts.

This project demonstrates a common production pattern used to safely
deploy new features without redeploying code.

---

## What This Service Does

- Stores feature flags with rollout configuration
- Determines whether a feature is enabled for a specific user
- Supports gradual rollouts using percentage-based sampling
- Logs feature evaluation results for debugging and observability
- Provides a simple admin interface to manage feature flags

---

## Core Concepts

### Feature Flags
Each feature has:
- A global ON/OFF switch
- A rollout percentage (0–100)

Even when a feature is enabled, only a subset of users may receive it
depending on the rollout percentage.

### Feature Evaluation
When a request is made to check a feature:
1. The feature configuration is loaded from the database
2. A rollout decision is calculated
3. The result is logged for later inspection
4. The enabled/disabled decision is returned

---

## API Overview

### Evaluate Feature (Core Endpoint)
GET /check-feature?user_id=<id>&feature_name=<name>

Returns whether the feature is enabled for the given user.

---

### Feature Administration
POST /features
GET /features
PUT /features/{feature_name}

Allows creation, listing, and modification of feature flags.

---

## Admin UI

A lightweight HTML-based admin UI is included to:
- View all feature flags
- Toggle feature availability
- Adjust rollout percentages

The UI communicates directly with the backend APIs.

http://127.0.0.1:8000/static/admin.html

---

## Running Locally

```
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy
uvicorn main:app --reload
```
**Project Structure**
```
feature-flag-service/  */n*
├── main.py        # API routes and business logic   
├── models.py      # Database models     
├── schemas.py     # Request/response schemas  
├── database.py    # Database configuration    
├── static/        # Admin UI   
└── README.md  
```

Design Notes
SQLite is used for simplicity and local development
Authentication is intentionally omitted
The focus is on backend logic and system design
Designed to be extended with auth, caching, or persistence layers


## License
MIT

