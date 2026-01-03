# VibeScape Test Suite

Comprehensive pytest test suite with 325+ tests achieving 75%+ code coverage.

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_blender.py

# Run specific test class
pytest tests/test_server.py::TestHealthEndpoint

# Run with verbose output
pytest -v

# Stop on first failure
pytest -x
```

## Test Organization

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_seasonal_config.py  # Seasonal weight configuration (35 tests)
├── test_blender.py          # SeasonBlender date interpolation (68 tests)
├── test_seasons_base.py     # Abstract base class (50 tests)
├── test_seasons_*.py        # Individual season modules (10 files, 100+ tests)
├── test_generate_icons.py   # Icon generation utilities (30 tests)
└── test_server.py           # FastAPI endpoints & server logic (100+ tests)
```

## Key Fixtures (conftest.py)

- `clean_env` - Clean environment variables for isolated tests
- `mock_env` - Pre-configured test environment
- `sample_image` - PIL Image for testing
- `sample_base64_image` - Base64-encoded image data
- `test_client` - FastAPI TestClient for endpoint testing
- `reset_server_globals` - Reset server state between tests
- `frozen_*_date` - Freeze time to specific dates with freezegun

## What's Tested

### Core Functionality (96-100% coverage)
- ✅ Seasonal weight interpolation and blending
- ✅ Date handling with PST/PDT timezone support
- ✅ All 11 season prompt generators
- ✅ Icon generation (ICO, PNG formats)
- ✅ Seasonal configuration validation

### Server (64% coverage)
- ✅ All 13 FastAPI endpoints
- ✅ Session management with LRU eviction
- ✅ Image caching and TTL logic
- ✅ Statistics tracking
- ✅ Health and version endpoints
- ⚠️ Async image generation (requires external APIs)
- ⚠️ Startup lifecycle and background tasks

## Test Approach

**Unit Tests**: Individual functions and classes tested in isolation with mocking for external dependencies (aiohttp, SwarmUI, OpenAI).

**Integration Tests**: FastAPI endpoints tested with TestClient to verify request/response handling.

**Async Testing**: pytest-asyncio handles async functions with `@pytest.mark.asyncio` decorator and `asyncio_mode=auto`.

**Date Testing**: freezegun freezes time for deterministic seasonal logic testing.

## Coverage Targets

- **Core libraries**: 95%+ (blender, seasons, icons, config)
- **Server endpoints**: 60%+ (async/startup code harder to test)
- **Overall**: 75%+

View detailed coverage: `open htmlcov/index.html`

## Common Test Patterns

### Testing Seasonal Logic
```python
from freezegun import freeze_time

def test_christmas_active():
    blender = SeasonBlender()
    with freeze_time("2026-12-25"):
        weights = blender.get_active_seasons()
        assert "christmas" in weights
```

### Testing Endpoints
```python
def test_health_endpoint(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
```

### Testing Async Functions
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

## Dependencies

Installed via `requirements.txt`:
- pytest >= 7.4.0
- pytest-asyncio >= 0.21.0
- pytest-cov >= 4.1.0
- pytest-mock >= 3.11.0
- httpx >= 0.24.0
- freezegun >= 1.2.0
