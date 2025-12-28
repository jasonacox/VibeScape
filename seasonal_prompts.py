"""Seasonal prompt generation for VibeScape."""
from datetime import datetime
from typing import List, Tuple
import random


class SeasonalPrompts:
    """Generate seasonal and holiday-appropriate image prompts."""
    
    def __init__(self):
        """Initialize the seasonal prompt generator."""
        self.base_style = "beautiful ambient art, serene, calming, artistic, high quality"
        
    def get_current_theme(self) -> str:
        """Determine the current theme based on date."""
        now = datetime.now()
        month = now.month
        day = now.day
        
        # Holiday themes (higher priority)
        if month == 12 and day >= 20:
            if day >= 31:
                return "new_years_eve"
            elif day >= 24:
                return "christmas"
            else:
                return "christmas_prep"
        elif month == 1 and day <= 2:
            return "new_years"
        elif month == 2 and day == 14:
            return "valentines"
        elif month == 10 and day >= 25:
            return "halloween"
        elif month == 11 and day >= 20:
            return "thanksgiving"
        
        # Seasonal themes
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:  # 9, 10, 11
            return "fall"
    
    def get_theme_prompts(self, theme: str) -> List[str]:
        """Get prompt elements for a specific theme."""
        prompts = {
            "christmas": [
                "cozy living room with decorated Christmas tree, warm fireplace, twinkling lights, presents",
                "snowy winter village at night, Christmas lights, church steeple, peaceful snowfall",
                "warm cabin interior, Christmas decorations, hot cocoa, window showing snow outside",
                "elegant Christmas dining room, candlelight, festive table setting, evergreen garland",
                "snowy forest with deer, winter wonderland, soft morning light, peaceful scene",
            ],
            "christmas_prep": [
                "cozy home with Christmas decorations being put up, warm lighting, festive atmosphere",
                "winter scene with first snow, pine trees, peaceful cabin in distance",
                "warm living room with fireplace, winter evening, comfortable and inviting",
                "snowy mountain landscape, cozy lodge, smoke from chimney, twilight",
            ],
            "new_years_eve": [
                "elegant celebration scene, champagne, gold and silver decorations, midnight countdown",
                "city skyline with fireworks, night celebration, sparkling lights, festive atmosphere",
                "sophisticated party setting, champagne glasses, elegant decor, glamorous",
                "winter night celebration, fireworks over snowy landscape, magical atmosphere",
            ],
            "new_years": [
                "fresh morning scene, new beginnings, sunrise over peaceful landscape",
                "clean minimalist space, fresh flowers, bright morning light, hopeful atmosphere",
                "winter morning, fresh snow, bright sun, peaceful and optimistic scene",
                "elegant space with fresh start theme, organized, bright, inspiring",
            ],
            "valentines": [
                "romantic setting, soft pink and red tones, roses, candlelight, elegant",
                "cozy intimate scene, warm lighting, comfortable space, romantic atmosphere",
                "beautiful floral arrangement, soft pastels, elegant presentation, love theme",
            ],
            "halloween": [
                "atmospheric autumn scene, pumpkins, fallen leaves, warm candlelight, cozy",
                "mysterious but beautiful forest, autumn colors, twilight, enchanting",
                "elegant Halloween decor, autumn harvest theme, warm and inviting",
            ],
            "thanksgiving": [
                "warm dining room, harvest theme, autumn colors, abundant table, grateful atmosphere",
                "cozy autumn scene, pumpkins, corn stalks, warm lighting, harvest celebration",
                "peaceful countryside, autumn harvest, golden hour, bountiful and warm",
            ],
            "winter": [
                "cozy cabin interior, warm fireplace, snow visible through window, comfortable",
                "snowy mountain landscape, serene, peaceful, morning light on snow",
                "warm library with fireplace, books, comfortable chairs, winter evening",
                "hot springs in snowy setting, steam rising, peaceful winter scene",
                "cozy bedroom with view of snowy landscape, warm lighting, comfortable",
                "winter forest scene, snow-covered trees, peaceful, soft light",
            ],
            "spring": [
                "blooming garden, cherry blossoms, peaceful spring morning, fresh and vibrant",
                "meadow with wildflowers, gentle breeze, sunny spring day, colorful",
                "peaceful park scene, spring flowers, trees budding, fresh air feeling",
                "elegant indoor space with spring flowers, bright natural light, fresh",
                "countryside spring scene, rolling hills, flowers blooming, peaceful",
            ],
            "summer": [
                "peaceful beach scene, calm waters, sunset colors, serene and warm",
                "tranquil forest path, dappled sunlight, lush greenery, peaceful",
                "elegant patio or terrace, warm summer evening, soft lighting, relaxing",
                "peaceful lake scene, mountains in background, clear blue sky, serene",
                "beautiful garden in full bloom, summer evening, peaceful atmosphere",
            ],
            "fall": [
                "cozy living room, autumn colors, warm lighting, comfortable atmosphere",
                "forest path with autumn leaves, warm golden light, peaceful and beautiful",
                "elegant study or library, autumn view through window, warm and cozy",
                "peaceful countryside, autumn harvest colors, rolling hills, serene",
                "cozy coffee shop interior, rain on windows, autumn decoration, warm",
            ],
        }
        
        return prompts.get(theme, prompts["fall"])
    
    def generate_prompt(self) -> Tuple[str, str]:
        """Generate a complete prompt based on current season/holiday.
        
        Returns:
            Tuple of (theme, full_prompt)
        """
        theme = self.get_current_theme()
        theme_prompts = self.get_theme_prompts(theme)
        selected_prompt = random.choice(theme_prompts)
        
        # Combine with base style
        full_prompt = f"{selected_prompt}, {self.base_style}"
        
        return theme, full_prompt
    
    def get_theme_display_name(self, theme: str) -> str:
        """Get a human-readable display name for a theme."""
        names = {
            "christmas": "Christmas",
            "christmas_prep": "Holiday Season",
            "new_years_eve": "New Year's Eve",
            "new_years": "New Year",
            "valentines": "Valentine's Day",
            "halloween": "Halloween",
            "thanksgiving": "Thanksgiving",
            "winter": "Winter",
            "spring": "Spring",
            "summer": "Summer",
            "fall": "Fall",
        }
        return names.get(theme, theme.title())
