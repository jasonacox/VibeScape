# VibeScape Release Notes


## Version 1.0.4 (2026-01-01)

### Performance & Architecture Improvements
- **Non-Blocking Image Generation**: All image generation now happens in background tasks, providing instant HTTP responses even during 5-15+ second generation times
- **Background Generation Queue**: When cached image expires TTL, server immediately returns old image while triggering background generation of new one
- **Smart Cache Strategy**: Serves cached images instantly to all concurrent requests during active generation
- **Generation Lock**: Thread-safe `GENERATION_IN_PROGRESS` flag prevents duplicate concurrent generations

### Operational Monitoring
- **Failure Tracking**: Added `images_failed` counter to track generation errors and exceptions
- **Enhanced Stats**: `/stats` endpoint now includes failure count alongside success metrics for operational visibility
- **Statistics Consistency**: Both startup and background generation now update success/failure counters and timing metrics

### Configuration & Flexibility
- **Timezone Support**: Added `TIMEZONE` environment variable for timezone-aware date calculations (default: America/Los_Angeles)
- **Debug Logging**: Added `DEBUG` environment variable to enable debug-level logging for troubleshooting
- **Cross-Timezone Support**: Server correctly handles seasonal transitions based on configured timezone, even when hosted in different timezone (e.g., UTC/GMT)

### Technical Changes
- Timezone-aware date calculations in `blender.py` and `new_years.py` using Python's `zoneinfo`
- Refactored `/image` endpoint to use fire-and-forget background tasks for generation
- All generation paths (startup, background, endpoint) now consistently track metrics
- Improved error handling with failure counting in all generation contexts

---

## Version 1.0.3 (2026-01-01)

### Performance & User Experience Improvements
- **Non-Blocking Server Startup**: Initial image generation now runs in background task, allowing the splash page to display immediately upon server start instead of waiting 5-15+ seconds for first image generation
- **Instant Responsiveness**: Server accepts connections and serves UI immediately while preparing first cached image

### Security Improvements
- **API Documentation Disabled by Default**: FastAPI documentation endpoints (`/docs`, `/redoc`, `/openapi.json`) are now disabled in production for enhanced security. Enable with `ENABLE_DOCS=true` environment variable for development/testing.

---

## Version 1.0.2 (2026-01-01)

### Initial VibeScape Release
- **Rebranded from Christmas AI Dreams to VibeScape** - Year-round seasonal image generation
- **11 Seasonal Themes**: Christmas, Winter, New Year's, Spring, Summer, Fall, Thanksgiving, Fourth of July, Easter, Halloween, Valentine's Day
- **Intelligent Seasonal Blending**: Configuration-based weight system with linear interpolation between key dates
- **Dynamic Year Support**: New Year's prompts automatically include the correct year (current year on 1/1, next year before 1/1)
- **Configurable Transitions**: Easy-to-edit seasonal_config.py for precise control over holiday ramp-ups and transitions
- **Dual Image Providers**: Support for SwarmUI and OpenAI backends
- **Startup Image Cache**: Server pre-generates an image on startup for instant first view
- **Session Management**: Viewer tracking with automatic cleanup and LRU eviction
- **Modern UI**: Updated branding with landscape favicon, splash screen, and download functionality
- **API Endpoints**: `/season` endpoint to view active seasons and weights

### Technical Improvements
- Modular season architecture with SeasonBase abstract class
- Preserved original Christmas prompt generation logic
- Port changed to 4002 (default)
- Logging cleanup: Moved verbose logs to debug level
- Docker support with multi-architecture builds (amd64, arm64, arm/v7)

### Configuration
- SwarmUI default: `http://localhost:7801`
- Model: `Flux/flux1-schnell-fp8`
- Refresh interval: 60 seconds
- Image dimensions: 1024x1024

---

## Previous Versions

### v1.0.0-christmas
- Original Christmas AI Dreams release
- Single theme (Christmas only)
- SwarmUI integration
- Basic web UI with auto-refresh
