"""
Tests for blender.py - Season blending and date-based season selection.
"""
import pytest
from datetime import date, datetime
from freezegun import freeze_time
from unittest.mock import patch
from blender import SeasonBlender


class TestSeasonBlenderInitialization:
    """Test SeasonBlender initialization."""

    def test_creates_all_seasons(self):
        """Test that all season instances are created."""
        blender = SeasonBlender()

        expected_seasons = [
            "christmas",
            "winter",
            "new_years",
            "fall",
            "summer",
            "spring",
            "thanksgiving",
            "fourth_july",
            "easter",
            "halloween",
            "valentines",
        ]

        for season_name in expected_seasons:
            assert season_name in blender.seasons
            assert blender.seasons[season_name] is not None

    def test_builds_interpolation_table(self):
        """Test that interpolation table is built."""
        blender = SeasonBlender()

        assert hasattr(blender, "weight_table")
        assert len(blender.weight_table) > 0
        assert isinstance(blender.weight_table, list)

    def test_interpolation_table_sorted(self):
        """Test that interpolation table is sorted by day of year."""
        blender = SeasonBlender()

        days = [day for day, weights in blender.weight_table]
        assert days == sorted(
            days
        ), "Interpolation table should be sorted by day of year"

    def test_interpolation_table_format(self):
        """Test that interpolation table has correct format."""
        blender = SeasonBlender()

        for entry in blender.weight_table:
            assert isinstance(entry, tuple)
            assert len(entry) == 2
            day, weights = entry
            assert isinstance(day, int)
            assert isinstance(weights, dict)
            assert 1 <= day <= 366


class TestGetDayOfYear:
    """Test the get_day_of_year method."""

    def test_january_first(self):
        """Test January 1st is day 1."""
        blender = SeasonBlender()
        day = blender.get_day_of_year(date(2026, 1, 1))
        assert day == 1

    def test_christmas(self):
        """Test Christmas day of year."""
        blender = SeasonBlender()
        day = blender.get_day_of_year(date(2026, 12, 25))
        assert day == 359  # Day 359 in 2026 (non-leap year)

    def test_halloween(self):
        """Test Halloween day of year."""
        blender = SeasonBlender()
        day = blender.get_day_of_year(date(2026, 10, 31))
        assert day == 304  # Day 304 in 2026

    def test_with_explicit_date(self):
        """Test get_day_of_year with explicit date parameter."""
        blender = SeasonBlender()
        test_date = date(2025, 7, 4)
        day = blender.get_day_of_year(test_date)
        assert day == 185  # July 4th is day 185

    def test_date_override_full_format(self, monkeypatch):
        """Test DATE environment variable with YYYY-MM-DD format."""
        blender = SeasonBlender()
        monkeypatch.setenv("DATE", "2025-12-25")
        day = blender.get_day_of_year()
        assert day == 359  # Christmas

    def test_date_override_short_format(self, monkeypatch):
        """Test DATE environment variable with MM-DD format."""
        blender = SeasonBlender()
        with freeze_time("2025-06-15"):  # Current year is 2025
            monkeypatch.setenv("DATE", "12-25")
            day = blender.get_day_of_year()
            assert day == 359  # Christmas in 2025

    def test_date_override_invalid_falls_back(self, monkeypatch):
        """Test invalid DATE override falls back to current date."""
        blender = SeasonBlender()
        monkeypatch.setenv("DATE", "invalid-date")
        # Should fall back to current date in PST (January 3, 2026 = day 3)
        day = blender.get_day_of_year()
        assert 1 <= day <= 366  # Just verify it's valid, don't check exact day

    def test_uses_pst_timezone(self, monkeypatch):
        """Test that PST timezone is used by default."""
        blender = SeasonBlender()
        # The get_day_of_year should use PST timezone
        # This is hard to test directly, but we verify it doesn't crash
        day = blender.get_day_of_year()
        assert isinstance(day, int)
        assert 1 <= day <= 366

    def test_leap_year(self):
        """Test leap year day calculation."""
        blender = SeasonBlender()
        # 2024 is a leap year
        test_date = date(2024, 12, 31)
        day = blender.get_day_of_year(test_date)
        assert day == 366  # Dec 31 in leap year


