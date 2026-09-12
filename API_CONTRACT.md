# LIFE RPG / LIFEDEX — REST API Contract (API_CONTRACT.md)

**Base URL**: `/api/v1`  
**Authentication Scheme**: HTTP Bearer Token (`Authorization: Bearer <jwt_token>`)  
**Format**: `application/json` (All requests and responses)

---

## 1. Authentication Endpoints

### `POST /auth/register`
Creates a new user, default character profile, and awakens the starter **Aetherling** companion.

**Request Body:**
```json
{
  "username": "adventurer42",
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "timezone": "UTC"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "adventurer42",
    "email": "user@example.com",
    "timezone": "UTC",
    "created_at": "2026-09-12T16:00:00Z"
  }
}
```

---

### `POST /auth/login`
Authenticates user and returns JWT.

**Request Body:**
```json
{
  "username": "adventurer42",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "adventurer42",
    "email": "user@example.com",
    "timezone": "UTC"
  }
}
```

---

### `GET /auth/me`
Returns current authenticated user details.

**Headers:** `Authorization: Bearer <token>`  
**Response (200 OK):**
```json
{
  "id": 1,
  "username": "adventurer42",
  "email": "user@example.com",
  "timezone": "UTC"
}
```

---

## 2. Character & Progression Endpoints

### `GET /character`
Returns character level, XP, streak status, and attribute totals.

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "level": 7,
  "current_xp": 1450,
  "xp_for_next_level": 1820,
  "streak": {
    "current_streak": 5,
    "longest_streak": 12,
    "last_activity_date": "2026-09-12"
  },
  "attributes": {
    "STR": 45.0,
    "INT": 85.0,
    "WIS": 30.0,
    "DIS": 60.0,
    "VIT": 40.0,
    "CHA": 20.0
  }
}
```

---

## 3. Activities & Habits Endpoints

### `GET /activities`
Lists all activities owned by authenticated user.

**Query Parameters:**
- `category` (optional): `HABIT` | `TASK`
- `is_active` (optional): `true` | `false`

**Response (200 OK):**
```json
[
  {
    "id": 10,
    "title": "Code Backend Architecture",
    "description": "2 hours focused coding on FastAPI",
    "category": "HABIT",
    "difficulty": "HARD",
    "primary_attribute": "INT",
    "secondary_attribute": "DIS",
    "is_active": true,
    "cooldown_hours": 24,
    "completed_today": false,
    "last_completed_at": "2026-09-11T14:30:00Z"
  }
]
```

---

### `POST /activities`
Creates a new custom activity.

**Request Body:**
```json
{
  "title": "Daily 5km Run",
  "description": "Morning aerobic exercise",
  "category": "HABIT",
  "difficulty": "MEDIUM",
  "primary_attribute": "STR",
  "secondary_attribute": "VIT",
  "cooldown_hours": 24
}
```

**Response (201 Created):** Returns the created activity object.

---

### `POST /activities/{id}/complete`
The core game engine action. Validates, awards XP, scales attributes, updates streak, checks evolution, and returns the full Progression Diff.

**Request Body (Optional metadata):**
```json
{
  "notes": "Completed at 7:00 AM, felt energized"
}
```

**Response (200 OK) — Progression Diff:**
```json
{
  "activity_id": 10,
  "activity_title": "Code Backend Architecture",
  "completed_at": "2026-09-12T16:50:00Z",
  "xp_earned": 96,
  "streak_bonus_multiplier": 0.20,
  "attribute_gains": {
    "INT": 10.0,
    "DIS": 4.0
  },
  "character": {
    "level": 8,
    "current_xp": 1546,
    "leveled_up": false
  },
  "creature": {
    "creature_id": 1,
    "name": "Sparky",
    "species_code": "LUMINAUR",
    "species_name": "Luminaur",
    "previous_level": 9,
    "current_level": 10,
    "leveled_up": true,
    "bond_score": 45,
    "mood": "ECSTATIC",
    "evolution_triggered": true,
    "evolved_from": "Aetherling",
    "evolved_to": "Luminaur",
    "evolution_tier": 2
  },
  "streak": {
    "current_streak": 6,
    "longest_streak": 12,
    "streak_advanced": true
  },
  "new_achievements": [
    {
      "code": "FIRST_EVOLUTION",
      "name": "Awakened Potential",
      "description": "Witness your companion's first evolution.",
      "icon_url": "/assets/badges/first_evolution.svg"
    }
  ]
}
```

---

## 4. Goal Quest Chains Endpoints

### `GET /quest-chains`
Lists all multi-step goal chains.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Master Full-Stack Python & React",
    "description": "Construct production-grade IRL RPG app",
    "status": "IN_PROGRESS",
    "total_steps": 4,
    "completed_steps": 1,
    "steps": [
      {
        "id": 101,
        "step_order": 1,
        "title": "FastAPI Architecture & Engine",
        "difficulty": "HARD",
        "status": "COMPLETED"
      },
      {
        "id": 102,
        "step_order": 2,
        "title": "PostgreSQL & Migration Setup",
        "difficulty": "MEDIUM",
        "status": "UNLOCKED"
      },
      {
        "id": 103,
        "step_order": 3,
        "title": "React Frontend & Framer Motion",
        "difficulty": "HARD",
        "status": "LOCKED"
      }
    ]
  }
]
```

