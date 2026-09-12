# LIFE RPG / LIFEDEX — Project Requirements (REQUIREMENTS.md)

## 1. Executive Summary & Competition Objective

LIFE RPG (LIFEDEX) turns real-life self-improvement into an immersive, monster-taming game experience. Competing against 1,000+ teams, the project rejects shallow "gamification" (simple XP bars on a to-do list) in favor of deep game systems:
- An **original creature universe ("Anima")** where companions branch into specialized forms reflecting how the user lives their real life.
- A **multi-pillar attribute engine** (Strength, Intelligence, Wisdom, Discipline, Vitality, Charisma).
- **Goal quest chains** that break epic life aspirations into unlocking sequential quests.
- An **immutable life chronicle** celebrating the user's real-world transformation.

---

## 2. Functional Requirements (FR)

### FR1: Authentication & Identity Management
- **FR1.1**: Secure user registration with unique username and email.
- **FR1.2**: Password encryption using industry-standard hashing algorithms (`bcrypt` / `argon2`).
- **FR1.3**: Session management via stateless JSON Web Tokens (JWT Bearer tokens).
- **FR1.4**: Strict tenant isolation: users can never view, complete, or mutate another user's data.

### FR2: Character Attributes & Core Profile
- **FR2.1**: Each character possesses a character level, total XP, and 6 core attributes:
  - **STR (Strength)**: Physical exertion, strength training, athletic output.
  - **INT (Intelligence)**: Programming, engineering, mathematics, analytical problem solving.
  - **WIS (Wisdom)**: Reading, meditation, philosophical reflection, writing.
  - **DIS (Discipline)**: Habit consistency, focus blocks, deep work adherence.
  - **VIT (Vitality)**: Sleep duration, nutrition, recovery, hydration, active wellness.
  - **CHA (Charisma)**: Public speaking, interpersonal communication, teamwork.
- **FR2.2**: Non-linear level curves prevent inflation while rewarding long-term sustained effort.

### FR3: Activity & Habit Engine
- **FR3.1**: Users can create, update, list, and soft-delete activities.
- **FR3.2**: Activity categorization: `HABIT` (recurring daily/weekly), `TASK` (one-off action), or `QUEST_STEP` (part of a chain).
- **FR3.3**: Difficulty tiers: `TRIVIAL` (1x), `EASY` (1.5x), `MEDIUM` (2.5x), `HARD` (4x), `HEROIC` (7x).
- **FR3.4**: Attribute weights: each activity assigns primary and optional secondary attributes.
- **FR3.5**: Cooldown and frequency enforcement: daily habits can only be completed once per calendar day (evaluated in user timezone).

### FR4: Quest Chains (Major Goals)
- **FR4.1**: Users can create epic goals (e.g. "Run a Half Marathon", "Ship Fullstack SaaS").
- **FR4.2**: Goals break down into sequential quest steps with clear completion criteria.
- **FR4.3**: Step unlocking: Step $N+1$ remains locked until Step $N$ is verified and completed.
- **FR4.4**: Completing an entire quest chain yields bonus companion bond and rare chronicle entries.

### FR5: Creature ("Anima") System
- **FR5.1**: Every new player receives an initial companion: **Aetherling (Origin Wisp)**.
- **FR5.2**: Companions have their own companion level, companion XP, and a **Bond Meter** (0–100) reflecting emotional connection.
- **FR5.3**: Companion gains XP alongside character XP when activities are completed.
- **FR5.4**: Emotional state reflects user behavior (e.g. `THRIVING` during high streaks, `RESTING` when idle).

### FR6: Branched Evolution Engine
- **FR6.1**: Evolutions are deterministic, server-evaluated milestone events.
- **FR6.2**: Evolution triggers occur when:
  - Companion reaches required level threshold (e.g., Level 10 for Tier 2; Level 25 for Tier 3).
  - Specific attribute dominance or combination is fulfilled (e.g., INT $\ge 40\%$ triggers *Arcanist Lumina*; STR $\ge 40\%$ triggers *Pyrokyn*).
  - Streak or quest chain prerequisites are met.
- **FR6.3**: Evolution permanently registers in the user's **Lifedex** (creature collection).
- **FR6.4**: Player can switch active companion between unlocked forms in their collection.

### FR7: Streak Engine
- **FR7.1**: Tracks `current_streak`, `longest_streak`, and `last_activity_date`.
- **FR7.2**: Timezone-aware calculation prevents false resets caused by UTC boundary transitions.
- **FR7.3**: Streak increments on consecutive calendar days; maintains current count on multiple activities in same day; resets to 1 if a full calendar day is missed.
- **FR7.4**: Milestone rewards at 3, 7, 14, 21, 30, and 100 consecutive days.

### FR8: Collection ("Lifedex")
- **FR8.1**: Catalog of all known Anima species and forms in the universe.
- **FR8.2**: Status per creature: `LOCKED` (mystery silhouette), `DISCOVERED` (seen in lore), or `AWAKENED` (evolved/owned).
- **FR8.3**: Detailed stats, lore, evolution path, and discovery timestamp for awakened creatures.

### FR9: Chronicle (Life Event Stream)
- **FR9.1**: Append-only event history capturing every meaningful milestone:
  - Activity completions with attribute diffs.
  - Level ups and tier upgrades.
  - Evolutions and form unlocks.
  - Streak milestones reached.
  - Achievements earned.
- **FR9.2**: Provides rich narrative summaries of personal growth over time.

### FR10: Achievements & Trophies
- **FR10.1**: Built-in system badges awarded dynamically upon meeting conditions (e.g., "Centurion" = 100 tasks; "Iron Will" = 14-day streak; "Polymath" = All 6 attributes $\ge 50$).

---

## 3. Non-Functional Requirements (NFR)

### NFR1: Server Authority & Anti-Cheat
- **Zero Client Trust**: Progression metrics (XP, attributes, level, evolution) can never be set directly via client requests.
- **Replay Protection**: Activity completions enforce idempotent execution or cooldown check to prevent automated request flooding.
- **Boundary Validation**: Numerical values must be strictly validated against positive, realistic bounds.

### NFR2: Performance & Scalability
- **API Response Latency**: Sub-100ms response time for standard activity completions and data fetches.
- **Transactional Integrity**: All attribute gains, creature XP, evolution checks, and chronicle logging must execute inside an atomic database transaction.

### NFR3: Code Quality & Architecture
- Clean separation of concerns: API Routes $\rightarrow$ Service/Game Engines $\rightarrow$ Models & Database.
- 100% type annotations in Python backend (Pydantic v2 & typing).
- Comprehensive automated test coverage for all game calculations and boundary conditions.
