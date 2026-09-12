# LIFE RPG / LIFEDEX — Core Game Systems & Math (GAME_SYSTEM.md)

This document specifies the exact game mechanics, mathematical progression curves, attribute distributions, and rule sets powering **LIFE RPG / LIFEDEX**.

---

## 1. The Six-Pillar Attribute System

Rather than generic "Points", character and creature evolution is shaped by six fundamental life pillars:

| Code | Attribute Name | Real-World Activities | Primary Game Influence |
| :--- | :--- | :--- | :--- |
| **STR** | **Strength** | Weightlifting, calisthenics, running, sports, physical exertion | Companion physical power, defensive resilience |
| **INT** | **Intelligence** | Coding, software architecture, mathematics, engineering, study | Companion analytical power, arcanist evolution |
| **WIS** | **Wisdom** | Reading, philosophy, meditation, journal reflection, chess | Companion intuition, mystical forms, patience |
| **DIS** | **Discipline** | Waking early, deep work blocks, cold showers, fasting, habit streaks | Companion willpower, evolution stability, guardians |
| **VIT** | **Vitality** | Sleep quality, healthy nutrition, hydration, mobility, recovery | Companion energy pool, organic growth, flourishing |
| **CHA** | **Charisma** | Public speaking, networking, leadership, group collaboration | Companion radiance, social aura, inspiring forms |

### Attribute Dominance Formula
When checking evolution branches, the system evaluates the **Relative Attribute Share ($S_a$)** across all earned attribute points:

$$S_a = \frac{\text{AttributeValue}(a)}{\sum_{k \in \{\text{STR, INT, WIS, DIS, VIT, CHA}\}} \text{AttributeValue}(k)}$$

- **Dominance Threshold**: An attribute is considered **Dominant** if $S_a \ge 0.35$ (35% or more of all points).
- **Dual Hybrid Threshold**: Two attributes form a **Hybrid Pair** if $(S_{a1} + S_{a2}) \ge 0.60$ and both are individually $\ge 0.25$.
- **Harmonic / Balanced**: If no single attribute exceeds 0.25, the player has achieved a balanced lifestyle, qualifying for the rare **Paragon / Harmonix** lineage.

---

## 2. Experience Points (XP) & Level Curve

Progression uses a convex, polynomial leveling curve to reward early momentum while making high tiers feel prestigious and earned:

### Formula: XP Required for Level $L$
The cumulative XP required to reach Level $L$ is:

$$\text{XP}_{\text{cumulative}}(L) = \left\lfloor 100 \times (L - 1)^{1.6} \right\rfloor \quad \text{for } L \ge 1$$

To find the XP needed to advance from Level $L$ to $L + 1$:
$$\Delta \text{XP}(L) = \text{XP}_{\text{cumulative}}(L + 1) - \text{XP}_{\text{cumulative}}(L)$$

### Progression Milestones Reference Table

| Level | Cumulative XP Required | XP to Next Level | Typical Effort Benchmark |
| :---: | :---: | :---: | :--- |
| **1** | 0 | 100 | Day 1: First activity completed |
| **2** | 100 | 151 | Day 2–3: Establishing routine |
| **5** | 918 | 344 | End of Week 1 |
| **10** | 3,365 | 588 | **Tier 2 Evolution Threshold** (~3 weeks) |
| **15** | 7,043 | 818 | Mid-game mastery |
| **20** | 11,833 | 1,038 | High consistency |
| **25** | 17,665 | 1,250 | **Tier 3 Apex Evolution Threshold** (~2–3 months) |
| **30** | 24,489 | 1,457 | Master companion status |

---

## 3. Activity Difficulty Multipliers & Distribution

Activities have a base reward value of **$20\text{ XP}$**, scaled by difficulty tier:

