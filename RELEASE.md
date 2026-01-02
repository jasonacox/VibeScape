# VibeScape Release Notes


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
