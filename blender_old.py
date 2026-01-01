"""
VibeScape Season Blender

Date-aware seasonal selection system that determines which seasons
are currently active and their relative weights for generating
a natural blend of seasonal imagery throughout the year.

The blender uses a 2-week transition period between themes to create
smooth, gradual changes rather than abrupt switches.
"""
import logging
from datetime import datetime, date
from typing import Dict, List, Tuple

from seasons.christmas import Christmas
from seasons.winter import Winter
from seasons.new_years import NewYears
from seasons.spring import Spring
from seasons.fall import Fall
from seasons.summer import Summer

logger = logging.getLogger("vibescape.blender")


class SeasonBlender:
    """
    Determines active seasons and their weights based on the current date.
    
    Uses a 2-week (14-day) transition period to blend between themes.
    During transitions, both the outgoing and incoming themes are active
    with gradually shifting weights.
    """
    
    # Transition period in days (2 weeks)
    TRANSITION_DAYS = 14
    
    def __init__(self):
        """Initialize all available season generators."""
        self.seasons = {
            "christmas": Christmas(),
            "winter": Winter(),
            "new_years": NewYears(),
            "spring": Spring(),
            "fall": Fall(),
            "summer": Summer(),
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
        
        logger.info("Built interpolation table with %d key dates", len(self.weight_table))
    
    def get_day_of_year(self, target_date: date = None) -> int:
        """
        Get the day of year (1-366) for a given date.
        
        Args:
            target_date: Date to check (defaults to today)
            
        Returns:
            int: Day of year (1-366)
        """
        if target_date is None:
            target_date = datetime.now().date()
        return target_date.timetuple().tm_yday
    
    def _get_day_of_year(self, target_date: date = None) -> int:
        """Deprecated: Use get_day_of_year instead."""
        return self.get_day_of_year(target_date)
    
    def _date_from_month_day(self, month: int, day: int) -> int:
        """
        Convert month/day to day-of-year.
        
        Args:
            month: Month (1-12)
            day: Day of month
            
        Returns:
            int: Day of year
        """
        # Use a non-leap year for consistency
        return date(2025, month, day).timetuple().tm_yday
    
    def _is_in_range(self, current_day: int, start_day: int, end_day: int) -> bool:
        """
        Check if current day is within a range, handling year wraparound.
        
        Args:
            current_day: Current day of year
            start_day: Start day of range
            end_day: End day of range (may be less than start if wrapping)
            
        Returns:
            bool: True if current day is in range
        """
        if start_day <= end_day:
            return start_day <= current_day <= end_day
        else:
            # Range wraps around year end (e.g., Dec 20 to Jan 10)
            return current_day >= start_day or current_day <= end_day
    
    def _calculate_smooth_weight(self, current_day: int, start: int, 
                                 peak_start: int, peak_end: int, end: int) -> float:
        """
        Calculate smooth weight for a season with proper blending.
        
        Weight pattern:
        - start → peak_start: 0.0 → 1.0 (2-week ramp up)
        - peak_start → peak_end: 1.0 (full strength)
        - peak_end → end: 1.0 → 0.0 (2-week ramp down)
        
        Args:
            current_day: Current day of year
            start: When theme starts appearing (0 weight)
            peak_start: When theme reaches full strength (1.0 weight)
            peak_end: When theme starts declining (1.0 weight)
            end: When theme stops appearing (0 weight)
            
        Returns:
            float: Weight from 0.0 to 1.0
        """
        # Helper to calculate days between two points (handling year wrap)
        def days_between(day1: int, day2: int) -> int:
            if day1 <= day2:
                return day2 - day1
            else:
                # Wrap around year end
                return (365 - day1) + day2
        
        # Check if current day is in the season's range
        in_range = False
        if start <= end:
            in_range = start <= current_day <= end
        else:
            # Wraps around year (e.g., Dec to Jan)
            in_range = current_day >= start or current_day <= end
        
        if not in_range:
            return 0.0
        
        # In peak period - full strength
        if peak_start <= peak_end:
            if peak_start <= current_day <= peak_end:
                return 1.0
        else:
            # Peak wraps year
            if current_day >= peak_start or current_day <= peak_end:
                return 1.0
        
        # In ramp-up period (start → peak_start)
        ramp_up_in_range = False
        if start <= peak_start:
            ramp_up_in_range = start <= current_day < peak_start
        else:
            ramp_up_in_range = current_day >= start or current_day < peak_start
        
        if ramp_up_in_range:
            days_from_start = days_between(start, current_day)
            ramp_up_length = days_between(start, peak_start)
            if ramp_up_length > 0:
                return max(0.0, min(1.0, days_from_start / ramp_up_length))
            return 1.0
        
        # In ramp-down period (peak_end → end)
        ramp_down_in_range = False
        if peak_end <= end:
            ramp_down_in_range = peak_end < current_day <= end
        else:
            ramp_down_in_range = current_day > peak_end or current_day <= end
        
        if ramp_down_in_range:
            days_from_peak_end = days_between(peak_end, current_day)
            ramp_down_length = days_between(peak_end, end)
            if ramp_down_length > 0:
                return max(0.0, min(1.0, 1.0 - (days_from_peak_end / ramp_down_length)))
            return 0.0
        
        return 0.0
    
    def get_active_seasons(self, target_date: date = None) -> Dict[str, float]:
        """
        Get currently active seasons with their weights.
        
        Args:
            target_date: Date to check (defaults to today)
            
        Returns:
            Dict mapping season names to weights (0.0-1.0)
            Weights are normalized to sum to 1.0
        """
        day_of_year = self.get_day_of_year(target_date)
        weights = {}
        
        # Define seasonal periods with smooth 2-week transitions
        # Each period: (season_name, start_day, peak_start, peak_end, end_day)
        # - Blends from 0→100% over 2 weeks (start to peak_start)
        # - Stays at 100% during peak period (peak_start to peak_end)
        # - Blends from 100→0% over 2 weeks (peak_end to end_day)
        
        # Thanksgiving: Nov 18-30
        thanksgiving = ("fall", 
                       self._date_from_month_day(11, 18),  # Start blending in
                       self._date_from_month_day(11, 25),  # Peak start (Thanksgiving day)
                       self._date_from_month_day(11, 27),  # Peak end
                       self._date_from_month_day(11, 30))  # Start blending out
        
        # Christmas: Nov 28 - Dec 26
        christmas = ("christmas",
                    self._date_from_month_day(11, 28),   # Start blending in (overlaps with Thanksgiving)
                    self._date_from_month_day(12, 12),   # Peak start
                    self._date_from_month_day(12, 25),   # Peak end (Christmas Day)
                    self._date_from_month_day(12, 26))   # Start blending out
        
        # New Years: Dec 24 - Jan 8
        newyears = ("new_years",
                   self._date_from_month_day(12, 24),   # Start blending in (overlaps with Christmas)
                   self._date_from_month_day(12, 31),   # Peak start (New Year's Eve)
                   self._date_from_month_day(1, 2),     # Peak end
                   self._date_from_month_day(1, 8))     # Start blending out
        
        # Winter: Jan 1 - Mar 14
        winter = ("winter",
                 self._date_from_month_day(1, 1),      # Start blending in (overlaps with New Years)
                 self._date_from_month_day(1, 15),     # Peak start
                 self._date_from_month_day(2, 15),     # Peak end
                 self._date_from_month_day(3, 14))     # Start blending out
        
        # Spring: Mar 1 - May 31
        spring = ("spring",
                 self._date_from_month_day(3, 1),      # Start blending in
                 self._date_from_month_day(3, 15),     # Peak start
                 self._date_from_month_day(5, 15),     # Peak end
                 self._date_from_month_day(5, 31))     # Start blending out
        
        # Summer: May 20 - Sep 7
        summer = ("summer",
                 self._date_from_month_day(5, 20),     # Start blending in
                 self._date_from_month_day(6, 3),      # Peak start
                 self._date_from_month_day(8, 24),     # Peak end
                 self._date_from_month_day(9, 7))      # Start blending out
        
        # Fall: Aug 25 - Nov 30
        fall = ("fall",
               self._date_from_month_day(8, 25),       # Start blending in
               self._date_from_month_day(9, 8),        # Peak start
               self._date_from_month_day(11, 10),      # Peak end
               self._date_from_month_day(11, 30))      # Blends into Christmas
        
        # All seasons to check
        all_seasons = [thanksgiving, christmas, newyears, winter, spring, summer, fall]
        
        # Calculate weight for each season
        for season_name, start, peak_start, peak_end, end in all_seasons:
            weight = self._calculate_smooth_weight(day_of_year, start, peak_start, peak_end, end)
            if weight > 0:
                weights[season_name] = weight
        
        # If no weights calculated (shouldn't happen), default to current season
        if not weights:
            # Default fallback based on month
            month = datetime.now().month
            if month in [12, 1, 2]:
                weights["winter"] = 1.0
            elif month in [3, 4, 5]:
                weights["spring"] = 1.0
            elif month in [6, 7, 8]:
                weights["summer"] = 1.0
            else:
                weights["fall"] = 1.0
        
        # Normalize weights to sum to 1.0
        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}
        
        logger.info("Day %d: Active seasons: %s", day_of_year, weights)
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
        
        logger.info("Generated prompt from %s: %s...", season_name, prompt[:100])
        return prompt, season_name
