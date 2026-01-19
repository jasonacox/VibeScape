"""
Pytest configuration and shared fixtures for VibeScape tests.
"""
import io
import base64
import os
import sys
from datetime import date, datetime
from typing import Generator
from unittest.mock import Mock, AsyncMock

import pytest
from PIL import Image
from fastapi.testclient import TestClient
from freezegun import freeze_time

# Ensure the project root is in the path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture
def clean_env(monkeypatch):
    """Clean environment for testing - removes all VibeScape env vars."""
    env_vars = [
        "PORT",
        "SWARMUI",
        "IMAGE_MODEL",
        "IMAGE_CFGSCALE",
        "IMAGE_STEPS",
        "IMAGE_WIDTH",
        "IMAGE_HEIGHT",
        "IMAGE_SEED",
        "IMAGE_TIMEOUT",
        "IMAGE_PROVIDER",
        "OPENAI_IMAGE_API_KEY",
        "OPENAI_IMAGE_API_BASE",
        "OPENAI_IMAGE_MODEL",
        "OPENAI_IMAGE_SIZE",
        "REFRESH_SECONDS",
        "POLL_INTERVAL",
        "DATE",
        "ENABLE_DOCS",
        "TIMEZONE",
        "DEBUG",
    ]
    for var in env_vars:
        monkeypatch.delenv(var, raising=False)
    return monkeypatch


@pytest.fixture
def mock_env(clean_env):
    """Set up a mock environment with default test values."""
    clean_env.setenv("PORT", "4002")
    clean_env.setenv("SWARMUI", "http://localhost:7801")
    clean_env.setenv("IMAGE_MODEL", "test-model")
    clean_env.setenv("REFRESH_SECONDS", "60")
    clean_env.setenv("IMAGE_PROVIDER", "swarmui")
    clean_env.setenv("ENABLE_DOCS", "false")
    return clean_env


@pytest.fixture
def sample_image() -> Image.Image:
    """Generate a simple test PIL Image."""
    img = Image.new("RGB", (100, 100), color=(73, 109, 137))
    return img


@pytest.fixture
def sample_image_with_letterbox() -> Image.Image:
    """Generate a test image with letterbox bars (black bars top/bottom)."""
    img = Image.new("RGB", (100, 100), color=(73, 109, 137))
    # Add black bars on top and bottom
    for y in range(10):  # Top 10 pixels
        for x in range(100):
            img.putpixel((x, y), (0, 0, 0))
    for y in range(90, 100):  # Bottom 10 pixels
        for x in range(100):
            img.putpixel((x, y), (0, 0, 0))
    return img


@pytest.fixture
def sample_rgba_image() -> Image.Image:
    """Generate a test RGBA image."""
    img = Image.new("RGBA", (100, 100), color=(73, 109, 137, 255))
    return img


@pytest.fixture
def sample_base64_image(sample_image) -> str:
    """Convert sample image to base64 string."""
    buf = io.BytesIO()
    sample_image.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


@pytest.fixture
def sample_base64_data_uri(sample_base64_image) -> str:
    """Convert sample image to data URI format."""
    return f"data:image/jpeg;base64,{sample_base64_image}"


@pytest.fixture
def sample_png_bytes(sample_image) -> bytes:
    """Convert sample image to PNG bytes."""
    buf = io.BytesIO()
    sample_image.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def temp_static_dir(tmp_path, sample_png_bytes):
    """Create a temporary static directory with test icons."""
    static_dir = tmp_path / "static"
    static_dir.mkdir()

    # Create sample icon files
    (static_dir / "apple-touch-icon.png").write_bytes(sample_png_bytes)
    (static_dir / "favicon-32x32.png").write_bytes(sample_png_bytes)
    (static_dir / "favicon.ico").write_bytes(sample_png_bytes)

    return static_dir


@pytest.fixture
def mock_swarmui_response(sample_base64_image):
    """Mock SwarmUI API response structure."""
    return {
        "session_id": "test-session-123",
        "images": [f"data:image/jpeg;base64,{sample_base64_image}"],
    }


@pytest.fixture
def mock_openai_response(sample_base64_image):
    """Mock OpenAI API response structure."""
    return {"data": [{"b64_json": sample_base64_image}]}


@pytest.fixture
def frozen_christmas_date():
    """Freeze time to Christmas Day 2025."""
    with freeze_time("2025-12-25"):
        yield


@pytest.fixture
def frozen_halloween_date():
    """Freeze time to Halloween 2025."""
    with freeze_time("2025-10-31"):
        yield


@pytest.fixture
def frozen_july_fourth_date():
    """Freeze time to July 4th 2025."""
    with freeze_time("2025-07-04"):
        yield


@pytest.fixture
def frozen_new_years_date():
    """Freeze time to New Year's Day 2026."""
    with freeze_time("2026-01-01"):
        yield


@pytest.fixture
def season_blender():
    """Create a SeasonBlender instance for testing."""
    from blender import SeasonBlender

    return SeasonBlender()


@pytest.fixture
def mock_aiohttp_session():
    """Mock aiohttp.ClientSession for testing."""
    mock = AsyncMock()
    mock.post = AsyncMock()
    mock.get = AsyncMock()
    return mock


@pytest.fixture
def mock_aiohttp_response(sample_base64_image):
    """Mock aiohttp response object."""
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(
        return_value={
            "session_id": "test-session-123",
            "images": [f"data:image/jpeg;base64,{sample_base64_image}"],
        }
    )
    return mock_resp


@pytest.fixture(autouse=False)
def reset_server_globals():
    """Reset server global variables between tests.

    Use this fixture explicitly in tests that modify server state.
    """
    import server

    # Save original values
    original_sessions = server.SESSIONS.copy()
    original_viewers = server.CONNECTED_VIEWERS
    original_max_viewers = server.MAX_CONNECTED_VIEWERS
    original_last_activity = server.LAST_ACTIVITY
    original_last_image = server.LAST_IMAGE
    original_last_image_time = server.LAST_IMAGE_TIME
    original_generation_in_progress = server.GENERATION_IN_PROGRESS
    original_images_generated = server.IMAGES_GENERATED
    original_images_failed = server.IMAGES_FAILED

    yield

    # Restore original values
    server.SESSIONS.clear()
    server.SESSIONS.update(original_sessions)
    server.CONNECTED_VIEWERS = original_viewers
    server.MAX_CONNECTED_VIEWERS = original_max_viewers
    server.LAST_ACTIVITY = original_last_activity
    server.LAST_IMAGE = original_last_image
    server.LAST_IMAGE_TIME = original_last_image_time
    server.GENERATION_IN_PROGRESS = original_generation_in_progress
    server.IMAGES_GENERATED = original_images_generated
    server.IMAGES_FAILED = original_images_failed


@pytest.fixture
def test_client(reset_server_globals):
    """Create a FastAPI TestClient for testing endpoints."""
    import server
    from fastapi.testclient import TestClient

    client = TestClient(server.app)
    return client
