from typing import Dict
from app.models.creature import Creature
from app.models.character import Character
from app.schemas.creature import CreatureStats

class CreatureService:
    @staticmethod
    def calculate_stats(creature: Creature, character: Character) -> CreatureStats:
        attr_map = {attr.code: attr.value for attr in character.attributes} if character.attributes else {}
        
        str_val = attr_map.get("STR", 0.0)
        int_val = attr_map.get("INT", 0.0)
        wis_val = attr_map.get("WIS", 0.0)
        dis_val = attr_map.get("DIS", 0.0)
        vit_val = attr_map.get("VIT", 0.0)
        cha_val = attr_map.get("CHA", 0.0)
        
        level = creature.level
        bond = creature.bond_score
        
        hp = int(100 + (vit_val * 5.0) + (level * 10))
        attack = int(10 + (str_val * 2.5) + (int_val * 1.5))
        defense = int(10 + (dis_val * 3.0) + (wis_val * 1.0))
        focus = int(50 + (int_val * 3.0) + (wis_val * 2.0))
        presence = int(10 + (cha_val * 2.5) + (bond * 0.5))
        
        return CreatureStats(
            hp=hp,
            attack=attack,
            defense=defense,
            focus=focus,
            presence=presence
        )

    @staticmethod
    def determine_mood(bond_score: int, current_streak: int, active_today: bool, days_inactive: int = 0) -> str:
        if bond_score >= 80 and current_streak >= 7:
            return "ECSTATIC"
        elif active_today:
            return "ENERGIZED"
        elif days_inactive >= 3:
            return "DROOPY"
        else:
            return "CONTENT"

    @staticmethod
    def award_bond(creature: Creature, points: int) -> int:
        creature.bond_score = min(100, max(0, creature.bond_score + points))
        return creature.bond_score
