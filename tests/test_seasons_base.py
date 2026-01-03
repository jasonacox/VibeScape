"""
Tests for seasons/base.py - Base class for seasonal prompt generators.
"""
import pytest
import random
from abc import ABC
from seasons.base import SeasonBase


class ConcreteSeasonForTesting(SeasonBase):
    """Concrete implementation of SeasonBase for testing."""
    
    @property
    def name(self) -> str:
        return "test_season"
    
    @property
    def scene_keywords(self) -> list[str]:
        return [
            "test scene one",
            "test scene two",
            "test scene three",
        ]
    
    @property
    def extras(self) -> list[str]:
        return [
            "extra one",
            "extra two",
            "extra three",
            "extra four",
        ]


class TestSeasonBaseAbstract:
    """Test that SeasonBase is abstract and cannot be instantiated."""
    
    def test_cannot_instantiate_directly(self):
        """Test that SeasonBase cannot be instantiated directly."""
        with pytest.raises(TypeError):
            SeasonBase()
    
    def test_is_abstract_base_class(self):
        """Test that SeasonBase is an ABC."""
        assert issubclass(SeasonBase, ABC)
    
    def test_requires_name_property(self):
        """Test that name property must be implemented."""
        class MissingName(SeasonBase):
            @property
            def scene_keywords(self):
                return []
            @property
            def extras(self):
                return []
        
        with pytest.raises(TypeError):
            MissingName()
    
    def test_requires_scene_keywords_property(self):
        """Test that scene_keywords property must be implemented."""
        class MissingSceneKeywords(SeasonBase):
            @property
            def name(self):
                return "test"
            @property
            def extras(self):
                return []
        
        with pytest.raises(TypeError):
            MissingSceneKeywords()
    
    def test_requires_extras_property(self):
        """Test that extras property must be implemented."""
        class MissingExtras(SeasonBase):
            @property
            def name(self):
                return "test"
            @property
            def scene_keywords(self):
                return []
        
        with pytest.raises(TypeError):
            MissingExtras()


class TestConcreteSeasonImplementation:
    """Test a concrete implementation of SeasonBase."""
    
    def test_can_instantiate_concrete_class(self):
        """Test that concrete implementation can be instantiated."""
        season = ConcreteSeasonForTesting()
        assert season is not None
    
    def test_name_property(self):
        """Test that name property works."""
        season = ConcreteSeasonForTesting()
        assert season.name == "test_season"
    
    def test_scene_keywords_property(self):
        """Test that scene_keywords property works."""
        season = ConcreteSeasonForTesting()
        assert len(season.scene_keywords) == 3
        assert "test scene one" in season.scene_keywords
    
    def test_extras_property(self):
        """Test that extras property works."""
        season = ConcreteSeasonForTesting()
        assert len(season.extras) == 4
        assert "extra one" in season.extras
    
    def test_repr(self):
        """Test __repr__ method."""
        season = ConcreteSeasonForTesting()
        repr_str = repr(season)
        assert "ConcreteSeasonForTesting" in repr_str
        assert "test_season" in repr_str


class TestStylePrefixes:
    """Test style prefix behavior."""
    
    def test_has_default_style_prefix(self):
        """Test that SeasonBase has a default STYLE_PREFIX."""
        assert hasattr(SeasonBase, 'STYLE_PREFIX')
        assert isinstance(SeasonBase.STYLE_PREFIX, str)
        assert len(SeasonBase.STYLE_PREFIX) > 0
    
    def test_has_alternate_styles(self):
        """Test that SeasonBase has alternate styles."""
        assert hasattr(SeasonBase, 'ALTERNATE_STYLES')
        assert isinstance(SeasonBase.ALTERNATE_STYLES, list)
        assert len(SeasonBase.ALTERNATE_STYLES) > 0
    
    def test_all_alternate_styles_are_strings(self):
        """Test that all alternate styles are non-empty strings."""
        for style in SeasonBase.ALTERNATE_STYLES:
            assert isinstance(style, str)
            assert len(style) > 0
    
    def test_default_style_is_photorealistic(self):
        """Test that default style mentions photorealistic/cinematic."""
        style = SeasonBase.STYLE_PREFIX.lower()
        assert any(word in style for word in ["photorealistic", "cinematic", "detailed"])
    
    def test_alternate_styles_are_different(self):
        """Test that alternate styles offer variety."""
        styles = SeasonBase.ALTERNATE_STYLES
        # Should have multiple different styles
        assert len(set(styles)) == len(styles), "Alternate styles should be unique"


