"""
Tests for seasons/christmas.py - Christmas season prompt generator.
"""
import pytest
from seasons.christmas import Christmas
from seasons.base import SeasonBase


class TestChristmasBasics:
    """Test basic Christmas season properties."""
    
    def test_can_instantiate(self):
        """Test that Christmas can be instantiated."""
        season = Christmas()
        assert season is not None
    
    def test_is_season_base(self):
        """Test that Christmas extends SeasonBase."""
        season = Christmas()
        assert isinstance(season, SeasonBase)
    
    def test_name_property(self):
        """Test that name property returns 'Christmas'."""
        season = Christmas()
        assert season.name == "Christmas"
    
    def test_has_scene_keywords(self):
        """Test that Christmas has scene keywords."""
        season = Christmas()
        assert len(season.scene_keywords) > 0
        assert isinstance(season.scene_keywords, list)
    
    def test_has_extras(self):
        """Test that Christmas has extras."""
        season = Christmas()
        assert len(season.extras) > 0
        assert isinstance(season.extras, list)
    
    def test_all_scene_keywords_are_strings(self):
        """Test that all scene keywords are non-empty strings."""
        season = Christmas()
        for keyword in season.scene_keywords:
            assert isinstance(keyword, str)
            assert len(keyword) > 0
    
    def test_all_extras_are_strings(self):
        """Test that all extras are non-empty strings."""
        season = Christmas()
        for extra in season.extras:
            assert isinstance(extra, str)
            assert len(extra) > 0


class TestChristmasSceneKeywords:
    """Test Christmas scene keywords."""
    
    def test_has_santa_scenes(self):
        """Test that Christmas includes Santa-related scenes."""
        season = Christmas()
        santa_keywords = [k for k in season.scene_keywords if "santa" in k.lower()]
        assert len(santa_keywords) > 0, "Should have Santa-related scenes"
    
    def test_has_christmas_tree(self):
        """Test that Christmas tree is included."""
        season = Christmas()
        tree_found = any("tree" in k.lower() for k in season.scene_keywords)
        assert tree_found, "Should have Christmas tree scenes"
    
    def test_has_snow_scenes(self):
        """Test that snow scenes are included."""
        season = Christmas()
        snow_found = any("snow" in k.lower() for k in season.scene_keywords)
        assert snow_found, "Should have snow-related scenes"
    
    def test_has_variety_of_scenes(self):
        """Test that Christmas has good variety of scenes."""
        season = Christmas()
        # Should have at least 15 different scenes for variety
        assert len(season.scene_keywords) >= 15
    
    def test_scenes_are_unique(self):
        """Test that all scene keywords are unique."""
        season = Christmas()
        assert len(season.scene_keywords) == len(set(season.scene_keywords))


class TestChristmasExtras:
    """Test Christmas extras."""
    
    def test_has_festive_extras(self):
        """Test that extras include festive elements."""
        season = Christmas()
        # Should have some festive-related extras
        festive_words = ["snow", "lights", "warm", "candle", "glow", "cozy"]
        has_festive = any(
            any(word in extra.lower() for word in festive_words)
            for extra in season.extras
        )
        assert has_festive, "Should have festive-themed extras"
    
    def test_has_sufficient_extras(self):
        """Test that there are enough extras for variety."""
        season = Christmas()
        # Should have at least 8 extras for good variety
        assert len(season.extras) >= 8
    
    def test_extras_are_unique(self):
        """Test that all extras are unique."""
        season = Christmas()
        assert len(season.extras) == len(set(season.extras))


class TestChristmasPromptGeneration:
    """Test Christmas prompt generation."""
    
    def test_get_prompt_returns_string(self):
        """Test that get_prompt returns a string."""
        season = Christmas()
        prompt = season.get_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0
    
    def test_prompt_contains_scene(self):
        """Test that prompt contains a Christmas scene."""
        season = Christmas()
        prompt = season.get_prompt()
        scene_found = any(scene in prompt for scene in season.scene_keywords)
        assert scene_found, f"No Christmas scene in prompt: {prompt}"
    
    def test_prompt_contains_festive_atmosphere(self):
        """Test that Christmas prompts include 'festive atmosphere'."""
        season = Christmas()
        prompt = season.get_prompt()
        assert "festive atmosphere" in prompt, \
            f"Christmas prompt should include 'festive atmosphere': {prompt}"
    
    def test_prompt_has_style(self):
        """Test that prompt includes style prefix."""
        season = Christmas()
        prompt = season.get_prompt()
        has_style = (
            SeasonBase.STYLE_PREFIX in prompt or
            any(style in prompt for style in SeasonBase.ALTERNATE_STYLES)
        )
        assert has_style, f"No style prefix in prompt: {prompt}"
    
    def test_prompt_variety(self):
        """Test that multiple prompts show variety."""
        season = Christmas()
        prompts = {season.get_prompt() for _ in range(20)}
        # Should have at least some variety
        assert len(prompts) > 1, "All prompts identical"
    
    def test_prompt_structure(self):
        """Test that Christmas prompts have expected structure."""
        season = Christmas()
        prompt = season.get_prompt()
        
        # Should have commas separating components
        assert "," in prompt
        parts = prompt.split(",")
        # Should have multiple parts (style, scene, extras, festive atmosphere)
        assert len(parts) >= 3


class TestChristmasThemeConsistency:
    """Test that Christmas season maintains theme consistency."""
    
    def test_no_non_christmas_holidays(self):
        """Test that Christmas doesn't reference other holidays."""
        season = Christmas()
        all_text = " ".join(season.scene_keywords + season.extras).lower()
        
        # Should not mention other holidays
        other_holidays = ["halloween", "thanksgiving", "easter", "valentine"]
        for holiday in other_holidays:
            assert holiday not in all_text, \
                f"Christmas season should not reference {holiday}"
    
    def test_christmas_themed_content(self):
        """Test that content is Christmas-themed."""
        season = Christmas()
        all_text = " ".join(season.scene_keywords + season.extras).lower()
        
        # Should have Christmas-related words
        christmas_words = ["christmas", "santa", "snow", "winter", "cozy", "festive"]
        has_christmas_theme = any(word in all_text for word in christmas_words)
        assert has_christmas_theme, "Content should be Christmas-themed"
