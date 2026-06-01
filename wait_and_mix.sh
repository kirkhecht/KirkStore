#!/bin/bash
# Wait for stories 01-05 to be ready in the stories dir, then run finalize_mix.sh
cd /home/user/KirkStore

STORIES_DIR="project/documentary/stories"
LOG="/tmp/wait_and_mix.log"

echo "Waiting for stories 01-05 to be assembled..." | tee $LOG

NEEDED=("01_in_the_beginning.mp4" "02_the_fall.mp4" "03_cain_and_abel.mp4"
        "04_noah_and_the_flood.mp4" "05_the_tower_of_babel.mp4")

while true; do
  ALL_DONE=1
  for f in "${NEEDED[@]}"; do
    if [ ! -f "$STORIES_DIR/$f" ] || [ "$(stat -c%s "$STORIES_DIR/$f")" -lt 5000000 ]; then
      ALL_DONE=0
      echo "  Still waiting: $f ($(stat -c%s "$STORIES_DIR/$f" 2>/dev/null || echo '0') bytes)" | tee -a $LOG
      break
    fi
  done
  if [ $ALL_DONE -eq 1 ]; then
    echo "All stories 01-05 ready!" | tee -a $LOG
    break
  fi
  echo "$(date): Checking again in 60s..." | tee -a $LOG
  sleep 60
done

echo "Starting finalize_mix.sh..." | tee -a $LOG
bash /home/user/KirkStore/finalize_mix.sh 2>&1 | tee -a $LOG
