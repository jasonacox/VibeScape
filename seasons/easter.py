"""
Easter season prompt generator.

Generates Easter scenes with bunnies, eggs, hunts, candy,
Christian resurrection themes, and spring celebrations.
"""
from .base import SeasonBase


class Easter(SeasonBase):
    """
    Easter season prompt generator.
    
    Creates joyful Easter scenes featuring egg hunts, bunnies,
    spring celebrations, and Christian resurrection themes.
    """
    
    @property
    def name(self) -> str:
        return "Easter"
    
    @property
    def scene_keywords(self) -> list[str]:
        return [
            "Easter bunny with basket of colorful eggs",
            "children hunting for Easter eggs in garden",
            "colorful Easter eggs in spring grass",
            "Easter basket filled with candy and treats",
            "family Easter egg decorating activity",
            "Easter Sunday church celebration",
            "spring garden with hidden Easter eggs",
            "Easter brunch table with decorations",
            "bunny family in spring meadow",
            "painted Easter eggs in nest",
            "children in Easter Sunday outfits",
            "Easter egg hunt in blooming garden",
            "cross and flowers for resurrection Sunday",
            "Easter lily arrangements in church",
            "chocolate bunnies and Easter candy",
            "spring flowers and Easter decorations",
            "family gathering for Easter dinner",
            "pastel colored Easter celebration",
            "Easter parade with bonnets and spring attire",
            "sunrise Easter service outdoors",
            "resurrection garden with empty tomb",
            "children with Easter baskets full of eggs",
            "spring lamb in pastoral Easter scene",
            "Easter egg tree with hanging decorations",
            "Palm Sunday procession with palms",
            "Easter morning sunrise over flowers",
            "joyful Easter celebration gathering",
            "spring butterfly and Easter eggs",
            "church decorated for Easter Sunday",
            "family portrait in Easter spring setting",
        ]
    
    @property
    def extras(self) -> list[str]:
        return [
            "pastel spring colors",
            "blooming flowers",
            "soft spring light",
            "joyful celebration",
            "renewal and hope",
            "spring freshness",
            "colorful decorations",
            "Easter morning glow",
            "new life symbolism",
            "spring garden beauty",
            "festive atmosphere",
            "resurrection joy",
            "children's excitement",
            "spring awakening",
            "Easter sunshine",
            "soft bokeh lights",
        ]
