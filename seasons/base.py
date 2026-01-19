"""
Base class for all seasonal prompt generators.
"""
from abc import ABC, abstractmethod
import random


class SeasonBase(ABC):
    """
    Abstract base class for seasonal prompt generators.

    Each season should implement:
    - name: str - Season identifier
    - scene_keywords: list - Scene descriptions for this season
    - extras: list - Additional elements to enhance scenes
    - get_prompt() - Generate a random prompt for this season
    """

    # Default style prefix (can be overridden by subclasses)
    STYLE_PREFIX = (
        "Ultra-detailed, cinematic, photorealistic, 8k, dramatic lighting, "
        "warm color grading, high dynamic range, shallow depth of field"
        "Photorealistic, ultra-detailed, 8k, cinematic composition, "
        "professional photography, natural lighting, crisp focus, "
        "high dynamic range, rich textures, authentic atmosphere, "
        "realistic depth of field, magazine quality"
    )

    # Alternative styles for variety (20% chance for artistic variation)
    ALTERNATE_STYLES = [
        "Whimsical, storybook illustration, watercolor, soft palette, hand-painted, no signature, no text",
        "Vintage postcard, warm tones, slight film grain, nostalgic, no signature, no text",
        "Painterly, oil painting, soft brush strokes, cozy mood, no signature, no text",
        "Children's book illustration, flat colors, high charm, no signature, no text",
        "Impressionist style, visible brush strokes, play of light, vibrant colors, no signature, no text",
        "Digital art, concept art style, detailed matte painting, atmospheric, no signature, no text",
        "Anime background style, detailed, soft colors, studio quality, no signature, no text",
        "Fantasy art, ethereal, dreamlike, rich colors, magical atmosphere, no signature, no text",
        "Minimalist, clean composition, bold colors, graphic design aesthetic, no signature, no text",
        "Moody photography, film noir lighting, high contrast, dramatic shadows, no signature, no text",
    ]

    # Time of day variations to add diversity
    TIME_OF_DAY = [
        "at golden hour",
        "at blue hour",
        "at sunrise",
        "at sunset",
        "at dawn",
        "at dusk",
        "at midday",
        "in morning light",
        "in afternoon light",
        "in evening light",
        "at night",
        "under moonlight",
        "during magic hour",
    ]

    # Atmospheric/weather conditions for variety
    ATMOSPHERIC_CONDITIONS = [
        "with dramatic clouds",
        "with soft mist",
        "with light fog",
        "with volumetric lighting",
        "with god rays",
        "with lens flare",
        "with atmospheric haze",
        "with clear skies",
        "with overcast lighting",
        "with diffused light through clouds",
    ]

    # Compositional variations
    COMPOSITION_STYLES = [
        "wide angle view",
        "aerial view",
        "birds eye view",
        "from ground level",
        "intimate close-up",
        "expansive vista",
        "rule of thirds composition",
        "centered composition",
        "off-center composition",
        "depth of field emphasis",
    ]

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the season name."""
        pass

    @property
    @abstractmethod
    def scene_keywords(self) -> list[str]:
        """Return list of scene keywords for this season."""
        pass

    @property
    @abstractmethod
    def extras(self) -> list[str]:
        """Return list of extra elements to enhance scenes."""
        pass

    @property
    @abstractmethod
    def scene_objects(self) -> list[str]:
        """Return list of objects that can appear in scenes for this season."""
        pass

    def get_prompt(self, month: int = None) -> str:
        """
        Generate a random prompt for this season with maximum variation.

        Includes randomization of:
        - Artistic style (20% chance of alternate styles, 80% photorealistic)
        - Number of extras (1-3 random)
        - Scene objects (50% chance of adding 1-2 season-appropriate objects)
        - Time of day (40% chance)
        - Atmospheric conditions (30% chance)
        - Composition style (25% chance)
        - Month context (optional) to shape seasonal details

        Args:
            month: Current month (1-12) to help shape prompt context

        Returns:
            str: A complete prompt ready for image generation with high uniqueness
        """
        scene = random.choice(self.scene_keywords)

        # Vary the number of extras: 1, 2, or 3 (weighted toward 2)
        num_extras = random.choices([1, 2, 3], weights=[0.3, 0.5, 0.2])[0]
        num_extras = min(num_extras, len(self.extras))
        take = random.sample(self.extras, k=num_extras)

        # 20% chance to use an alternate artistic style (80% photorealistic)
        style_prefix = self.STYLE_PREFIX
        if random.random() < 0.2:
            style_prefix = random.choice(self.ALTERNATE_STYLES)

        # Build prompt components list
        components = [style_prefix, scene]

        # Add extras
        if take:
            components.extend(take)

        # 50% chance to add 1-2 scene objects for additional variety
        if self.scene_objects and random.random() < 0.5:
            num_objects = random.choices([1, 2], weights=[0.6, 0.4])[0]
            num_objects = min(num_objects, len(self.scene_objects))
            objects = random.sample(self.scene_objects, k=num_objects)
            # Format objects naturally: "with a dog" or "with a lamp and chair"
            if len(objects) == 1:
                components.append(f"with a {objects[0]}")
            else:
                components.append(f"with a {objects[0]} and {objects[1]}")

        # 40% chance to add time of day variation
        if random.random() < 0.4:
            components.append(random.choice(self.TIME_OF_DAY))

        # 30% chance to add atmospheric/weather condition
        if random.random() < 0.3:
            components.append(random.choice(self.ATMOSPHERIC_CONDITIONS))

        # 25% chance to add compositional style
        if random.random() < 0.25:
            components.append(random.choice(self.COMPOSITION_STYLES))

        # Shuffle the order of extras and modifiers (but keep style prefix first and scene second)
        if len(components) > 2:
            modifiers = components[2:]
            random.shuffle(modifiers)
            components = components[:2] + modifiers

        prompt = ", ".join(components)
        return prompt

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"
