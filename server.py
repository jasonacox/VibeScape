#!/usr/bin/env python3
"""
VibeScape - AI-generated seasonal scene web service.

Serves a single-page UI that polls for new AI-generated seasonal scenes every
REFRESH_SECONDS. Supports SwarmUI and OpenAI image providers. Features viewer
tracking (pauses generation when no viewers connected), image caching, dynamic
favicon generation at startup, seasonal blending, and usage statistics.

Key Environment Variables:
  IMAGE_PROVIDER       - "swarmui" (default) or "openai"
  
  SwarmUI Settings:
    SWARMUI            - SwarmUI API base URL (default: http://localhost:7801)
    IMAGE_MODEL        - Model name (default: Flux/flux1-schnell-fp8)
    IMAGE_CFGSCALE     - CFG scale (default: 1.0)
    IMAGE_STEPS        - Generation steps (default: 6)
  
  OpenAI Settings:
    OPENAI_IMAGE_API_KEY    - OpenAI API key (required for openai provider)
    OPENAI_IMAGE_API_BASE   - API base URL (default: https://api.openai.com/v1)
    OPENAI_IMAGE_MODEL      - Model name (default: dall-e-3)
    OPENAI_IMAGE_SIZE       - Image size (default: 1024x1024)
  
  Server Settings:
    PORT               - HTTP port (default: 4002)
    REFRESH_SECONDS    - Minimum seconds between image generations (default: 60)
    POLL_INTERVAL      - Client poll frequency in seconds (default: 10)
    IMAGE_TIMEOUT      - Generation timeout in seconds (default: 300)
    DATE               - Date override for testing (format: YYYY-MM-DD or MM-DD)
    ENABLE_DOCS        - Enable FastAPI docs endpoints /docs and /redoc (default: false)

Usage:
  # SwarmUI example
  export SWARMUI="http://10.0.1.25:7801"
  export IMAGE_MODEL="Flux/flux1-schnell-fp8"
  python3 server.py

  # OpenAI example
  export IMAGE_PROVIDER="openai"
  export OPENAI_IMAGE_API_KEY="sk-..."
  python3 server.py

Endpoints:
  /                  - Main UI (auto-refreshing image viewer)
  /image             - JSON: generates/returns new scene (or cached if viewers=0)
  /stats             - JSON: usage stats (images generated, viewers, timing)
  /favicon.ico       - Multi-size ICO favicon (cached at startup)
  /apple-touch-icon.png - 180x180 PNG for iOS (cached at startup)
  /favicon-32x32.png - 32x32 PNG favicon (cached at startup)
  /health            - Health check
  /version           - Version and provider info
  /connect           - POST: register viewer connection
  /disconnect        - POST: unregister viewer
  /viewers           - GET: current viewer count

Author:
    Jason A. Cox
    github.com/jasonacox/VibeScape
    1 January 2026
"""
import io
import os
import sys
import random
import base64
import asyncio
import threading
import json
import uuid
import time
from collections import OrderedDict
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
import uvicorn

# Ensure chatbot package is importable when running from repo root
ROOT = os.path.dirname(os.path.abspath(__file__))
CHATBOT_PATH = os.path.join(ROOT, "chatbot")
if CHATBOT_PATH not in sys.path:
    sys.path.insert(0, CHATBOT_PATH)

import aiohttp
from PIL import Image, ImageDraw

# Import seasonal blender
from blender import SeasonBlender

# ── CONSTANTS ────────────────────────────────────────────────────────────────

# Icon sizes
ICON_SIZE_LARGE = 180
ICON_SIZE_SMALL = 32
ICON_CACHE_DURATION = 86400  # 1 day in seconds

# Session management
MAX_SESSIONS = 1000
SESSION_CLEANUP_INTERVAL = 60  # seconds

# Prompt validation
MAX_PROMPT_LENGTH = 500

# ── CONFIGURATION ────────────────────────────────────────────────────────────

# Configuration (environment overrides)
PORT = int(os.environ.get("PORT", 4002))
SWARMUI = os.environ.get("SWARMUI", "http://localhost:7801")
# Normalize SWARMUI: ensure a URL scheme is present so aiohttp requests succeed.
if SWARMUI and not SWARMUI.startswith("http://") and not SWARMUI.startswith("https://"):
    SWARMUI = "http://" + SWARMUI
IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "Flux/flux1-schnell-fp8")
IMAGE_CFGSCALE = float(os.environ.get("IMAGE_CFGSCALE", 1.0))
IMAGE_STEPS = int(os.environ.get("IMAGE_STEPS", 6))
IMAGE_WIDTH = int(os.environ.get("IMAGE_WIDTH", 1280)) # 1024
IMAGE_HEIGHT = int(os.environ.get("IMAGE_HEIGHT", 720)) # 1024
IMAGE_SEED = int(os.environ.get("IMAGE_SEED", -1))
IMAGE_TIMEOUT = int(os.environ.get("IMAGE_TIMEOUT", 300))
IMAGE_PROVIDER = os.environ.get("IMAGE_PROVIDER", "swarmui").lower()

# Server version
VERSION = "1.0.5"

# OpenAI image settings
OPENAI_IMAGE_API_KEY = os.environ.get("OPENAI_IMAGE_API_KEY", "")
OPENAI_IMAGE_API_BASE = os.environ.get("OPENAI_IMAGE_API_BASE", "https://api.openai.com/v1")
OPENAI_IMAGE_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "dall-e-3")
OPENAI_IMAGE_SIZE = os.environ.get("OPENAI_IMAGE_SIZE", "1024x1024")

