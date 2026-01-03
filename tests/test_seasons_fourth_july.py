"""
Tests for seasons/fourth_july.py - Fourth of July season prompt generator.
"""
import pytest
from seasons.fourth_july import FourthOfJuly
from seasons.base import SeasonBase


class TestFourthOfJulyBasics:
    def test_can_instantiate(self):
        season = FourthOfJuly()
        assert season is not None
    
    def test_is_season_base(self):
        season = FourthOfJuly()
        assert isinstance(season, SeasonBase)
    
    def test_name_property(self):
        season = FourthOfJuly()
        assert season.name == "Fourth of July"
    
    def test_has_scene_keywords(self):
        season = FourthOfJuly()
        assert len(season.scene_keywords) > 0
        assert isinstance(season.scene_keywords, list)
    
    def test_has_extras(self):
        season = FourthOfJuly()
        assert len(season.extras) > 0
        assert isinstance(season.extras, list)
    
    def test_all_scene_keywords_are_strings(self):
        season = FourthOfJuly()
        for keyword in season.scene_keywords:
            assert isinstance(keyword, str)
            assert len(keyword) > 0
    
    def test_all_extras_are_strings(self):
        season = FourthOfJuly()
        for extra in season.extras:
            assert isinstance(extra, str)
            assert len(extra) > 0


class TestFourthOfJulyPromptGeneration:
    def test_get_prompt_returns_string(self):
        season = FourthOfJuly()
        prompt = season.get_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0
    
    def test_prompt_contains_scene(self):
        season = FourthOfJuly()
        prompt = season.get_prompt()
        scene_found = any(scene in prompt for scene in season.scene_keywords)
        assert scene_found
    
    def test_prompt_variety(self):
        season = FourthOfJuly()
        prompts = {season.get_prompt() for _ in range(20)}
        assert len(prompts) > 1
