import math
from typing import Tuple

DIFFICULTY_MULTIPLIERS = {
    "TRIVIAL": 1.0,
    "EASY": 1.5,
    "MEDIUM": 2.5,
    "HARD": 4.0,
    "HEROIC": 7.0
}

BASE_XP = 20

class ProgressionEngine:
    @staticmethod
    def calculate_xp_earned(difficulty: str, current_streak: int = 0) -> Tuple[int, float]:
        multiplier = DIFFICULTY_MULTIPLIERS.get(difficulty.upper(), 2.5)
        streak_bonus = min(max(current_streak, 0) * 0.02, 0.30)
        raw_xp = BASE_XP * multiplier * (1.0 + streak_bonus)
        return int(math.floor(raw_xp)), streak_bonus

    @staticmethod
    def cumulative_xp_for_level(level: int) -> int:
        if level <= 1:
            return 0
        return int(math.floor(100.0 * ((level - 1) ** 1.6)))

    @staticmethod
    def calculate_level_from_xp(total_xp: int) -> Tuple[int, int, int]:
        level = 1
        while True:
            xp_next = ProgressionEngine.cumulative_xp_for_level(level + 1)
            if total_xp < xp_next:
                break
            level += 1
            if level >= 100: # Practical safety cap
                break
        
        xp_current_level_threshold = ProgressionEngine.cumulative_xp_for_level(level)
        xp_next_level_threshold = ProgressionEngine.cumulative_xp_for_level(level + 1)
        return level, xp_current_level_threshold, xp_next_level_threshold
