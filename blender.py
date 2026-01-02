"""
VibeScape Season Blender

Date-aware seasonal selection system that uses a configuration table
to determine which seasons are currently active and their relative weights.

The blender interpolates between key dates defined in seasonal_config.py
to create smooth transitions throughout the year.
"""
import os
import logging
from datetime import datetime, date
from zoneinfo import ZoneInfo
from typing import Dict, Tuple

from seasons.christmas import Christmas
from seasons.winter import Winter
from seasons.new_years import NewYears
from seasons.fall import Fall
from seasons.summer import Summer
from seasons.spring import Spring
from seasons.thanksgiving import Thanksgiving
from seasons.fourth_july import FourthOfJuly
from seasons.easter import Easter
from seasons.halloween import Halloween
from seasons.valentines import Valentines
from seasonal_config import SEASONAL_WEIGHTS, get_day_of_year as config_day_of_year

logger = logging.getLogger("vibescape.blender")

# Timezone to use for date calculations (configurable via TIMEZONE env var, defaults to PST/PDT)
TIMEZONE = ZoneInfo(os.environ.get("TIMEZONE", "America/Los_Angeles"))


class SeasonBlender:
    """
    Determines active seasons and their weights based on the current date.
    
    Uses a configuration table (seasonal_config.py) with key dates and
    interpolates linearly between them for smooth transitions.
    """
    
    def __init__(self):
        """Initialize all available season generators."""
        self.seasons = {
            "christmas": Christmas(),
            "winter": Winter(),
            "new_years": NewYears(),
            "fall": Fall(),
            "summer": Summer(),
            "spring": Spring(),
            "thanksgiving": Thanksgiving(),
            "fourth_july": FourthOfJuly(),
            "easter": Easter(),
            "halloween": Halloween(),
            "valentines": Valentines(),
        }
        
        # Convert config to sorted list for interpolation
        self._build_interpolation_table()
    
    def _build_interpolation_table(self):
        """Build sorted list of (day_of_year, weights) from config."""
        self.weight_table = []
        for (month, day), weights in SEASONAL_WEIGHTS.items():
            day_of_year = config_day_of_year(month, day)
            self.weight_table.append((day_of_year, weights))
        
        # Sort by day of year
        self.weight_table.sort(key=lambda x: x[0])
        
        logger.debug("Built interpolation table with %d key dates", len(self.weight_table))
    
    def get_day_of_year(self, target_date: date = None) -> int:
        """
        Get the day of year (1-366) for a given date.
        
        Args:
            target_date: Date to check (defaults to today in PST, or DATE env override)
            
        Returns:
            int: Day of year (1-366)
        """
        if target_date is None:
            # Check for DATE environment variable override (format: YYYY-MM-DD or MM-DD)
            date_override = os.environ.get("DATE")
            if date_override:
                try:
                    if len(date_override.split('-')) == 2:
                        # MM-DD format - use current year in PST
                        month, day = map(int, date_override.split('-'))
                        now_pst = datetime.now(TIMEZONE)
                        target_date = date(now_pst.year, month, day)
                    else:
                        # YYYY-MM-DD format
                        target_date = datetime.strptime(date_override, "%Y-%m-%d").date()
                    logger.info("Using DATE override: %s (day %d)", target_date, target_date.timetuple().tm_yday)
                except (ValueError, TypeError) as e:
                    logger.warning("Invalid DATE override '%s': %s - using current date", date_override, e)
                    target_date = datetime.now(TIMEZONE).date()
            else:
                # Use current date in PST timezone
                target_date = datetime.now(TIMEZONE).date()
        return target_date.timetuple().tm_yday
    
    def _interpolate_weights(self, day_of_year: int) -> Dict[str, float]:
        """
        Get weights for a specific day by interpolating between key dates.
        
        Args:
            day_of_year: Day of year (1-366)
            
        Returns:
            Dict of season weights
        """
        # Find the two key dates to interpolate between
        before = None
        after = None
        
        for i, (key_day, weights) in enumerate(self.weight_table):
            if key_day == day_of_year:
                # Exact match - no interpolation needed
                return weights.copy()
            elif key_day < day_of_year:
                before = (key_day, weights)
            elif key_day > day_of_year and after is None:
                after = (key_day, weights)
                break
        
        # Handle year wrap-around
        if before is None:
            # We're before the first entry - wrap to end of year
            before = (self.weight_table[-1][0], self.weight_table[-1][1])
            after = (self.weight_table[0][0], self.weight_table[0][1])
            # Adjust for year wraparound
            day_of_year += 365
        elif after is None:
            # We're after the last entry - wrap to beginning of year
            after = (self.weight_table[0][0] + 365, self.weight_table[0][1])
        
        # Linear interpolation
        before_day, before_weights = before
        after_day, after_weights = after
        
        # Calculate interpolation ratio
        total_span = after_day - before_day
        current_offset = day_of_year - before_day
        ratio = current_offset / total_span if total_span > 0 else 0
        
        # Get all unique seasons from both weight dicts
        all_seasons = set(before_weights.keys()) | set(after_weights.keys())
        
        # Interpolate each season's weight
        result = {}
        for season in all_seasons:
            before_weight = before_weights.get(season, 0.0)
            after_weight = after_weights.get(season, 0.0)
            interpolated = before_weight + (after_weight - before_weight) * ratio
            if interpolated > 0.001:  # Only include if weight is meaningful
                result[season] = interpolated
        
        # Normalize to ensure sum = 1.0
        total = sum(result.values())
        if total > 0:
            result = {k: v / total for k, v in result.items()}
        
        return result
    
    def get_active_seasons(self, target_date: date | int = None) -> Dict[str, float]:
        """
        Get currently active seasons with their weights.
        
        Args:
            target_date: Date to check (defaults to today), or day_of_year as int
            
        Returns:
            Dict mapping season names to weights (0.0-1.0)
            Weights are normalized to sum to 1.0
        """
        if isinstance(target_date, int):
            day_of_year = target_date
        else:
            day_of_year = self.get_day_of_year(target_date)
        weights = self._interpolate_weights(day_of_year)
        
        logger.debug("Day %d: Active seasons: %s", day_of_year, weights)
        return weights
    
    def get_random_season(self, target_date: date = None) -> Tuple[str, object]:
        """
        Select a random season based on current weights.
        
        Args:
            target_date: Date to check (defaults to today)
            
        Returns:
            Tuple of (season_name, season_instance)
        """
        import random
        
        weights = self.get_active_seasons(target_date)
        
        # Convert weights to list for random.choices
        season_names = list(weights.keys())
        season_weights = list(weights.values())
        
        # Select one season based on weights
        selected_name = random.choices(season_names, weights=season_weights, k=1)[0]
        selected_season = self.seasons[selected_name]
        
        return selected_name, selected_season
    
    def get_prompt(self, target_date: date = None) -> Tuple[str, str]:
        """
        Generate a prompt from a randomly selected active season.
        
        Args:
            target_date: Date to check (defaults to today)
            
        Returns:
            Tuple of (prompt, season_name)
        """
        season_name, season = self.get_random_season(target_date)
        prompt = season.get_prompt()
        
        logger.debug("Generated prompt from %s: %s...", season_name, prompt[:100])
        return prompt, season_name
