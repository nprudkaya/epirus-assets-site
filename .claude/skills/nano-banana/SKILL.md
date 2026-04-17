---
name: nano-banana
description: Generate images using Google Gemini (Nano Banana 2). Requires GEMINI_API_KEY in .env file.
---

# Nano Banana — Image Generator

Generate an image using Google Gemini's image generation model.

**User's request:** $ARGUMENTS

## Prerequisites

- Python 3.10+
- `google-genai` package (`pip install google-genai`)
- `GEMINI_API_KEY` in `.env` file (get free key at aistudio.google.com)

## How to generate

Write and run this Python script:

```python
import os
import sys
from pathlib import Path
from datetime import datetime

# Load .env
env_file = Path(".env")
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key] = value

from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found. Add it to .env file.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

prompt = "<USER'S IMAGE DESCRIPTION HERE>"

try:
    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE', 'TEXT']
        )
    )

    if not response.candidates:
        print("❌ No response — image may have been blocked by safety filter")
        sys.exit(1)

    candidate = response.candidates[0]
    if not candidate.content or not candidate.content.parts:
        print("❌ No content in response — try a different prompt")
        sys.exit(1)

    for part in candidate.content.parts:
        if part.inline_data is not None:
            ext = "png" if "png" in part.inline_data.mime_type else "jpg"
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filepath = f"images/{timestamp}.{ext}"
            Path("images").mkdir(exist_ok=True)
            Path(filepath).write_bytes(part.inline_data.data)
            print(f"✅ Image saved: {filepath}")
            break
    else:
        print("❌ No image in response — model returned text only")
        sys.exit(1)

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
```

## Important

1. Replace `<USER'S IMAGE DESCRIPTION HERE>` with the actual prompt based on the user's request
2. Write the prompt in the SAME language the user used
3. If `google-genai` is not installed, install it first: `pip install google-genai`
4. After generating, show the image to the user using the Read tool
