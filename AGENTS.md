# LIFE RPG / LIFEDEX — Multi-Agent Team Collaboration Guide (AGENTS.md)

This document establishes the official roles, ownership boundaries, responsibilities, and communication protocols for the 4 autonomous developer agents building **LIFE RPG / LIFEDEX**.

All 4 agents operate on a single shared Git repository. To prevent collisions, race conditions, or architecture divergence, all agents must strictly respect the boundaries and guidelines defined below.

---

## 1. Team Directory & Responsibility Matrix

| Agent | Primary Role | Domain & Core Responsibilities | Primary Owned Paths |
| :--- | :--- | :--- | :--- |
| **PERSON 1** | **Lead Architect, Backend & Game Systems** | Overall system architecture, FastAPI backend, game & progression logic, attribute system, creature progression & evolution engine, streaks, quest chains, chronicle history, REST API endpoints, server-side anti-cheat, backend unit & domain tests. | `backend/app/`, `backend/tests/`, `ARCHITECTURE.md`, `GAME_SYSTEM.md`, `CREATURE_SYSTEM.md`, `EVOLUTION_SYSTEM.md`, `API_CONTRACT.md` |
| **PERSON 2** | **Frontend & UI/UX Experience** | React + TypeScript web application, Tailwind CSS, Framer Motion animations, creature visualization & status HUD, game feel, sound effects integration, Lifedex codex screens, responsive mobile & desktop layout. | `frontend/`, `DESIGN_SYSTEM.md`, UI assets |
| **PERSON 3** | **Database, Data Architecture & Security** | PostgreSQL database schema, SQLAlchemy/Alembic migrations, performance indexing, database constraints, row-level security (RLS), JWT security & password hashing policies, data integrity, backup/restore scripts. | `database/`, `backend/alembic/`, `DATABASE_SCHEMA.md` |
| **PERSON 4** | **QA, Integration & CI/CD** | End-to-end integration tests, GitHub Actions CI/CD pipelines, Docker & Docker Compose setup, load testing, anti-cheat penetration testing, deployment guides, production readiness checks. | `.github/`, `docker/`, `tests/integration/`, `Dockerfile`, `docker-compose.yml` |

---

## 2. Agent Specific Guidelines & Protocols

### Person 1 (Lead Architect, Backend & Game Systems) — Current Active Agent
- **Ownership**: The brain of the game. Every XP point, level-up, evolution check, streak validation, and chronicle entry is computed and validated server-side.
- **Rules**:
  - Never trust client inputs for progression metrics.
  - Expose clean, strongly-typed REST APIs adhering to [`API_CONTRACT.md`](./API_CONTRACT.md).
  - Provide Person 2 with comprehensive OpenAPI docs (`/docs`) and deterministic responses.
  - If schema adjustments are required, document the rationale in [`DATABASE_SCHEMA.md`](./DATABASE_SCHEMA.md) and coordinate with Person 3.

### Person 2 (Frontend & UI/UX Experience)
- **Ownership**: Transforming backend state into an immersive, game-first tactile experience.
- **Rules**:
  - Strictly adhere to [`API_CONTRACT.md`](./API_CONTRACT.md) for network calls and request/response payloads.
  - Do not invent client-side game state calculations that override or bypass backend calculations.
  - Adhere to [`DESIGN_SYSTEM.md`](./DESIGN_SYSTEM.md) for color tokens, typography, HUD layouts, and creature representation.
  - If additional API endpoints or fields are needed, request an update to [`API_CONTRACT.md`](./API_CONTRACT.md) rather than making assumptions.

### Person 3 (Database, Data Architecture & Security)
- **Ownership**: The persistence layer, data safety, and schema integrity.
- **Rules**:
  - Person 3 is the ultimate authority on migrations, indexing, and PostgreSQL configuration.
  - Ensure all foreign keys, cascade rules, and audit timestamps are consistent across all models.
  - Keep [`DATABASE_SCHEMA.md`](./DATABASE_SCHEMA.md) perfectly synchronized with migration scripts.

### Person 4 (QA, Integration, CI/CD & Deployment)
- **Ownership**: System stability, automated testing pipelines, and packaging.
- **Rules**:
  - Maintain the automated GitHub Actions workflows (lint, type check, pytest, frontend build).
  - Author comprehensive integration tests in `tests/integration/` that verify end-to-end user journeys across backend and database.
  - Verify that Docker configurations build cleanly and reliably across Linux and Windows environments.

---

## 3. Git Workflow & Safety Rules

All team members must follow safe, collaborative Git practices:

1. **Branch Naming**:
   - Person 1: `feature/game-engine` or `feature/backend-*`
   - Person 2: `feature/frontend-*`
   - Person 3: `feature/database-*`
   - Person 4: `feature/cicd-*` or `feature/qa-*`
2. **Never Work Directly on `main`**:
   - `main` is protected and represents tested, deployable milestones.
3. **Prohibited Git Actions**:
   - `git push --force` or `git push -f` is **strictly forbidden**.
   - `git reset --hard` on shared branches is forbidden.
   - Never overwrite or delete another developer's branch.
4. **Pull Requests**:
   - Each agent submits a Pull Request against `main` when a milestone passes all tests and conforms to documentation.

---

## 4. Shared Source of Truth Documents

The following documents govern the entire project:
- [`README.md`](./README.md) — Project vision, quickstart, pitch.
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — Complete technical architecture & system interactions.
- [`REQUIREMENTS.md`](./REQUIREMENTS.md) — Functional and non-functional specifications.
- [`GAME_SYSTEM.md`](./GAME_SYSTEM.md) — Attributes, XP formulas, multipliers, quest chains.
- [`CREATURE_SYSTEM.md`](./CREATURE_SYSTEM.md) — Original Anima species, stats, bonds, and lifecycle.
- [`EVOLUTION_SYSTEM.md`](./EVOLUTION_SYSTEM.md) — Deterministic evolution state machine & branch rules.
- [`API_CONTRACT.md`](./API_CONTRACT.md) — Complete REST API contract for frontend integration.
- [`DATABASE_SCHEMA.md`](./DATABASE_SCHEMA.md) — Relational schema, indices, constraints.
- [`DESIGN_SYSTEM.md`](./DESIGN_SYSTEM.md) — Visual standards, colors, typography, UI components.
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — Git guidelines and coding standards.
- [`TASKS.md`](./TASKS.md) — Master backlog and progress tracker across all 4 agents.
