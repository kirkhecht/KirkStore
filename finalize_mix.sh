#!/bin/bash
# Wait for all 19 story source files to be present (Brady voice),
# then delete old mixed files and re-run mix_audio.py.
set -e

STORIES_DIR="project/documentary/stories"
MIXED_DIR="$STORIES_DIR/mixed"
LOG="/tmp/finalize_mix.log"

cd /home/user/KirkStore

echo "=== Finalize Mix ===" | tee $LOG
date | tee -a $LOG

# Check all 19 story source files exist
EXPECTED=(
  "01_in_the_beginning.mp4"
  "02_the_fall.mp4"
  "03_cain_and_abel.mp4"
  "04_noah_and_the_flood.mp4"
  "05_the_tower_of_babel.mp4"
  "06_calling_of_abram.mp4"
  "07_covenant_with_god.mp4"
  "08_the_three_visitors.mp4"
  "09_sodom_and_gomorrah.mp4"
  "10_birth_of_isaac.mp4"
  "11_binding_of_isaac.mp4"
  "12_rebekah_wife_of_isaac.mp4"
  "13_jacob_and_esau.mp4"
  "14_jacobs_dream_at_bethel.mp4"
  "15_jacob_leah_and_rachel.mp4"
  "16_jacob_wrestles_with_god.mp4"
  "17_joseph_and_his_brothers.mp4"
  "18_joseph_in_egypt.mp4"
  "19_pharaohs_dreams.mp4"
)

echo "Checking story sources..." | tee -a $LOG
MISSING=0
for f in "${EXPECTED[@]}"; do
  if [ ! -f "$STORIES_DIR/$f" ]; then
    echo "  MISSING: $f" | tee -a $LOG
    MISSING=$((MISSING+1))
  fi
done

if [ $MISSING -gt 0 ]; then
  echo "ERROR: $MISSING story files missing. Aborting." | tee -a $LOG
  exit 1
fi

echo "All 19 story sources present." | tee -a $LOG

# Delete old mixed files so mix_audio.py re-processes all
echo "Deleting old mixed files..." | tee -a $LOG
rm -f "$MIXED_DIR"/*.mp4
echo "Cleared mixed dir." | tee -a $LOG

# Run mix_audio.py
echo "Running mix_audio.py..." | tee -a $LOG
python mix_audio.py 2>&1 | tee -a $LOG

echo "=== Mix complete ===" | tee -a $LOG
