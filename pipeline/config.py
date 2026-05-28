"""Central configuration for the KirkStore pipeline."""
import os
from pathlib import Path

# ── Directories ────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(os.getenv("KIRKSTORE_PROJECT_ROOT", "./project"))

DIRS = {
    "audio":         PROJECT_ROOT / "audio",
    "scripts":       PROJECT_ROOT / "scripts",
    "scene_json":    PROJECT_ROOT / "scene_json",
    "image_prompts": PROJECT_ROOT / "image_prompts",
    "images":        PROJECT_ROOT / "images",
    "subtitles":     PROJECT_ROOT / "subtitles",
    "ffmpeg":        PROJECT_ROOT / "ffmpeg",
    "exports":       PROJECT_ROOT / "exports",
    "logs":          PROJECT_ROOT / "logs",
    "transcripts":   PROJECT_ROOT / "transcripts",
    "production":    PROJECT_ROOT / "production",
}

# ── Scene segmentation ─────────────────────────────────────────────────────────
SCENE_MIN_DURATION   = 2.0   # seconds
SCENE_MAX_DURATION   = 6.0   # seconds
SCENE_IDEAL_DURATION = 4.0   # target average
SILENCE_THRESHOLD    = 0.40  # silence gap that marks a cut candidate

# ── Video output ───────────────────────────────────────────────────────────────
VIDEO_WIDTH   = 1920
VIDEO_HEIGHT  = 1080
VIDEO_FPS     = 25
VIDEO_CODEC   = "libx264"
AUDIO_CODEC   = "aac"
VIDEO_BITRATE = "8M"
AUDIO_BITRATE = "192k"
VIDEO_PRESET  = "slow"
VIDEO_PROFILE = "high"
VIDEO_LEVEL   = "4.1"

# ── Subtitle formatting ────────────────────────────────────────────────────────
SUBTITLE_MAX_CHARS = 42
SUBTITLE_MAX_LINES = 2
SUBTITLE_FONT      = "Arial"
SUBTITLE_FONTSIZE  = 24
SUBTITLE_MARGIN_V  = 60

# ── Image generation style ─────────────────────────────────────────────────────
IMAGE_BASE_STYLE = (
    "ultra realistic cinematic film still, dramatic lighting, "
    "high contrast, emotionally immersive, 16:9 aspect ratio, "
    "photorealistic, no text, no watermarks"
)

# ── Whisper ────────────────────────────────────────────────────────────────────
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny | base | small | medium | large

# ── Claude API (optional) ──────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL      = "claude-sonnet-4-6"
USE_AI_PROMPTS    = bool(ANTHROPIC_API_KEY)

# ── Replicate / image generation ──────────────────────────────────────────────
REPLICATE_API_KEY    = os.getenv("REPLICATE_API_KEY", "")
IMAGE_MODEL          = "black-forest-labs/flux-dev"
IMAGE_WIDTH          = 1344   # 16:9 at ~720p equivalent for Flux
IMAGE_HEIGHT         = 768
IMAGE_STEPS          = 28
IMAGE_GUIDANCE       = 3.5
IMAGE_BATCH_WORKERS  = 4      # parallel requests

# ── Narration pacing (ElevenLabs typical) ─────────────────────────────────────
DEFAULT_WPM = 150
