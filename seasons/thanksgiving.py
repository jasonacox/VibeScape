"""
Thanksgiving season prompt generator.

Generates Thanksgiving scenes with family gatherings, feasts,
gratitude themes, and historical celebration elements.
"""
from .base import SeasonBase


class Thanksgiving(SeasonBase):
    """
    Thanksgiving season prompt generator.
    
    Creates warm family gathering scenes, traditional feasts,
    harvest celebrations, and gratitude-themed imagery.
    """
    
    @property
    def name(self) -> str:
        return "Thanksgiving"
    
    @property
    def scene_keywords(self) -> list[str]:
        return [
            "family gathered around Thanksgiving dinner table",
            "golden roasted turkey centerpiece on dining table",
            "traditional Thanksgiving feast with all the trimmings",
            "pumpkin and apple pies on rustic table",
            "family giving thanks before meal",
            "cornucopia overflowing with harvest bounty",
            "Thanksgiving table setting with autumn decorations",
            "kitchen preparing Thanksgiving dinner",
            "family cooking together in warm kitchen",
            "pilgrim and Native American historical feast",
            "rustic farmhouse Thanksgiving celebration",
            "multi-generational family gathering",
            "Thanksgiving parade scene",
            "autumn harvest table with gourds and wheat",
            "cranberry sauce and side dishes spread",
            "carved turkey being served",
            "family sharing gratitude around table",
            "cozy dining room with Thanksgiving decorations",
            "traditional Thanksgiving foods display",
            "children helping prepare Thanksgiving meal",
            "elegant Thanksgiving table with candles",
            "warm kitchen with homemade pies cooling",
            "family football game on Thanksgiving",
            "Thanksgiving leftovers sandwich creation",
            "grateful family holding hands at table",
            "autumn-themed Thanksgiving centerpiece",
            "historical Thanksgiving reenactment scene",
            "farmhouse table with seasonal harvest",
            "Thanksgiving blessing and prayer moment",
            "warm gathering with friends and family",
        ]
    
    @property
    def extras(self) -> list[str]:
        return [
            "warm candlelight",
            "autumn colors and textures",
            "golden hour lighting",
            "family togetherness",
            "grateful expressions",
            "harvest decorations",
            "cozy atmosphere",
            "traditional recipes",
            "steaming dishes",
            "rustic wooden table",
            "seasonal abundance",
            "warm inviting glow",
            "festive tablecloth",
            "thankful mood",
            "home-cooked warmth",
            "soft bokeh lights",
        ]