class TestGetPrompt:
    """Test the get_prompt method."""
    
    def test_returns_string(self):
        """Test that get_prompt returns a string."""
        season = ConcreteSeasonForTesting()
        prompt = season.get_prompt()
        assert isinstance(prompt, str)
    
    def test_prompt_not_empty(self):
        """Test that prompt is not empty."""
        season = ConcreteSeasonForTesting()
        prompt = season.get_prompt()
        assert len(prompt) > 0
    
    def test_prompt_contains_scene(self):
        """Test that prompt contains a scene keyword."""
        season = ConcreteSeasonForTesting()
        prompt = season.get_prompt()
        
        # Should contain at least one scene keyword
        scene_found = any(scene in prompt for scene in season.scene_keywords)
        assert scene_found, f"No scene keyword found in prompt: {prompt}"
    
    def test_prompt_contains_extras(self):
        """Test that prompt contains extras (up to 2)."""
        season = ConcreteSeasonForTesting()
        prompt = season.get_prompt()
        
        # Should contain at least one extra
        extra_found = any(extra in prompt for extra in season.extras)
        assert extra_found, f"No extras found in prompt: {prompt}"
    
    def test_prompt_contains_style(self):
        """Test that prompt contains a style prefix."""
        season = ConcreteSeasonForTesting()
        prompt = season.get_prompt()
        
        # Should contain default style or one of the alternates
        has_default = SeasonBase.STYLE_PREFIX in prompt
        has_alternate = any(style in prompt for style in SeasonBase.ALTERNATE_STYLES)
        
        assert has_default or has_alternate, f"No style prefix found in prompt: {prompt}"
    
    def test_default_style_used_most_often(self):
        """Test that default style is used more often than alternates (~80%)."""
        season = ConcreteSeasonForTesting()
        
        default_count = 0
        alternate_count = 0
        iterations = 100
        
        for _ in range(iterations):
            prompt = season.get_prompt()
            if SeasonBase.STYLE_PREFIX in prompt:
                default_count += 1
            else:
                alternate_count += 1
        
        # Default should be used around 80% of the time
        # Allow some statistical variance (60-95%)
        assert 60 <= default_count <= 95, \
            f"Default style used {default_count}/{iterations} times, expected ~80"
    
    def test_alternate_styles_used_occasionally(self):
        """Test that alternate styles are used occasionally (~20%)."""
        season = ConcreteSeasonForTesting()
        
        alternate_found = False
        for _ in range(50):  # Try 50 times, should see at least one alternate
            prompt = season.get_prompt()
            if any(style in prompt for style in SeasonBase.ALTERNATE_STYLES):
                alternate_found = True
                break
        
        assert alternate_found, "Alternate styles never used in 50 tries"
    
    def test_prompt_format_consistency(self):
        """Test that prompt format is consistent."""
        season = ConcreteSeasonForTesting()
        prompt = season.get_prompt()
        
        # Prompt should have commas separating parts
        assert "," in prompt
        # Should have multiple components
        parts = [p.strip() for p in prompt.split(",")]
        assert len(parts) >= 3, f"Prompt should have at least 3 parts: {prompt}"
    
    def test_different_prompts_on_multiple_calls(self):
        """Test that multiple calls can produce different prompts."""
        season = ConcreteSeasonForTesting()
        
        prompts = set()
        for _ in range(20):
            prompts.add(season.get_prompt())
        
        # Should see some variety (though might not always be different)
        # With 3 scenes and 4 extras, should see multiple unique prompts
        assert len(prompts) > 1, "All prompts identical across 20 calls"
    
    def test_extras_selection_respects_count(self):
        """Test that up to 2 extras are selected."""
        season = ConcreteSeasonForTesting()
        
        # Count how many extras appear in a prompt
        prompt = season.get_prompt()
        extras_in_prompt = sum(1 for extra in season.extras if extra in prompt)
        
        # Should have 0, 1, or 2 extras (usually 2)
        assert 0 <= extras_in_prompt <= 2
    
    def test_empty_extras_handled(self):
        """Test that empty extras list is handled gracefully."""
        class SeasonWithNoExtras(SeasonBase):
            @property
            def name(self):
                return "test"
            @property
            def scene_keywords(self):
                return ["test scene"]
            @property
            def extras(self):
                return []
        
        season = SeasonWithNoExtras()
        prompt = season.get_prompt()
        
        # Should still work, just without extras
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "test scene" in prompt


