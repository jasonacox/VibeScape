"""
Christmas season prompt generator.

Preserves the original Christmas AI Dreams prompt generation logic.
"""
from .base import SeasonBase
import random


class Christmas(SeasonBase):
    """
    Christmas season prompt generator.

    Generates festive Christmas scenes with various elements like
    Santa, decorations, winter activities, and cozy holiday moments.
    """

    @property
    def name(self) -> str:
        return "Christmas"

    @property
    def scene_keywords(self) -> list[str]:
        return [
            "winter snow scene",
            "cozy warm fireplace scene",
            "Christmas tree with lights",
            "decorations and lights on a house",
            "pile of Christmas presents",
            "family Christmas dinner table",
            "nativity scene",
            "Bethlehem star over a town",
            "Santa Claus meeting children",
            "Santa's workshop with elves",
            "Santa's sleigh in the night sky",
            "reindeer in a snowy field",
            "ice skating on a frozen pond",
            "children building a snowman",
            "carolers singing in the snow",
            "Christmas wreath on a door",
            "hot cocoa by the fireplace",
            "Christmas cookies on a plate",
            "snow-covered pine forest",
            "festive holiday village",
            "Christmas lights on a tree at night",
            "winter snow-covered cottage at dusk",
            "holiday market with wooden stalls and twinkling lights",
            "enchanted northern-lights over a pine forest",
            "ice castle with frosted turrets",
            "cozy kitchen baking cookies",
            "Victorian street with vintage decorations",
            "toy-train circling a decorated tree",
            "snow globe miniature village",
            "rooftop silhouette with sleigh in the sky",
            "stockings hung by the chimney",
            "gingerbread house with candy decorations",
            "Christmas village with lit windows",
            "wrapped presents under tree",
            "festive mantelpiece with garland",
            "children opening presents by tree",
            "advent calendar on wall",
            "Christmas Eve church service with candles",
            "snowman with scarf and top hat",
            "festive shop window display",
            "Christmas card scene with mailbox",
            "nutcracker dolls on display",
            "poinsettia plants and pine cones",
            "festive table centerpiece with candles",
            "snowy town square with giant tree",
            "Christmas morning sunrise scene",
            "Santa checking his list",
            "elves decorating cookies",
            "reindeer with jingle bells",
            "magical Christmas forest path",
            "winter wonderland with ice sculptures",
        ]

    @property
    def extras(self) -> list[str]:
        return [
            "snow falling softly",
            "warm glow from lanterns",
            "children playing",
            "candles and garlands",
            "cozy wool textures",
            "gold and red ornaments",
            "soft bokeh lights",
            "steam rising from mugs of hot cocoa",
            "frosted window patterns",
            "gingerbread textures and icing",
            "elves wrapping gifts",
            "gentle film grain",
            "reflections on wet cobblestone",
            "twinkling fairy lights",
            "pine and cinnamon scents visually implied",
            "ribbons and bows",
            "candy cane patterns",
            "wrapped presents with bows",
            "holly and mistletoe",
        ]

    @property
    def scene_objects(self) -> list[str]:
        return [
            "decorated Christmas tree",
            "rocking chair",
            "toy train",
            "nutcracker doll",
            "gift-wrapped present",
            "advent calendar",
            "Christmas stocking",
            "gingerbread house",
            "candle holder",
            "snow globe",
            "toy soldier",
            "rocking horse",
            "santa hat",
            "holiday wreath",
            "brass bell",
            "wooden sled",
            "porcelain angel",
            "vintage ornament",
            "festive garland",
            "poinsettia plant",
        ]

    def get_prompt(self, month: int = None) -> str:
        """Generate Christmas prompt with guaranteed 'festive atmosphere' suffix."""
        base_prompt = super().get_prompt(month=month)
        return f"{base_prompt}, festive atmosphere"
