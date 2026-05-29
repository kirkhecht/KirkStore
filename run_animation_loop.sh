#!/bin/bash
# Runs gen_ai_animation.py one scene at a time to avoid container process kills.
# Each scene takes ~4 minutes. Script resumes automatically from last completed scene.

LOG=/tmp/ai_animation_run.log
CLIPS_DIR=/home/user/KirkStore/project/documentary/ai_clips

cd /home/user/KirkStore

for i in $(seq 1 110); do
    CLIP=$(printf "%s/%03d.mp4" "$CLIPS_DIR" "$i")
    if [ -f "$CLIP" ]; then
        echo "[$(date '+%H:%M')] Scene $i already done, skipping" >> "$LOG"
        continue
    fi
    echo "[$(date '+%H:%M')] Starting scene $i ..." >> "$LOG"
    python3 gen_ai_animation.py --start "$i" --end "$i" >> "$LOG" 2>&1
    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "[$(date '+%H:%M')] Scene $i exited with code $STATUS" >> "$LOG"
    fi
done

echo "[$(date '+%H:%M')] All scenes done — running final assembly" >> "$LOG"
python3 gen_ai_animation.py --assemble-only >> "$LOG" 2>&1
echo "[$(date '+%H:%M')] COMPLETE" >> "$LOG"
