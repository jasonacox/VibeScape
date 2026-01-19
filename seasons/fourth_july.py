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
            # Flag-focused scenes
            "large American flag waving proudly against blue sky",
            "row of American flags lining suburban street",
            "American flag bunting draped on front porch",
            "close-up of American flag rippling in summer breeze",
            "stars and stripes flag on flagpole at sunset",
            "vintage American flag hanging on historic building",
            "child holding American flag, patriotic pride",
            "multiple American flags at Independence Day parade",
            # Red, white, and blue decorations
            "backyard decorated with red white and blue balloons and streamers",
            "patriotic table setting with stars and stripes tablecloth",
            "red white and blue bunting on porch railings",
            "festive yard with American flag banners everywhere",
            "picnic table covered with patriotic decorations and flags",
            "neighborhood houses decorated with American flags",
            "stars and stripes themed party decorations",
            "red white and blue paper lanterns hanging",
            # Fireworks with patriotic elements
            "spectacular fireworks over Statue of Liberty",
            "red white and blue fireworks bursting in night sky",
            "patriotic fireworks display over American flag",
            "fireworks show with American flag in foreground",
            "starry fireworks over Independence Day celebration",
            # Parades and gatherings
            "Independence Day parade with marching band and flags",
            "Main street parade with red white and blue floats",
            "children waving American flags at parade",
            "veterans marching with American flags",
            "patriotic parade with classic cars and flags",
            # Food and celebrations
            "BBQ grill with American flag apron and decorations",
            "red white and blue cupcakes with flag toppers",
            "patriotic themed picnic spread with flags",
            "watermelon slices arranged like American flag",
            "dessert table with stars and stripes decorations",
            # Patriotic attire and activities
            "family wearing red white and blue clothing at celebration",
            "kids in patriotic costumes with American flags",
            "baseball game with American flags flying",
            "beach scene with American flag beach towels",
            "outdoor concert with giant American flag backdrop",
            # Summer patriotic scenes
            "American flags reflecting on lake at sunset",
            "beach bonfire with American flags at dusk",
            "town square with fountain and American flags",
            "summer evening celebration with flags and lights",
        ]

    @property
    def extras(self) -> list[str]:
        return [
            "brilliant fireworks bursts",
            "vibrant red white and blue colors",
            "stars and stripes everywhere",
            "American flags flying proudly",
            "patriotic spirit and pride",
            "summer evening warmth",
            "festive celebration atmosphere",
            "red white and blue bunting",
            "star-spangled decorations",
            "American flag motifs",
            "patriotic color scheme",
            "freedom and independence",
            "outdoor party atmosphere",
            "sparkler trails of light",
            "starry night sky",
            "community togetherness",
            "red white and blue balloons",
            "stars and stripes patterns",
            "patriotic pride everywhere",
            "Independence Day magic",
        ]

    @property
    def scene_objects(self) -> list[str]:
        return [
            "American flag",
            "fireworks display",
            "picnic basket",
            "red white and blue bunting",
            "sparklers",
            "BBQ grill",
            "cooler",
            "beach towel",
            "folding chair",
            "patriotic banner",
            "star decoration",
            "watermelon slice",
            "Uncle Sam hat",
            "cornhole board",
            "Frisbee",
            "paper lantern",
            "picnic table",
            "hot dog stand",
            "star-spangled balloon",
            "liberty bell decoration",
        ]
