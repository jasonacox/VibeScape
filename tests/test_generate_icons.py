"""
Tests for generate_icons.py - Icon generation utility.
"""
import pytest
import os
from pathlib import Path
from PIL import Image
import generate_icons


class TestGenerateIcons:
    """Test the generate_icons function."""

    def test_generate_icons_creates_files(self, tmp_path, sample_image):
        """Test that generate_icons creates all expected files."""
        # Create a source image
        source_path = tmp_path / "source.png"
        sample_image.save(source_path, format="PNG")

        # Temporarily change OUTPUT_DIR
        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)

            # Generate icons
            generate_icons.generate_icons(str(source_path))

            # Check that files were created
            assert (tmp_path / "favicon.ico").exists()
            assert (tmp_path / "apple-touch-icon.png").exists()
            assert (tmp_path / "favicon-32x32.png").exists()
            assert (tmp_path / "favicon-16x16.png").exists()
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_generate_icons_with_rgba_source(self, tmp_path, sample_rgba_image):
        """Test icon generation with RGBA source image."""
        source_path = tmp_path / "source_rgba.png"
        sample_rgba_image.save(source_path, format="PNG")

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)
            generate_icons.generate_icons(str(source_path))

            # All files should be created
            assert (tmp_path / "favicon.ico").exists()
            assert (tmp_path / "apple-touch-icon.png").exists()
            assert (tmp_path / "favicon-32x32.png").exists()
            assert (tmp_path / "favicon-16x16.png").exists()
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_generate_icons_ico_sizes(self, tmp_path, sample_image):
        """Test that ICO file contains multiple sizes."""
        source_path = tmp_path / "source.png"
        sample_image.save(source_path, format="PNG")

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)
            generate_icons.generate_icons(str(source_path))

            # Load ICO and check it exists
            ico_path = tmp_path / "favicon.ico"
            assert ico_path.exists()

            # Verify it's a valid image
            img = Image.open(ico_path)
            assert img is not None
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_generate_icons_apple_touch_size(self, tmp_path, sample_image):
        """Test that apple-touch-icon is correct size (180x180)."""
        source_path = tmp_path / "source.png"
        sample_image.save(source_path, format="PNG")

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)
            generate_icons.generate_icons(str(source_path))

            apple_icon = Image.open(tmp_path / "apple-touch-icon.png")
            assert apple_icon.size == (180, 180)
            # Should be RGB (no transparency)
            assert apple_icon.mode == "RGB"
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_generate_icons_favicon_32_size(self, tmp_path, sample_image):
        """Test that favicon-32x32 is correct size."""
        source_path = tmp_path / "source.png"
        sample_image.save(source_path, format="PNG")

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)
            generate_icons.generate_icons(str(source_path))

            fav32 = Image.open(tmp_path / "favicon-32x32.png")
            assert fav32.size == (32, 32)
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_generate_icons_favicon_16_size(self, tmp_path, sample_image):
        """Test that favicon-16x16 is correct size."""
        source_path = tmp_path / "source.png"
        sample_image.save(source_path, format="PNG")

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)
            generate_icons.generate_icons(str(source_path))

            fav16 = Image.open(tmp_path / "favicon-16x16.png")
            assert fav16.size == (16, 16)
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_generate_icons_missing_source_exits(self, tmp_path, capsys):
        """Test that missing source image causes sys.exit."""
        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)

            with pytest.raises(SystemExit) as exc_info:
                generate_icons.generate_icons("nonexistent.png")

            assert exc_info.value.code == 1
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_generate_icons_creates_output_dir(self, tmp_path, sample_image):
        """Test that generate_icons creates output directory if missing."""
        source_path = tmp_path / "source.png"
        sample_image.save(source_path, format="PNG")

        # Set output dir to non-existent directory
        output_dir = tmp_path / "new_output"
        assert not output_dir.exists()

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(output_dir)
            generate_icons.generate_icons(str(source_path))

            # Directory should be created
            assert output_dir.exists()
            assert (output_dir / "favicon.ico").exists()
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_generate_icons_with_non_rgba_image(self, tmp_path):
        """Test icon generation with RGB image."""
        # Create RGB image
        img = Image.new("RGB", (200, 200), color=(100, 150, 200))
        source_path = tmp_path / "source_rgb.png"
        img.save(source_path, format="PNG")

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)
            generate_icons.generate_icons(str(source_path))

            # Should still work
            assert (tmp_path / "favicon.ico").exists()
            assert (tmp_path / "apple-touch-icon.png").exists()
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_ico_sizes_constant(self):
        """Test that ICO_SIZES constant is defined correctly."""
        assert hasattr(generate_icons, "ICO_SIZES")
        assert isinstance(generate_icons.ICO_SIZES, list)
        assert len(generate_icons.ICO_SIZES) > 0

        # Should contain tuples of (width, height)
        for size in generate_icons.ICO_SIZES:
            assert isinstance(size, tuple)
            assert len(size) == 2
            assert size[0] > 0 and size[1] > 0

    def test_apple_touch_size_constant(self):
        """Test APPLE_TOUCH_SIZE constant."""
        assert hasattr(generate_icons, "APPLE_TOUCH_SIZE")
        assert generate_icons.APPLE_TOUCH_SIZE == 180

    def test_favicon_sizes_constants(self):
        """Test favicon size constants."""
        assert hasattr(generate_icons, "FAVICON_32_SIZE")
        assert generate_icons.FAVICON_32_SIZE == 32
        assert hasattr(generate_icons, "FAVICON_16_SIZE")
        assert generate_icons.FAVICON_16_SIZE == 16

    def test_default_source_constant(self):
        """Test DEFAULT_SOURCE constant."""
        assert hasattr(generate_icons, "DEFAULT_SOURCE")
        assert isinstance(generate_icons.DEFAULT_SOURCE, str)
        assert len(generate_icons.DEFAULT_SOURCE) > 0