# Default refresh interval in seconds - server rate-limits image generation to this interval
# (server won't generate a new image until at least this many seconds have passed)
DEFAULT_REFRESH = int(os.environ.get("REFRESH_SECONDS", "60"))

# Client poll interval - how often the browser checks for new images
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "10"))

# API documentation (disable in production for security)
ENABLE_DOCS = os.environ.get("ENABLE_DOCS", "false").lower() in ("true", "1", "yes")

# Create FastAPI app with conditional documentation
app = FastAPI(
    docs_url="/docs" if ENABLE_DOCS else None,
    redoc_url="/redoc" if ENABLE_DOCS else None,
    openapi_url="/openapi.json" if ENABLE_DOCS else None,
)

# Initialize seasonal blender
season_blender = SeasonBlender()

# Session state (sessions, viewers, activity) - single lock for all related state
SESSIONS: OrderedDict[str, float] = OrderedDict()
SESSION_TTL = 300  # 5 minutes in seconds
CONNECTED_VIEWERS = 0
MAX_CONNECTED_VIEWERS = 0
LAST_ACTIVITY = 0.0
SESSION_STATE_LOCK = threading.Lock()

# Image cache (last generated image and metadata)
LAST_IMAGE: dict | None = None
LAST_IMAGE_TIME: float | None = None
GENERATION_IN_PROGRESS = False
IMAGE_CACHE_LOCK = threading.Lock()

# In-memory cached icons (generated on startup, no lock needed for reads)
ICON_LOCK = threading.Lock()  # Only used during startup generation
APPLE_TOUCH_BYTES: bytes | None = None
FAVICON_32_BYTES: bytes | None = None
FAVICON_ICO_BYTES: bytes | None = None
# Stats (generation metrics)
IMAGES_GENERATED = 0
IMAGES_FAILED = 0
STATS_LOCK = threading.Lock()
# Generation time stats (seconds)
GEN_TIME_COUNT = 0
GEN_TIME_SUM = 0.0
GEN_TIME_MIN: float | None = None
GEN_TIME_MAX: float | None = None

# Logging
LOG_LEVEL = logging.DEBUG if os.environ.get("DEBUG", "").lower() in ("true", "1", "yes") else logging.INFO
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("vibescape_server")
logger.info("Starting VibeScape server - version %s", VERSION)
# Log effective configuration on startup (redact sensitive values)
try:
    config = {
        "PORT": PORT,
        "SWARMUI": SWARMUI,
        "IMAGE_PROVIDER": IMAGE_PROVIDER,
        "IMAGE_MODEL": IMAGE_MODEL,
        "IMAGE_CFGSCALE": IMAGE_CFGSCALE,
        "IMAGE_STEPS": IMAGE_STEPS,
        "IMAGE_WIDTH": IMAGE_WIDTH,
        "IMAGE_HEIGHT": IMAGE_HEIGHT,
        "IMAGE_SEED": IMAGE_SEED,
        "IMAGE_TIMEOUT": IMAGE_TIMEOUT,
        "REFRESH_SECONDS": DEFAULT_REFRESH,
        "OPENAI_IMAGE_API_BASE": OPENAI_IMAGE_API_BASE,
        "OPENAI_IMAGE_MODEL": OPENAI_IMAGE_MODEL,
        "OPENAI_IMAGE_SIZE": OPENAI_IMAGE_SIZE,
        # Do not log secret values — only indicate presence
        "OPENAI_IMAGE_API_KEY": ("SET" if OPENAI_IMAGE_API_KEY else "NOT SET"),
    }
    logger.info("Effective configuration:\n%s", "\n".join(f"{k}: {v}" for k, v in config.items()))
except Exception:
    logger.exception("Failed to log configuration")