| Difficulty | Multiplier | XP Earned | Attribute Gain | Example Real-World Task |
| :--- | :---: | :---: | :---: | :--- |
| **TRIVIAL** | $1.0\times$ | $20\text{ XP}$ | 2 pts | Drink 500ml water, make bed, 1 min stretch |
| **EASY** | $1.5\times$ | $30\text{ XP}$ | 4 pts | 15 min brisk walk, 10 pages reading, daily standup |
| **MEDIUM** | $2.5\times$ | $50\text{ XP}$ | 8 pts | 45 min workout, 1 hour focused coding session |
| **HARD** | $4.0\times$ | $80\text{ XP}$ | 14 pts | 2 hour deep work sprint, intense 10km run |
| **HEROIC** | $7.0\times$ | $140\text{ XP}$ | 25 pts | Complete major project milestone, half-marathon |

### Attribute Distribution Calculation
When completing an activity:
- If only a **Primary Attribute** is specified: $100\%$ of the attribute gain is awarded to that pillar.
- If both a **Primary** and **Secondary Attribute** are specified:
  - Primary Attribute receives $\lceil 0.70 \times \text{Attribute Gain} \rceil$
  - Secondary Attribute receives $\lfloor 0.30 \times \text{Attribute Gain} \rfloor$

---

## 4. Streak Mechanics & Consistency Multiplier

Consistency is the cornerstone of life transformation. The streak engine calculates consecutive days using the user's localized timezone:

### Streak Multiplier Bonus Formula
Maintaining a streak grants a focus bonus on all XP earned:

$$\text{Streak Bonus} = \min\left( \text{Current Streak} \times 0.02, \; 0.30 \right)$$

$$\text{Final XP} = \left\lfloor \text{Base XP} \times \text{Difficulty Multiplier} \times (1 + \text{Streak Bonus}) \right\rfloor$$

*(Example: A 10-day streak grants a $+20\%$ XP bonus; maximum streak bonus caps at $+30\%$ at 15+ days).*

### Streak Milestone Unlocks
- **Day 3**: "Ignition Spark" (Achievement + Companion Bond +10)
- **Day 7**: "Week of Steel" (Achievement + Tier 2 Evolution Eligibility)
- **Day 14**: "Unbreakable Routine" (Exclusive Companion Aura visual effect)
- **Day 30**: "Forged in Iron" (Achievement + Rare Lifedex Crest)
- **Day 100**: "Centurion Legend" (Apex Title + Legendary Chronicle Entry)

---

## 5. Goal Quest Chains

For large aspirations, the engine supports hierarchical **Quest Chains**:
```
GOAL: "Become a Full-Stack Engineer"
  ├── Step 1 [COMPLETED]: "Complete Python Backend Tutorial"
  ├── Step 2 [ACTIVE]:    "Build REST API with FastAPI"
  ├── Step 3 [LOCKED]:    "Create React Frontend Interface"
  └── Step 4 [LOCKED]:    "Deploy Docker Container to Cloud"
```

- **Locking Rule**: Step $i+1$ cannot be marked complete until Step $i$ is verified and completed.
- **Quest Chain Completion Reward**: Completing all steps in a chain awards a $+50\%$ bonus XP pool and triggers a guaranteed Companion Bond surge (+25 Bond points).

---

## 6. Immutable Chronicle Stream

The Chronicle is an append-only event log recording every meaningful action. Every entry contains:
- `timestamp`: ISO-8601 UTC timestamp.
- `event_type`: `ACTIVITY_COMPLETED` | `LEVEL_UP` | `EVOLUTION_OCCURRED` | `STREAK_MILESTONE` | `ACHIEVEMENT_UNLOCKED` | `QUEST_CHAIN_COMPLETED`.
- `title`: Human-readable summary (e.g., *"Evolved into Arcanist Lumina"*).
- `details`: Rich JSON payload recording attribute diffs, new levels, and streak numbers.

---

## 7. Server Anti-Cheat & Integrity Rules

1. **Idempotent Execution**: Rapid duplicate requests for the same activity completion within 5 seconds are rejected with `HTTP 409 Conflict`.
2. **Frequency Cooldowns**:
   - Habits marked as `DAILY` can only be completed once per calendar date (in user's timezone).
3. **Daily Sanity Ceiling**: A user cannot complete more than 40 activities within any 24-hour window (prevents automated bots from farming XP).
4. **Prerequisite Enforcement**: Attempting to complete a locked quest step returns `HTTP 400 Bad Request`.
