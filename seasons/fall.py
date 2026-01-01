"""
Fall/Autumn season prompt generator.

Generates autumn scenes with colorful foliage, harvest themes,
cozy moments, and the beauty of the changing season.
"""
from .base import SeasonBase


class Fall(SeasonBase):
    """
    Fall/Autumn season prompt generator.
    
    Creates scenes celebrating autumn colors, harvest time,
    cozy fall activities, and the transition to cooler weather.
    """
    
    @property
    def name(self) -> str:
        return "Fall"
    
    @property
    def scene_keywords(self) -> list[str]:
        return [
            "autumn forest with golden and red leaves",
            "countryside road lined with colorful trees",
            "cozy porch with fall decorations",
            "pumpkin patch at golden hour",
            "harvest table with autumn bounty",
            "rustic barn surrounded by fall foliage",
            "maple trees in brilliant autumn colors",
            "fallen leaves covering forest path",
            "cozy sweater weather scene with hot cider",
            "farmhouse with autumn harvest display",
            "misty autumn morning in countryside",
            "apple orchard in fall colors",
            "corn maze entrance with autumn decorations",
            "crackling fire with fall ambiance",
            "autumn vineyard with grape harvest",
            "covered bridge surrounded by fall trees",
            "cozy reading scene with autumn view",
            "hayride through autumn landscape",
            "fall market with seasonal produce",
            "mountain landscape in peak autumn colors",
            "lakeside cabin with fall reflections",
            "autumn sunset over golden fields",
            "pumpkins and mums on farmhouse steps",
            "woodland path carpeted with leaves",
            "cozy interior with fall decorating",
            "harvest moon rising over autumn scene",
            "rustic fall wreath on wooden door",
            "autumn picnic in colorful park",
            "golden hour light through fall trees",
            "peaceful autumn garden scene",
        ]
    
    @property
    def extras(self) -> list[str]:
        return [
            "golden autumn light",
            "vibrant fall colors",
            "cozy flannel textures",
            "warm cider and spices",
            "crisp autumn air",
            "rustling leaves",
            "harvest abundance",
            "warm earth tones",
            "gentle breeze",
            "copper and amber hues",
            "woodland atmosphere",
            "natural textures",
            "cozy blankets",
            "seasonal comfort",
            "nostalgic mood",
            "soft bokeh lights",
        ]
