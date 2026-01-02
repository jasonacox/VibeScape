"""
VibeScape Seasonal Weight Configuration

This table defines the exact weights for each season on key dates throughout
the year. The blender will interpolate between these key dates to get smooth
transitions while giving us precise control over holiday ramp-ups and terminal dates.

Format: Each entry is (month, day): {season: weight, ...}
Weights should sum to 1.0 (100%) for each date.
"""

# Key dates with exact seasonal weights
# Format: (month, day): {"season_name": weight, ...}
SEASONAL_WEIGHTS = {
    # Thanksgiving transition - Start ramping up Christmas
    (11, 23): {"fall": 0.85, "thanksgiving": 0.15},
    (11, 24): {"fall": 0.60, "thanksgiving": 0.40},
    (11, 25): {"thanksgiving": 1.0},                            # Thanksgiving Day - 100%
    (11, 26): {"thanksgiving": 0.80, "christmas": 0.20},       # Day after Thanksgiving - Christmas begins
    (11, 28): {"thanksgiving": 0.65, "christmas": 0.35},
    (11, 30): {"thanksgiving": 0.50, "christmas": 0.50},
    
    # December - Christmas ramps up
    (12, 2): {"thanksgiving": 0.35, "christmas": 0.65},
    (12, 5): {"thanksgiving": 0.20, "christmas": 0.80},
    (12, 8): {"thanksgiving": 0.10, "christmas": 0.90},
    (12, 11): {"christmas": 1.0},
    (12, 14): {"christmas": 1.0},
    (12, 17): {"christmas": 1.0},
    
    # Christmas peak
    (12, 20): {"christmas": 1.0},
    (12, 23): {"christmas": 1.0},
    (12, 24): {"christmas": 1.0},                              # Christmas Eve - 100%
    (12, 25): {"christmas": 1.0},                              # Christmas Day - 100%
    
    # New Year's transition
    (12, 26): {"christmas": 0.70, "new_years": 0.30},         # Day after Christmas
    (12, 27): {"christmas": 0.50, "new_years": 0.50},
    (12, 28): {"christmas": 0.30, "new_years": 0.70},
    (12, 29): {"christmas": 0.15, "new_years": 0.85},
    (12, 30): {"new_years": 0.25, "winter": 0.75},
    (12, 31): {"new_years": 0.90, "winter": 0.10},                              # New Year's Eve - 100%
    
    # New Year's Day is terminal
    (1, 1): {"new_years": 0.5, "winter": 0.5},                                # New Year's Day - 100%
    (1, 2): {"winter": 0.8, "new_years": 0.2},                                    # Switch to Winter
    
    # Winter season
    (1, 5): {"winter": 1.0},
    (1, 15): {"winter": 1.0},
    (2, 1): {"winter": 1.0},
    (2, 10): {"winter": 0.90, "valentines": 0.10},            # Valentine's week approaches
    (2, 12): {"winter": 0.60, "valentines": 0.40},
    (2, 13): {"winter": 0.30, "valentines": 0.70},
    (2, 14): {"valentines": 1.0},                              # Valentine's Day - 100%
    (2, 15): {"winter": 1.0},                                  # Back to winter
    (2, 20): {"winter": 1.0},
    (2, 28): {"winter": 1.0},
    
    # Spring transition
    (3, 1): {"winter": 0.90, "spring": 0.10},
    (3, 5): {"winter": 0.70, "spring": 0.30},
    (3, 10): {"winter": 0.50, "spring": 0.50},
    (3, 15): {"winter": 0.30, "spring": 0.70},
    (3, 20): {"winter": 0.10, "spring": 0.90},                # Spring Equinox
    (3, 25): {"spring": 1.0},
    
    # Spring season
    (4, 1): {"spring": 1.0},
    (4, 10): {"spring": 0.90, "easter": 0.10},                 # Easter week approaches
    (4, 13): {"spring": 0.70, "easter": 0.30},                 # Palm Sunday week
    (4, 17): {"spring": 0.50, "easter": 0.50},
    (4, 20): {"easter": 1.0},                                   # Easter Sunday (approximate - varies by year)
    (4, 21): {"spring": 1.0},                                   # Back to spring
    (5, 1): {"spring": 1.0},
    (5, 15): {"spring": 1.0},
    
    # Summer transition
    (5, 20): {"spring": 0.80, "summer": 0.20},
    (5, 25): {"spring": 0.50, "summer": 0.50},
    (5, 31): {"spring": 0.20, "summer": 0.80},
    (6, 3): {"summer": 1.0},
    
    # Summer season
    (6, 15): {"summer": 1.0},
    (6, 28): {"summer": 0.90, "fourth_july": 0.10},           # Fourth of July week approaches
    (7, 1): {"summer": 0.70, "fourth_july": 0.30},
    (7, 3): {"summer": 0.50, "fourth_july": 0.50},
    (7, 4): {"fourth_july": 1.0},                              # Independence Day - 100%
    (7, 5): {"summer": 1.0},                                   # Back to summer
    (7, 15): {"summer": 1.0},
    (8, 1): {"summer": 1.0},
    (8, 20): {"summer": 1.0},
    
    # Fall transition
    (8, 25): {"summer": 0.85, "fall": 0.15},
    (8, 30): {"summer": 0.60, "fall": 0.40},
    (9, 3): {"summer": 0.40, "fall": 0.60},
    (9, 7): {"summer": 0.20, "fall": 0.80},
    (9, 10): {"fall": 1.0},
    
    # Fall season
    (9, 22): {"fall": 1.0},                                    # Fall Equinox
    (10, 1): {"fall": 1.0},
    (10, 15): {"fall": 1.0},
    (10, 25): {"fall": 0.85, "halloween": 0.15},              # Halloween week approaches
    (10, 28): {"fall": 0.60, "halloween": 0.40},
    (10, 30): {"fall": 0.30, "halloween": 0.70},
    (10, 31): {"halloween": 1.0},                              # Halloween - 100%
    (11, 1): {"fall": 1.0},                                    # Back to fall
    (11, 10): {"fall": 1.0},
    (11, 20): {"fall": 1.0},
}


