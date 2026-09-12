# LIFE RPG / LIFEDEX

> **Transform your real-life progress into an epic creature-taming RPG.**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4+-38B2AC.svg)](https://tailwindcss.com/)

---

## 🌟 Vision & The Core Loop

Built for a 1,000+ team hackathon, **LIFE RPG / LIFEDEX** rejects the mundane trope of *"To-Do List + XP Bar"*. Instead, it treats your personal self-improvement as the heartbeat of a living digital universe.

```
REAL-LIFE PROGRESS
        ↓
ACTIVITIES & HABITS
        ↓
SIX-PILLAR ATTRIBUTES (STR, INT, WIS, DIS, VIT, CHA)
        ↓
CREATURE ("ANIMA") DEVELOPMENT
        ↓
BRANCHED EVOLUTION
        ↓
LIFEDEX COLLECTION
```

Every user awakens with the same morphic companion: **Aetherling (The Origin Wisp)**. How you spend your waking hours determines what it evolves into:
- Code, study mathematics, and read architecture? $\rightarrow$ Awaken **Luminaur (The Arcanist)**.
- Lift weights, run trails, and push athletic boundaries? $\rightarrow$ Awaken **Pyrokyn (The Ember Vanguard)**.
- Meditate, journal, and reflect? $\rightarrow$ Awaken **Sylphora (The Mindweaver)**.
- Cultivate balanced mastery across all 6 life pillars? $\rightarrow$ Awaken the ultra-rare **Harmonix (The Equilibrium Drake)**.

---

## 🏆 Key Features

- 🦊 **Original Creature Universe ("Anima")**: 15 distinct species across 3 tiers, complete with original lore, stat scalers, emotional states, and visual expressions.
- 🧬 **Deterministic Branched Evolution**: Companion metamorphosis mirrors your personal attribute ratios, streaks, and completed milestones.
- ⚡ **Six-Pillar Attribute Engine**: Multi-dimensional character development across Strength, Intelligence, Wisdom, Discipline, Vitality, and Charisma.
- 🛡️ **Goal Quest Chains**: Break down epic life aspirations into unlocking sequential quest steps.
- 🔥 **Timezone-Aware Streak Engine**: Consistency bonuses, milestone achievements, and anti-cheat validation.
- 📜 **Immutable Chronicle**: An append-only historical log celebrating your real-world achievements and companion growth.
- 📖 **Lifedex Collection**: Discover and unlock every branch in the Anima family tree.
- 🔒 **Server-Authoritative Anti-Cheat**: Zero client trust for progression metrics; secure JWT authentication and strict user isolation.

---

## 👥 Autonomous Team Structure

Four autonomous agents collaborate on this repository:

| Role | Domain | Primary Focus |
| :--- | :--- | :--- |
| **PERSON 1** | **Backend & Game Systems (Lead Architect)** | Progression engine, evolution state machine, REST API, anti-cheat, server validation, Pytest suite. |
| **PERSON 2** | **Frontend & UI/UX Experience** | React + TypeScript app, Framer Motion animations, companion status HUD, tactile game feel. |
| **PERSON 3** | **Database & Security** | PostgreSQL schema, Alembic migrations, database constraints, indexing, RLS policies. |
| **PERSON 4** | **QA, Integration & CI/CD** | Automated CI workflows, Docker packaging, end-to-end testing, deployment orchestration. |

---

## 📚 Project Documentation (Source of Truth)

- 🤖 [AGENTS.md](./AGENTS.md) — Team roles, boundaries, and collaboration protocols.
- 🏛️ [ARCHITECTURE.md](./ARCHITECTURE.md) — System architecture, modular design, and data flows.
- 📋 [REQUIREMENTS.md](./REQUIREMENTS.md) — Functional and non-functional specifications.
- 🎮 [GAME_SYSTEM.md](./GAME_SYSTEM.md) — Progression curves, XP formulas, and attribute distributions.
- 🐾 [CREATURE_SYSTEM.md](./CREATURE_SYSTEM.md) — Species catalog, stats, emotional bond mechanics.
- 🧬 [EVOLUTION_SYSTEM.md](./EVOLUTION_SYSTEM.md) — Deterministic evolution state machine and branching rules.
- 🔌 [API_CONTRACT.md](./API_CONTRACT.md) — Complete REST API contract with request/response schemas.
- 🗄️ [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) — Relational schema, indices, foreign keys, and constraints.
- 🎨 [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) — Design tokens, color palette, typography, and motion standards.
- 🤝 [CONTRIBUTING.md](./CONTRIBUTING.md) — Git workflow and safety guidelines.
- 📌 [TASKS.md](./TASKS.md) — Master backlog and milestone tracker.

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.13+
- Node.js 20+ & npm

### Backend Setup (FastAPI)
```bash
# 1. Navigate to backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations / seed
# (Handled automatically on startup in development mode)

# 5. Start the FastAPI development server
uvicorn app.main:app --reload --port 8000

# 6. Open interactive API docs: http://localhost:8000/docs
```

### Running Backend Tests
```bash
pytest -v backend/tests/
```