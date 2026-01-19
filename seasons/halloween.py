"""
Halloween season prompt generator.

Generates Halloween scenes with trick-or-treating, pumpkins,
costumes, haunted houses, and festive spooky celebrations.
"""
from .base import SeasonBase


class Halloween(SeasonBase):
    """
    Halloween season prompt generator.

    Creates fun and festive Halloween scenes with costumes,
    decorations, trick-or-treating, and family-friendly spooky themes.
    """

    @property
    def name(self) -> str:
        return "Halloween"

    @property
    def scene_keywords(self) -> list[str]:
        return [
            "children trick-or-treating in costumes",
            "carved jack-o-lanterns glowing on porch",
            "Halloween decorated house with lights",
            "kids in creative Halloween costumes",
            "pumpkin patch with orange pumpkins",
            "haunted house with festive decorations",
            "neighborhood trick-or-treat evening",
            "witch decorations and black cats",
            "Halloween candy bowl on doorstep",
            "family carving pumpkins together",
            "spooky but friendly Halloween party",
            "autumn leaves and Halloween decorations",
            "children with trick-or-treat bags",
            "Halloween costume parade",
            "festive jack-o-lantern display",
            "decorated front porch for Halloween",
            "kids bobbing for apples",
            "Halloween themed treats and cookies",
            "friendly ghosts and pumpkin decorations",
            "costume contest celebration",
            "autumn evening with Halloween lights",
            "children showing off costumes",
            "pumpkin carving family activity",
            "haunted mansion with orange lights",
            "Halloween party with decorations",
            "trick-or-treaters at decorated door",
            "black cats and autumn pumpkins",
            "festive Halloween neighborhood scene",
            "candy corn and Halloween treats",
            "family in coordinated costumes",
        ]

    @property
    def extras(self) -> list[str]:
        return [
            "orange and purple lights",
            "autumn evening atmosphere",
            "festive spooky decorations",
            "children's excitement",
            "glowing jack-o-lanterns",
            "costume creativity",
            "trick-or-treat magic",
            "playful spookiness",
            "harvest moon glow",
            "neighborhood celebration",
            "candy filled bags",
            "autumn night sky",
            "festive fun atmosphere",
            "family friendly spooks",
            "Halloween spirit",
            "soft bokeh lights",
        ]

    @property
    def scene_objects(self) -> list[str]:
        return [
            "carved jack-o-lantern",
            "witch's broomstick",
            "black cat",
            "candy bucket",
            "ghost decoration",
            "skeleton",
            "spider web",
            "cauldron",
            "witch hat",
            "pumpkin",
            "lantern",
            "scarecrow",
            "haunted house model",
            "potion bottle",
            "candy corn bowl",
            "cobweb decoration",
            "tombstone prop",
            "bat decoration",
            "orange string lights",
            "costume mask",
        ]
