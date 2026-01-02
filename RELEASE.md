# VibeScape Release Notes


## Version 1.0.6 (2026-01-02)

### Bug Fixes
- **Improved Web Client Polling**: Fixed unreliable polling in web UI that caused missed image updates
  - Replaced `setInterval` with chained `setTimeout` to prevent drift and stacking during slow network conditions
  - Fixed timestamp tracking to use response timestamp instead of status timestamp
  - Added visibility change handler to immediately poll when browser tab becomes active (browsers throttle intervals in background tabs)
- **Static Icon Loading**: Server now loads pre-generated icons from `static/` directory instead of generating at startup
  - Added `generate_icons.py` script to create favicon.ico, apple-touch-icon.png, and favicon-32x32.png from source image
  - Falls back to generated landscape icons if static files are missing

### Build Improvements
- **Docker Image Size Reduction**: Dockerfile now copies only required server files, excluding tvOS app, images, and documentation

---

## Version 1.0.5 (2026-01-02)

### Bandwidth Optimization
- **New `/image/status` Endpoint**: Lightweight status check (~100 bytes) returns image availability and timestamp without full payload
- **Smart Client Polling**: Web UI and tvOS app now check status first, only downloading full image when timestamp changes
- **Bandwidth Reduction**: ~99% reduction in network traffic during idle periods (1-2MB image vs 100 byte status check)
- **Timestamp Tracking**: Added `timestamp` field to `/image` response for client-side change detection

### UI Improvements
- **Full-Screen Image Display**: Web UI now scales images to fill browser viewport while maintaining aspect ratio using `object-fit: contain`
- **tvOS Error Handling**: Error messages only display when no cached image exists, providing graceful degradation during server restarts

### API Changes
- **Breaking**: `/image` response now includes `timestamp` field (existing clients may need updates)
- **New endpoint**: `GET /image/status` returns `{available: bool, timestamp: float, age_seconds: float}`
- **Optional fields**: `image_data` and `prompt` in `/image` response are now nullable for placeholder states

### Client Updates
- Web UI implements status polling with timestamp comparison
- tvOS app implements status polling with graceful error handling
- Both clients maintain last known timestamp to avoid redundant downloads

### New: Apple TV (tvOS) App
- **First Release**: Native tvOS client application for Apple TV
- **Full-Screen Display**: Optimized for television viewing with automatic scaling
- **Smart Polling**: Uses `/image/status` endpoint for bandwidth-efficient updates
- **Configurable Server**: Built-in settings to point to any VibeScape server instance
- **Graceful Fallback**: Displays last known image during server restarts or network issues
- **Auto-Refresh**: Continuous polling for new seasonal content
- See [tvos/README.md](tvos/README.md) for build and installation instructions

---

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
