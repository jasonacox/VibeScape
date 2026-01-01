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
        ]
    
    def get_prompt(self) -> str:
        """
        Generate a random Christmas scene prompt.
        
        Uses the original Christmas AI Dreams logic:
        - Picks a random scene
        - Adds 2 random extras
        - 20% chance of alternate artistic style
        - Adds "festive atmosphere" suffix
        
        Returns:
            str: A complete Christmas-themed prompt
        """
        scene = random.choice(self.scene_keywords)
        take = random.sample(self.extras, k=2)
        
        # Occasionally use an alternate illustrative style for variety
        style_prefix = self.STYLE_PREFIX
        if random.random() < 0.2:  # 20% chance to choose an alternate style
            style_prefix = random.choice(self.ALTERNATE_STYLES)
        
        prompt = f"{style_prefix}, {scene}, {take[0]}, {take[1]}, festive atmosphere"
        return prompt
