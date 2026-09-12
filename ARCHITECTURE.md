# LIFE RPG / LIFEDEX — System Architecture (ARCHITECTURE.md)

## 1. High-Level System Overview

LIFE RPG (LIFEDEX) converts real-life self-improvement habits into a rich, monster-taming RPG progression system. The architecture is engineered around the principle of **Server Authority**: the client renders the UI, triggers intent, and plays animations, but the backend is the single source of truth for progression math, attribute scaling, streak continuity, evolution conditions, and collection status.

```
+-------------------------------------------------------------------------+
|                                CLIENT LAYER                             |
|       React + TypeScript + Tailwind CSS + Framer Motion (Person 2)       |
+------------------------------------+------------------------------------+
                                     |
                       HTTPS / JSON (REST API)
                       Bearer JWT Authentication
                                     |
                                     v
+-------------------------------------------------------------------------+
|                              BACKEND LAYER                              |
|                   FastAPI + Python 3.13 (Person 1)                       |
|                                                                         |
|  +-------------------+  +--------------------+  +--------------------+  |
|  |  Auth & Security  |  | Activity Controller|  | Creature Controller|  |
|  +-------------------+  +--------------------+  +--------------------+  |
|  | Character Contrl  |  |  Quest Chain Contrl|  | Chronicle & Achieve|  |
|  +-------------------+  +--------------------+  +--------------------+  |
|                                                                         |
|                     === DOMAIN GAME ENGINES ===                         |
|  +-------------------------------------------------------------------+  |
|  | 1. Activity & Quest Engine: Cooldowns, prerequisites, difficulty  |  |
|  | 2. Attribute Engine: Multi-pillar allocation (STR/INT/WIS/etc.)   |  |
|  | 3. Creature Engine: Experience curve, bond score, stat scalers    |  |
|  | 4. Evolution Engine: Deterministic rule evaluation & branching    |  |
|  | 5. Streak Engine: Timezone-aware date tracking & milestone awards |  |
|  | 6. Chronicle Engine: Immutable event sourcing for life history   |  |
|  | 7. Anti-Cheat & Rule Validator: Server-side legitimacy validation |  |
|  +-------------------------------------------------------------------+  |
+------------------------------------+------------------------------------+
                                     |
                           SQLAlchemy (Async ORM)
                                     |
                                     v
+-------------------------------------------------------------------------+
|                            PERSISTENCE LAYER                            |
|                 PostgreSQL / SQLite (Dev & Tests) (Person 3)            |
|                                                                         |
|   [users] <---> [characters] <---> [attributes]                         |
|      |               |                                                  |
|      v               v                                                  |
| [activities] <-> [creatures] <-> [collection_entries]                   |
|      |               |                                                  |
|      v               v                                                  |
| [quest_chains]  [chronicle_events] <-> [achievements]                   |
+-------------------------------------------------------------------------+
```

---

## 2. Core Architectural Principles

### 2.1 Server-Authoritative Progression
- The frontend **NEVER** sends progression metrics (such as `xp_to_add`, `new_level`, `evolve_into_species`).
- The frontend only submits user actions (e.g., `POST /api/v1/activities/42/complete`).
- The server:
  1. Authenticates the user and verifies activity ownership.
  2. Validates execution constraints (frequency limits, daily cooldowns, quest chain step prerequisites).
  3. Computes raw XP and attribute distributions using deterministic server formulas.
  4. Updates character and active creature state within a single atomic database transaction.
  5. Evaluates evolution thresholds and unlocks new forms when criteria are satisfied.
  6. Evaluates streak continuity against user's local timezone.
  7. Emits structured `Chronicle` events and unlocks any newly earned achievements.
  8. Returns a rich **Progression Diff** to the client so the frontend can orchestrate celebration animations.

### 2.2 Rich Progression Diff Response Pattern
When an activity is completed, the API responds with the state changes resulting from the action:
```json
{
  "activity_id": 42,
  "completed_at": "2026-09-12T16:45:00Z",
  "xp_earned": 120,
  "attribute_gains": {
    "INT": 15.0,
    "DIS": 10.0
  },
  "character_level_up": false,
  "creature_progression": {
    "creature_id": 1,
    "xp_gained": 120,
    "previous_level": 9,
    "new_level": 10,
    "leveled_up": true,
    "evolution_triggered": true,
    "evolved_from": "Aetherling",
    "evolved_to": "Arcanist Lumina",
    "new_form_unlocked": true
  },
  "streak_update": {
    "current_streak": 8,
    "longest_streak": 8,
    "streak_milestone_reached": false
  },
  "unlocked_achievements": [
    {
      "code": "FIRST_EVOLUTION",
      "name": "Awakened Potential",
      "description": "Witness your companion's first evolution."
    }
  ]
}
```
This enables Person 2 to build thrilling animation sequences (e.g. XP fill bar -> Level Up banner -> Evolution flash -> Lifedex badge) without needing to perform math on the client.

---

## 3. Technology Stack Rationale

| Component | Choice | Rationale |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI (Python 3.13)** | High performance, native async/await, Pydantic v2 validation, automatic OpenAPI / Swagger interactive documentation, excellent for clean REST contracts. |
| **ORM & Persistence** | **SQLAlchemy 2.0** | Industry-standard Python ORM. Seamless transition between SQLite for instant, zero-dependency testing and PostgreSQL for production deployments. |
| **Data Validation** | **Pydantic v2** | Blazing fast Rust-powered validation, strict typing, easy schema sharing with frontend. |
| **Authentication** | **JWT (Bearer Tokens) + Passlib/Bcrypt** | Stateless, scalable, secure, industry standard for single-page applications. |
| **Frontend Framework** | **React + TypeScript + Vite** | Rapid component development, type safety directly aligning with backend schemas. |
| **Styling & Motion** | **Tailwind CSS + Framer Motion** | Essential for delivering a game-feel experience with smooth XP bars, floating combat-style text numbers, and creature evolution effects. |

---

## 4. Repository Structure

```
IRLRPG/
├── AGENTS.md                 # Multi-agent role matrix and guidelines
├── ARCHITECTURE.md           # System architecture overview (this file)
├── REQUIREMENTS.md           # Functional & non-functional requirements
├── GAME_SYSTEM.md            # Progression curves, formulas, attributes
├── CREATURE_SYSTEM.md        # Creature lore, species, stats, bonds
├── EVOLUTION_SYSTEM.md       # Evolution branches, conditions, algorithms
├── API_CONTRACT.md           # Complete REST API specifications
├── DATABASE_SCHEMA.md        # Relational schema and database design
├── DESIGN_SYSTEM.md          # UI tokens, aesthetic direction, components
├── CONTRIBUTING.md           # Git workflow and code quality guidelines
├── TASKS.md                  # Team task board and milestones
├── README.md                 # Project vision, pitch, setup
│
├── backend/
│   ├── app/
│   │   ├── api/v1/           # API Routers & Endpoints
│   │   ├── core/             # Configuration, Database, Security, Error handlers
│   │   ├── models/           # SQLAlchemy DB Models
│   │   ├── schemas/          # Pydantic Schemas (Request/Response)
│   │   ├── services/         # Domain Game Engines (Game, Streak, Evolution, etc.)
│   │   └── main.py           # FastAPI Application Entrypoint
│   ├── tests/                # Automated Pytest Suite
│   ├── requirements.txt      # Python Dependencies
│   └── pytest.ini            # Pytest Configuration
│
└── frontend/                 # React + TypeScript App (Person 2 workspace)
```