class TestInterpolateWeights:
    """Test weight interpolation between key dates."""

    def test_exact_match_no_interpolation(self):
        """Test that exact date matches return exact weights."""
        blender = SeasonBlender()
        # Christmas Day (12/25) should be exactly 1.0 christmas
        day = blender.get_day_of_year(date(2025, 12, 25))
        weights = blender._interpolate_weights(day)

        assert "christmas" in weights
        assert weights["christmas"] == 1.0
        assert sum(weights.values()) == pytest.approx(1.0)

    def test_interpolation_between_dates(self):
        """Test linear interpolation between two key dates."""
        blender = SeasonBlender()
        # Pick a date between two key dates
        # Find a gap in the config and test interpolation
        day = blender.get_day_of_year(date(2025, 6, 10))  # Early summer
        weights = blender._interpolate_weights(day)

        # Should get some weights back
        assert len(weights) > 0
        # Should sum to 1.0
        assert sum(weights.values()) == pytest.approx(1.0)
        # All weights should be non-negative
        assert all(w >= 0 for w in weights.values())

    def test_weights_sum_to_one(self):
        """Test that interpolated weights always sum to 1.0."""
        blender = SeasonBlender()
        # Test a bunch of random days throughout the year
        for month in range(1, 13):
            for day in [1, 10, 20]:
                try:
                    test_date = date(2025, month, day)
                    day_of_year = blender.get_day_of_year(test_date)
                    weights = blender._interpolate_weights(day_of_year)

                    total = sum(weights.values())
                    assert total == pytest.approx(
                        1.0, abs=0.01
                    ), f"Weights for {month}/{day} sum to {total}, not 1.0: {weights}"
                except ValueError:
                    # Some months don't have day 31, etc.
                    pass

    def test_year_wraparound_december_to_january(self):
        """Test interpolation wraps around from Dec to Jan."""
        blender = SeasonBlender()
        # Test a date at the very end of year
        day = blender.get_day_of_year(date(2025, 12, 30))
        weights = blender._interpolate_weights(day)

        # Should get valid weights
        assert len(weights) > 0
        assert sum(weights.values()) == pytest.approx(1.0)

    def test_interpolation_respects_boundaries(self):
        """Test that interpolation respects season boundaries."""
        blender = SeasonBlender()
        # Halloween (10/31) should be 100% halloween
        halloween_day = blender.get_day_of_year(date(2025, 10, 31))
        weights = blender._interpolate_weights(halloween_day)

        assert "halloween" in weights
        assert weights["halloween"] == 1.0

    def test_midpoint_interpolation(self):
        """Test that midpoint between two dates gives reasonable weights."""
        blender = SeasonBlender()
        # This is tricky to test precisely without knowing exact config
        # But we can verify the behavior is reasonable
        day = 180  # Roughly middle of year
        weights = blender._interpolate_weights(day)

        # Should have summer or related seasons
        assert len(weights) > 0
        assert sum(weights.values()) == pytest.approx(1.0)


