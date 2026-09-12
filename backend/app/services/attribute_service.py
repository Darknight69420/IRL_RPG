from typing import Dict, Optional, Tuple
import math

ATTRIBUTE_POINTS_MAP = {
    "TRIVIAL": 2.0,
    "EASY": 4.0,
    "MEDIUM": 8.0,
    "HARD": 14.0,
    "HEROIC": 25.0
}

VALID_ATTRIBUTES = {"STR", "INT", "WIS", "DIS", "VIT", "CHA"}

class AttributeService:
    @staticmethod
    def calculate_gains(difficulty: str, primary_attr: str, secondary_attr: Optional[str] = None) -> Dict[str, float]:
        base_points = ATTRIBUTE_POINTS_MAP.get(difficulty.upper(), 8.0)
        gains = {}
        
        primary_attr = primary_attr.upper()
        if primary_attr not in VALID_ATTRIBUTES:
            primary_attr = "INT"
            
        if secondary_attr and secondary_attr.upper() in VALID_ATTRIBUTES and secondary_attr.upper() != primary_attr:
            sec_attr = secondary_attr.upper()
            primary_gain = math.ceil(base_points * 0.70)
            secondary_gain = math.floor(base_points * 0.30)
            gains[primary_attr] = float(primary_gain)
            gains[sec_attr] = float(secondary_gain)
        else:
            gains[primary_attr] = float(base_points)
            
        return gains

    @staticmethod
    def calculate_dominance(attributes: Dict[str, float]) -> Tuple[Optional[str], float, Dict[str, float]]:
        total_points = sum(attributes.values())
        if total_points <= 0.0:
            return None, 0.0, {k: 0.0 for k in VALID_ATTRIBUTES}
            
        percentages = {k: (attributes.get(k, 0.0) / total_points) for k in VALID_ATTRIBUTES}
        dominant_code, max_pct = max(percentages.items(), key=lambda x: x[1])
        
        # Check if dominant code meets the 35% threshold
        if max_pct >= 0.35:
            return dominant_code, max_pct, percentages
        else:
            return None, max_pct, percentages
