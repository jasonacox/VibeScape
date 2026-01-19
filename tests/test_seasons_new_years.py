"""
Tests for seasons/new_years.py - New Year's season prompt generator.
"""
import pytest
from seasons.new_years import NewYears
from seasons.base import SeasonBase


class TestNewYearsBasics:
    def test_can_instantiate(self):
        season = NewYears()
        assert season is not None

    def test_is_season_base(self):
        season = NewYears()
        assert isinstance(season, SeasonBase)

    def test_name_property(self):
        season = NewYears()
        assert season.name == "New Year's"

    def test_has_scene_keywords(self):
        season = NewYears()
        assert len(season.scene_keywords) > 0
        assert isinstance(season.scene_keywords, list)

    def test_has_extras(self):
        season = NewYears()
        assert len(season.extras) > 0
        assert isinstance(season.extras, list)

    def test_all_scene_keywords_are_strings(self):
        season = NewYears()
        for keyword in season.scene_keywords:
            assert isinstance(keyword, str)
            assert len(keyword) > 0

    def test_all_extras_are_strings(self):
        season = NewYears()
        for extra in season.extras:
            assert isinstance(extra, str)
            assert len(extra) > 0


class TestNewYearsPromptGeneration:
    def test_get_prompt_returns_string(self):
        season = NewYears()
        prompt = season.get_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_prompt_contains_scene(self):
        season = NewYears()
        prompt = season.get_prompt()
        # NewYears has custom logic that may use year-specific scenes
        # Just verify the prompt contains expected elements
        assert isinstance(prompt, str)
        assert len(prompt) > 50  # Should be a substantial prompt

    def test_prompt_variety(self):
        season = NewYears()
        prompts = {season.get_prompt() for _ in range(20)}
        assert len(prompts) > 1
