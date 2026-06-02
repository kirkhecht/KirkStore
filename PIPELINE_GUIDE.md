# KirkStore Documentary Production Pipeline

> Automated post-narration workflow for ElevenLabs-exported MP3 chapters.
> Narration audio is the **fixed master timeline** — everything else adapts to it.

---

## Quick Start

### 1. Install dependencies

```bash
bash install.sh
```

Or manually:

```bash
pip install -r requirements.txt
# macOS:
brew install ffmpeg
# Ubuntu/Debian:
sudo apt-get install -y ffmpeg
```

### 2. Place your MP3 files

Drop your ElevenLabs narration MP3s into any folder. The pipeline will discover and rename them automatically.

```
/my-project/narration/
  01_intro.mp3
  02_chapter_one.mp3
  ...
```

### 3. Run the pipeline

```bash
# Full pipeline — real audio
python run_pipeline.py --source-dir /my-project/narration

# Demo mode — no MP3s needed, runs on synthetic data
python run_pipeline.py --demo

# With Claude API for richer image prompts
ANTHROPIC_API_KEY=sk-... python run_pipeline.py --source-dir /path --ai

# Use a larger Whisper model for better transcription accuracy
python run_pipeline.py --source-dir /path --whisper medium

# Run only specific phases
python run_pipeline.py --source-dir /path --phases 3,4,5
```

### 4. Generate images

Open `project/image_prompts/image_prompts.csv`. Each row has a ready-to-use
`prompt` column. Feed these into:

- **Flux Pro 1.1** (recommended for photorealism)
- **Midjourney v6** (`--ar 16:9 --style raw`)
- **DALL-E 3** via API or ChatGPT
- **Stable Diffusion XL**

Save rendered images as:
```
project/exports/images/chXX_sceneXXXX.jpg
```
(Match exactly — the assembly script expects this naming.)

### 5. Assemble the video

```bash
bash project/ffmpeg/assemble_video.sh
```

Final output: `project/exports/documentary_final.mp4`

---

## Pipeline Phases

| Phase | Module | What it does |
|---|---|---|
| 1 | `phase1_organize` | Scans source dir, renames files, copies to project, writes `master_index.csv` |
| 2 | `phase2_analyze` | Extracts duration, runs Whisper transcription, detects silences, writes `chapter_XX_summary.json` |
| 3 | `phase3_segment` | Cuts narration into 2–6s cinematic scenes, writes `scene_timeline.json` |
| 4 | `phase4_prompts` | Generates Flux/SD/GPT image prompts per scene, writes `image_prompts.csv` |
| 5 | `phase5_subtitles` | Produces `.srt` and `.ass` subtitle files aligned to narration |
| 6 | `phase6_ffmpeg` | Builds `ffmpeg_plan.json` and `assemble_video.sh` with Ken Burns motion |
| 7 | `phase7_dashboard` | Generates `production_report.md` with pacing analysis and render estimates |

---

## Project Output Structure

```
project/
├── audio/                    ← Renamed MP3 files (01_intro.mp3, etc.)
├── scripts/                  ← Copied script/guide files
├── transcripts/
│   ├── chapter_01.json       ← Whisper word timestamps
│   ├── chapter_01_summary.json
│   └── ...
├── scene_json/
│   ├── chapter_01_scenes.json
│   ├── scene_timeline.json   ← Master scene list (all chapters)
│   └── ...
├── image_prompts/
│   ├── image_prompts.csv     ← Master prompt sheet
│   ├── chapter_01_prompts.csv
│   └── ...
├── subtitles/
│   ├── master.srt
│   ├── master.ass
│   ├── chapter_01.srt
│   └── ...
├── ffmpeg/
│   ├── ffmpeg_plan.json      ← Full timing/motion map
│   ├── assemble_video.sh     ← Run this to build the video
│   └── chapter_01_concat.txt
├── exports/
│   ├── images/               ← Place generated images here
│   ├── clips/                ← Auto-created scene clips
│   ├── chapters/             ← Per-chapter compiled videos
│   └── documentary_final.mp4
├── logs/
│   └── pipeline.log
└── production/
    ├── master_index.csv
    └── production_report.md
```

---

## Scene JSON Schema

```json
{
  "scene_number": 12,
  "chapter": 2,
  "chapter_title": "Rise of Empire",
  "start": 52.3,
  "end": 56.8,
  "duration": 4.5,
  "narration": "The kingdom fell into chaos.",
  "emotion": "dark_and_tense",
  "visual_description": "burning ancient city at dusk, dramatic smoke",
  "image_prompt": "burning ancient city at dusk, dark and brooding, ultra realistic...",
  "motion_recommendation": "slow_zoom_in",
  "subtitle_text": "The kingdom fell into chaos."
}
```

---

## Image Naming Convention

Images must match exactly:
```
ch{chapter_number:02d}_scene{scene_number:04d}.jpg
```
Examples:
```
ch01_scene0001.jpg   ← Chapter 1, Scene 1
ch02_scene0047.jpg   ← Chapter 2, Scene 47
```

---

## Ken Burns Motion Presets

| Preset | Use Case |
|---|---|
| `slow_zoom_in` | Default — builds tension |
| `slow_zoom_out` | Reveals, endings, triumph |
| `slow_pan_left` | Exploring environments |
| `wide_slow_pan` | Epic establishing shots |
| `push_in_fast` | Dramatic reveals |
| `static_with_subtle_zoom` | Solemn, contemplative moments |
| `slow_zoom_out_with_tilt_up` | Hope, liberation, new beginnings |

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Enable Claude-powered image prompts |
| `WHISPER_MODEL` | `base` | Whisper model size (tiny/base/small/medium/large) |
| `KIRKSTORE_PROJECT_ROOT` | `./project` | Override project output directory |

---

## Dependencies

| Package | Purpose |
|---|---|
| `mutagen` | MP3 metadata / duration extraction |
| `openai-whisper` | Word-level transcription |
| `anthropic` | Claude API for AI image prompts (optional) |
| `pydub` | Audio processing utilities |
| `nltk` | Sentence tokenisation |
| `numpy` | Numerical operations |
| `pandas` | CSV/DataFrame operations |
| `tqdm` | Progress bars |
| `ffmpeg` (binary) | Video assembly |

---

## Scaling to Multiple Episodes

The pipeline is fully episode-aware. For a series:

1. Use a separate `--project-root` per episode:
   ```bash
   python run_pipeline.py --source-dir ./ep01_audio --project-root ./ep01_project
   python run_pipeline.py --source-dir ./ep02_audio --project-root ./ep02_project
   ```

2. Each episode gets its own isolated `project/` directory with all outputs.

3. Use a wrapper script to process all episodes in a loop:
   ```bash
   for ep in ep01 ep02 ep03; do
     python run_pipeline.py --source-dir ./${ep}_audio --project-root ./${ep}_project
   done
   ```

---

## Troubleshooting

**"No audio files found"**
→ Check `--source-dir` path. Supported formats: `.mp3 .wav .m4a .aac .flac .ogg`

**"mutagen not installed"**
→ `pip install mutagen`

**"openai-whisper not installed"**
→ `pip install openai-whisper` — pipeline will fall back to estimated timestamps without it.

**Whisper is very slow**
→ Use `--whisper tiny` for speed. Transcripts are cached — only run once per chapter.

**FFmpeg errors in assembly script**
→ Ensure all images exist at the expected paths in `project/exports/images/`.

**Claude API prompts not generating**
→ Set `ANTHROPIC_API_KEY` environment variable before running.

---

*KirkStore Documentary Pipeline — built for scalable documentary production*