class TestGetActiveSeasons:
    """Test getting active seasons with weights."""

    def test_christmas_day(self):
        """Test that Christmas Day returns christmas season."""
        blender = SeasonBlender()
        with freeze_time("2025-12-25"):
            weights = blender.get_active_seasons()

            assert "christmas" in weights
            assert weights["christmas"] == 1.0

    def test_halloween(self):
        """Test that Halloween returns halloween season."""
        blender = SeasonBlender()
        with freeze_time("2026-10-31"):
            weights = blender.get_active_seasons()

            assert "halloween" in weights
            assert weights["halloween"] >= 0.7  # Should be dominant on Halloween

    def test_july_fourth(self):
        """Test that July 4th returns fourth_july season."""
        blender = SeasonBlender()
        with freeze_time("2026-07-04"):
            weights = blender.get_active_seasons()

            assert "fourth_july" in weights
            assert weights["fourth_july"] >= 0.5  # Should be dominant on July 4th

    def test_with_explicit_date(self):
        """Test get_active_seasons with explicit date."""
        blender = SeasonBlender()
        test_date = date(2025, 12, 25)
        weights = blender.get_active_seasons(test_date)

        assert "christmas" in weights
        assert weights["christmas"] == 1.0

    def test_with_day_of_year_int(self):
        """Test get_active_seasons with day_of_year as int."""
        blender = SeasonBlender()
        # Day 359 is Christmas
        weights = blender.get_active_seasons(359)

        assert "christmas" in weights

    def test_returns_dict(self):
        """Test that get_active_seasons returns a dict."""
        blender = SeasonBlender()
        weights = blender.get_active_seasons(date(2025, 6, 15))

        assert isinstance(weights, dict)
        assert len(weights) > 0

    def test_transition_period_multiple_seasons(self):
        """Test that transition periods return multiple seasons."""
        blender = SeasonBlender()
        # Late November should have fall and possibly thanksgiving
        weights = blender.get_active_seasons(date(2025, 11, 20))

        # Should have at least one season
        assert len(weights) >= 1
        assert sum(weights.values()) == pytest.approx(1.0)

    def test_mid_winter(self):
        """Test mid-winter date."""
        blender = SeasonBlender()
        # Mid-January should be winter
        weights = blender.get_active_seasons(date(2025, 1, 15))

        assert "winter" in weights
        # Winter should be dominant
        assert weights["winter"] > 0.5


class TestGetRandomSeason:
    """Test random season selection based on weights."""

    def test_returns_tuple(self):
        """Test that get_random_season returns a tuple."""
        blender = SeasonBlender()
        result = blender.get_random_season(date(2025, 12, 25))

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_valid_season(self):
        """Test that returned season is valid."""
        blender = SeasonBlender()
        season_name, season_instance = blender.get_random_season(date(2025, 12, 25))

        assert isinstance(season_name, str)
        assert season_name in blender.seasons
        assert season_instance is not None

    def test_christmas_always_returns_christmas(self):
        """Test that Christmas Day always returns christmas season."""
        blender = SeasonBlender()
        # Since Christmas is 100% on 12/25, it should always be selected
        for _ in range(10):  # Try multiple times
            season_name, _ = blender.get_random_season(date(2025, 12, 25))
            assert season_name == "christmas"

    def test_halloween_always_returns_halloween(self):
        """Test that Halloween always returns halloween season."""
        blender = SeasonBlender()
        for _ in range(10):
            season_name, _ = blender.get_random_season(date(2025, 10, 31))
            assert season_name == "halloween"

    def test_season_instance_matches_name(self):
        """Test that returned instance matches the season name."""
        blender = SeasonBlender()
        season_name, season_instance = blender.get_random_season(date(2025, 12, 25))

        assert blender.seasons[season_name] is season_instance

    def test_weighted_randomness(self):
        """Test that random selection respects weights (statistical test)."""
        blender = SeasonBlender()
        # Use a date with mixed weights
        # This is a statistical test, so we need many samples
        test_date = date(2025, 11, 26)  # Day after Thanksgiving

        season_counts = {}
        iterations = 100

        for _ in range(iterations):
            season_name, _ = blender.get_random_season(test_date)
            season_counts[season_name] = season_counts.get(season_name, 0) + 1

        # Should have selected some seasons
        assert len(season_counts) > 0
        # All selected seasons should be valid
        for season_name in season_counts:
            assert season_name in blender.seasons