@asynccontextmanager
async def _lifespan(app):
    logger.info("Application startup — generating cached assets and ready to serve requests.")
    
    # Background task to clean up stale sessions
    async def _cleanup_sessions():
        while True:
            try:
                await asyncio.sleep(SESSION_CLEANUP_INTERVAL)
                now = time.time()
                with SESSION_STATE_LOCK:
                    stale = [sid for sid, last_seen in SESSIONS.items() if now - last_seen > SESSION_TTL]
                    for sid in stale:
                        del SESSIONS[sid]
                    if stale:
                        logger.info("Cleaned up %d stale sessions (TTL=%ds)", len(stale), SESSION_TTL)
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Error in session cleanup task")
    
    cleanup_task = asyncio.create_task(_cleanup_sessions())
    
    # Generate and cache small PNG icons to avoid regenerating on each request
    try:
        def _make_landscape_icon(size: int) -> Image.Image:
            """Create a simple landscape icon representing VibeScape."""
            im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(im)
            
            # Sky gradient (upper 60%)
            sky_height = int(size * 0.6)
            for y in range(sky_height):
                # Gradient from light blue to deeper blue
                ratio = y / sky_height
                r = int(135 + (70 - 135) * ratio)
                g = int(206 + (130 - 206) * ratio)
                b = int(235 + (180 - 235) * ratio)
                draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
            
            # Ground (lower 40%)
            ground_color = (76, 187, 23, 255)  # Green
            draw.rectangle((0, sky_height, size, size), fill=ground_color)
            
            # Sun in top right
            sun_r = int(size * 0.12)
            sun_x = int(size * 0.75)
            sun_y = int(size * 0.25)
            draw.ellipse((sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r), 
                        fill=(255, 220, 100, 255))
            
            # Mountains (simple triangles)
            mountain_color = (100, 100, 120, 255)
            # Left mountain
            draw.polygon([
                (0, sky_height),
                (int(size * 0.35), int(size * 0.35)),
                (int(size * 0.55), sky_height)
            ], fill=mountain_color)
            # Right mountain
            draw.polygon([
                (int(size * 0.45), sky_height),
                (int(size * 0.70), int(size * 0.25)),
                (size, sky_height)
            ], fill=mountain_color)
            
            return im

        def _png_bytes_from_image(img: Image.Image) -> bytes:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()

        # Build and cache the common sizes (PNG + multi-size ICO)
        global APPLE_TOUCH_BYTES, FAVICON_32_BYTES, FAVICON_ICO_BYTES
        with ICON_LOCK:
            try:
                if APPLE_TOUCH_BYTES is None:
                    APPLE_TOUCH_BYTES = _png_bytes_from_image(_make_landscape_icon(ICON_SIZE_LARGE))
                if FAVICON_32_BYTES is None:
                    FAVICON_32_BYTES = _png_bytes_from_image(_make_landscape_icon(ICON_SIZE_SMALL))
                if FAVICON_ICO_BYTES is None:
                    # Create ICO containing several sizes
                    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                    max_size = max(s[0] for s in sizes)
                    base = _make_landscape_icon(max_size)
                    buf = io.BytesIO()
                    base.save(buf, format="ICO", sizes=sizes)
                    FAVICON_ICO_BYTES = buf.getvalue()
            except Exception:
                logger.exception("Failed to generate cached icons at startup")
    except Exception:
        logger.exception("Unexpected error during startup icon generation")
    
    # Generate initial image in background (don't block server startup)
    async def _generate_initial_image():
        global LAST_IMAGE, LAST_IMAGE_TIME
        global IMAGES_GENERATED, IMAGES_FAILED, GEN_TIME_COUNT, GEN_TIME_SUM, GEN_TIME_MIN, GEN_TIME_MAX
        try:
            logger.info("Generating initial image for cache...")
            loop = asyncio.get_running_loop()
            t0 = loop.time()
            initial_result = await generate_scene()
            elapsed = loop.time() - t0
            
            if "error" not in initial_result:
                # Update stats
                try:
                    with STATS_LOCK:
                        IMAGES_GENERATED += 1
                        GEN_TIME_COUNT += 1
                        GEN_TIME_SUM += elapsed
                        if GEN_TIME_MIN is None or elapsed < GEN_TIME_MIN:
                            GEN_TIME_MIN = elapsed
                        if GEN_TIME_MAX is None or elapsed > GEN_TIME_MAX:
                            GEN_TIME_MAX = elapsed
                except Exception:
                    logger.exception("Failed to update generation stats")
                
                with IMAGE_CACHE_LOCK:
                    LAST_IMAGE = initial_result
                    LAST_IMAGE_TIME = time.time()
                logger.info("Successfully generated and cached initial image")
            else:
                # Count failure
                try:
                    with STATS_LOCK:
                        IMAGES_FAILED += 1
                except Exception:
                    logger.exception("Failed to update failure stats")
                logger.warning("Failed to generate initial image: %s", initial_result.get("error"))
        except Exception:
            # Count exception as failure
            try:
                with STATS_LOCK:
                    IMAGES_FAILED += 1
            except Exception:
                pass
            logger.exception("Failed to generate initial image at startup")
    
    # Start background task for initial image generation
    initial_image_task = asyncio.create_task(_generate_initial_image())
    
    try:
        yield
    finally:
        logger.info("Application shutdown initiated — performing cleanup.")
        cleanup_task.cancel()
        initial_image_task.cancel()
        try:
            await cleanup_task
        except asyncio.CancelledError:
            pass
        try:
            await initial_image_task
        except asyncio.CancelledError:
            pass

# Use the lifespan context to avoid deprecated on_event handlers
app.router.lifespan_context = _lifespan


def build_prompt() -> tuple[str, str]:
    """Return a randomized seasonal prompt using the blender.
    
    Returns:
        tuple: (prompt, season_name)
    """
    prompt, season_name = season_blender.get_prompt()
    logger.debug("Built %s prompt: %s", season_name, prompt)
    return prompt, season_name


