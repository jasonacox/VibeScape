"""
Spring season prompt generator.

Generates spring scenes with blooming flowers, fresh growth,
renewal themes, and the awakening of nature.
"""
from .base import SeasonBase


class Spring(SeasonBase):
    """
    Spring season prompt generator.
    
    Creates scenes celebrating spring renewal, blooming nature,
    fresh growth, and the transition from winter to warmth.
    """
    
    @property
    def name(self) -> str:
        return "Spring"
    
    @property
    def scene_keywords(self) -> list[str]:
        return [
            "cherry blossoms in full bloom",
            "spring meadow filled with wildflowers",
            "garden awakening with tulips and daffodils",
            "baby animals in spring pasture",
            "rain shower with rainbow",
            "blooming magnolia tree",
            "spring orchard with blossoms",
            "fresh green leaves emerging",
            "butterfly garden in spring",
            "spring creek with flowing water",
            "morning dew on spring flowers",
            "rolling hills with spring wildflowers",
            "picnic in blooming park",
            "spring rain on garden",
            "birds building nests in trees",
            "spring sunrise over fields",
            "fresh vegetable garden sprouting",
            "wisteria covered pergola",
            "spring forest with ferns unfurling",
            "flowering dogwood trees",
            "spring bike ride through countryside",
            "outdoor spring breakfast scene",
            "spring cleaning and open windows",
            "children flying kites in park",
            "spring wedding garden setting",
            "farmers market with spring produce",
            "greenhouse filled with seedlings",
            "spring thunderstorm approaching",
            "lambs and calves in pasture",
            "fresh spring bouquet on table",
        ]
    
    @property
    def extras(self) -> list[str]:
        return [
            "soft spring light",
            "gentle spring breeze",
            "fresh green colors",
            "renewal and growth",
            "pastel flower colors",
            "morning freshness",
            "clear blue skies",
            "delicate petals",
            "nature awakening",
            "vibrant new life",
            "warm sunshine",
            "hopeful atmosphere",
            "natural beauty",
            "fresh air",
            "peaceful mood",
            "soft bokeh lights",
        ]