### `POST /quest-chains`
Create a new multi-step quest chain.

---

## 5. Creature & Collection (Lifedex) Endpoints

### `GET /creatures/current`
Returns full profile of user's active Anima companion.

**Response (200 OK):**
```json
{
  "id": 1,
  "nickname": "Sparky",
  "species": {
    "id": 3,
    "code": "LUMINAUR",
    "name": "Luminaur",
    "archetype": "The Arcanist",
    "tier": 2,
    "dominant_attribute": "INT",
    "description": "Sleek fox-like creature enveloped in indigo geometric light rings.",
    "sprite_asset_key": "luminaur_idle"
  },
  "level": 10,
  "current_xp": 3400,
  "bond_score": 45,
  "mood": "ECSTATIC",
  "stats": {
    "hp": 250,
    "attack": 140,
    "defense": 80,
    "focus": 210,
    "presence": 75
  }
}
```

---

### `GET /creatures/collection`
Returns the complete **Lifedex** catalog (15 total species).

**Response (200 OK):**
```json
[
  {
    "species_id": 1,
    "species_code": "AETHERLING",
    "species_name": "Aetherling",
    "tier": 1,
    "status": "AWAKENED",
    "unlocked_at": "2026-09-12T16:00:00Z"
  },
  {
    "species_id": 3,
    "species_code": "LUMINAUR",
    "species_name": "Luminaur",
    "tier": 2,
    "status": "AWAKENED",
    "unlocked_at": "2026-09-12T16:50:00Z"
  },
  {
    "species_id": 2,
    "species_code": "PYROKYN",
    "species_name": "???",
    "tier": 2,
    "status": "LOCKED",
    "silhouette_asset_key": "pyrokyn_locked"
  }
]
```

---

### `POST /creatures/active/{species_id}`
Switches active companion form between any awakened species.

---

## 6. Chronicle & History Endpoints

### `GET /chronicle`
Paginated audit stream of life events.

**Query Parameters:**
- `page` (default: 1)
- `page_size` (default: 20)

**Response (200 OK):**
```json
{
  "total": 45,
  "page": 1,
  "items": [
    {
      "id": 101,
      "event_type": "EVOLUTION_OCCURRED",
      "title": "Aetherling evolved into Luminaur!",
      "description": "Dominance in Intelligence (INT) triggered Ascension to Tier 2 Arcanist.",
      "created_at": "2026-09-12T16:50:00Z",
      "metadata": {
        "previous_species": "AETHERLING",
        "new_species": "LUMINAUR",
        "level": 10
      }
    }
  ]
}
```

---

## 7. Standard Error Response Schema

All errors adhere to RFC 7807 problem details:
```json
{
  "detail": {
    "error_code": "COOLDOWN_ACTIVE",
    "message": "This habit was already completed today. Available again tomorrow.",
    "cooldown_remaining_seconds": 18450
  }
}
```

| HTTP Status | Error Code | Description |
| :---: | :--- | :--- |
| `400` | `LOCKED_STEP` | Attempted to complete a quest step whose prerequisite is incomplete. |
| `401` | `UNAUTHORIZED` | Invalid or expired Bearer token. |
| `403` | `FORBIDDEN` | Attempting to access or complete another user's activity. |
| `404` | `NOT_FOUND` | Resource ID does not exist. |
| `409` | `COOLDOWN_ACTIVE` | Frequency cooldown prevents re-completion. |
| `422` | `VALIDATION_ERROR` | Request payload failed Pydantic schema validation. |
