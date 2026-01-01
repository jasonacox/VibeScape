# VibeScape

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
- `/image` - JSON: generates/returns new scene
- `/season` - JSON: current active seasons and weights
- `/stats` - JSON: usage statistics
- `/health` - Health check
- `/version` - Version and provider info

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
- `REFRESH_SECONDS` - Client poll interval (default: 60)
- `IMAGE_TIMEOUT` - Generation timeout in seconds (default: 300)
- `IMAGE_PROVIDER` - "swarmui" (default) or "openai"

**SwarmUI Settings:**
- `SWARMUI` - SwarmUI API base URL (default: http://localhost:7801)
- `IMAGE_MODEL` - Model name (default: Flux/flux1-schnell-fp8)
- `IMAGE_CFGSCALE` - CFG scale (default: 1.0)
- `IMAGE_STEPS` - Generation steps (default: 6)
- `IMAGE_WIDTH` - Image width (default: 1024)
- `IMAGE_HEIGHT` - Image height (default: 1024)

**OpenAI Settings:**
- `OPENAI_IMAGE_API_KEY` - OpenAI API key (required for openai provider)
- `OPENAI_IMAGE_API_BASE` - API base URL (default: https://api.openai.com/v1)
- `OPENAI_IMAGE_MODEL` - Model name (default: dall-e-3)
- `OPENAI_IMAGE_SIZE` - Image size (default: 1024x1024)

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

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/84170fc8-bf76-4cb2-b754-9ca8147ec45f" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/623261c4-9d6b-4dc1-86a7-44b9eb6d2582" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/ab0962c8-6b6e-42d4-aa8f-e21205daca25" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/e69f334f-ee18-4871-bc46-7d9366cbc00c" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/b53a1c29-ab7a-4aac-8eb9-8900c05a2149" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/83f2db5a-f2c7-41fb-9fa1-1f44cf32c527" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/8cdfc88f-3a58-4a06-b12c-2b851320f115" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/8105055a-6935-4467-a93a-a4699645b6bf" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/c90e3f89-604d-470f-ae22-038f3f95844d" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/bccecb03-58d6-4442-a988-2fd27f78808d" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/c88c1533-3944-40f6-bd02-67a802a3fa73" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/1ea366e0-836c-437b-bfe9-7189651b608f" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/070f5de8-9ac1-418f-9713-8cc8cc59b1cb" style="width:400px;height:400px;object-fit:cover;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.25);" />

