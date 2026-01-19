"""
Tests for seasonal_config.py - seasonal weight configuration.
"""
import pytest
from datetime import date
from seasonal_config import SEASONAL_WEIGHTS, get_day_of_year, validate_config


class TestSeasonalWeights:
    """Test the SEASONAL_WEIGHTS configuration."""

    def test_weights_exist(self):
        """Test that SEASONAL_WEIGHTS is not empty."""
        assert len(SEASONAL_WEIGHTS) > 0
        assert isinstance(SEASONAL_WEIGHTS, dict)

    def test_all_weights_sum_to_one(self):
        """Test that all weight dictionaries sum to 1.0 (within tolerance)."""
        for date_key, weights in SEASONAL_WEIGHTS.items():
            total = sum(weights.values())
            assert (
                abs(total - 1.0) < 0.01
            ), f"Weights for {date_key[0]}/{date_key[1]} sum to {total:.3f}, not 1.0: {weights}"

    def test_date_keys_format(self):
        """Test that all date keys are tuples of (month, day)."""
        for date_key in SEASONAL_WEIGHTS.keys():
            assert isinstance(date_key, tuple)
            assert len(date_key) == 2
            month, day = date_key
            assert isinstance(month, int)
            assert isinstance(day, int)
            assert 1 <= month <= 12
            assert 1 <= day <= 31

    def test_weight_values_valid(self):
        """Test that all weight values are between 0.0 and 1.0."""
        for date_key, weights in SEASONAL_WEIGHTS.items():
            for season, weight in weights.items():
                assert isinstance(
                    weight, (int, float)
                ), f"Weight for {season} on {date_key} is not numeric: {weight}"
                assert (
                    0.0 <= weight <= 1.0
                ), f"Weight for {season} on {date_key} is out of range: {weight}"

    def test_season_names_valid(self):
        """Test that all season names are valid strings."""
        valid_seasons = {
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
        }
        for date_key, weights in SEASONAL_WEIGHTS.items():
            for season in weights.keys():
                assert isinstance(season, str)
                assert (
                    season in valid_seasons
                ), f"Unknown season '{season}' in config for {date_key}"

    def test_christmas_dates_defined(self):
        """Test that Christmas key dates are defined."""
        assert (12, 24) in SEASONAL_WEIGHTS  # Christmas Eve
        assert (12, 25) in SEASONAL_WEIGHTS  # Christmas Day

    def test_christmas_day_is_100_percent(self):
        """Test that Christmas Day is 100% Christmas."""
        christmas_weights = SEASONAL_WEIGHTS[(12, 25)]
        assert "christmas" in christmas_weights
        assert christmas_weights["christmas"] == 1.0

    def test_halloween_dates_defined(self):
        """Test that Halloween key dates are defined."""
        assert (10, 31) in SEASONAL_WEIGHTS  # Halloween

    def test_halloween_is_100_percent(self):
        """Test that Halloween is 100% Halloween."""
        halloween_weights = SEASONAL_WEIGHTS[(10, 31)]
        assert "halloween" in halloween_weights
        assert halloween_weights["halloween"] == 1.0

    def test_thanksgiving_dates_defined(self):
        """Test that Thanksgiving key dates are defined."""
        assert (11, 25) in SEASONAL_WEIGHTS  # Thanksgiving (approximate)

    def test_fourth_july_dates_defined(self):
        """Test that Fourth of July key dates are defined."""
        assert (7, 4) in SEASONAL_WEIGHTS

    def test_fourth_july_is_100_percent(self):
        """Test that July 4th is 100% fourth_july."""
        july4_weights = SEASONAL_WEIGHTS[(7, 4)]
        assert "fourth_july" in july4_weights
        assert july4_weights["fourth_july"] == 1.0

    def test_new_years_dates_defined(self):
        """Test that New Year's key dates are defined."""
        assert (12, 31) in SEASONAL_WEIGHTS  # New Year's Eve
        assert (1, 1) in SEASONAL_WEIGHTS  # New Year's Day

    def test_valentines_day_defined(self):
        """Test that Valentine's Day is defined."""
        assert (2, 14) in SEASONAL_WEIGHTS
        valentines_weights = SEASONAL_WEIGHTS[(2, 14)]
        assert "valentines" in valentines_weights
        assert valentines_weights["valentines"] == 1.0

    def test_easter_dates_defined(self):
        """Test that Easter approximate dates are defined."""
        # Easter is around April 20 (varies by year)
        assert (4, 20) in SEASONAL_WEIGHTS

    def test_base_seasons_coverage(self):
        """Test that base seasons (winter, spring, summer, fall) appear in config."""
        all_seasons = set()
        for weights in SEASONAL_WEIGHTS.values():
            all_seasons.update(weights.keys())

        assert "winter" in all_seasons
        assert "spring" in all_seasons
        assert "summer" in all_seasons
        assert "fall" in all_seasons

    def test_christmas_transition_to_new_years(self):
        """Test that there's a gradual transition from Christmas to New Year's."""
        # Dec 26 should have both Christmas and New Year's
        if (12, 26) in SEASONAL_WEIGHTS:
            weights = SEASONAL_WEIGHTS[(12, 26)]
            assert "christmas" in weights
            assert "new_years" in weights
            # Christmas should still be dominant
            assert weights["christmas"] > weights["new_years"]

    def test_thanksgiving_transition_to_christmas(self):
        """Test that there's a transition from Thanksgiving to Christmas."""
        # Nov 26 (day after Thanksgiving) should have both
        if (11, 26) in SEASONAL_WEIGHTS:
            weights = SEASONAL_WEIGHTS[(11, 26)]
            assert "thanksgiving" in weights or "christmas" in weights

    def test_year_coverage_january(self):
        """Test that January dates are covered."""
        jan_dates = [key for key in SEASONAL_WEIGHTS.keys() if key[0] == 1]
        assert len(jan_dates) > 0, "No January dates defined"

    def test_year_coverage_december(self):
        """Test that December dates are covered."""
        dec_dates = [key for key in SEASONAL_WEIGHTS.keys() if key[0] == 12]
        assert len(dec_dates) > 0, "No December dates defined"

    def test_config_sorted_by_date(self):
        """Test that we can sort config by date (for interpolation)."""
        dates = list(SEASONAL_WEIGHTS.keys())
        day_of_years = [get_day_of_year(month, day) for month, day in dates]
        # Just verify we can compute day of year for all dates
        assert len(day_of_years) == len(dates)
        assert all(isinstance(d, int) for d in day_of_years)
        assert all(1 <= d <= 366 for d in day_of_years)


