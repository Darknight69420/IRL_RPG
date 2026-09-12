# LIFE RPG / LIFEDEX — Team Backlog & Master Task Board (TASKS.md)

This board coordinates active work streams across the 4 autonomous agents.

---

## PERSON 1: Lead Architect, Backend & Game Systems (Current Agent)

### Phase 1: Architecture & Shared Foundation (Completed)
- [x] Create `AGENTS.md` (Multi-agent roles & rules)
- [x] Create `ARCHITECTURE.md` (System architecture & data flows)
- [x] Create `REQUIREMENTS.md` (Functional & non-functional specs)
- [x] Create `GAME_SYSTEM.md` (Progression curves, attribute math, streak mechanics)
- [x] Create `CREATURE_SYSTEM.md` (Original Anima universe, species, stats, bonds)
- [x] Create `EVOLUTION_SYSTEM.md` (Deterministic state machine & branching rules)
- [x] Create `API_CONTRACT.md` (Full REST API contract for frontend)
- [x] Create `DATABASE_SCHEMA.md` (PostgreSQL relational schema & constraints)
- [x] Create `DESIGN_SYSTEM.md` (Visual design tokens & motion standards)
- [x] Create `CONTRIBUTING.md` (Git safety & branch guidelines)
- [x] Create `TASKS.md` (Team task board)
- [x] Update `README.md` (Project pitch, setup, and overview)

### Phase 2: Full Backend & Engine Implementation (Active)
- [ ] Initialize Python 3.13 project structure with FastAPI & SQLAlchemy
- [ ] Implement SQLAlchemy data models (`User`, `Character`, `Attribute`, `Species`, `Creature`, `Collection`, `Streak`, `Activity`, `QuestChain`, `QuestStep`, `Chronicle`, `Achievement`)
- [ ] Seed the 15 original Anima species into the database
- [ ] Implement Pydantic v2 validation schemas matching `API_CONTRACT.md`
- [ ] Implement JWT authentication, password hashing, and user isolation
- [ ] Implement `AttributeEngine` & `ProgressionEngine` (XP curves, difficulty multipliers)
- [ ] Implement `CreatureEngine` (Stats, bond score, mood states)
- [ ] Implement `EvolutionEngine` (Tier 1 $\rightarrow$ Tier 2 branched logic, Tier 3 apex, Lifedex registration)
- [ ] Implement `StreakEngine` (Timezone-aware date tracking, milestone bonuses)
- [ ] Implement `QuestChainEngine` (Goal hierarchy & step locking)
- [ ] Implement `ChronicleEngine` (Immutable event logging)
- [ ] Implement `AchievementEngine` (Automated badge unlocks)
- [ ] Implement Anti-Cheat and validation guards (cooldowns, idempotency, ownership)
- [ ] Implement API routers (`auth`, `character`, `activities`, `creatures`, `quest_chains`, `chronicle`, `achievements`)
- [ ] Author comprehensive Pytest test suite covering all game mechanics and edge cases

---

## PERSON 2: Frontend, UI/UX & Visual Experience

- [ ] Initialize React + TypeScript + Vite workspace in `frontend/`
- [ ] Configure Tailwind CSS with the 6-pillar attribute tokens (`DESIGN_SYSTEM.md`)
- [ ] Build Auth Views (Login, Registration, Welcome Companion Awakening)
- [ ] Build Main HUD / Character Status Window (XP bar, level badge, streak counter)
- [ ] Build Six-Pillar Attribute Radar Chart / Hexagon
- [ ] Build Companion Sanctuary View (Interactive idle stage, mood orb, bond meter)
- [ ] Build Activity & Habit Manager (Daily list, difficulty tags, tactile complete button)
- [ ] Build Framer Motion Evolution Metamorphosis celebration modal
- [ ] Build Lifedex Codex Grid (Awakened colored cards vs mysterious locked silhouettes)
- [ ] Build Goal Quest Chain Visualizer (Interactive unlocked step tree)
- [ ] Build Chronicle Timeline Stream

---

## PERSON 3: Database, Data Architecture & Security

- [ ] Review `DATABASE_SCHEMA.md` and initialize Alembic migrations
- [ ] Configure PostgreSQL production connection pooling and session lifecycle
- [ ] Implement database indexes for query optimization
- [ ] Implement database-level check constraints and cascades
- [ ] Implement automated seed script for the 15 Anima species and system achievements
- [ ] Review password hashing and JWT secret configuration for security compliance

---

## PERSON 4: QA, Integration, CI/CD & Deployment

- [ ] Configure GitHub Actions workflow for automated backend testing and linting
- [ ] Configure frontend build verification in CI
- [ ] Create `Dockerfile` for FastAPI backend
- [ ] Create `Dockerfile` for React frontend
- [ ] Author `docker-compose.yml` orchestrating PostgreSQL, Backend, and Frontend
- [ ] Author end-to-end integration tests in `tests/integration/`
- [ ] Run load testing and rate-limiting penetration tests
