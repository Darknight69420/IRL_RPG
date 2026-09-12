# LIFE RPG / LIFEDEX — Deterministic Evolution Engine (EVOLUTION_SYSTEM.md)

## 1. Core Philosophy: Evolution as Personal Metamorphosis

In standard RPGs, evolution is a generic linear milestone: *Reach level 16 $\rightarrow$ evolve into predetermined creature*.

In **LIFE RPG / LIFEDEX**, evolution is a **mirror of human behavior**. Two players who start on the exact same day with the exact same starter companion (**Aetherling**) will arrive at completely different creatures after 30 days based solely on how they spent their waking hours:
- The programmer/mathematician evolves **Luminaur (The Arcanist)**.
- The athlete/weightlifter evolves **Pyrokyn (The Ember Vanguard)**.
- The balanced practitioner of meditation, reading, and fitness evolves **Harmonix (The Equilibrium Drake)**.

---

## 2. The Evolution State Machine

Evolution is strictly evaluated server-side upon the completion of any activity. The client cannot request or force an evolution.

```
                    ┌─────────────────────────┐
                    │   TIER 1: AETHERLING    │
                    │       (Level 1-9)       │
                    └────────────┬────────────┘
                                 │
                 Condition: Level >= 10, Bond >= 40
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  EVALUATE ATTRIBUTES    │
                    └────────────┬────────────┘
        ┌───────────┬────────────┼───────────┬───────────┐
        │           │            │           │           │
     STR>=35%    INT>=35%     WIS>=35%    DIS>=35%    Balanced
        │           │            │           │           │
        ▼           ▼            ▼           ▼           ▼
   [ PYROKYN ] [ LUMINAUR ] [ SYLPHORA ] [ AEGISKYN ] [ HARMONIX ]
        │           │            │           │           │
        └───────────┴────────────┼───────────┴───────────┘
                                 │
       Condition: Level >= 25, Bond >= 80, Streak >= 21, Chain >= 1
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    TIER 3: APEX MYTHIC  │
                    │ (Ignitan / Archon / etc)│
                    └─────────────────────────┘
```

---

## 3. Exact Mathematical Evolution Rules

### Tier 1 $\rightarrow$ Tier 2 (Ascension)
- **Base Level Gate**: Companion Level $\ge 10$.
- **Bond Gate**: Companion Bond Score $\ge 40$.
- **Attribute Evaluation**:
  Compute total attribute points:
  $$P_{\text{total}} = \text{STR} + \text{INT} + \text{WIS} + \text{DIS} + \text{VIT} + \text{CHA}$$

  If $P_{\text{total}} == 0$, evolution defaults to **Harmonix**. Otherwise, calculate percentage share $S_a = P_a / P_{\text{total}}$:

  1. **Pyrokyn**: $S_{\text{STR}} \ge 0.35$
  2. **Luminaur**: $S_{\text{INT}} \ge 0.35$
  3. **Sylphora**: $S_{\text{WIS}} \ge 0.35$
  4. **Aegiskyn**: $S_{\text{DIS}} \ge 0.35$
  5. **Floravita**: $S_{\text{VIT}} \ge 0.35$
  6. **Solaris**: $S_{\text{CHA}} \ge 0.35$
  7. **Harmonix (Tie-Break / Balance)**:
     - If no single attribute reaches $0.35$, or if multiple attributes are tied at the highest share, the companion evolves into **Harmonix (The Equilibrium Drake)**.

---

### Tier 2 $\rightarrow$ Tier 3 (Apex Metamorphosis)
- **Base Level Gate**: Companion Level $\ge 25$.
- **Bond Gate**: Companion Bond Score $\ge 80$.
- **Streak Gate**: Active or Longest Streak $\ge 21$ consecutive days.
- **Quest Chain Gate**: At least $1$ complete Goal Quest Chain finalized.
- **Target Form**:
  The companion evolves directly into the Apex form corresponding to its Tier 2 lineage:
  - `Pyrokyn` $\rightarrow$ `Ignitan Colossus`
  - `Luminaur` $\rightarrow$ `Archon Chronosage`
  - `Sylphora` $\rightarrow$ `Aethermind Oracle`
  - `Aegiskyn` $\rightarrow$ `Bastion Juggernaut`
  - `Floravita` $\rightarrow$ `Yggdrasil Vitalis`
  - `Solaris` $\rightarrow$ `Sovereign Solari`
  - `Harmonix` $\rightarrow$ `Primordial Paragon`

---

## 4. Lifedex Unlock & Form Switching

1. **Permanent Codex Registration**:
   Every time an evolution is verified, the server inserts an entry into the user's **Lifedex Collection** table (`collection_entries`), recording:
   - `species_id`
   - `species_name`
   - `unlocked_at` timestamp
   - `historical_attributes` at the moment of evolution.
2. **Form Bonding**:
   Players can set any previously unlocked Anima form as their **Active Companion** via:
   `POST /api/v1/creatures/active/{species_id}`.
   This guarantees that evolving a creature never robs the player of aesthetics they love, while rewarding curiosity to unlock all 15 species.

---

## 5. Server Algorithm Pseudocode

```python
def evaluate_evolution(creature: Creature, character: Character, streak: Streak, completed_chains_count: int) -> Optional[Species]:
    # Check Tier 1 -> Tier 2
    if creature.species.tier == 1:
        if creature.level >= 10 and creature.bond_score >= 40:
            total_points = sum(character.attributes.values())
            if total_points == 0:
                return get_species_by_code("HARMONIX")
            
            # Find maximum attribute
            dominant_attr, max_pts = max(character.attributes.items(), key=lambda x: x[1])
            share = max_pts / total_points
            
            if share >= 0.35:
                mapping = {
                    "STR": "PYROKYN",
                    "INT": "LUMINAUR",
                    "WIS": "SYLPHORA",
                    "DIS": "AEGISKYN",
                    "VIT": "FLORAVITA",
                    "CHA": "SOLARIS"
                }
                return get_species_by_code(mapping[dominant_attr])
            else:
                return get_species_by_code("HARMONIX")
                
    # Check Tier 2 -> Tier 3
    elif creature.species.tier == 2:
        if (creature.level >= 25 and 
            creature.bond_score >= 80 and 
            streak.longest_streak >= 21 and 
            completed_chains_count >= 1):
            
            apex_mapping = {
                "PYROKYN": "IGNITAN_COLOSSUS",
                "LUMINAUR": "ARCHON_CHRONOSAGE",
                "SYLPHORA": "AETHERMIND_ORACLE",
                "AEGISKYN": "BASTION_JUGGERNAUT",
                "FLORAVITA": "YGGDRASIL_VITALIS",
                "SOLARIS": "SOVEREIGN_SOLARI",
                "HARMONIX": "PRIMORDIAL_PARAGON"
            }
            target_code = apex_mapping.get(creature.species.code)
            if target_code:
                return get_species_by_code(target_code)
                
    return None
```
