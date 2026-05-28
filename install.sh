#!/usr/bin/env bash
set -euo pipefail

echo "============================================"
echo " KirkStore Documentary Pipeline — Installer"
echo "============================================"

# Python deps
echo "[1/3] Installing Python dependencies..."
pip install -r requirements.txt

# Whisper depends on ffmpeg at the OS level too
echo "[2/3] Checking ffmpeg..."
if ! command -v ffmpeg &>/dev/null; then
    echo "  ffmpeg not found. Attempting install..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y ffmpeg
    elif command -v brew &>/dev/null; then
        brew install ffmpeg
    else
        echo "  ERROR: Please install ffmpeg manually: https://ffmpeg.org/download.html"
        exit 1
    fi
else
    echo "  ffmpeg found: $(ffmpeg -version 2>&1 | head -1)"
fi

# NLTK data for sentence tokenization
echo "[3/3] Downloading NLTK punkt tokenizer..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('punkt_tab', quiet=True)"

echo ""
echo "Done. Run the pipeline with:"
echo "  python run_pipeline.py --source-dir /path/to/your/mp3s"
echo "  python run_pipeline.py --demo   (try without audio files)"
