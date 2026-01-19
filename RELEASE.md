# VibeScape Release Notes


## Version 1.0.11 (2026-01-14)

### Major Prompt Variation Enhancement
- **Dramatically Increased Image Uniqueness**: Completely redesigned prompt generation system to eliminate repetitive images
  - **Variable Extras**: Changed from fixed 2 extras to dynamic 1-3 extras (30% → 1 extra, 50% → 2 extras, 20% → 3 extras)
  - **Enhanced Style Variation**: Increased alternate artistic style probability from 20% → 50% for more visual diversity
  - **Expanded Style Library**: Added 6 new artistic styles (Impressionist, Digital art, Anime, Fantasy, Minimalist, Moody photography) bringing total to 10 alternate styles
  - **New Modifier Systems**: Added three new randomized modifier categories:
    - Time of Day (40% chance): 13 options including golden hour, blue hour, sunrise, sunset, dawn, dusk, midday, various light conditions
    - Atmospheric Conditions (30% chance): 10 options including dramatic clouds, mist, fog, volumetric lighting, god rays, lens flare
    - Composition Styles (25% chance): 10 options including wide angle, aerial view, rule of thirds, depth of field emphasis
  - **Randomized Modifier Order**: Shuffles order of extras and modifiers for additional structural variation
  - **Mathematical Impact**: Increased unique combinations from hundreds to millions - virtually guarantees no duplicate images

### Content Expansion
- **Winter Season Enhancement**: Significantly expanded content pools
  - Added 20 new scene keywords (50 total, was 30) including alpine villages, ice caves, northern lights, frozen harbors, snowy owls
  - Added 10 new extras (26 total, was 16) including sparkling ice crystals, chimney smoke, crunchy snow texture, bare tree silhouettes
  - +67% more scene variety, +63% more atmospheric elements
  
- **Christmas Season Enhancement**: Major content expansion
  - Added 21 new scene keywords (51 total, was 30) including stockings, gingerbread houses, advent calendars, nutcrackers, poinsettias
  - Added 6 new extras (19 total, was 13) including twinkling lights, pine scents, ribbons, candy canes, holly and mistletoe
  - +70% more scene variety, +46% more festive elements
  - Maintained guaranteed "festive atmosphere" suffix for consistent holiday theming

### Testing & Quality
- Updated all test suites to reflect new variation system expectations
- Verified 100% unique prompts in validation testing (25+ consecutive generations)
- All 321+ tests passing with enhanced variation logic

---

## Version 1.0.9 (2026-01-08)

### Bug Fixes
- **Peak Viewer Count Tracking**: Fixed `MAX_CONNECTED_VIEWERS` not updating when sessions are tracked via `/image` endpoint
  - Previously only `/connect` endpoint updated the peak viewer count
  - Clients calling `/image` directly would increase current viewers but peak would remain stale
  - Now both `/image` and `/connect` endpoints properly track and update peak viewer statistics

### Prompt Improvements
- **No Signature Directive**: Added "no signature, no text" instructions to alternate artistic styles
  - Prevents AI models from hallucinating an artist signature or text overlays on illustrated/painted style images
  - Applies to all 4 alternate styles: watercolor, vintage postcard, oil painting, and children's book illustration
  - Ensures clean, signature-free images in the 20% of generations that use alternate artistic styles

### Content Enhancements
- **Rainy Season Content**: Significantly expanded Spring season with comprehensive rain-themed scenes and atmosphere
  - Added 15 new rain-focused scene keywords: rain on flowers, puddle reflections, cozy rainy interiors, spring storms, misty mornings
  - Added 10 new rain-related extras: gentle rain, water droplets, misty atmosphere, reflections, glistening wetness, storm clouds, rainbows, petrichor
  - Spring season (March-May) now authentically captures the rainy season with "April showers" aesthetic
  - Rain scenes naturally blend with blooming flowers and renewal themes for complete seasonal experience

---

## Version 1.0.8 (2026-01-03)

### Image Quality Improvements
- **Automatic Letterbox Removal**: Server now intelligently detects and removes black letterbox bars from generated images
  - Smart detection algorithm checks for uniform darkness and low variance to distinguish letterbox bars from legitimate dark content
  - Only scans top and bottom 10% of image to avoid false positives
  - Requires minimum 10-pixel bar height to trigger cropping
  - Logs detection: "Detected letterbox bars: top=X, bottom=Y pixels"
  - Applies to both SwarmUI and OpenAI generated images
  - Typical removal: 5-10% of image height when letterbox bars are present

---

## Version 1.0.7 (2026-01-02)

### Image Display Improvements
- **Full-Screen Coverage**: Both web client and tvOS app now fill the entire screen without black bars while maintaining image aspect ratio
  - Web client: Changed CSS `object-fit` from `contain` to `cover` for edge-to-edge display
  - tvOS app: Changed SwiftUI `aspectRatio` from `.fit` to `.fill` with `.clipped()` modifier
  - Images now scale uniformly (maintaining x/y ratio) to completely cover viewport, cropping overflow rather than letterboxing/pillarboxing

---

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
