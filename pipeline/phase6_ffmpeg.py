"""
Phase 6 — FFmpeg Preparation
Generates ffmpeg_plan.json, concat lists, and assemble_video.sh.
The shell script combines images with Ken Burns motion, syncs narration,
and burns subtitles into a YouTube-optimised 1080p H.264 MP4.
"""
import json
from pathlib import Path

from .config import (DIRS, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS,
                     VIDEO_CODEC, AUDIO_CODEC, VIDEO_BITRATE, AUDIO_BITRATE,
                     VIDEO_PRESET, VIDEO_PROFILE, VIDEO_LEVEL)
from .utils import setup_logging, save_json, format_duration

log = setup_logging("phase6", "phase6.log")

# Ken Burns zoom direction presets (zoompan filter params)
_ZOOM_PRESETS: dict[str, dict] = {
    "slow_zoom_in":  {
        "z": "min(zoom+0.0012,1.5)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)",
    },
    "slow_zoom_out": {
        "z": "if(eq(on,1),1.5,max(zoom-0.0012,1.0))",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)",
    },
    "slow_pan_left": {
        "z": "min(zoom+0.0008,1.3)",
        "x": "if(gte(x,iw),0,x+2)",
        "y": "ih/2-(ih/zoom/2)",
    },
    "wide_slow_pan": {
        "z": "min(zoom+0.0006,1.2)",
        "x": "if(gte(x,iw),0,x+1)",
        "y": "ih/2-(ih/zoom/2)",
    },
    "slow_zoom_out_with_tilt_up": {
        "z": "if(eq(on,1),1.4,max(zoom-0.001,1.0))",
        "x": "iw/2-(iw/zoom/2)",
        "y": "max(ih/2-(ih/zoom/2)-1*on,0)",
    },
    "push_in_fast": {
        "z": "min(zoom+0.002,1.8)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)",
    },
    "static_with_subtle_zoom": {
        "z": "min(zoom+0.0005,1.1)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)",
    },
}

_DEFAULT_ZOOM = _ZOOM_PRESETS["slow_zoom_in"]


def _zoompan_filter(motion: str, duration: float, fps: int = VIDEO_FPS) -> str:
    p = _ZOOM_PRESETS.get(motion, _DEFAULT_ZOOM)
    frames = int(duration * fps)
    return (
        f"zoompan=z='{p['z']}':x='{p['x']}':y='{p['y']}':"
        f"d={frames}:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={fps}"
    )


def build_plan(chapters: list[dict], all_scenes: dict[int, list[dict]]) -> dict:
    plan = {
        "project":  "KirkStore Documentary",
        "video":    {
            "width": VIDEO_WIDTH, "height": VIDEO_HEIGHT,
            "fps": VIDEO_FPS, "codec": VIDEO_CODEC,
            "bitrate": VIDEO_BITRATE, "preset": VIDEO_PRESET,
            "profile": VIDEO_PROFILE, "level": VIDEO_LEVEL,
        },
        "audio":    {"codec": AUDIO_CODEC, "bitrate": AUDIO_BITRATE},
        "chapters": [],
    }

    total_scenes = 0
    for ch in chapters:
        num    = ch["chapter_number"]
        scenes = all_scenes.get(num, [])
        audio  = str(DIRS["audio"] / ch["filename"])

        chapter_entry = {
            "chapter_number": num,
            "chapter_title":  ch["chapter_title"],
            "audio_file":     audio,
            "duration":       ch.get("duration_seconds", 0),
            "scenes": [],
        }

        for s in scenes:
            image_file = str(
                DIRS["exports"] / f"images/ch{num:02d}_scene{s['scene_number']:04d}.jpg"
            )
            zoom = _ZOOM_PRESETS.get(s.get("motion_recommendation", ""), _DEFAULT_ZOOM)
            chapter_entry["scenes"].append({
                "scene_number":   s["scene_number"],
                "start":          s["start"],
                "end":            s["end"],
                "duration":       s["duration"],
                "image_file":     image_file,
                "motion":         s.get("motion_recommendation", "slow_zoom_in"),
                "zoompan_z":      zoom["z"],
                "zoompan_x":      zoom["x"],
                "zoompan_y":      zoom["y"],
                "narration":      s["narration"][:80],
                "image_prompt":   s.get("image_prompt", ""),
                "transition":     "fade" if s["duration"] >= 5 else "cut",
                "fade_duration":  0.5 if s["duration"] >= 5 else 0.0,
            })
            total_scenes += 1

        plan["chapters"].append(chapter_entry)

    plan["summary"] = {
        "total_chapters": len(chapters),
        "total_scenes":   total_scenes,
        "total_images_required": total_scenes,
    }
    return plan


