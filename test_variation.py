#!/usr/bin/env python3
"""
Test script to demonstrate prompt variation improvements.
Shows how many unique prompts are generated from the same season.
"""
from seasons.winter import Winter
from seasons.christmas import Christmas


def test_variation(season, name, count=20):
    """Generate multiple prompts and show uniqueness."""
    print(f"\n{'='*80}")
    print(f"Testing {name} - Generating {count} prompts:")
    print(f"{'='*80}\n")

    prompts = []
    for i in range(count):
        prompt = season.get_prompt()
        prompts.append(prompt)
        print(f"{i+1:2d}. {prompt[:100]}...")

    unique_prompts = len(set(prompts))
    print(f"\n{'='*80}")
    print(
        f"Results: {unique_prompts}/{count} unique prompts ({unique_prompts/count*100:.1f}% unique)"
    )
    print(f"{'='*80}\n")

    return unique_prompts, count


if __name__ == "__main__":
    winter = Winter()
    christmas = Christmas()

    # Test Winter
    w_unique, w_total = test_variation(winter, "Winter", 20)

    # Test Christmas
    c_unique, c_total = test_variation(christmas, "Christmas", 20)

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Winter:    {w_unique}/{w_total} unique ({w_unique/w_total*100:.1f}%)")
    print(f"Christmas: {c_unique}/{c_total} unique ({c_unique/c_total*100:.1f}%)")
    print("\nWith the enhanced variation system:")
    print("- 50% chance of alternate artistic styles (vs 20% before)")
    print("- Variable number of extras: 1-3 (vs fixed 2 before)")
    print("- 40% chance of time-of-day modifier")
    print("- 30% chance of atmospheric condition")
    print("- 25% chance of composition style")
    print("- Expanded scene keyword pools (50 vs 30 for Winter)")
    print("- Expanded extras pools (26 vs 16 for Winter)")
    print("- Randomized order of modifiers for additional variety")
    print("=" * 80)