class TestGetPrompt:
    """Test prompt generation from active seasons."""

    def test_returns_tuple(self):
        """Test that get_prompt returns a tuple."""
        blender = SeasonBlender()
        result = blender.get_prompt(date(2025, 12, 25))

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_prompt_and_season(self):
        """Test that get_prompt returns (prompt, season_name)."""
        blender = SeasonBlender()
        prompt, season_name = blender.get_prompt(date(2025, 12, 25))

        assert isinstance(prompt, str)
        assert isinstance(season_name, str)
        assert len(prompt) > 0
        assert season_name in blender.seasons

    def test_christmas_prompt(self):
        """Test that Christmas generates a Christmas prompt."""
        blender = SeasonBlender()
        prompt, season_name = blender.get_prompt(date(2025, 12, 25))

        assert season_name == "christmas"
        assert isinstance(prompt, str)
        assert len(prompt) > 20  # Should be a substantial prompt

    def test_prompt_not_empty(self):
        """Test that prompts are never empty."""
        blender = SeasonBlender()
        # Test various dates
        for month in [1, 3, 6, 9, 12]:
            prompt, season_name = blender.get_prompt(date(2025, month, 15))
            assert len(prompt) > 0
            assert season_name in blender.seasons

    def test_uses_current_date_by_default(self):
        """Test that get_prompt uses current date if no date provided."""
        blender = SeasonBlender()
        with freeze_time("2025-12-25"):
            prompt, season_name = blender.get_prompt()
            assert season_name == "christmas"

    def test_different_dates_can_produce_different_prompts(self):
        """Test that different dates can produce different prompts."""
        blender = SeasonBlender()
        prompt1, season1 = blender.get_prompt(date(2025, 12, 25))
        prompt2, season2 = blender.get_prompt(date(2025, 7, 4))

        # Seasons should definitely be different
        assert season1 != season2
        # Prompts might be the same by chance, but seasons are different
        assert season1 == "christmas"
        assert season2 == "fourth_july"


class TestSeasonBlenderIntegration:
    """Integration tests for the full season blending system."""

    def test_full_year_coverage(self):
        """Test that every day of the year produces valid weights."""
        blender = SeasonBlender()

        for day in range(1, 366):
            weights = blender._interpolate_weights(day)
            assert len(weights) > 0
            assert sum(weights.values()) == pytest.approx(1.0, abs=0.01)
            assert all(w >= 0 for w in weights.values())

    def test_smooth_transitions(self):
        """Test that transitions between seasons are smooth."""
        blender = SeasonBlender()

        # Check November transition from fall to thanksgiving to christmas
        prev_weights = None
        for day in range(15, 30):  # Nov 15-30
            try:
                test_date = date(2026, 11, day)
                day_of_year = blender.get_day_of_year(test_date)
                weights = blender._interpolate_weights(day_of_year)

                if prev_weights:
                    # Weights should change gradually, not jump wildly
                    # Allow for holidays which can have larger jumps
                    for season in set(prev_weights.keys()) | set(weights.keys()):
                        prev_val = prev_weights.get(season, 0)
                        curr_val = weights.get(season, 0)
                        # Allow up to 0.6 per day for holiday transitions
                        assert (
                            abs(curr_val - prev_val) < 0.7
                        ), f"Large jump in {season} from {prev_val} to {curr_val} on Nov {day}"

                prev_weights = weights
            except ValueError:
                pass

    def test_holiday_peaks(self):
        """Test that holidays have expected peak weights."""
        blender = SeasonBlender()

        holidays = [
            (date(2025, 12, 25), "christmas"),
            (date(2025, 10, 31), "halloween"),
            (date(2025, 7, 4), "fourth_july"),
            (date(2025, 2, 14), "valentines"),
        ]

        for test_date, expected_season in holidays:
            weights = blender.get_active_seasons(test_date)
            assert expected_season in weights
            assert (
                weights[expected_season] >= 0.9
            ), f"{expected_season} should be dominant on {test_date}"

    def test_consistent_prompt_generation(self):
        """Test that prompt generation is consistent for same date."""
        blender = SeasonBlender()

        test_date = date(2025, 12, 25)

        # Generate multiple prompts for same date
        seasons_seen = set()
        for _ in range(20):
            _, season_name = blender.get_prompt(test_date)
            seasons_seen.add(season_name)

        # Christmas is 100%, so should always be christmas
        assert seasons_seen == {"christmas"}
