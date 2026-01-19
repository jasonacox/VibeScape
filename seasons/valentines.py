"""Valentine's Day season theme."""
import random
from .base import SeasonBase


class Valentines(SeasonBase):
    """Valentine's Day theme generator - hearts, romance, and love."""

    @property
    def name(self) -> str:
        return "valentines"

    @property
    def scene_keywords(self) -> list[str]:
        return [
            "romantic candlelit dinner for two",
            "couple holding hands under starlight",
            "heart-shaped box of chocolates",
            "bouquet of red roses",
            "love birds perched together",
            "romantic sunset picnic",
            "couple dancing under the stars",
            "heart balloons floating in sky",
            "romantic walk through rose garden",
            "couple sharing a kiss",
            "cozy fireplace with two wine glasses",
            "romantic Parisian cafe scene",
            "couple on romantic beach sunset",
            "heart-shaped lights decoration",
            "romantic gondola ride in Venice",
            "couple embracing in falling rose petals",
            "romantic rooftop dinner with city lights",
            "lovebirds in heart-shaped nest",
            "couple ice skating hand in hand",
            "romantic cabin getaway with snow",
            "heart-shaped cookies and cupcakes",
            "couple stargazing on blanket",
            "romantic flower shop window display",
            "couple sharing umbrella in gentle rain",
            "heart confetti celebration",
        ]

    @property
    def extras(self) -> list[str]:
        return [
            "red and pink color palette",
            "heart motifs everywhere",
            "romantic lighting",
            "soft bokeh lights background",
            "dreamy atmosphere",
            "love is in the air",
            "romantic mood",
            "tender moment",
            "heartfelt emotion",
            "intimate setting",
            "valentine's day celebration",
            "rose petals scattered",
            "cupid's arrows",
            "sweet romance",
            "loving embrace",
            "soft bokeh lights",
        ]

    @property
    def scene_objects(self) -> list[str]:
        return [
            "bouquet of red roses",
            "heart-shaped box of chocolates",
            "champagne bottle",
            "love letter",
            "romantic candle",
            "teddy bear",
            "heart-shaped pillow",
            "red wine glasses",
            "jewelry box",
            "valentine card",
            "silk ribbon",
            "rose petals",
            "heart balloons",
            "photo frame",
            "gift box with bow",
            "perfume bottle",
            "couples' coffee mugs",
            "string of lights",
            "velvet cushion",
            "romantic book",
        ]
