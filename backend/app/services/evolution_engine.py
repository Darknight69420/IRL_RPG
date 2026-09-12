from typing import Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.creature import Creature, CollectionEntry
from app.models.character import Character
from app.models.species import Species
from app.models.streak import Streak
from app.models.quest_chain import QuestChain

TIER_2_MAPPING = {
    "STR": "PYROKYN",
    "INT": "LUMINAUR",
    "WIS": "SYLPHORA",
    "DIS": "AEGISKYN",
    "VIT": "FLORAVITA",
    "CHA": "SOLARIS"
}

TIER_3_MAPPING = {
    "PYROKYN": "IGNITAN_COLOSSUS",
    "LUMINAUR": "ARCHON_CHRONOSAGE",
    "SYLPHORA": "AETHERMIND_ORACLE",
    "AEGISKYN": "BASTION_JUGGERNAUT",
    "FLORAVITA": "YGGDRASIL_VITALIS",
    "SOLARIS": "SOVEREIGN_SOLARI",
    "HARMONIX": "PRIMORDIAL_PARAGON"
}

class EvolutionEngine:
    @staticmethod
    def check_evolution(
        db: Session,
        creature: Creature,
        character: Character,
        streak: Streak
    ) -> Optional[Species]:
        current_species = creature.species
        if not current_species:
            return None

        # Check Tier 1 -> Tier 2
        if current_species.tier == 1:
            if creature.level >= 10 and creature.bond_score >= 40:
                attr_map = {a.code: a.value for a in character.attributes} if character.attributes else {}
                total_points = sum(attr_map.values())
                
                target_code = "HARMONIX" # Fallback if balanced or 0
                if total_points > 0:
                    dominant_attr, max_pts = max(attr_map.items(), key=lambda x: x[1])
                    if (max_pts / total_points) >= 0.35:
                        target_code = TIER_2_MAPPING.get(dominant_attr, "HARMONIX")

                target_species = db.query(Species).filter(Species.code == target_code).first()
                return target_species

        # Check Tier 2 -> Tier 3
        elif current_species.tier == 2:
            # Check completed chains count
            completed_chains = db.query(QuestChain).filter(
                QuestChain.user_id == creature.user_id,
                QuestChain.status == "COMPLETED"
            ).count()

            max_streak = max(streak.current_streak, streak.longest_streak)
            if (creature.level >= 25 and 
                creature.bond_score >= 80 and 
                max_streak >= 21 and 
                completed_chains >= 1):
                
                target_code = TIER_3_MAPPING.get(current_species.code)
                if target_code:
                    target_species = db.query(Species).filter(Species.code == target_code).first()
                    return target_species

        return None

    @staticmethod
    def apply_evolution(db: Session, creature: Creature, new_species: Species) -> CollectionEntry:
        creature.species_id = new_species.id
        creature.species = new_species
        
        # Ensure registered in collection
        existing_col = db.query(CollectionEntry).filter(
            CollectionEntry.user_id == creature.user_id,
            CollectionEntry.species_id == new_species.id
        ).first()

        if not existing_col:
            new_col = CollectionEntry(
                user_id=creature.user_id,
                species_id=new_species.id,
                status="AWAKENED",
                unlocked_at=datetime.now(timezone.utc)
            )
            db.add(new_col)
            return new_col
        else:
            existing_col.status = "AWAKENED"
            return existing_col
