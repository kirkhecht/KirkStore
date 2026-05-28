# KirkStore

**AI-assisted documentary production pipeline** for ElevenLabs narration exports.

Automates the entire post-narration workflow: audio analysis → scene segmentation → image prompt generation → subtitle creation → FFmpeg video assembly.

## Get started

```bash
bash install.sh
python run_pipeline.py --demo                         # try it without MP3s
python run_pipeline.py --source-dir /path/to/mp3s    # real production run
```

See [PIPELINE_GUIDE.md](PIPELINE_GUIDE.md) for full documentation.