def write_concat_list(chapter: dict, chapter_num: int) -> Path:
    """Write an FFmpeg concat demuxer list for one chapter's scenes."""
    out = DIRS["ffmpeg"] / f"chapter_{chapter_num:02d}_concat.txt"
    lines = []
    for s in chapter["scenes"]:
        lines.append(f"file '{s['image_file']}'")
        lines.append(f"duration {s['duration']:.3f}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def write_assembly_script(plan: dict) -> Path:
    """Generate assemble_video.sh — the complete FFmpeg build script."""
    W, H, FPS = VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS
    out_path = DIRS["ffmpeg"] / "assemble_video.sh"

    lines = [
        "#!/usr/bin/env bash",
        "# KirkStore Documentary — FFmpeg Assembly Script",
        "# Auto-generated by pipeline/phase6_ffmpeg.py",
        "# Usage: bash assemble_video.sh",
        "",
        "set -euo pipefail",
        "",
        f'EXPORTS="{DIRS["exports"]}"',
        f'AUDIO_DIR="{DIRS["audio"]}"',
        f'SUBS_DIR="{DIRS["subtitles"]}"',
        f'FFMPEG_DIR="{DIRS["ffmpeg"]}"',
        "",
        "mkdir -p \"$EXPORTS/clips\" \"$EXPORTS/chapters\"",
        "",
        "echo '================================================'",
        "echo ' KirkStore Documentary — Video Assembly'",
        "echo '================================================'",
        "",
    ]

    chapter_clip_vars = []

    for ch in plan["chapters"]:
        num   = ch["chapter_number"]
        title = ch["chapter_title"]
        audio = ch["audio_file"]
        dur   = ch["duration"]

        lines += [
            f"# ─── Chapter {num:02d}: {title} ───────────────────────────────────────",
            f'echo "[{num:02d}] Assembling: {title}"',
            "",
        ]

        scene_clips = []
        for s in ch["scenes"]:
            snum  = s["scene_number"]
            img   = s["image_file"]
            sdur  = s["duration"]
            frames = int(sdur * FPS)
            z     = s["zoompan_z"]
            x     = s["zoompan_x"]
            y     = s["zoompan_y"]

            clip = f"$EXPORTS/clips/ch{num:02d}_s{snum:04d}.mp4"
            scene_clips.append(clip)

            # Fade for longer scenes
            vf = (
                f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                f"crop={W}:{H},"
                f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},"
                f"format=yuv420p"
            )
            if s["fade_duration"] > 0:
                fd = s["fade_duration"]
                vf += f",fade=t=out:st={sdur - fd:.2f}:d={fd:.2f}"

            lines += [
                f"# Scene {snum}: {s['narration'][:60]}",
                f'ffmpeg -y -loop 1 -t {sdur:.3f} -i "{img}" \\',
                f'  -vf "{vf}" \\',
                f'  -r {FPS} -c:v {VIDEO_CODEC} -preset ultrafast -pix_fmt yuv420p \\',
                f'  "{clip}"',
                "",
            ]

        # Concat chapter clips
        concat_list = str(DIRS["ffmpeg"] / f"chapter_{num:02d}_concat.txt")
        chapter_silent = f"$EXPORTS/chapters/ch{num:02d}_silent.mp4"
        chapter_audio  = f"$EXPORTS/chapters/ch{num:02d}_with_audio.mp4"
        chapter_subs   = f"$EXPORTS/chapters/ch{num:02d}_final.mp4"
        srt_file       = str(DIRS["subtitles"] / f"chapter_{num:02d}.srt")

        # Build concat list on-the-fly
        lines += [
            f"# Concat all {len(scene_clips)} clips for chapter {num:02d}",
            f"{{ ",
        ]
        for clip in scene_clips:
            lines += [f"  echo \"file '{clip}'\";"]
        lines += [
            f'}} > "{concat_list}"',
            f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -c copy "{chapter_silent}"',
            "",
            f"# Add narration audio",
            f'ffmpeg -y -i "{chapter_silent}" -i "{audio}" \\',
            f'  -map 0:v -map 1:a \\',
            f'  -c:v copy -c:a {AUDIO_CODEC} -b:a {AUDIO_BITRATE} \\',
            f'  -shortest "{chapter_audio}"',
            "",
            f"# Burn subtitles",
            f'ffmpeg -y -i "{chapter_audio}" \\',
            f"  -vf \"subtitles='{srt_file}':force_style='FontName={plan['video'].get('codec',VIDEO_CODEC)}'\" \\",
            f'  -c:v {VIDEO_CODEC} -preset {VIDEO_PRESET} -profile:v {VIDEO_PROFILE} \\',
            f'  -b:v {VIDEO_BITRATE} -c:a copy "{chapter_subs}"',
            "",
        ]
        chapter_clip_vars.append(chapter_subs)

    # Final concat of all chapters
    final_out = f"$EXPORTS/documentary_final.mp4"
    master_srt = str(DIRS["subtitles"] / "master.srt")

    lines += [
        "# ─── Final Assembly: All Chapters ───────────────────────────────────────",
        'echo "Combining all chapters into final documentary…"',
        "",
        'FINAL_CONCAT="$FFMPEG_DIR/final_concat.txt"',
        "{",
    ]
    for cp in chapter_clip_vars:
        lines.append(f"  echo \"file '{cp}'\";")
    lines += [
        '} > "$FINAL_CONCAT"',
        "",
        f'ffmpeg -y -f concat -safe 0 -i "$FINAL_CONCAT" \\',
        f'  -c:v {VIDEO_CODEC} -preset {VIDEO_PRESET} -profile:v {VIDEO_PROFILE} \\',
        f'  -level:v {VIDEO_LEVEL} -b:v {VIDEO_BITRATE} \\',
        f'  -c:a {AUDIO_CODEC} -b:a {AUDIO_BITRATE} \\',
        f'  -movflags +faststart \\',
        f'  "{final_out}"',
        "",
        'echo ""',
        'echo "✓ Assembly complete: $EXPORTS/documentary_final.mp4"',
        'echo ""',
        f'ffprobe -v quiet -show_format "{final_out}" 2>&1 | grep -E "duration|size|bit_rate" || true',
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out_path.chmod(0o755)
    return out_path


def run(chapters: list[dict], all_scenes: dict[int, list[dict]]) -> dict:
    """Build FFmpeg plan and shell script."""
    log.info("=== Phase 6: FFmpeg Preparation ===")
    DIRS["ffmpeg"].mkdir(parents=True, exist_ok=True)
    (DIRS["exports"] / "images").mkdir(parents=True, exist_ok=True)

    plan = build_plan(chapters, all_scenes)
    plan_path = DIRS["ffmpeg"] / "ffmpeg_plan.json"
    save_json(plan, plan_path)
    log.info("ffmpeg_plan.json: %d chapters, %d scenes",
             plan["summary"]["total_chapters"],
             plan["summary"]["total_scenes"])

    for ch in plan["chapters"]:
        write_concat_list(ch, ch["chapter_number"])

    script_path = write_assembly_script(plan)
    log.info("assemble_video.sh → %s", script_path)

    return plan