def get_day_of_year(month: int, day: int) -> int:
    """Convert month/day to day of year."""
    from datetime import date
    return date(2025, month, day).timetuple().tm_yday


def validate_config():
    """Validate that all weights sum to 1.0."""
    for date_key, weights in SEASONAL_WEIGHTS.items():
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:  # Allow small floating point errors
            print(f"WARNING: Weights for {date_key[0]}/{date_key[1]} sum to {total:.2f}, not 1.0")
            print(f"  Weights: {weights}")
    print("Configuration validation complete.")


if __name__ == "__main__":
    # Validate and show the configuration
    validate_config()
    print(f"\nTotal key dates defined: {len(SEASONAL_WEIGHTS)}")
    
    # Show a sample
    print("\nSample holiday dates:")
    for date_key in [(4, 20), (7, 4), (10, 31), (11, 25), (12, 25), (1, 1)]:
        if date_key in SEASONAL_WEIGHTS:
            weights = SEASONAL_WEIGHTS[date_key]
            weight_str = ", ".join([f"{k}: {v*100:.0f}%" for k, v in sorted(weights.items())])
            print(f"  {date_key[0]:02d}/{date_key[1]:02d}: {weight_str}")
    for date_key in [(11, 25), (12, 25), (1, 1), (1, 2), (3, 20), (7, 4)]:
        if date_key in SEASONAL_WEIGHTS:
            weights = SEASONAL_WEIGHTS[date_key]
            weight_str = ", ".join([f"{k}: {v*100:.0f}%" for k, v in sorted(weights.items())])
            print(f"  {date_key[0]:02d}/{date_key[1]:02d}: {weight_str}")
