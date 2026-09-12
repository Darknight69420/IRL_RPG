# LIFE RPG / LIFEDEX — Creature System & Universe Lore (CREATURE_SYSTEM.md)

## 1. The Anima Universe Lore

In the world of **LIFE RPG / LIFEDEX**, creatures are known as **Anima** (singular: *Animon* or *Anima*). 

Anima are metaphysical lifeforms forged from the raw psychological resonance of human discipline, passion, and deliberate effort. They are not captured in the wild with spherical cages. Instead, an Anima **crystallizes from your daily habits**. 

An Anima reflects its human partner's real-life choices like a living mirror:
- Spend your days lifting weights and running sprints, and your Anima develops dense volcanic armor and immense physical power.
- Spend your nights engineering code, solving algorithmic puzzles, and studying complex systems, and your Anima sprouts glowing runic circuits and crystalline focus gems.
- Cultivate mindfulness, meditation, and deep literature, and your Anima ascends into an ethereal, celestial presence.

---

## 2. Species Catalog & Evolution Tree

### Tier 1: The Origin Seed (Starter)
Every player begins their journey with a single morphic entity:

```
                      [ TIER 1: STARTER ]
                          AETHERLING
                      (The Origin Wisp)
                             │
     ┌──────────┬────────────┼────────────┬──────────┬──────────┐
     │          │            │            │          │          │
[STR Dom]  [INT Dom]    [WIS Dom]    [DIS Dom]  [VIT Dom]  [CHA Dom]
     │          │            │            │          │          │
     ▼          ▼            ▼            ▼          ▼          ▼
[TIER 2]   [TIER 2]     [TIER 2]     [TIER 2]   [TIER 2]   [TIER 2]
 PYROKYN   LUMINAUR     SYLPHORA     AEGISKYN   FLORAVITA  SOLARIS
(Vanguard) (Arcanist)  (Mindweaver)  (Warden)   (Sprout)   (Herald)
     │          │            │            │          │          │
     └──────────┴────────────┴─────┬──────┴──────────┴──────────┘
                                   │
                                   ▼
                           [TIER 2 BALANCED]
                               HARMONIX
                         (Equilibrium Drake)
```

#### Species 001: Aetherling (The Origin Wisp)
- **Classification**: Morphic Companion
- **Visual Description**: A floating, soft-glowing sphere of starlight with expressive, luminous eyes and a playful translucent tail. It hums with latent elemental energy, waiting for the player's choices to shape its destiny.
- **Starting Level**: 1
- **Base Attributes**: Balanced distribution across all 6 stats.
- **Temperament**: Curious, loyal, highly impressionable.

---

### Tier 2: Ascendant Forms (Level 10+)
Triggered when the companion reaches **Level 10**, possesses a **Bond $\ge 40$**, and satisfies an attribute dominance requirement:

| Species ID | Name | Archetype | Trigger Condition | Visual & Lore Signature |
| :---: | :--- | :--- | :--- | :--- |
| **#002** | **Pyrokyn** | The Ember Vanguard | STR Dominant ($\ge 35\%$ total pts) | Bipedal flame-creature with obsidian knuckle plates and trailing embers. Radiates heat and athletic vigor. |
| **#003** | **Luminaur** | The Arcanist | INT Dominant ($\ge 35\%$ total pts) | Sleek fox-like creature enveloped in indigo geometric light rings and floating arcane scrolls. |
| **#004** | **Sylphora** | The Mindweaver | WIS Dominant ($\ge 35\%$ total pts) | Feathered ethereal owl-serpent that glides silently, surrounded by gentle wind currents and soft chimes. |
| **#005** | **Aegiskyn** | The Iron Warden | DIS Dominant ($\ge 35\%$ total pts) | Armored wolf-sentinel clad in interlocking silver plates, unbreakable poise, and a stone-cold stare. |
| **#006** | **Floravita** | The Living Grove | VIT Dominant ($\ge 35\%$ total pts) | Quadruped creature composed of living moss, glowing bioluminescent blossoms, and wooden stag horns. |
| **#007** | **Solaris** | The Dawn Herald | CHA Dominant ($\ge 35\%$ total pts) | Magnificent golden bird-lion with a shimmering solar crest that invigorates everyone nearby. |
| **#008** | **Harmonix** | The Equilibrium Drake | Balanced (No stat $> 25\%$, all $\ge 12\%$) | Iridescent dragonling pulsing through the color spectrum; represents rare holistic mastery of all life pillars. |

---

### Tier 3: Apex Mythics (Level 25+)
The pinnacle of human consistency. Requires **Level 25**, **Streak $\ge 21$ days**, and completion of at least **one Goal Quest Chain**:

| Species ID | Name | Archetype | Evolved From | Visual Signature |
| :---: | :--- | :--- | :--- | :--- |
| **#009** | **Ignitan Colossus** | Apex Vanguard | Pyrokyn | Massive volcano-forged golem engulfed in continuous plasma fire. |
| **#010** | **Archon Chronosage**| Apex Arcanist | Luminaur | Celestial entity hovering inside fractured concentric time-dials. |
| **#011** | **Aethermind Oracle** | Apex Mindweaver | Sylphora | Transcendent cosmic being crowned with perpetual starlight aurora. |
| **#012** | **Bastion Juggernaut**| Apex Warden | Aegiskyn | Fortress-class metallic titan with an impenetrable diamond shield. |
| **#013** | **Yggdrasil Vitalis** | Apex Grove | Floravita | World-tree leviathan blooming with restorative spiritual essence. |
| **#014** | **Sovereign Solari** | Apex Herald | Solaris | Regal celestial monarch radiating blinding daytime warmth and inspiration. |
| **#015** | **Primordial Paragon** | Apex Polymath | Harmonix | Legendary six-winged cosmic sovereign embodying total human self-actualization. |

---

## 3. Companion Stats & Scaling Formulas

An Anima's combat/companion stats derive directly from the player's personal 6-pillar attribute scores:

$$\text{Max HP} = 100 + (\text{VIT} \times 5) + (\text{Level} \times 10)$$
$$\text{Attack Power} = 10 + (\text{STR} \times 2.5) + (\text{INT} \times 1.5)$$
$$\text{Willpower / Defense} = 10 + (\text{DIS} \times 3.0) + (\text{WIS} \times 1.0)$$
$$\text{Focus / Mana} = 50 + (\text{INT} \times 3.0) + (\text{WIS} \times 2.0)$$
$$\text{Presence / Aura} = 10 + (\text{CHA} \times 2.5) + (\text{Bond} \times 0.5)$$

---

## 4. Emotional States & Bond Meter

Companions are living digital partners, not passive stat cards. Their emotional state actively reflects the player's daily diligence:

### Bond Meter (0 to 100 Points)
- **+2 Bond**: Per completed activity (max 10/day).
- **+5 Bond**: On maintaining a daily streak.
- **+25 Bond**: On completing a full Goal Quest Chain.
- **-5 Bond**: If no activity is logged for 3 consecutive days (never drops below 0).

### Mood States
1. **ECSTATIC** (Bond $\ge 80$ & Streak $\ge 7$): Companion exhibits vibrant glowing particle animations and grants $+10\%$ bonus XP on all activities.
2. **ENERGIZED** (Activity logged today): Active, happy animations and responsive sound cues.
3. **CONTENT** (Default healthy state): Normal ambient idle animations.
4. **DROOPY / RESTING** (Inactive $\ge 3$ days): Companion slumbers quietly, gently nudging the player to return to their habits.
