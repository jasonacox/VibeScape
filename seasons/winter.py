"""
Winter season prompt generator.

Generates winter scenes focusing on natural beauty, cozy moments,
and the magic of the cold season (without specific holiday themes).
"""
from .base import SeasonBase


class Winter(SeasonBase):
    """
    Winter season prompt generator.
    
    Creates serene winter landscapes, cozy indoor scenes,
    and winter activities without specific holiday references.
    """
    
    @property
    def name(self) -> str:
        return "Winter"
    
    @property
    def scene_keywords(self) -> list[str]:
        return [
            "snow-covered mountain landscape at sunset",
            "frozen lake with ice formations",
            "cozy cabin in snowy woods",
            "winter forest with frost-covered trees",
            "snow-covered village street at twilight",
            "warm interior with window overlooking snowy landscape",
            "ice crystals on tree branches",
            "snowflakes falling in soft light",
            "frozen waterfall in winter forest",
            "cozy reading nook by frosted window",
            "winter sunrise over snowy hills",
            "footprints in fresh snow",
            "icicles hanging from cottage eaves",
            "steaming mug by window overlooking winter scene",
            "snow-dusted evergreen forest",
            "frozen river winding through landscape",
            "winter birds on snowy branches",
            "moonlight on snow-covered field",
            "warm firelight glowing through cabin windows",
            "snow-covered bridge over frozen stream",
            "winter mountain peaks in morning light",
            "cozy blankets and warm lighting indoors",
            "frost patterns on window glass",
            "snowdrifts against wooden fence",
            "winter wildlife in snowy habitat",
            "lantern light in snowy evening",
            "ski lodge exterior in mountains",
            "winter garden with snow-covered plants",
            "warm soup and bread on rustic table",
            "peaceful winter morning scene",
        ]
    
    @property
    def extras(self) -> list[str]:
        return [
            "soft diffused lighting",
            "gentle snowfall",
            "warm golden hour glow",
            "peaceful atmosphere",
            "crystalline ice textures",
            "cozy wool and fur textures",
            "steam rising into cold air",
            "blue winter shadows",
            "pristine untouched snow",
            "warm amber interior lighting",
            "frosted details",
            "serene silence",
            "natural beauty",
            "winter magic",
            "tranquil mood",
            "soft bokeh lights",
        ]
