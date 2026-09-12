# LIFE RPG / LIFEDEX — Design System & Visual Guidelines (DESIGN_SYSTEM.md)

This document provides visual guidelines, design tokens, color palettes, and motion principles for **Person 2 (Frontend & UI/UX Experience)**.

---

## 1. Aesthetic Vision: The Modern Hunter HUD

The visual tone of **LIFE RPG / LIFEDEX** sits at the intersection of a **sleek modern game status window** (e.g. Solo Leveling / Persona HUD) and an **organic monster-companion sanctuary**. 

### Guiding Pillars
1. **Game-Feel First**: Every action should generate tactile feedback — button presses feel tactile, XP bars surge with physics, attribute gains trigger floating numerals, and evolutions feel triumphant.
2. **Glanceable Clarity**: The user's companion, current streak, active daily habits, and attribute balance should be readable in under 3 seconds.
3. **Restraint Over Clutter**: Dark translucent glassmorphism surfaces with high-contrast neon accents, avoiding overwhelming visual noise.

---

## 2. Color Palette & Design Tokens

### Base Theme (Dark / Obsidian Default)
```css
--bg-canvas:       #0A0D14;  /* Deepest cosmic void */
--bg-surface:      #111726;  /* Panel & card background */
--bg-surface-elev: #1A2238;  /* Hovered or elevated state */
--border-subtle:   #2A3654;  /* Subtle panel borders */
--border-glow:     #3B82F666;/* Active glowing borders */
--text-primary:    #F8FAFC;  /* High contrast primary text */
--text-secondary:  #94A3B8;  /* Muted labels & timestamps */
--text-muted:      #64748B;  /* Inactive states & placeholders */
```

### The Six Pillar Attribute Colors
Each attribute has a dedicated semantic color family for icons, tags, and progress bars:

| Attribute | Code | Primary Hex | Glow Accent Hex | Semantic Association |
| :--- | :--- | :--- | :--- | :--- |
| **Strength** | `STR` | `#EF4444` | `#F87171` | Blazing Ember / Crimson |
| **Intelligence** | `INT` | `#38BDF8` | `#60A5FA` | Arcane Cyan / Electric Blue |
| **Wisdom** | `WIS` | `#14B8A6` | `#2DD4BF` | Ethereal Teal / Emerald |
| **Discipline** | `DIS` | `#EAB308` | `#FDE047` | Unyielding Gold / Amber |
| **Vitality** | `VIT` | `#22C55E` | `#4ADE80` | Living Jade / Forest |
| **Charisma** | `CHA` | `#A855F7` | `#C084FC` | Celestial Violet / Magenta |

---

## 3. Typography Hierarchy

- **Primary UI Font**: `Outfit` or `Inter` (geometric, modern, accessible sans-serif).
- **RPG Data & Numbers**: `JetBrains Mono` or `Space Grotesk` (monospace numbers prevent layout shift when XP or stats tick upward).
- **Scale**:
  - `Display / Level`: `text-4xl font-black tracking-tight`
  - `Section Header`: `text-xl font-bold uppercase tracking-wider`
  - `Card Title`: `text-base font-semibold`
  - `Body / Metadata`: `text-sm text-slate-400`
  - `Badge / Pill`: `text-xs font-mono font-bold`

---

## 4. Animation & Motion Design (Framer Motion)

### 4.1 Activity Completion Micro-Interaction
When the user marks an activity complete:
1. Checkbox snaps with a quick haptic spring (`scale: [1, 1.25, 1]`).
2. Floating number floats upward and fades: `+96 XP`, `+10 INT` (`y: [0, -35]`, `opacity: [1, 0]`, duration: 0.8s).
3. Companion status widget bounces with a happy idle expression.
4. XP bar smoothly fills using spring dynamics (`damping: 15, stiffness: 100`).

### 4.2 The Evolution Metamorphosis Sequence
When the API returns `evolution_triggered: true`:
1. **The Gathering**: Screen dims with a radial dark vignette; companion sprite elevates to center screen.
2. **The Pulse**: A glowing aura in the color of the dominant attribute pulses 3 times in sync with an ascending chime.
3. **The Reveal**: Companion morphs from its Tier 1 silhouette into the unlocked Tier 2 form with a dynamic particle burst.
4. **The Trophy**: A modal congratulates the user, displaying the creature's new archetype, stats, and a **"Registered in Lifedex"** animated stamp.

---

## 5. Key UI Component Standards

### 5.1 The Companion Stage
- Placed prominently on the dashboard.
- Displays animated idle state, active bond meter (0–100), current mood badge (`ECSTATIC`, `ENERGIZED`, etc.), and level progress bar.

### 5.2 Attribute Hexagon / Radar Chart
- Visualizes the player's 6 attributes as a spider chart.
- Immediately informs the player which evolution branch they are cultivating.

### 5.3 Lifedex Codex Grid
- 3 columns on mobile, 5 columns on desktop.
- **Awakened**: Full color illustration/sprite, species name, tier badge, discovery date.
- **Locked**: Mystery dark silhouette with glowing question mark and attribute clue (e.g. *"Requires high discipline"*).