class TestGetDayOfYear:
    """Test the get_day_of_year helper function."""

    def test_january_first(self):
        """Test that January 1st is day 1."""
        assert get_day_of_year(1, 1) == 1

    def test_december_31st(self):
        """Test that December 31st is day 365 (non-leap year)."""
        day = get_day_of_year(12, 31)
        assert day in (365, 366)  # Could be leap year

    def test_christmas(self):
        """Test Christmas day of year."""
        day = get_day_of_year(12, 25)
        assert day == 359  # Christmas is day 359 in non-leap year

    def test_july_fourth(self):
        """Test July 4th day of year."""
        day = get_day_of_year(7, 4)
        assert day == 185  # July 4th is day 185 in non-leap year

    def test_all_months(self):
        """Test that we can get day of year for all months."""
        for month in range(1, 13):
            day = get_day_of_year(month, 1)
            assert isinstance(day, int)
            assert 1 <= day <= 366

    def test_returns_int(self):
        """Test that function returns an integer."""
        result = get_day_of_year(6, 15)
        assert isinstance(result, int)

    def test_monotonic_increase(self):
        """Test that day of year increases monotonically through the year."""
        prev_day = 0
        for month in range(1, 13):
            for day in [1, 15]:
                try:
                    day_of_year = get_day_of_year(month, day)
                    assert (
                        day_of_year > prev_day
                    ), f"Day {month}/{day} ({day_of_year}) should be after previous ({prev_day})"
                    prev_day = day_of_year
                except ValueError:
                    # Some months don't have day 31
                    pass


class TestValidateConfig:
    """Test the validate_config function."""

    def test_validate_config_runs(self, capsys):
        """Test that validate_config runs without error."""
        validate_config()
        captured = capsys.readouterr()
        assert "Configuration validation complete" in captured.out

    def test_validate_config_detects_invalid_weights(self, capsys, monkeypatch):
        """Test that validate_config warns about invalid weight sums."""
        # Temporarily modify SEASONAL_WEIGHTS to have invalid sum
        import seasonal_config

        original_weights = seasonal_config.SEASONAL_WEIGHTS.copy()

        # Add an invalid entry
        seasonal_config.SEASONAL_WEIGHTS[(13, 1)] = {
            "test": 0.5
        }  # Sums to 0.5, not 1.0

        try:
            validate_config()
            captured = capsys.readouterr()
            # Should see a warning about invalid sum
            assert "WARNING" in captured.out or "13/1" in captured.out
        finally:
            # Restore original
            seasonal_config.SEASONAL_WEIGHTS = original_weights

    def test_no_warnings_for_valid_config(self, capsys):
        """Test that valid config produces no warnings."""
        validate_config()
        captured = capsys.readouterr()
        # Count warnings - should be 0 for a valid config
        warning_count = captured.out.count("WARNING")
        assert warning_count == 0, f"Expected no warnings, got {warning_count}"


class TestConfigCompleteness:
    """Test that the configuration provides complete year coverage."""

    def test_minimum_number_of_dates(self):
        """Test that we have a reasonable number of key dates defined."""
        # Should have at least 30 key dates for good interpolation
        assert len(SEASONAL_WEIGHTS) >= 30

    def test_all_holidays_have_100_percent(self):
        """Test that major holidays are defined at 100%."""
        # These holidays should be 100% on their day
        holidays_100 = [
            (12, 25, "christmas"),  # Christmas
            (10, 31, "halloween"),  # Halloween
            (7, 4, "fourth_july"),  # Fourth of July
            (2, 14, "valentines"),  # Valentine's Day
        ]

        for month, day, expected_season in holidays_100:
            if (month, day) in SEASONAL_WEIGHTS:
                weights = SEASONAL_WEIGHTS[(month, day)]
                assert (
                    expected_season in weights
                ), f"{expected_season} not found in weights for {month}/{day}"
                assert (
                    weights[expected_season] == 1.0
                ), f"{expected_season} on {month}/{day} is not 100%: {weights[expected_season]}"

    def test_no_duplicate_dates(self):
        """Test that no dates are defined multiple times."""
        dates = list(SEASONAL_WEIGHTS.keys())
        assert len(dates) == len(set(dates)), "Duplicate dates found in config"

    def test_seasonal_coverage_distribution(self):
        """Test that seasons are well distributed across the year."""
        # Count how many times each season appears
        season_counts = {}
        for weights in SEASONAL_WEIGHTS.values():
            for season in weights.keys():
                season_counts[season] = season_counts.get(season, 0) + 1

        # All base seasons should appear multiple times
        base_seasons = ["winter", "spring", "summer", "fall"]
        for season in base_seasons:
            assert season in season_counts, f"Base season {season} never appears"
            assert (
                season_counts[season] >= 3
            ), f"Base season {season} only appears {season_counts[season]} times"
