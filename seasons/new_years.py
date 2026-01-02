"""
New Year's celebration prompt generator.

Generates scenes celebrating the new year with fireworks,
celebrations, fresh starts, and festive gatherings — with a
dreamy, seasonal-memory vibe.
"""
import os
import random
from datetime import datetime, date
from zoneinfo import ZoneInfo
from .base import SeasonBase

# Timezone to use for date calculations (configurable via TIMEZONE env var, defaults to PST/PDT)
TIMEZONE = ZoneInfo(os.environ.get("TIMEZONE", "America/Los_Angeles"))


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
        # Mix: big celebration + quiet reflective + intimate + winter + global/varied settings
        return [
            # Iconic / big scenes
            "spectacular fireworks display over a city skyline at midnight",
            "rooftop party overlooking fireworks, city lights below",
            "harbor fireworks reflecting on water, shimmering trails in the night",
            "New Year's Eve countdown crowd, confetti in the air, bright stage lights",
            "ball drop style countdown moment, cheering crowd, sparkling confetti",
            "grand ballroom New Year's celebration, formal attire, chandeliers",
            "winter festival outdoors with fire pits, bundled up crowd, distant fireworks",

            # Intimate / cozy
            "cozy living room at midnight, warm string lights, quiet celebration",
            "intimate candlelit gathering, champagne toast, soft bokeh lights",
            "midnight kiss under fireworks, silhouettes against the sky",
            "hands clinking champagne glasses, close-up, bubbles catching the light",
            "champagne bottle popping, celebratory spray, freeze-frame moment",
            "sparklers in hands, long exposure light trails, laughing faces",

            # Reflective / memory / renewal
            "handwritten New Year's resolutions in a journal, pen and paper, candle glow",
            "calendar page turning to January, soft morning light, hopeful atmosphere",
            "first sunrise of the year over mountains, calm, pastel sky",
            "snowy street at night, distant fireworks glow, quiet and dreamy",
            "fresh snow on New Year's morning, footprints, crisp air, early light",

            # Visual symbols / details
            "gold and silver decorations, balloons, streamers, elegant table setting",
            "countdown clock face near midnight, close-up, dramatic lighting",
            "party hats and noisemakers on a table, confetti scattered, warm lighting",
            "neon reflections on wet pavement after fireworks, cinematic night scene",

            # Non-city / varied settings
            "beach bonfire New Year's celebration, fireworks over the ocean",
            "small town main street celebration, twinkling lights, gentle snowfall",
        ]

    @property
    def extras(self) -> list[str]:
        # Prefer concrete, visual cues over abstract mood words
        return [
            "gold foil confetti",
            "silver streamers",
            "glittering decorations",
            "soft bokeh lights",
            "warm string lights",
            "candlelight glow",
            "champagne bubbles",
            "sparkler light trails",
            "firework smoke haze",
            "neon reflections on wet pavement",
            "cinematic night lighting",
            "shallow depth of field",
            "lens flare",
            "rim lighting",
            "snow flurries",
            "winter breath in the air",
            "glowing city lights",
            "crowd silhouettes",
            "balloon numbers",
            "marquee sign lights",
        ]

    def _ny_window(self, now: datetime) -> bool:
        """
        Only inject explicit year text around New Year's.
        Adjust this window to taste.
        """
        d = now.date()
        start = date(now.year, 12, 20)
        end = date(now.year + 1, 1, 5)
        return start <= d <= end

    def get_prompt(self) -> str:
        """
        Generate a New Year's prompt with optional year inclusion.

        - Year is "next year" during December, otherwise current year.
        - Year text is only injected during a New Year window (Dec 20–Jan 5) by default.
        """
        now = datetime.now(TIMEZONE)

        # Determine which year to display (more sensible across the year)
        if now.month == 12:
            year = now.year + 1
        else:
            year = now.year

        # 20% chance to include the year (only during the NY window)
        use_year = self._ny_window(now) and (random.random() < 0.2)

        if use_year:
            year_keywords = [
                f"Happy New Year {year} celebration, balloon numbers, confetti",
                f"Welcome {year} party scene, marquee sign lights, champagne toast",
                f"{year} New Year's Eve countdown on a giant digital screen, cheering crowd",
                f"Celebrating the arrival of {year}, fireworks over the skyline",
                f"{year} written with sparklers, long exposure light trails",
                f"{year} neon sign glowing at midnight, cinematic night lighting",
                f"champagne toast to {year}, close-up glasses, bubbles and bokeh",
            ]
            scene = random.choice(year_keywords)
        else:
            scene = random.choice(self.scene_keywords)
            
            # If scene mentions numbers/countdown, replace with year-specific version
            if "numbers" in scene.lower() or "countdown" in scene.lower():
                if "balloon numbers" in scene.lower():
                    scene = f"New Year {year} balloon numbers floating, festive celebration"
                elif "countdown" in scene.lower():
                    scene = scene.replace("countdown", f"{year} countdown")

        # Take 1–3 extras for variation
        k = random.choice([1, 2, 3])
        take = random.sample(self.extras, k=min(k, len(self.extras)))
        
        # If "balloon numbers" extra is selected, ensure year is in scene
        if "balloon numbers" in take and str(year) not in scene:
            scene = f"New Year {year} celebration with {scene}"

        # 20% chance to use an alternate artistic style
        style_prefix = self.STYLE_PREFIX
        if random.random() < 0.2 and getattr(self, "ALTERNATE_STYLES", None):
            style_prefix = random.choice(self.ALTERNATE_STYLES)

        extras_str = ", ".join(take) if take else ""
        if extras_str:
            return f"{style_prefix}, {scene}, {extras_str}"
        return f"{style_prefix}, {scene}"