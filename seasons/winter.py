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
            "snow-laden pine tree branches",
            "ice fishing hut on frozen lake",
            "alpine village nestled in mountains",
            "frozen pond reflecting bare trees",
            "snowy pathway through woods",
            "stone cottage with smoking chimney",
            "winter bird feeder covered in snow",
            "icy stream flowing through snow banks",
            "snow-covered rooftops in village",
            "warm bakery window with frost patterns",
            "wooden fence line disappearing into snowstorm",
            "ice cave with blue frozen walls",
            "snowy owl perched on branch",
            "northern lights over winter landscape",
            "frozen harbor with boats in ice",
            "cozy library with winter view",
            "snow angels in pristine field",
            "winter barn with red doors in snow",
            "frozen fountain in town square",
            "sleepy winter town at night",
            "fireplace with crackling fire in cozy room",
            "fireplace interior with warm lighting and rustic decor",
            "wood burning in stone fireplace with cozy seating inside",
            "inside of log cabin with firewood stacked by fireplace",
            "cozy living room with fur throw and warm firelight",
            "rustic cabin interior with glowing fireplace and wooden furniture",
            "snow-covered pine trees with icicles hanging from branches",
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
            "sparkling ice crystals",
            "wisps of chimney smoke",
            "crunchy snow texture",
            "muted pastel sky",
            "bare tree silhouettes",
            "twinkling starlight",
            "foggy breath in cold air",
            "layers of snow texture",
            "icy blue color palette",
            "warm contrast with cold surroundings",
        ]

    @property
    def scene_objects(self) -> list[str]:
        return [
            "wooden rocking chair",
            "sled",
            "lantern",
            "snow shovel",
            "knitted blanket",
            "steaming mug",
            "vintage skis",
            "firewood stack",
            "ice skates",
            "wool mittens",
            "brass telescope",
            "wooden bench",
            "copper kettle",
            "stone fireplace",
            "frost-covered window",
            "cabin door",
            "rustic mailbox",
            "old sleigh",
            "pine cone basket",
            "snowshoes",
        ]
