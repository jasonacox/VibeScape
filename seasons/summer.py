"""
Summer season prompt generator.

Generates summer scenes with beaches, vacation vibes, outdoor activities,
and the warmth and energy of the summer season.
"""
from .base import SeasonBase


class Summer(SeasonBase):
    """
    Summer season prompt generator.

    Creates vibrant summer scenes featuring beaches, outdoor adventures,
    vacation moments, and the bright energy of warm summer days.
    """

    @property
    def name(self) -> str:
        return "Summer"

    @property
    def scene_keywords(self) -> list[str]:
        return [
            "pristine beach with turquoise water",
            "tropical paradise with palm trees",
            "outdoor BBQ gathering with friends",
            "sunset over ocean waves",
            "pool party with colorful floats",
            "beach bonfire at twilight",
            "surfing in crystal clear waves",
            "summer road trip scenic vista",
            "lakeside dock at golden hour",
            "outdoor cafe in summer sunshine",
            "vineyard picnic on summer day",
            "sailboat on sparkling blue water",
            "summer garden in full bloom",
            "ice cream stand on sunny boardwalk",
            "hammock between palm trees",
            "outdoor music festival scene",
            "mountain hiking trail with wildflowers",
            "watermelon and refreshments at picnic",
            "beach volleyball game at sunset",
            "camping under starry summer sky",
            "kayaking on calm summer lake",
            "outdoor movie night setup",
            "farmers market on sunny morning",
            "sunflower field in golden light",
            "porch swing on summer evening",
            "lighthouse on sunny coastal day",
            "tropical fruit stand with vibrant colors",
            "outdoor yoga at sunrise",
            "summer carnival with lights",
            "fishing pier at golden hour",
        ]

    @property
    def extras(self) -> list[str]:
        return [
            "brilliant sunshine",
            "bright vibrant colors",
            "warm golden hour",
            "refreshing cool drinks",
            "gentle ocean breeze",
            "clear blue skies",
            "playful atmosphere",
            "relaxed vacation mood",
            "sparkling water",
            "tropical vibes",
            "outdoor adventure",
            "sun-kissed glow",
            "carefree energy",
            "summer warmth",
            "joyful moments",
            "soft bokeh lights",
        ]

    @property
    def scene_objects(self) -> list[str]:
        return [
            "beach ball",
            "surfboard",
            "cooler",
            "beach umbrella",
            "hammock",
            "sunglasses",
            "flip-flops",
            "kayak",
            "beach towel",
            "watermelon slice",
            "seashells",
            "sand bucket",
            "inflatable float",
            "picnic basket",
            "camping tent",
            "guitar",
            "bicycle",
            "skateboard",
            "fishing rod",
            "beach chair",
        ]
