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
    )
    
    # Alternative styles for variety (20% chance)
    ALTERNATE_STYLES = [
        "Whimsical, storybook illustration, watercolor, soft palette, hand-painted",
        "Vintage postcard, warm tones, slight film grain, nostalgic",
        "Painterly, oil painting, soft brush strokes, cozy mood",
        "Children's book illustration, flat colors, high charm",
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
    
    def get_prompt(self) -> str:
        """
        Generate a random prompt for this season.
        
        Returns:
            str: A complete prompt ready for image generation
        """
        scene = random.choice(self.scene_keywords)
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
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"
