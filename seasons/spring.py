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
            # Close-up/macro shots of budding and blooming
            "close-up of cherry blossom branch with pink petals, soft focus background",
            "macro shot of tulip unfurling, morning dew drops on petals",
            "tight shot of magnolia bud opening, delicate white petals emerging",
            "close-up of fresh green leaves unfurling from bud, backlit by sun",
            "macro view of daffodil center, yellow stamens, soft bokeh",
            "close-up of apple blossom cluster, white flowers with pink edges",
            "tight crop of wisteria blooms cascading, purple clusters in detail",
            "macro shot of dandelion seed head, soft light catching fuzz",
            "close-up of dogwood flower with four petals, spring morning light",
            "tight shot of lilac blooms, purple flowers in sharp detail",
            "macro view of peony bud about to open, pink layers visible",
            "close-up of iris petals with water droplets, deep purple hues",
            "tight shot of hyacinth spike, tiny purple flowers clustered",
            "macro of forsythia branch with bright yellow blooms",
            "close-up of crocus emerging through last snow, purple and white",
            
            # Garden and landscape scenes
            "cherry blossoms in full bloom over park pathway",
            "spring meadow filled with wildflowers stretching to horizon",
            "garden awakening with rows of tulips and daffodils",
            "blooming magnolia tree in front yard, petals on grass",
            "spring orchard with pink and white blossoms on trees",
            "rolling hills covered in spring wildflowers, golden hour",
            "wisteria covered pergola with hanging purple blooms",
            "spring forest floor with ferns unfurling, dappled sunlight",
            "flowering dogwood trees lining residential street",
            "farmers market stall with spring flowers and produce",
            
            # Activity and life scenes
            "butterfly on spring flower, macro detail of wings",
            "baby animals in spring pasture with new grass",
            "morning dew on spider web in garden, macro shot",
            "birds building nest in blooming tree branch",
            "rain shower with rainbow over green fields",
            "spring creek with flowing water over mossy rocks",
            "picnic blanket in blooming park, basket of flowers",
            "children flying kites in park with spring blossoms",
            "outdoor spring breakfast on patio with flowers",
            "greenhouse filled with seedlings in small pots",
            "fresh spring bouquet on table, close-up of mixed flowers",
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
            "soft bokeh background",
            "shallow depth of field",
            "macro photography",
            "morning dew drops",
            "backlit translucent petals",
        ]