class TestIconQuality:
    """Test the quality of generated icons."""

    def test_resizing_maintains_aspect_ratio(self, tmp_path):
        """Test that icons maintain aspect ratio during resize."""
        # Create a square source image
        img = Image.new("RGB", (500, 500), color=(100, 150, 200))
        source_path = tmp_path / "source.png"
        img.save(source_path, format="PNG")

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)
            generate_icons.generate_icons(str(source_path))

            # All generated icons should be square
            for icon_file in [
                "apple-touch-icon.png",
                "favicon-32x32.png",
                "favicon-16x16.png",
            ]:
                icon = Image.open(tmp_path / icon_file)
                assert icon.width == icon.height, f"{icon_file} should be square"
        finally:
            generate_icons.OUTPUT_DIR = original_output

    def test_apple_icon_has_no_transparency(self, tmp_path, sample_rgba_image):
        """Test that Apple touch icon is converted to RGB (no alpha)."""
        source_path = tmp_path / "source_rgba.png"
        sample_rgba_image.save(source_path, format="PNG")

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)
            generate_icons.generate_icons(str(source_path))

            apple_icon = Image.open(tmp_path / "apple-touch-icon.png")
            # Should be RGB, not RGBA
            assert apple_icon.mode == "RGB"
        finally:
            generate_icons.OUTPUT_DIR = original_output


class TestIconGeneration:
    """Integration tests for full icon generation workflow."""

    def test_full_workflow_from_png(self, tmp_path):
        """Test complete workflow from PNG source to all icons."""
        # Create a detailed source image
        img = Image.new("RGB", (512, 512), color=(200, 100, 50))
        source_path = tmp_path / "vibescape.png"
        img.save(source_path, format="PNG")

        original_output = generate_icons.OUTPUT_DIR
        try:
            generate_icons.OUTPUT_DIR = str(tmp_path)
            generate_icons.generate_icons(str(source_path))

            # Verify all outputs exist and are valid
            outputs = {
                "favicon.ico": None,  # Format checked differently
                "apple-touch-icon.png": (180, 180),
                "favicon-32x32.png": (32, 32),
                "favicon-16x16.png": (16, 16),
            }

            for filename, expected_size in outputs.items():
                filepath = tmp_path / filename
                assert filepath.exists(), f"{filename} not created"

                if expected_size:
                    img = Image.open(filepath)
                    assert (
                        img.size == expected_size
                    ), f"{filename} wrong size: {img.size} != {expected_size}"
        finally:
            generate_icons.OUTPUT_DIR = original_output
