from sqlalchemy.orm import Session
from app.models.species import Species
from app.models.achievement import Achievement

SPECIES_SEED = [
    # Tier 1 (Starter)
    {
        "code": "AETHERLING",
        "name": "Aetherling",
        "archetype": "The Origin Wisp",
        "tier": 1,
        "dominant_attribute": None,
        "description": "A floating, soft-glowing sphere of starlight with expressive luminous eyes. It hums with latent elemental energy, waiting for the player's choices to shape its destiny.",
        "sprite_asset_key": "aetherling_idle"
    },
    # Tier 2 (Ascendant Evolutions)
    {
        "code": "PYROKYN",
        "name": "Pyrokyn",
        "archetype": "The Ember Vanguard",
        "tier": 2,
        "dominant_attribute": "STR",
        "description": "Bipedal flame-creature with obsidian knuckle plates and trailing embers. Radiates heat and athletic vigor.",
        "sprite_asset_key": "pyrokyn_idle"
    },
    {
        "code": "LUMINAUR",
        "name": "Luminaur",
        "archetype": "The Arcanist",
        "tier": 2,
        "dominant_attribute": "INT",
        "description": "Sleek fox-like creature enveloped in indigo geometric light rings and floating arcane scrolls.",
        "sprite_asset_key": "luminaur_idle"
    },
    {
        "code": "SYLPHORA",
        "name": "Sylphora",
        "archetype": "The Mindweaver",
        "tier": 2,
        "dominant_attribute": "WIS",
        "description": "Feathered ethereal owl-serpent that glides silently, surrounded by gentle wind currents and soft chimes.",
        "sprite_asset_key": "sylphora_idle"
    },
    {
        "code": "AEGISKYN",
        "name": "Aegiskyn",
        "archetype": "The Iron Warden",
        "tier": 2,
        "dominant_attribute": "DIS",
        "description": "Armored wolf-sentinel clad in interlocking silver plates, unbreakable poise, and a stone-cold stare.",
        "sprite_asset_key": "aegiskyn_idle"
    },
    {
        "code": "FLORAVITA",
        "name": "Floravita",
        "archetype": "The Living Grove",
        "tier": 2,
        "dominant_attribute": "VIT",
        "description": "Quadruped creature composed of living moss, glowing bioluminescent blossoms, and wooden stag horns.",
        "sprite_asset_key": "floravita_idle"
    },
    {
        "code": "SOLARIS",
        "name": "Solaris",
        "archetype": "The Dawn Herald",
        "tier": 2,
        "dominant_attribute": "CHA",
        "description": "Magnificent golden bird-lion with a shimmering solar crest that invigorates everyone nearby.",
        "sprite_asset_key": "solaris_idle"
    },
    {
        "code": "HARMONIX",
        "name": "Harmonix",
        "archetype": "The Equilibrium Drake",
        "tier": 2,
        "dominant_attribute": None,
        "description": "Iridescent dragonling pulsing through the color spectrum; represents rare holistic mastery of all life pillars.",
        "sprite_asset_key": "harmonix_idle"
    },
    # Tier 3 (Apex Mythics)
    {
        "code": "IGNITAN_COLOSSUS",
        "name": "Ignitan Colossus",
        "archetype": "Apex Vanguard",
        "tier": 3,
        "dominant_attribute": "STR",
        "description": "Massive volcano-forged golem engulfed in continuous plasma fire.",
        "sprite_asset_key": "ignitan_colossus_idle"
    },
    {
        "code": "ARCHON_CHRONOSAGE",
        "name": "Archon Chronosage",
        "archetype": "Apex Arcanist",
        "tier": 3,
        "dominant_attribute": "INT",
        "description": "Celestial entity hovering inside fractured concentric time-dials.",
        "sprite_asset_key": "archon_chronosage_idle"
    },
    {
        "code": "AETHERMIND_ORACLE",
        "name": "Aethermind Oracle",
        "archetype": "Apex Mindweaver",
        "tier": 3,
        "dominant_attribute": "WIS",
        "description": "Transcendent cosmic being crowned with perpetual starlight aurora.",
        "sprite_asset_key": "aethermind_oracle_idle"
    },
    {
        "code": "BASTION_JUGGERNAUT",
        "name": "Bastion Juggernaut",
        "archetype": "Apex Warden",
        "tier": 3,
        "dominant_attribute": "DIS",
        "description": "Fortress-class metallic titan with an impenetrable diamond shield.",
        "sprite_asset_key": "bastion_juggernaut_idle"
    },
    {
        "code": "YGGDRASIL_VITALIS",
        "name": "Yggdrasil Vitalis",
        "archetype": "Apex Grove",
        "tier": 3,
        "dominant_attribute": "VIT",
        "description": "World-tree leviathan blooming with restorative spiritual essence.",
        "sprite_asset_key": "yggdrasil_vitalis_idle"
    },
    {
        "code": "SOVEREIGN_SOLARI",
        "name": "Sovereign Solari",
        "archetype": "Apex Herald",
        "tier": 3,
        "dominant_attribute": "CHA",
        "description": "Regal celestial monarch radiating blinding daytime warmth and inspiration.",
        "sprite_asset_key": "sovereign_solari_idle"
    },
    {
        "code": "PRIMORDIAL_PARAGON",
        "name": "Primordial Paragon",
        "archetype": "Apex Polymath",
        "tier": 3,
        "dominant_attribute": None,
        "description": "Legendary six-winged cosmic sovereign embodying total human self-actualization.",
        "sprite_asset_key": "primordial_paragon_idle"
    }
]

ACHIEVEMENT_SEED = [
    {
        "code": "FIRST_STEP",
        "name": "First Step",
        "description": "Complete your very first real-world activity.",
        "icon_url": "/assets/badges/first_step.svg"
    },
    {
        "code": "STREAK_3",
        "name": "Ignition Spark",
        "description": "Maintain an uninterrupted 3-day activity streak.",
        "icon_url": "/assets/badges/streak_3.svg"
    },
    {
        "code": "STREAK_7",
        "name": "Week of Steel",
        "description": "Maintain an uninterrupted 7-day activity streak.",
        "icon_url": "/assets/badges/streak_7.svg"
    },
    {
        "code": "FIRST_EVOLUTION",
        "name": "Awakened Potential",
        "description": "Witness your companion's first evolution into Tier 2.",
        "icon_url": "/assets/badges/first_evolution.svg"
    },
    {
        "code": "APEX_EVOLUTION",
        "name": "Transcendent Mastery",
        "description": "Evolve an Anima companion into its Tier 3 Apex form.",
        "icon_url": "/assets/badges/apex_evolution.svg"
    },
    {
        "code": "CHAIN_COMPLETED",
        "name": "Goal Crusher",
        "description": "Complete all steps of an Epic Goal Quest Chain.",
        "icon_url": "/assets/badges/chain_completed.svg"
    }
]

def seed_database(db: Session):
    for s_data in SPECIES_SEED:
        existing = db.query(Species).filter(Species.code == s_data["code"]).first()
        if not existing:
            species = Species(**s_data)
            db.add(species)
    
    for a_data in ACHIEVEMENT_SEED:
        existing_ach = db.query(Achievement).filter(Achievement.code == a_data["code"]).first()
        if not existing_ach:
            achievement = Achievement(**a_data)
            db.add(achievement)
            
    db.commit()
