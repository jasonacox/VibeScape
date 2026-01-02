#!/usr/bin/env python3
"""
Generate web icons from a source PNG image.

Creates:
  - static/favicon.ico (multi-size: 16, 32, 48, 64, 128, 256)
  - static/apple-touch-icon.png (180x180)
  - static/favicon-32x32.png (32x32)
  - static/favicon-16x16.png (16x16)

Usage:
  python3 generate_icons.py [source_image.png]
  
  If no source image is provided, defaults to 'vibescape-web-icon.png'
"""

import os
import sys
from PIL import Image

# Default source image
DEFAULT_SOURCE = "static/vibescape-web-icon.png"

# Output directory
OUTPUT_DIR = "static"

# Icon sizes
ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
APPLE_TOUCH_SIZE = 180
FAVICON_32_SIZE = 32
FAVICON_16_SIZE = 16


def generate_icons(source_path: str) -> None:
    """Generate all icon formats from source image."""
    
    # Validate source exists
    if not os.path.exists(source_path):
        print(f"Error: Source image not found: {source_path}")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load source image
    print(f"Loading source image: {source_path}")
    source = Image.open(source_path)
    
    # Convert to RGBA if needed
    if source.mode != "RGBA":
        source = source.convert("RGBA")
    
    print(f"Source size: {source.width}x{source.height}")
    
    # Generate favicon.ico (multi-size)
    ico_path = os.path.join(OUTPUT_DIR, "favicon.ico")
    print(f"Generating {ico_path} with sizes: {[s[0] for s in ICO_SIZES]}")
    
    # Create resized versions for ICO
    max_ico_size = max(s[0] for s in ICO_SIZES)
    ico_base = source.copy()
    if ico_base.width != max_ico_size or ico_base.height != max_ico_size:
        ico_base = ico_base.resize((max_ico_size, max_ico_size), Image.Resampling.LANCZOS)
    
    ico_base.save(ico_path, format="ICO", sizes=ICO_SIZES)
    print(f"  ✓ Created {ico_path}")
    
    # Generate apple-touch-icon.png (180x180)
    apple_path = os.path.join(OUTPUT_DIR, "apple-touch-icon.png")
    print(f"Generating {apple_path} ({APPLE_TOUCH_SIZE}x{APPLE_TOUCH_SIZE})")
    
    apple_icon = source.copy()
    apple_icon = apple_icon.resize((APPLE_TOUCH_SIZE, APPLE_TOUCH_SIZE), Image.Resampling.LANCZOS)
    # Apple touch icons should not have transparency - convert to RGB with white background
    if apple_icon.mode == "RGBA":
        background = Image.new("RGB", apple_icon.size, (255, 255, 255))
        background.paste(apple_icon, mask=apple_icon.split()[3])  # Use alpha as mask
        apple_icon = background
    apple_icon.save(apple_path, format="PNG")
    print(f"  ✓ Created {apple_path}")
    
    # Generate favicon-32x32.png
    fav32_path = os.path.join(OUTPUT_DIR, "favicon-32x32.png")
    print(f"Generating {fav32_path} ({FAVICON_32_SIZE}x{FAVICON_32_SIZE})")
    
    fav32 = source.copy()
    fav32 = fav32.resize((FAVICON_32_SIZE, FAVICON_32_SIZE), Image.Resampling.LANCZOS)
    fav32.save(fav32_path, format="PNG")
    print(f"  ✓ Created {fav32_path}")
    
    # Generate favicon-16x16.png (bonus)
    fav16_path = os.path.join(OUTPUT_DIR, "favicon-16x16.png")
    print(f"Generating {fav16_path} ({FAVICON_16_SIZE}x{FAVICON_16_SIZE})")
    
    fav16 = source.copy()
    fav16 = fav16.resize((FAVICON_16_SIZE, FAVICON_16_SIZE), Image.Resampling.LANCZOS)
    fav16.save(fav16_path, format="PNG")
    print(f"  ✓ Created {fav16_path}")
    
    print(f"\nAll icons generated successfully in '{OUTPUT_DIR}/' directory!")
    print("\nGenerated files:")
    for f in os.listdir(OUTPUT_DIR):
        fpath = os.path.join(OUTPUT_DIR, f)
        size = os.path.getsize(fpath)
        print(f"  {f}: {size:,} bytes")


if __name__ == "__main__":
    # Get source image from command line or use default
    if len(sys.argv) > 1:
        source_image = sys.argv[1]
    else:
        source_image = DEFAULT_SOURCE
    
    generate_icons(source_image)
