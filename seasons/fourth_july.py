"""
Fourth of July / Independence Day prompt generator.

Generates patriotic celebration scenes with fireworks, summer fun,
outdoor parties, and American independence themes.
"""
from .base import SeasonBase


class FourthOfJuly(SeasonBase):
    """
    Fourth of July / Independence Day prompt generator.
    
    Creates patriotic celebration scenes featuring fireworks,
    BBQs, outdoor parties, and summer independence festivities.
    """
    
    @property
    def name(self) -> str:
        return "Fourth of July"
    
    @property
    def scene_keywords(self) -> list[str]:
        return [
            "spectacular fireworks over city skyline",
            "patriotic fireworks display in night sky",
            "backyard BBQ with American flags",
            "Independence Day parade down main street",
            "family picnic with red white and blue decorations",
            "hot dogs and hamburgers on grill",
            "outdoor party with patriotic bunting",
            "children waving American flags",
            "fireworks reflecting on lake water",
            "beach party with American flag towels",
            "festive Fourth of July celebration",
            "patriotic desserts and cupcakes",
            "sparklers lighting up summer evening",
            "community fireworks show crowd",
            "American flag waving in summer breeze",
            "BBQ cookout with friends and family",
            "red white and blue decorations everywhere",
            "kids playing with sparklers at dusk",
            "patriotic table setting with flags",
            "summer celebration in town square",
            "baseball game on Independence Day",
            "watermelon and summer treats",
            "outdoor concert with fireworks finale",
            "family watching fireworks from blanket",
            "patriotic themed party decorations",
            "hot dog eating contest celebration",
            "American pride celebration scene",
            "neighborhood block party with flags",
            "festive Fourth of July cookout",
            "children in patriotic costumes",
        ]
    
    @property
    def extras(self) -> list[str]:
        return [
            "brilliant fireworks bursts",
            "red white and blue colors",
            "patriotic spirit",
            "summer evening warmth",
            "festive celebration",
            "American flags flying",
            "outdoor party atmosphere",
            "grilled food aromas",
            "joyful gathering",
            "sparkler trails",
            "starry night sky",
            "community togetherness",
            "freedom celebration",
            "summer fun vibes",
            "Independence Day magic",
        ]