class TestPromptVariety:
    """Test that prompt generation provides good variety."""
    
    def test_all_scenes_can_be_selected(self):
        """Test that all scene keywords can appear in prompts."""
        season = ConcreteSeasonForTesting()
        
        scenes_seen = set()
        for _ in range(100):  # Try many times
            prompt = season.get_prompt()
            for scene in season.scene_keywords:
                if scene in prompt:
                    scenes_seen.add(scene)
        
        # Should see all scenes eventually
        assert len(scenes_seen) == len(season.scene_keywords), \
            f"Only saw {len(scenes_seen)}/{len(season.scene_keywords)} scenes"
    
    def test_all_extras_can_be_selected(self):
        """Test that all extras can appear in prompts."""
        season = ConcreteSeasonForTesting()
        
        extras_seen = set()
        for _ in range(200):  # Try many times
            prompt = season.get_prompt()
            for extra in season.extras:
                if extra in prompt:
                    extras_seen.add(extra)
        
        # Should see most or all extras
        assert len(extras_seen) >= len(season.extras) - 1, \
            f"Only saw {len(extras_seen)}/{len(season.extras)} extras"
    
    def test_all_alternate_styles_can_be_used(self):
        """Test that all alternate styles can be selected."""
        season = ConcreteSeasonForTesting()
        
        styles_seen = set()
        for _ in range(500):  # Need many tries since alternates are 20% chance
            prompt = season.get_prompt()
            for style in SeasonBase.ALTERNATE_STYLES:
                if style in prompt:
                    styles_seen.add(style)
        
        # Should see at least some alternate styles
        assert len(styles_seen) >= 2, \
            f"Only saw {len(styles_seen)} alternate styles"


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_single_scene_keyword(self):
        """Test with only one scene keyword."""
        class SingleSceneSeason(SeasonBase):
            @property
            def name(self):
                return "single"
            @property
            def scene_keywords(self):
                return ["only scene"]
            @property
            def extras(self):
                return ["extra1", "extra2"]
        
        season = SingleSceneSeason()
        prompt = season.get_prompt()
        
        assert "only scene" in prompt
    
    def test_single_extra(self):
        """Test with only one extra."""
        class SingleExtraSeason(SeasonBase):
            @property
            def name(self):
                return "single"
            @property
            def scene_keywords(self):
                return ["scene1", "scene2"]
            @property
            def extras(self):
                return ["only extra"]
        
        season = SingleExtraSeason()
        prompt = season.get_prompt()
        
        # Should still work
        assert isinstance(prompt, str)
    
    def test_many_scene_keywords(self):
        """Test with many scene keywords."""
        class ManyScenesSeason(SeasonBase):
            @property
            def name(self):
                return "many"
            @property
            def scene_keywords(self):
                return [f"scene {i}" for i in range(100)]
            @property
            def extras(self):
                return ["extra1", "extra2"]
        
        season = ManyScenesSeason()
        prompt = season.get_prompt()
        
        # Should select one of the many scenes
        assert any(f"scene {i}" in prompt for i in range(100))
    
    def test_many_extras(self):
        """Test with many extras."""
        class ManyExtrasSeason(SeasonBase):
            @property
            def name(self):
                return "many"
            @property
            def scene_keywords(self):
                return ["scene1"]
            @property
            def extras(self):
                return [f"extra{i:03d}" for i in range(100)]  # Use zero-padded numbers
        
        season = ManyExtrasSeason()
        prompt = season.get_prompt()
        
        # Should select exactly 2 extras (k=2)
        extra_count = sum(1 for i in range(100) if f"extra{i:03d}" in prompt)
        assert extra_count == 2, f"Expected 2 extras, found {extra_count}"
