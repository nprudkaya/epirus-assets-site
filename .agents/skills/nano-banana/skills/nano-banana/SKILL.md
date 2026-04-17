---
name: nano-banana
description: Generate images with Google Gemini. Text-to-image and style transfer from reference images.
arguments:
  - name: idea
    description: Your image idea (simple description)
    required: true
  - name: ref
    description: Path to reference image for style transfer (optional)
    required: false
---

# Nano Banana Image Generator

Generate an image using Google Gemini.

**User's idea:** $ARGUMENTS.idea
**Reference image:** $ARGUMENTS.ref

## Important: prompt language

**Write the image generation prompt in the SAME language as the user's request.** If the user writes in Russian — prompt in Russian. In English — in English. Do NOT auto-translate.

## Setup

Requires `GEMINI_API_KEY` in `.env` file. Get one at [aistudio.google.com](https://aistudio.google.com) → API Keys → Create API key. Free tier is sufficient.

## Usage

Run the script from the skill directory:

If reference image is provided:
```bash
python3 "$(dirname "$0")/nano_banana.py" -r "$ARGUMENTS.ref" "$ARGUMENTS.idea"
```

If no reference:
```bash
python3 "$(dirname "$0")/nano_banana.py" "$ARGUMENTS.idea"
```

## Options

| Flag | Description |
|------|-------------|
| `--pro` | Use Gemini Pro (best quality, slower) |
| `-a 16:9` | Aspect ratio (1:1, 4:3, 16:9, 9:16, 3:2, 4:5) |
| `-s 2K` | Image size (0.5K, 1K, 2K, 4K) |
| `-r path` | Reference image for style transfer |
| `-o path` | Output file path |
| `--no-open` | Don't auto-open the image |

## Examples

```bash
# Simple generation
python3 nano_banana.py "pixel art cat"

# With aspect ratio and output path
python3 nano_banana.py -a 16:9 -o hero.png "cyberpunk city at night"

# With reference image for style transfer
python3 nano_banana.py -r style.jpg "cat in this style"
```