async def _generate_swarmui(prompt: str) -> dict:
    """Generate image using SwarmUI backend."""
    logger.debug("Sending prompt to SwarmUI (%s) model=%s", SWARMUI, IMAGE_MODEL)
    
    async def _get_session_id(session: aiohttp.ClientSession) -> str | None:
        try:
            async with session.post(f"{SWARMUI.rstrip('/')}/API/GetNewSession", json={}, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("session_id")
        except Exception as e:
            logger.error("Error getting session id from SwarmUI: %s", e)
        return None

    async def _call_generate(session: aiohttp.ClientSession, session_id: str, prompt_text: str) -> str | None:
        params = {
            "model": IMAGE_MODEL,
            "width": IMAGE_WIDTH,
            "height": IMAGE_HEIGHT,
            "cfgscale": IMAGE_CFGSCALE,
            "steps": IMAGE_STEPS,
            "seed": IMAGE_SEED,
        }
        raw_input = {"prompt": str(prompt_text), **{k: v for k, v in params.items()}, "donotsave": True}
        data = {
            "session_id": session_id,
            "images": "1",
            "prompt": str(prompt_text),
            **{k: str(v) for k, v in params.items()},
            "donotsave": True,
            "rawInput": raw_input,
        }
        try:
            async with session.post(f"{SWARMUI.rstrip('/')}/API/GenerateText2Image", json=data, timeout=IMAGE_TIMEOUT) as resp:
                if resp.status == 200:
                    j = await resp.json()
                    imgs = j.get("images") or []
                    if imgs:
                        return imgs[0]
                else:
                    logger.error("SwarmUI GenerateText2Image returned status %s", resp.status)
        except Exception as e:
            logger.error("Error calling SwarmUI GenerateText2Image: %s", e)
        return None

    image_encoded = None
    try:
        async with aiohttp.ClientSession() as session:
            session_id = await _get_session_id(session)
            if not session_id:
                logger.error("Unable to obtain SwarmUI session id")
                return {"error": "No session"}
            image_encoded = await _call_generate(session, session_id, prompt)
    except Exception as e:
        logger.error("Unexpected error during SwarmUI generation: %s", e)
        return {"error": "Generation exception"}

    if not image_encoded:
        logger.error("Image generation failed for prompt: %s", prompt)
        return {"error": "Generation failed"}
    
    # Normalize to raw base64 payload
    if "," in image_encoded:
        image_b64 = image_encoded.split(",", 1)[1]
    else:
        image_b64 = image_encoded

    logger.info("Received image data (bytes ~ %d)", len(image_b64))

    try:
        image = Image.open(io.BytesIO(base64.b64decode(image_b64)))
    except Exception:
        return {"error": "Unable to decode image data"}

    # Resize down for web if necessary
    max_dim = 1024
    if image.width > max_dim or image.height > max_dim:
        image.thumbnail((max_dim, max_dim))
    # Convert to JPEG for browser-friendliness
    if image.mode == "RGBA":
        image = image.convert("RGB")
    out = io.BytesIO()
    image.save(out, format="JPEG", quality=90)
    out_b64 = base64.b64encode(out.getvalue()).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{out_b64}"

    return {"prompt": prompt, "image_data": data_uri}


async def _generate_openai(prompt: str) -> dict:
    """Generate image using OpenAI API."""

    async def _call_openai(session: aiohttp.ClientSession, prompt_text: str) -> str | None:
        url = f"{OPENAI_IMAGE_API_BASE.rstrip('/')}/images/generations"
        headers = {"Authorization": f"Bearer {OPENAI_IMAGE_API_KEY}", "Content-Type": "application/json"}
        body = {"model": OPENAI_IMAGE_MODEL, "prompt": prompt_text, "size": OPENAI_IMAGE_SIZE}
        try:
            async with session.post(url, json=body, headers=headers, timeout=IMAGE_TIMEOUT) as resp:
                if resp.status == 200:
                    j = await resp.json()
                    # Support both b64_json and url returns
                    data = j.get("data") or []
                    if data:
                        first = data[0]
                        if "b64_json" in first:
                            return first["b64_json"]
                        if "url" in first:
                            # fetch binary and return as base64
                            img_url = first["url"]
                            async with session.get(img_url) as img_resp:
                                if img_resp.status == 200:
                                    b = await img_resp.read()
                                    return base64.b64encode(b).decode("utf-8")
                else:
                    text = await resp.text()
                    logger.error("OpenAI images API returned %s: %s", resp.status, text)
        except Exception as e:
            logger.error("Error calling OpenAI Images API: %s", e)
        return None

    image_encoded = None
    try:
        async with aiohttp.ClientSession() as session:
            image_encoded = await _call_openai(session, prompt)
    except Exception as e:
        logger.error("Unexpected error during OpenAI generation: %s", e)
        return {"error": "Generation exception"}

    if not image_encoded:
        logger.error("OpenAI image generation failed for prompt: %s", prompt)
        return {"error": "Generation failed"}
    
    # Normalize to raw base64 payload
    if "," in image_encoded:
        image_b64 = image_encoded.split(",", 1)[1]
    else:
        image_b64 = image_encoded

    logger.info("Received image data (bytes ~ %d)", len(image_b64))

    try:
        image = Image.open(io.BytesIO(base64.b64decode(image_b64)))
    except Exception:
        return {"error": "Unable to decode image data"}

    # Resize down for web if necessary
    max_dim = 1024
    if image.width > max_dim or image.height > max_dim:
        image.thumbnail((max_dim, max_dim))
    # Convert to JPEG for browser-friendliness
    if image.mode == "RGBA":
        image = image.convert("RGB")
    out = io.BytesIO()
    image.save(out, format="JPEG", quality=90)
    out_b64 = base64.b64encode(out.getvalue()).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{out_b64}"

    return {"prompt": prompt, "image_data": data_uri}


async def generate_scene(prompt: str | None = None, season_name: str | None = None) -> dict:
    """Generate a seasonal scene image. If `prompt` is None, builds a random one."""
    if prompt is None:
        prompt, season_name = build_prompt()
    logger.info("Generating %s scene (%s): %s", season_name or "seasonal", IMAGE_PROVIDER, prompt)

    if IMAGE_PROVIDER == "swarmui":
        return await _generate_swarmui(prompt)
    elif IMAGE_PROVIDER == "openai":
        return await _generate_openai(prompt)
    else:
        return {"error": "unknown image provider"}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, refresh: int | None = None):
    """Serve a minimal HTML page that polls `/image` every X seconds."""
    # Client polls every POLL_INTERVAL seconds for responsiveness, server rate-limits generation to DEFAULT_REFRESH
    poll_interval = refresh or POLL_INTERVAL
    # If we have a cached last image, embed it so the page shows immediately
    with IMAGE_CACHE_LOCK:
        cached = LAST_IMAGE

    initial_image_js = json.dumps(cached.get("image_data")) if cached else "null"
    initial_prompt_js = json.dumps(cached.get("prompt")) if cached else "null"

    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
                <link rel="icon" href="/favicon.ico" />
                <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
                <meta name="theme-color" content="#4682b4" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <title>VibeScape - AI Powered Seasonal Dreams</title>
        <style>
            html,body {{ height:100%; margin:0; background:#111; color:#fff; display:flex; align-items:center; justify-content:center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; overflow:hidden; }}
            #imgContainer {{ position:relative; width:100%; height:100%; display:flex; align-items:center; justify-content:center; }}
            #img {{ width:100%; height:100%; object-fit:contain; box-shadow: 0 8px 30px rgba(0,0,0,0.6); display:block; }}
            #downloadBtn {{ position:absolute; top:16px; right:16px; padding:10px 16px; background:rgba(255,215,0,0.95); color:#111; border:none; border-radius:6px; font-size:14px; font-weight:600; cursor:pointer; opacity:0; transition:opacity 0.2s; box-shadow:0 4px 12px rgba(0,0,0,0.4); z-index:10; }}
            #downloadBtn:hover {{ background:#ffed4e; }}
            #imgContainer:hover #downloadBtn {{ opacity:1; }}
            /* Bottom-center translucent prompt overlay */
            #meta {{ position:fixed; left:50%; bottom:8px; transform:translateX(-50%); background:rgba(0,0,0,0.25); padding:4px 6px; border-radius:6px; font-family:Helvetica,Arial; font-size:12px; opacity:0.5; color:#fff; text-align:center; max-width:90%; pointer-events:auto; cursor:pointer; user-select:text; transition:opacity 0.2s; }}
            #meta:hover {{ opacity:0.9; }}
            #prompt {{ font-size:0.9em; user-select:text; }}
            #copyBtn {{ display:none; margin-left:8px; padding:2px 8px; background:#ffd700; color:#111; border:none; border-radius:4px; font-size:0.85em; cursor:pointer; font-weight:600; }}
            #copyBtn:hover {{ background:#ffed4e; }}
            #meta:hover #copyBtn {{ display:inline-block; }}
            /* Modern splash screen styling (red & gold theme) */
            #splash {{ display:none; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:40px; background:linear-gradient(135deg, rgba(178,17,17,0.18), rgba(255,215,0,0.12)); border-radius:20px; box-shadow:0 20px 60px rgba(0,0,0,0.5); max-width:600px; }}
            #splash-text {{ font-size:3.5em; font-weight:700; margin-bottom:20px; background:linear-gradient(45deg, #b30000, #ffd700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; letter-spacing:2px; text-shadow:2px 2px 6px rgba(0,0,0,0.4); }}
            #splash-link {{ margin-top:15px; font-size:1em; opacity:0.95; }}
            #splash-link a {{ color:#ffd700; text-decoration:none; transition:all 0.25s ease; }}
            #splash-link a:hover {{ color:#fff; text-shadow:0 1px 0 rgba(0,0,0,0.6); }}
            #splash-version {{ margin-top:25px; font-size:0.9em; opacity:0.6; font-weight:300; }}
        </style>
      </head>
            <body>
                <div id="imgContainer" style="display:none;">
                    <img id="img" src="" alt="Seasonal scene" />
                    <button id="downloadBtn">Download Image</button>
                </div>
                <div id="splash">
                        <div id="splash-text">VibeScape</div>
                        <div id="splash-subtitle" style="font-size:1.2em;margin-top:10px;opacity:0.9;">AI Powered Seasonal Dreams</div>
                        <div id="splash-link"><a href="http://github.com/jasonacox/VibeScape" target="_blank" rel="noopener">github.com/jasonacox/VibeScape</a></div>
                        <div id="splash-version">Version: {VERSION}</div>
                </div>
                <div id="meta">Prompt: <span id="prompt">(generating) - Please Wait...</span><button id="copyBtn">Copy Prompt</button></div>
                <script>
                    const pollInterval = {poll_interval} * 1000;
                    const initialImage = {initial_image_js};
                    const initialPrompt = {initial_prompt_js};
                    const splash = document.getElementById('splash');
                    const img = document.getElementById('img');
                    const promptEl = document.getElementById('prompt');

                    // Check if this is first visit using localStorage
                    const hasVisited = localStorage.getItem('vibescape_visited');
                    const isFirstVisit = !hasVisited;

                    // Notify server we're connected (use sendBeacon for unload-safe POST)
                    try {{
                        navigator.sendBeacon('/connect');
                    }} catch (e) {{ /* ignore */ }}

                    // Copy prompt to clipboard
                    const copyBtn = document.getElementById('copyBtn');
                    copyBtn.addEventListener('click', function(e) {{
                        e.stopPropagation();
                        const text = promptEl.textContent;
                        navigator.clipboard.writeText(text).then(function() {{
                            const originalText = copyBtn.textContent;
                            copyBtn.textContent = 'Copied!';
                            setTimeout(function() {{
                                copyBtn.textContent = originalText;
                            }}, 1500);
                        }}).catch(function(err) {{
                            console.error('Copy failed:', err);
                        }});
                    }});

                    // Download image
                    const imgContainer = document.getElementById('imgContainer');
                    const downloadBtn = document.getElementById('downloadBtn');
                    downloadBtn.addEventListener('click', function() {{
                        const dataUrl = img.src;
                        const link = document.createElement('a');
                        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
                        link.download = `vibescape-${{timestamp}}.jpg`;
                        link.href = dataUrl;
                        link.click();
                    }});

                    // Function to show image and hide splash
                    function showImage(imageData, promptText) {{
                        img.src = imageData;
                        promptEl.textContent = promptText || '';
                        imgContainer.style.display = 'inline-block';
                        splash.style.display = 'none';
                    }}

                    // Show splash screen if no image available OR if first visit
                    if (!initialImage || isFirstVisit) {{
                        splash.style.display = 'flex';
                        if (isFirstVisit) {{
                            localStorage.setItem('vibescape_visited', 'true');
                        }}
                        // If we have an image, show it after 2 seconds
                        if (initialImage) {{
                            setTimeout(function() {{
                                showImage(initialImage, initialPrompt);
                            }}, 2000);
                        }}
                    }} else {{
                        // Not first visit and have cached image: show immediately
                        showImage(initialImage, initialPrompt);
                    }}

                    // Notify server on unload that we're disconnecting
                    window.addEventListener('beforeunload', function() {{
                        try {{ 
                            navigator.sendBeacon('/disconnect');
                            // localStorage.removeItem('vibescape_visited');
                        }} catch (e) {{}}
                    }});

                    // Track last known image timestamp to avoid re-downloading same image
                    let lastImageTimestamp = null;

                    async function checkForNewImage() {{
                        try {{
                            // First check lightweight status endpoint
                            const statusRes = await fetch('/image/status');
                            if (!statusRes.ok) return;
                            const status = await statusRes.json();
                            
                            // If no image available yet, skip
                            if (!status.available) return;
                            
                            // If timestamp hasn't changed, skip download
                            if (lastImageTimestamp !== null && status.timestamp === lastImageTimestamp) {{
                                return;
                            }}
                            
                            // New image available - fetch it
                            const res = await fetch('/image');
                            if (!res.ok) return;
                            const j = await res.json();
                            if (j.image_data) {{
                                showImage(j.image_data, j.prompt);
                                lastImageTimestamp = status.timestamp;
                            }}
                        }} catch (e) {{
                            console.error(e);
                        }}
                    }}
                    
                    // Start polling after initial display logic
                    if (isFirstVisit) {{
                        // On first visit, wait 5s before starting to poll
                        setTimeout(function() {{
                            checkForNewImage();
                            setInterval(checkForNewImage, pollInterval);
                        }}, 5000);
                    }} else {{
                        // On subsequent visits, start polling immediately
                        checkForNewImage();
                        setInterval(checkForNewImage, pollInterval);
                    }}
                </script>
            </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/image")
async def image_endpoint(request: Request):
    """Generate and return a new seasonal scene as JSON with a `image_data` data URI."""
    # Declare globals at the top
    global CONNECTED_VIEWERS, LAST_ACTIVITY, LAST_IMAGE, LAST_IMAGE_TIME, GENERATION_IN_PROGRESS
    global IMAGES_GENERATED, GEN_TIME_COUNT, GEN_TIME_SUM, GEN_TIME_MIN, GEN_TIME_MAX
    
    # Register/refresh session for this image request
    session_id = request.headers.get("X-Session-ID")
    if not session_id:
        client_host = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        session_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{client_host}:{user_agent}"))
    
    now = time.time()
    with SESSION_STATE_LOCK:
        # Move to end (most recent) if exists, or add new
        if session_id in SESSIONS:
            SESSIONS.move_to_end(session_id)
        SESSIONS[session_id] = now
        # Enforce max session limit with LRU eviction
        while len(SESSIONS) > MAX_SESSIONS:
            # Remove oldest (first) session
            oldest_id = next(iter(SESSIONS))
            del SESSIONS[oldest_id]
            logger.warning("Session limit reached, evicted oldest session: %s", oldest_id[:8])
        session_count = len(SESSIONS)
        CONNECTED_VIEWERS = session_count
        LAST_ACTIVITY = now

    # Check cache and generation status
    with IMAGE_CACHE_LOCK:
        last_time = LAST_IMAGE_TIME
        cached_result = LAST_IMAGE
        generation_in_progress = GENERATION_IN_PROGRESS
    
    # Determine if we need to generate a new image
    should_generate = False
    if not cached_result:
        # No cached image at all
        should_generate = True
    elif last_time:
        elapsed_since_last = now - last_time
        if elapsed_since_last >= DEFAULT_REFRESH:
            # TTL expired
            should_generate = True
            logger.debug("Cache expired (%.1fs since last generation, TTL=%ds) — triggering background generation", 
                       elapsed_since_last, DEFAULT_REFRESH)
    
    # If we should generate and no generation in progress, start background generation
    if should_generate and not generation_in_progress:
        # Background task to generate new image
        async def _background_generate():
            global LAST_IMAGE, LAST_IMAGE_TIME, GENERATION_IN_PROGRESS
            global IMAGES_GENERATED, IMAGES_FAILED, GEN_TIME_COUNT, GEN_TIME_SUM, GEN_TIME_MIN, GEN_TIME_MAX
            
            # Set generation flag
            with IMAGE_CACHE_LOCK:
                GENERATION_IN_PROGRESS = True
            
            try:
                # Measure generation time
                loop = asyncio.get_running_loop()
                t0 = loop.time()
                result = await generate_scene()
                elapsed = loop.time() - t0
                
                if "error" not in result:
                    # Update stats
                    try:
                        with STATS_LOCK:
                            IMAGES_GENERATED += 1
                            GEN_TIME_COUNT += 1
                            GEN_TIME_SUM += elapsed
                            if GEN_TIME_MIN is None or elapsed < GEN_TIME_MIN:
                                GEN_TIME_MIN = elapsed
                            if GEN_TIME_MAX is None or elapsed > GEN_TIME_MAX:
                                GEN_TIME_MAX = elapsed
                    except Exception:
                        logger.exception("Failed to update generation stats")
                    
                    # Cache the new image
                    with IMAGE_CACHE_LOCK:
                        LAST_IMAGE = result
                        LAST_IMAGE_TIME = time.time()
                    logger.info("Background generation completed successfully")
                else:
                    # Count failure
                    try:
                        with STATS_LOCK:
                            IMAGES_FAILED += 1
                    except Exception:
                        logger.exception("Failed to update failure stats")
                    logger.error("Background generation failed: %s", result.get("error"))
            except Exception:
                # Count exception as failure
                try:
                    with STATS_LOCK:
                        IMAGES_FAILED += 1
                except Exception:
                    pass
                logger.exception("Background generation exception")
            finally:
                # Always clear the generation flag
                with IMAGE_CACHE_LOCK:
                    GENERATION_IN_PROGRESS = False
        
        # Start background task (fire and forget)
        asyncio.create_task(_background_generate())
        logger.debug("Started background image generation task")
    
    # Always return immediately with cached image (or placeholder if none)
    if cached_result:
        # Add timestamp to response for client-side caching
        response_data = cached_result.copy()
        response_data["timestamp"] = last_time
        headers = {"Cache-Control": f"public, max-age={DEFAULT_REFRESH}"}
        return JSONResponse(content=response_data, headers=headers)
    else:
        # No cached image yet, return placeholder
        return JSONResponse(content={"image_data": None, "prompt": "Generating first image...", "timestamp": None})


@app.get("/image/status")
async def image_status():
    """Lightweight endpoint to check if a new image is available without downloading full payload."""
    with IMAGE_CACHE_LOCK:
        last_time = LAST_IMAGE_TIME
        has_image = LAST_IMAGE is not None
    
    if has_image and last_time:
        return {
            "available": True,
            "timestamp": last_time,
            "age_seconds": time.time() - last_time
        }
    else:
        return {
            "available": False,
            "timestamp": None,
            "age_seconds": None
        }


@app.get("/season")
async def season_info():
    """Return information about currently active seasons and their weights."""
    try:
        weights = season_blender.get_active_seasons()
        day_of_year = season_blender.get_day_of_year()
        return {
            "day_of_year": day_of_year,
            "active_seasons": weights,
            "available_seasons": list(season_blender.seasons.keys()),
        }
    except Exception:
        logger.exception("Failed to get season info")
        return JSONResponse(status_code=500, content={"error": "unable to get season info"})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/version")
async def version():
    """Return service version and image provider details."""
    data = {
        "version": VERSION,
        "image_provider": IMAGE_PROVIDER,
    }
    try:
        if IMAGE_PROVIDER == "swarmui":
            data.update({"swarmui": SWARMUI, "model": IMAGE_MODEL})
        elif IMAGE_PROVIDER == "openai":
            data.update({"openai_base": OPENAI_IMAGE_API_BASE, "model": OPENAI_IMAGE_MODEL})
    except Exception:
        pass
    return data


@app.get("/stats")
async def stats():
    """Return usage and generation statistics."""
    try:
        # Read stats without locks - informational only, minor inaccuracies acceptable
        active_sessions = len(SESSIONS)
        current = CONNECTED_VIEWERS
        peak = MAX_CONNECTED_VIEWERS
        count = IMAGES_GENERATED
        failed = IMAGES_FAILED
        gen_count = GEN_TIME_COUNT
        gen_sum = GEN_TIME_SUM
        gen_min = GEN_TIME_MIN
        gen_max = GEN_TIME_MAX
        last_act = LAST_ACTIVITY
        last_img_time = LAST_IMAGE_TIME
        last_img_cached = LAST_IMAGE is not None
        has_ico = FAVICON_ICO_BYTES is not None
        has_apple = APPLE_TOUCH_BYTES is not None
        has_32 = FAVICON_32_BYTES is not None

        now = time.time()
        avg = (gen_sum / gen_count) if gen_count > 0 else None
        return {
            "version": VERSION,
            "image_provider": IMAGE_PROVIDER,
            "active_sessions": active_sessions,
            "session_ttl_s": SESSION_TTL,
            "current_connected": current,
            "peak_connected": peak,
            "images_generated": count,
            "images_failed": failed,
            "generation_time_min_s": gen_min,
            "generation_time_max_s": gen_max,
            "generation_time_avg_s": avg,
            "last_activity_ts": last_act,
            "last_activity_age_s": (now - last_act) if last_act else None,
            "last_image_cached": last_img_cached,
            "last_image_ts": last_img_time,
            "last_image_age_s": (now - last_img_time) if last_img_time else None,
            "favicon_ico_cached": has_ico,
            "apple_touch_cached": has_apple,
            "favicon_32_cached": has_32,
        }
    except Exception:
        logger.exception("Failed to read stats")
        return JSONResponse(status_code=500, content={"error": "unable to read stats"})


@app.get("/favicon.ico")
async def favicon():
    """Return cached multi-size ICO favicon."""
    try:
        if FAVICON_ICO_BYTES:
            headers = {"Cache-Control": f"public, max-age={ICON_CACHE_DURATION}"}
            return Response(content=FAVICON_ICO_BYTES, media_type="image/x-icon", headers=headers)
        logger.error("Favicon ICO cache is empty")
        return JSONResponse(status_code=404, content={"error": "favicon not available"})
    except Exception:
        logger.exception("Failed to serve favicon")
        return JSONResponse(status_code=500, content={"error": "favicon serve failed"})


@app.get("/apple-touch-icon.png")
async def apple_touch_icon():
    """Return cached PNG for Apple touch icons."""
    try:
        if APPLE_TOUCH_BYTES:
            headers = {"Cache-Control": f"public, max-age={ICON_CACHE_DURATION}"}
            return Response(content=APPLE_TOUCH_BYTES, media_type="image/png", headers=headers)
        logger.error("Apple touch icon cache is empty")
        return JSONResponse(status_code=404, content={"error": "apple icon not available"})
    except Exception:
        logger.exception("Failed to serve apple-touch-icon")
        return JSONResponse(status_code=500, content={"error": "apple icon serve failed"})


@app.get("/favicon-32x32.png")
async def favicon_32():
    """Return cached PNG favicon."""
    try:
        if FAVICON_32_BYTES:
            headers = {"Cache-Control": f"public, max-age={ICON_CACHE_DURATION}"}
            return Response(content=FAVICON_32_BYTES, media_type="image/png", headers=headers)
        logger.error("32x32 favicon cache is empty")
        return JSONResponse(status_code=404, content={"error": "favicon not available"})
    except Exception:
        logger.exception("Failed to serve favicon-32x32")
        return JSONResponse(status_code=500, content={"error": "favicon serve failed"})


@app.post("/connect")
async def connect(request: Request):
    """Mark a viewer as connected. Called from the page via `navigator.sendBeacon`."""
    try:
        # Generate or extract session ID from headers/body (use IP + User-Agent as fallback)
        session_id = request.headers.get("X-Session-ID")
        if not session_id:
            # Fallback: generate session ID from client info
            client_host = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("User-Agent", "unknown")
            session_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{client_host}:{user_agent}"))
        
        now = time.time()
        with SESSION_STATE_LOCK:
            # Move to end (most recent) if exists, or add new
            if session_id in SESSIONS:
                SESSIONS.move_to_end(session_id)
            SESSIONS[session_id] = now
            # Enforce max session limit with LRU eviction
            while len(SESSIONS) > MAX_SESSIONS:
                oldest_id = next(iter(SESSIONS))
                del SESSIONS[oldest_id]
                logger.warning("Session limit reached, evicted oldest session: %s", oldest_id[:8])
            session_count = len(SESSIONS)
            global CONNECTED_VIEWERS, MAX_CONNECTED_VIEWERS
            CONNECTED_VIEWERS = session_count
            if CONNECTED_VIEWERS > MAX_CONNECTED_VIEWERS:
                MAX_CONNECTED_VIEWERS = CONNECTED_VIEWERS
            global LAST_ACTIVITY
            LAST_ACTIVITY = now
        
        logger.info("Session connected: %s — total=%d (peak=%d)", session_id[:8], CONNECTED_VIEWERS, MAX_CONNECTED_VIEWERS)
        return {"connected": CONNECTED_VIEWERS, "session_id": session_id}
    except Exception:
        logger.exception("Failed to register connect")
        return JSONResponse(status_code=500, content={"error": "connect failed"})


@app.post("/disconnect")
async def disconnect(request: Request):
    """Mark a viewer as disconnected. Called from the page via `navigator.sendBeacon`."""
    try:
        session_id = request.headers.get("X-Session-ID")
        if not session_id:
            client_host = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("User-Agent", "unknown")
            session_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{client_host}:{user_agent}"))
        
        with SESSION_STATE_LOCK:
            if session_id in SESSIONS:
                del SESSIONS[session_id]
            session_count = len(SESSIONS)
            global CONNECTED_VIEWERS, LAST_ACTIVITY
            CONNECTED_VIEWERS = session_count
            LAST_ACTIVITY = time.time()
        
        logger.info("Session disconnected: %s — total=%d", session_id[:8], CONNECTED_VIEWERS)
        return {"connected": CONNECTED_VIEWERS}
    except Exception:
        logger.exception("Failed to register disconnect")
        return JSONResponse(status_code=500, content={"error": "disconnect failed"})


@app.get("/viewers")
async def viewers():
    """Return current viewer count."""
    try:
        with SESSION_STATE_LOCK:
            current = CONNECTED_VIEWERS
        return {"connected": current}
    except Exception:
        logger.exception("Failed to read viewers")
        return JSONResponse(status_code=500, content={"error": "unable to read viewers"})


if __name__ == '__main__':
    # Optional quick connectivity check to SwarmUI
    print(f"Starting VibeScape server on port {PORT}")
    print(f"Image provider: {IMAGE_PROVIDER}")
    if IMAGE_PROVIDER == "swarmui":
        print(f"SwarmUI host: {SWARMUI} model: {IMAGE_MODEL}")
    elif IMAGE_PROVIDER == "openai":
        print(f"OpenAI API base: {OPENAI_IMAGE_API_BASE} model: {OPENAI_IMAGE_MODEL}")
    # Run uvicorn programmatically and install our own signal handlers so
    # shutdown can be handled gracefully (useful for Ctrl-C and Docker SIGTERM).
    import signal

    config = uvicorn.Config(app, host='0.0.0.0', port=PORT, log_level="info", loop="asyncio", lifespan="on")
    server = uvicorn.Server(config)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def _handle_signal(sig_num, frame):
        try:
            name = signal.Signals(sig_num).name
        except Exception:
            name = str(sig_num)
        logger.info("Received signal %s, initiating graceful shutdown...", name)
        # Ask the server to shutdown asynchronously
        loop.create_task(server.shutdown())

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    try:
        loop.run_until_complete(server.serve())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Interrupted — shutting down")
    except Exception:
        logger.exception("Server error")
    finally:
        # Ensure loop is cleanly closed
        try:
            pending = asyncio.all_tasks(loop=loop)
            for t in pending:
                t.cancel()
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception:
            pass
        loop.close()
