"""
Tests for seasons/spring.py - Spring season prompt generator.
"""
import pytest
from seasons.spring import Spring
from seasons.base import SeasonBase


class TestSpringBasics:
    def test_can_instantiate(self):
        season = Spring()
        assert season is not None
    
    def test_is_season_base(self):
        season = Spring()
        assert isinstance(season, SeasonBase)
    
    def test_name_property(self):
        season = Spring()
        assert season.name == "Spring"
    
    def test_has_scene_keywords(self):
        season = Spring()
        assert len(season.scene_keywords) > 0
        assert isinstance(season.scene_keywords, list)
    
    def test_has_extras(self):
        season = Spring()
        assert len(season.extras) > 0
        assert isinstance(season.extras, list)
    
    def test_all_scene_keywords_are_strings(self):
        season = Spring()
        for keyword in season.scene_keywords:
            assert isinstance(keyword, str)
            assert len(keyword) > 0
    
    def test_all_extras_are_strings(self):
        season = Spring()
        for extra in season.extras:
            assert isinstance(extra, str)
            assert len(extra) > 0


class TestSpringPromptGeneration:
    def test_get_prompt_returns_string(self):
        season = Spring()
        prompt = season.get_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0
    
    def test_prompt_contains_scene(self):
        season = Spring()
        prompt = season.get_prompt()
        scene_found = any(scene in prompt for scene in season.scene_keywords)
        assert scene_found
    
    def test_prompt_variety(self):
        season = Spring()
        prompts = {season.get_prompt() for _ in range(20)}
        assert len(prompts) > 1
