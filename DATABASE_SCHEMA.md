# LIFE RPG / LIFEDEX — Relational Database Schema (DATABASE_SCHEMA.md)

This document specifies the complete relational schema, table structures, constraints, indices, and foreign key cascades for **Person 3 (Database & Security)**.

---

## 1. Entity-Relationship Overview

```
 [users] 1 ──── 1 [characters] 1 ──── * [character_attributes]
    │                 │
    │ 1               │ 1
    ├───────┐         └───────┐
    │       │                 │
    │ 1     │ 1               │ 1
    ▼       ▼                 ▼
[streaks] [creatures] * ─── 1 [species] 1 ─── * [collection_entries]
    │       │                                          ▲
    │       └───────────┐                              │
    │                   ▼                              │
    │ 1           [chronicle_events]                   │
    ├───────────────────┼──────────────────────────────┘
    │ 1                 │ 1
    ▼                   ▼
[activities]      [user_achievements] * ─── 1 [achievements]
    │
    │ 1
    ▼
[quest_chains] 1 ─── * [quest_steps]
```

---

## 2. Table Specifications

### 2.1 `users`
Core authentication and profile entity.
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

---

### 2.2 `characters`
Player's RPG avatar profile.
```sql
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    level INTEGER NOT NULL DEFAULT 1 CHECK (level >= 1),
    current_xp INTEGER NOT NULL DEFAULT 0 CHECK (current_xp >= 0),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_characters_user_id ON characters(user_id);
```

---

### 2.3 `character_attributes`
Stores current scores across the 6 life pillars.
```sql
CREATE TABLE character_attributes (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    code VARCHAR(10) NOT NULL CHECK (code IN ('STR', 'INT', 'WIS', 'DIS', 'VIT', 'CHA')),
    value DOUBLE PRECISION NOT NULL DEFAULT 0.0 CHECK (value >= 0.0),
    CONSTRAINT uq_character_attribute UNIQUE (character_id, code)
);
CREATE INDEX idx_char_attributes_char_id ON character_attributes(character_id);
```

---

### 2.4 `species`
Immutable master seed table defining all 15 Anima species.
```sql
CREATE TABLE species (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    archetype VARCHAR(100) NOT NULL,
    tier INTEGER NOT NULL CHECK (tier IN (1, 2, 3)),
    dominant_attribute VARCHAR(10) NULL,
    description TEXT NOT NULL,
    sprite_asset_key VARCHAR(100) NOT NULL
);
CREATE INDEX idx_species_code ON species(code);
CREATE INDEX idx_species_tier ON species(tier);
```

---

### 2.5 `creatures`
User's instantiated Anima companions.
```sql
CREATE TABLE creatures (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    species_id INTEGER NOT NULL REFERENCES species(id),
    nickname VARCHAR(50) NOT NULL,
    level INTEGER NOT NULL DEFAULT 1 CHECK (level >= 1),
    current_xp INTEGER NOT NULL DEFAULT 0 CHECK (current_xp >= 0),
    bond_score INTEGER NOT NULL DEFAULT 10 CHECK (bond_score >= 0 AND bond_score <= 100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_creatures_user_active ON creatures(user_id, is_active);
```

---

### 2.6 `collection_entries`
The Lifedex: tracks unlocked Anima forms per user.
```sql
CREATE TABLE collection_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    species_id INTEGER NOT NULL REFERENCES species(id),
    status VARCHAR(20) NOT NULL DEFAULT 'AWAKENED' CHECK (status IN ('DISCOVERED', 'AWAKENED')),
    unlocked_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_species_collection UNIQUE (user_id, species_id)
);
CREATE INDEX idx_collection_user_id ON collection_entries(user_id);
```

---

### 2.7 `streaks`
Consecutive activity tracking.
```sql
CREATE TABLE streaks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    current_streak INTEGER NOT NULL DEFAULT 0 CHECK (current_streak >= 0),
    longest_streak INTEGER NOT NULL DEFAULT 0 CHECK (longest_streak >= 0),
    last_activity_date DATE NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_streaks_user_id ON streaks(user_id);
```

---

### 2.8 `activities`
Real-life habits and tasks configured by the user.
```sql
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NULL,
    category VARCHAR(20) NOT NULL DEFAULT 'HABIT' CHECK (category IN ('HABIT', 'TASK')),
    difficulty VARCHAR(20) NOT NULL DEFAULT 'MEDIUM' CHECK (difficulty IN ('TRIVIAL', 'EASY', 'MEDIUM', 'HARD', 'HEROIC')),
    primary_attribute VARCHAR(10) NOT NULL CHECK (primary_attribute IN ('STR', 'INT', 'WIS', 'DIS', 'VIT', 'CHA')),
    secondary_attribute VARCHAR(10) NULL CHECK (secondary_attribute IN ('STR', 'INT', 'WIS', 'DIS', 'VIT', 'CHA')),
    cooldown_hours INTEGER NOT NULL DEFAULT 24,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_completed_at TIMESTAMP WITH TIME ZONE NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_activities_user_active ON activities(user_id, is_active);
```

---

### 2.9 `quest_chains` & `quest_steps`
Multi-step goal hierarchy.
```sql
CREATE TABLE quest_chains (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'IN_PROGRESS' CHECK (status IN ('IN_PROGRESS', 'COMPLETED', 'ABANDONED')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE NULL
);
CREATE INDEX idx_quest_chains_user ON quest_chains(user_id);

CREATE TABLE quest_steps (
    id SERIAL PRIMARY KEY,
    chain_id INTEGER NOT NULL REFERENCES quest_chains(id) ON DELETE CASCADE,
    step_order INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    difficulty VARCHAR(20) NOT NULL DEFAULT 'MEDIUM' CHECK (difficulty IN ('TRIVIAL', 'EASY', 'MEDIUM', 'HARD', 'HEROIC')),
    primary_attribute VARCHAR(10) NOT NULL DEFAULT 'INT',
    status VARCHAR(20) NOT NULL DEFAULT 'LOCKED' CHECK (status IN ('LOCKED', 'UNLOCKED', 'COMPLETED')),
    completed_at TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT uq_chain_step_order UNIQUE (chain_id, step_order)
);
CREATE INDEX idx_quest_steps_chain ON quest_steps(chain_id, step_order);
```

---

### 2.10 `chronicle_events`
Immutable event stream recording personal growth milestones.
```sql
CREATE TABLE chronicle_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    metadata_json TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_chronicle_user_date ON chronicle_events(user_id, created_at DESC);
```

---

### 2.11 `achievements` & `user_achievements`
System-wide trophies and badges.
```sql
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    icon_url VARCHAR(255) NOT NULL
);

CREATE TABLE user_achievements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    achievement_id INTEGER NOT NULL REFERENCES achievements(id),
    unlocked_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_achievement UNIQUE (user_id, achievement_id)
);
CREATE INDEX idx_user_achievements_user ON user_achievements(user_id);
```
