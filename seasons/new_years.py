"""
New Year's celebration prompt generator.

Generates scenes celebrating the new year with fireworks,
celebrations, fresh starts, and festive gatherings.
"""
import random
from datetime import datetime
from .base import SeasonBase


class NewYears(SeasonBase):
    """
    New Year's celebration prompt generator.
    
    Creates scenes of celebration, renewal, fireworks displays,
    and festive gatherings to welcome the new year.
    """
    
    @property
    def name(self) -> str:
        return "New Year's"
    
    @property
    def scene_keywords(self) -> list[str]:
        return [
            "spectacular fireworks display over city skyline",
            "midnight celebration with champagne toast",
            "Times Square style New Year's Eve gathering",
            "elegant party with balloons and confetti",
            "fireworks reflecting on water",
            "champagne glasses clinking in celebration",
            "countdown clock showing midnight",
            "festive party with dancing and lights",
            "New Year's Eve ball drop celebration",
            "rooftop party overlooking city fireworks",
            "sparklers and party poppers",
            "elegant dining table set for New Year's dinner",
            "confetti falling in celebration",
            "resolution journal and fresh calendar",
            "festive gathering with friends and family",
            "midnight kiss under fireworks",
            "champagne bottle popping with celebration",
            "city lights and fireworks at night",
            "elegant gold and silver decorations",
            "New Year's Eve countdown party scene",
            "hopeful sunrise on New Year's Day",
            "fresh snow on New Year's morning",
            "celebration with noisemakers and party hats",
            "festive cityscape with illuminated buildings",
            "intimate gathering with candlelight",
            "grand ballroom New Year's celebration",
            "outdoor winter celebration with fire pits",
            "New Year's toast with friends",
            "colorful fireworks bursting in night sky",
            "celebration with streaming ribbons and lights",
        ]
    
    @property
    def extras(self) -> list[str]:
        return [
            "golden confetti",
            "brilliant fireworks",
            "sparkling lights",
            "festive atmosphere",
            "joyful celebration",
            "champagne bubbles",
            "midnight magic",
            "glittering decorations",
            "hopeful mood",
            "elegant party attire",
            "vibrant colors",
            "celebratory energy",
            "new beginnings",
            "festive drinks",
            "party lights",
            "soft bokeh lights",
        ]
    
    def get_prompt(self) -> str:
        """
        Generate a New Year's prompt with the appropriate year.
        
        If before January 1st, uses next year (current year + 1).
        If on January 1st, uses current year.
        """
        now = datetime.now()
        
        # Determine which year to display
        if now.month == 1 and now.day == 1:
            year = now.year  # On New Year's Day, show current year
        else:
            year = now.year + 1  # Before 1/1, show next year
        
        # 20% chance to include the year in the prompt
        if random.random() < 0.2:
            year_keywords = [
                f"Happy New Year {year} celebration",
                f"Welcome {year} party scene",
                f"{year} New Year's Eve countdown",
                f"Celebrating the arrival of {year}",
                f"{year} written in sparklers",
                f"{year} illuminated in fireworks",
                f"champagne toast to {year}",
            ]
            scene = random.choice(year_keywords)
        else:
            scene = random.choice(self.scene_keywords)
        
        # Get extras
        take = random.sample(self.extras, k=min(2, len(self.extras)))
        
        # 20% chance to use an alternate artistic style
        style_prefix = self.STYLE_PREFIX
        if random.random() < 0.2:
            style_prefix = random.choice(self.ALTERNATE_STYLES)
        
        # Build prompt with scene and extras
        extras_str = ", ".join(take) if take else ""
        if extras_str:
            prompt = f"{style_prefix}, {scene}, {extras_str}"
        else:
            prompt = f"{style_prefix}, {scene}"
        
        return prompt
