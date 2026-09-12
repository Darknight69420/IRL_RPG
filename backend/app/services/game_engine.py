from datetime import datetime, timezone
from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.character import Character, CharacterAttribute
from app.models.creature import Creature
from app.models.streak import Streak
from app.models.activity import Activity
from app.core.exceptions import (
    ResourceNotFoundException,
    UnauthorizedResourceAccessException,
    CooldownActiveException,
    GameRuleException
)
from app.services.attribute_service import AttributeService
from app.services.progression_engine import ProgressionEngine
from app.services.creature_service import CreatureService
from app.services.evolution_engine import EvolutionEngine
from app.services.streak_service import StreakService
from app.services.chronicle_service import ChronicleService
from app.services.achievement_service import AchievementService
from app.schemas.activity import (
    ActivityCompletionResponse,
    CharacterProgressionDiff,
    CreatureProgressionDiff,
    StreakDiff,
    AchievementUnlocked
)

class GameEngine:
    @staticmethod
    def process_activity_completion(
        db: Session,
        user: User,
        activity_id: int,
        notes: Optional[str] = None
    ) -> ActivityCompletionResponse:
        now_utc = datetime.now(timezone.utc)
        user_tz = user.timezone or "UTC"
        today_local = StreakService.get_user_current_date(user_tz)

        # 1. Fetch and validate activity ownership
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            raise ResourceNotFoundException("Activity", activity_id)

        if activity.user_id != user.id:
            raise UnauthorizedResourceAccessException()

        if not activity.is_active:
            raise GameRuleException("ACTIVITY_INACTIVE", "Cannot complete an inactive activity.")

        # 2. Check cooldown for daily habits
        if activity.category == "HABIT" and activity.last_completed_at:
            last_date_local = activity.last_completed_at.astimezone(timezone.utc).date()
            # If completed on same local date, trigger cooldown
            if last_date_local == today_local:
                # Calculate approximate remaining seconds until next local midnight
                raise CooldownActiveException(remaining_seconds=3600 * 8)

        # 3. Fetch character, active creature, and streak
        character = user.character
        creature = db.query(Creature).filter(
            Creature.user_id == user.id,
            Creature.is_active == True
        ).first()
        
        streak = user.streak
        if not streak:
            streak = Streak(user_id=user.id, current_streak=0, longest_streak=0)
            db.add(streak)
            db.flush()

        # 4. Process streak
        streak_advanced = StreakService.update_streak(streak, user_tz)

        # 5. Compute XP with streak bonus
        xp_earned, streak_bonus_multiplier = ProgressionEngine.calculate_xp_earned(
            difficulty=activity.difficulty,
            current_streak=streak.current_streak
        )

        # 6. Update character progression
        prev_char_level = character.level
        character.current_xp += xp_earned
        new_char_level, _, _ = ProgressionEngine.calculate_level_from_xp(character.current_xp)
        char_leveled_up = (new_char_level > prev_char_level)
        character.level = new_char_level

        # 7. Compute & apply attribute gains
        attribute_gains = AttributeService.calculate_gains(
            difficulty=activity.difficulty,
            primary_attr=activity.primary_attribute,
            secondary_attr=activity.secondary_attribute
        )

        # Apply to character_attributes
        char_attrs_dict = {ca.code: ca for ca in character.attributes}
        for code, gain in attribute_gains.items():
            if code in char_attrs_dict:
                char_attrs_dict[code].value += gain
            else:
                new_attr = CharacterAttribute(
                    character_id=character.id,
                    code=code,
                    value=gain
                )
                db.add(new_attr)

        # 8. Update active creature progression
        creature_diff = None
        new_achievements: List[AchievementUnlocked] = []

        if creature:
            prev_creature_level = creature.level
            creature.current_xp += xp_earned
            new_creature_level, _, _ = ProgressionEngine.calculate_level_from_xp(creature.current_xp)
            creature_leveled_up = (new_creature_level > prev_creature_level)
            creature.level = new_creature_level

            # Bond rewards
            CreatureService.award_bond(creature, 2)
            if streak_advanced:
                CreatureService.award_bond(creature, 5)

            # Mood evaluation
            creature_mood = CreatureService.determine_mood(
                bond_score=creature.bond_score,
                current_streak=streak.current_streak,
                active_today=True
            )

            # 9. Evolution check
            prev_species_name = creature.species.name
            evolution_triggered = False
            evolved_to_name = None
            evolution_tier = None

            potential_evolution = EvolutionEngine.check_evolution(
                db=db,
                creature=creature,
                character=character,
                streak=streak
            )

            if potential_evolution and potential_evolution.id != creature.species_id:
                evolution_triggered = True
                evolved_to_name = potential_evolution.name
                evolution_tier = potential_evolution.tier
                EvolutionEngine.apply_evolution(db, creature, potential_evolution)

                # Record evolution in chronicle
                ChronicleService.record_event(
                    db=db,
                    user_id=user.id,
                    event_type="EVOLUTION_OCCURRED",
                    title=f"{creature.nickname} evolved into {potential_evolution.name}!",
                    description=f"Ascended to Tier {potential_evolution.tier} ({potential_evolution.archetype}).",
                    metadata={
                        "evolved_from": prev_species_name,
                        "evolved_to": potential_evolution.name,
                        "tier": potential_evolution.tier
                    }
                )

                # Check evolution achievements
                if potential_evolution.tier == 2:
                    new_achievements.extend(AchievementService.check_and_award(db, user.id, "FIRST_EVOLUTION"))
                elif potential_evolution.tier == 3:
                    new_achievements.extend(AchievementService.check_and_award(db, user.id, "APEX_EVOLUTION"))

            creature_diff = CreatureProgressionDiff(
                creature_id=creature.id,
                name=creature.nickname,
                species_code=creature.species.code,
                species_name=creature.species.name,
                previous_level=prev_creature_level,
                current_level=new_creature_level,
                leveled_up=creature_leveled_up,
                bond_score=creature.bond_score,
                mood=creature_mood,
                evolution_triggered=evolution_triggered,
                evolved_from=prev_species_name if evolution_triggered else None,
                evolved_to=evolved_to_name,
                evolution_tier=evolution_tier
            )

        # 10. Check streak achievements
        if streak.current_streak >= 3:
            new_achievements.extend(AchievementService.check_and_award(db, user.id, "STREAK_3"))
        if streak.current_streak >= 7:
            new_achievements.extend(AchievementService.check_and_award(db, user.id, "STREAK_7"))

        # 11. Check first step achievement
        new_achievements.extend(AchievementService.check_and_award(db, user.id, "FIRST_STEP"))

        # 12. Update activity timestamp
        activity.last_completed_at = now_utc

        # 13. Record activity completion in Chronicle
        ChronicleService.record_event(
            db=db,
            user_id=user.id,
            event_type="ACTIVITY_COMPLETED",
            title=f"Completed: {activity.title}",
            description=notes or f"Earned {xp_earned} XP across {', '.join(attribute_gains.keys())}.",
            metadata={
                "activity_id": activity.id,
                "xp_earned": xp_earned,
                "attribute_gains": attribute_gains,
                "current_streak": streak.current_streak
            }
        )

        # 14. Commit transaction
        db.commit()
        db.refresh(character)
        if creature:
            db.refresh(creature)
        db.refresh(streak)

        return ActivityCompletionResponse(
            activity_id=activity.id,
            activity_title=activity.title,
            completed_at=now_utc,
            xp_earned=xp_earned,
            streak_bonus_multiplier=streak_bonus_multiplier,
            attribute_gains=attribute_gains,
            character=CharacterProgressionDiff(
                level=character.level,
                current_xp=character.current_xp,
                leveled_up=char_leveled_up
            ),
            creature=creature_diff,
            streak=StreakDiff(
                current_streak=streak.current_streak,
                longest_streak=streak.longest_streak,
                streak_advanced=streak_advanced
            ),
            new_achievements=new_achievements
        )
