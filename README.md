# VibeScape

[![Backend Tests](https://github.com/jasonacox/VibeScape/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/jasonacox/VibeScape/actions/workflows/backend-tests.yml)
[![tvOS Build](https://github.com/jasonacox/VibeScape/actions/workflows/tvos-build.yml/badge.svg)](https://github.com/jasonacox/VibeScape/actions/workflows/tvos-build.yml)

## AI Powered Seasonal Dreams

An always-on ambient generative art experience that creates seasonal imagery to match the time of year. VibeScape automatically generates beautiful, themed scenes that evolve throughout the year — from cozy winter landscapes and festive holiday celebrations to vibrant spring gardens and warm summer sunsets.

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/f4f3d637-e569-42bb-aa47-c923247ce32e" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

## Features

- **11 Seasonal Themes** - Winter, Spring, Summer, Fall, Christmas, New Year's, Valentine's Day, Easter, Fourth of July, Halloween, and Thanksgiving
- **Intelligent Blending** - Smooth transitions between seasons with configurable ramp-up periods for holidays
- **Smart Prompts** - Each season has curated scene keywords and extras for varied, high-quality imagery
- **Date-Aware** - New Year's prompts include the correct year, holiday themes activate on schedule
- **Simple UI** - Maximizes each generated scene for impact, shows the prompt, auto-refreshes at configurable intervals
- **Startup Cache** - Pre-generates an image on startup for instant first view
- **Dual Providers** - Works with SwarmUI or OpenAI-compatible image generation APIs
- **Apple TV App** - Native tvOS client for displaying VibeScape on Apple TV (see [tvos/README.md](tvos/README.md))

## Quick Start

VibeScape uses either a locally hosted SwarmUI installation or an OpenAI image-gen API compatible endpoint. Use these simple docker commands to pull the engine and get it started.

**SwarmUI Option**

```bash
docker run --network host \
	-e IMAGE_PROVIDER=swarmui \
	-e SWARMUI="http://localhost:7801" \
	-e IMAGE_MODEL="Flux/flux1-schnell-fp8" \
	-e IMAGE_CFGSCALE="1.0" \
	-e IMAGE_STEPS="6" \
	jasonacox/vibescape:latest
```

**OpenAI Option**

```bash
docker run -p 4002:4002 \
	-e IMAGE_PROVIDER=openai \
	-e OPENAI_IMAGE_API_KEY="sk-..." \
	-e OPENAI_IMAGE_API_BASE="https://api.openai.com/v1" \
	-e OPENAI_IMAGE_MODEL="dall-e-3" \
	-e OPENAI_IMAGE_SIZE="1024x1024" \
	jasonacox/vibescape:latest
```

**Run as Service**

See the [server.sh](./server.sh) script to see how to run this as a service.

## Seasonal Configuration

VibeScape uses a configuration-based approach for seasonal transitions. Edit `seasonal_config.py` to customize:

- When each season/holiday becomes active
- Transition periods and ramp-up speeds
- Exact weight percentages for blending multiple themes

Example configuration for Halloween:
```python
(10, 25): {"fall": 0.85, "halloween": 0.15},  # Week before, 15% Halloween
(10, 28): {"fall": 0.60, "halloween": 0.40},  # 3 days before, 40% Halloween
(10, 30): {"fall": 0.30, "halloween": 0.70},  # Day before, 70% Halloween
(10, 31): {"halloween": 1.0},                  # Halloween Day - 100%
(11, 1): {"fall": 1.0},                        # Back to Fall
```

The blender automatically interpolates between key dates for smooth daily transitions.

## API Endpoints

- `/` - Main UI (auto-refreshing image viewer)
- `/image` - JSON: generates/returns new scene (instant response with cached image, generation happens in background)
- `/image/status` - JSON: lightweight status check (~100 bytes) returns `{available, timestamp, age_seconds}` to check if new image is ready without downloading full payload
- `/season` - JSON: current active seasons and weights
- `/stats` - JSON: usage statistics including generation times, success/failure counts, and cache status
- `/health` - Health check
- `/version` - Version and provider info

### Performance Features

**Non-Blocking Architecture**: The server returns cached images immediately while generating new ones in the background. This ensures every request gets an instant response, even during 5-15+ second image generation times.

**Background Generation**: When a cached image expires its TTL (default 60 seconds), the server immediately returns the old image while triggering background generation of a new one. The next request will get the fresh image.

**Startup Cache**: Initial image generation happens in the background during server startup, allowing the UI to be served immediately without waiting.

**Failure Tracking**: The `/stats` endpoint includes `images_failed` counter to help with operational monitoring of the generation backend.

**Bandwidth Optimization**: The `/image/status` endpoint provides a lightweight (~100 bytes) way to check if a new image is available without downloading the full payload (1-2MB). Clients poll this endpoint frequently and only fetch `/image` when the timestamp changes, reducing bandwidth by ~99% during idle periods.

## Timezone Configuration

VibeScape uses timezone-aware date calculations to ensure seasonal transitions happen at the correct local time, even if the server is running in a different timezone (e.g., UTC/GMT).

```bash
# Default: America/Los_Angeles (PST/PDT)
python3 server.py

# Use Eastern time
TIMEZONE="America/New_York" python3 server.py

# Use UTC
TIMEZONE="UTC" python3 server.py
```

Valid timezone identifiers: any from the [IANA timezone database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) (e.g., `America/Chicago`, `Europe/London`, `Asia/Tokyo`).

## Local Development

Quick steps to run the project locally for development:

```bash
# clone the repo
git clone https://github.com/jasonacox/VibeScape.git
cd VibeScape

# create and activate a virtualenv (macOS / Linux)
python3 -m venv .venv
source .venv/bin/activate

# upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# set providers and run the server (example using local SwarmUI)
export IMAGE_PROVIDER=swarmui
export SWARMUI="http://localhost:7801"
export REFRESH_SECONDS=60
./run_local_server.sh

# or run directly
# python3 server.py
```

### Environment Variables

**Server Settings:**
- `PORT` - HTTP port (default: 4002)
- `REFRESH_SECONDS` - Minimum seconds between image generations (default: 60)
- `POLL_INTERVAL` - Client poll frequency in seconds (default: 10)
- `IMAGE_TIMEOUT` - Generation timeout in seconds (default: 300)
- `IMAGE_PROVIDER` - "swarmui" (default) or "openai"
- `DATE` - Date override for testing seasons (format: YYYY-MM-DD or MM-DD)
- `TIMEZONE` - Timezone for date calculations (default: America/Los_Angeles)
- `DEBUG` - Enable debug logging (default: false, set to "true" for verbose logs)
- `ENABLE_DOCS` - Enable FastAPI documentation endpoints (default: false, set to "true" for /docs and /redoc)

**SwarmUI Settings:**
- `SWARMUI` - SwarmUI API base URL (default: http://localhost:7801)
- `IMAGE_MODEL` - Model name (default: Flux/flux1-schnell-fp8)
- `IMAGE_CFGSCALE` - CFG scale (default: 1.0)
- `IMAGE_STEPS` - Generation steps (default: 6)
- `IMAGE_WIDTH` - Image width (default: 1280)
- `IMAGE_HEIGHT` - Image height (default: 720)

**OpenAI Settings:**
- `OPENAI_IMAGE_API_KEY` - OpenAI API key (required for openai provider)
- `OPENAI_IMAGE_API_BASE` - API base URL (default: https://api.openai.com/v1)
- `OPENAI_IMAGE_MODEL` - Model name (default: dall-e-3)
- `OPENAI_IMAGE_SIZE` - Image size (default: 1024x1024)

### Testing Seasons

Use the `DATE` environment variable to test different seasons and holidays throughout the year:

```bash
# Test Halloween (October 31)
DATE=10-31 python3 server.py

# Test Christmas Eve with specific year
DATE=2025-12-24 python3 server.py

# Test Valentine's Day
DATE=02-14 python3 server.py

# Test Fourth of July
DATE=07-04 python3 server.py
```

The DATE override supports two formats:
- `MM-DD` - Uses current year
- `YYYY-MM-DD` - Specific date with year

## Project Structure

```
VibeScape/
├── seasons/              # Seasonal theme modules
│   ├── base.py          # Abstract base class for seasons
│   ├── christmas.py     # Christmas theme (preserved original logic)
│   ├── winter.py        # Winter scenes
│   ├── new_years.py     # New Year's celebrations (with year support)
│   ├── spring.py        # Spring awakening
│   ├── summer.py        # Summer vacation vibes
│   ├── fall.py          # Autumn colors
│   ├── thanksgiving.py  # Thanksgiving feast
│   ├── halloween.py     # Spooky Halloween
│   ├── easter.py        # Easter celebrations
│   ├── fourth_july.py   # Independence Day
│   └── valentines.py    # Valentine's Day romance
├── blender.py           # Seasonal weight calculation and interpolation
├── seasonal_config.py   # Configuration table with key dates and weights
├── server.py            # FastAPI web server
├── Dockerfile           # Multi-arch container build
└── requirements.txt     # Python dependencies
```

## Contributing

Ideas, fixes, and improvements are welcome! Fork the repo, make your changes, and open a pull request. Contributions could include:

- New seasonal themes or sub-themes
- Enhanced scene prompts for existing seasons
- UI improvements
- Additional image provider integrations
- Documentation improvements

## Share

Feel free to share your favorite generated scenes in our [Discussions](https://github.com/jasonacox/VibeScape/discussions) forum!

## Gallery

Example sampling of generated images.

### Christmas

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/84170fc8-bf76-4cb2-b754-9ca8147ec45f" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/623261c4-9d6b-4dc1-86a7-44b9eb6d2582" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/83f2db5a-f2c7-41fb-9fa1-1f44cf32c527" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/8cdfc88f-3a58-4a06-b12c-2b851320f115" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/8105055a-6935-4467-a93a-a4699645b6bf" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/c90e3f89-604d-470f-ae22-038f3f95844d" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/bccecb03-58d6-4442-a988-2fd27f78808d" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/c88c1533-3944-40f6-bd02-67a802a3fa73" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/1ea366e0-836c-437b-bfe9-7189651b608f" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/070f5de8-9ac1-418f-9713-8cc8cc59b1cb" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

### New Years 

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/ab0962c8-6b6e-42d4-aa8f-e21205daca25" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/e69f334f-ee18-4871-bc46-7d9366cbc00c" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/b53a1c29-ab7a-4aac-8eb9-8900c05a2149" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/2acf467b-d9e6-487d-96e6-2057ef1dd592" />

### Winter

<img width="400" alt="image" src="https://github.com/user-attachments/assets/5c4a69de-0223-43df-856e-7696c675485a" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/bb3509e0-d534-4aa4-a9b7-040ace3904fc" />

### Valentine's Day

<img width="400" alt="image" src="https://github.com/user-attachments/assets/d065d0ab-02c2-43e9-af6b-857849b1c103" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/775f6eca-1ba5-430d-81a9-71abb2879872" />

### Spring

<img width="400" alt="image" src="https://github.com/user-attachments/assets/a900a35b-16a4-4d1d-9fee-5cfc01e0038e" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/e7e28b7d-0217-4daf-8df1-be418c068707" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/0bb7e162-f852-4e98-a9fa-c150ab5143a4" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/6973d0f7-b8a3-47ab-a557-413316ecd415" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/7c1f7323-04d5-4dd6-9f7f-83cd61b9f620" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/61f9f130-5d8c-4c1d-86f3-e98ae6dd5e17" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/c22b3345-594e-4946-bc87-d0b0266b0dbb" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/29951d82-efd5-4c7e-b71e-0b7329899777" />


### Easter

<img width="400" alt="image" src="https://github.com/user-attachments/assets/7552da5d-2ac0-4f95-b7cb-c0da3fd2ebc4" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/d62943e9-d997-46ad-8e02-8c755a1ad049" />


### Summer

<img width="400" alt="image" src="https://github.com/user-attachments/assets/47006e85-e554-4db1-9051-61942f03a314" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/50ba0ec0-430c-45d3-86bd-88839988590a" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/8d5b10d2-7eba-4f5b-9aed-6d168dbb3245" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/a1a99e3f-ff31-4fff-930a-3a8147d025d8" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/d48a565f-d923-46b6-bea0-b9400b5655e4" />


### Fourth of July

<img width="400" alt="image" src="https://github.com/user-attachments/assets/af09c0d9-3dd5-4873-9365-b8ad09837731" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/2a6eb934-767c-4435-a07c-e1b27540e161" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/49fb45a6-97ab-4628-902f-ca585c638079" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/f0760ddd-5def-4d25-a295-f7bc15b2f4c3" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/f90e6357-f243-4617-ba5b-320fa42d071f" />


### Fall

<img width="400" alt="image" src="https://github.com/user-attachments/assets/256cc516-ac69-494b-8aaa-bab7a6ec9f7b" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/d9e4696e-500a-49fb-9600-d2574e5578a2" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/69b9f048-c28e-408a-b016-0b65e85edba7" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/ab911d96-ddc3-458b-8970-7cbb14075f29" />


### Halloween

<img width="400" alt="image" src="https://github.com/user-attachments/assets/b275cd49-9221-4304-a003-a8cc830bcd3f" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/db3fd850-afde-4324-a54d-b0adfb77387d" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/289fff16-d5e3-4970-b7e5-42a418ec4e34" />


### Thanksgiving

<img width="400" alt="image" src="https://github.com/user-attachments/assets/2698848c-5dd6-4228-859e-34b9d26c278a" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/13469476-9e25-47a2-b3f6-7ca33d0b031f" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/5ccf97dc-f41e-480d-8969-0936fe42ee1c" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/b02a5be4-9f50-497b-9db9-152f26cd340d" />

<img width="400" alt="image" src="https://github.com/user-attachments/assets/3d4f270b-867e-4215-acf4-411034bd0382" />
