import os
import sys
from pathlib import Path

env_file = Path(".env")
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key] = value

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
output_dir = Path("natasha-personal/SempreViva")

prompts = [
    {
        "name": "variant_2_refined_a",
        "prompt": (
            "Minimalist two-color logo on white background. Colors: sage green and golden yellow only. "
            "Top half: one single Helichrysum stoechas (immortelle) sprig -- "
            "one stem, a few small narrow leaves, one tight cluster of tiny round golden yellow flowers at the top. "
            "Bottom half: the words 'Sempre Viva' in large elegant serif italic font in sage green. "
            "Centered layout. Nothing else. No frames, no extra sprigs, no dividers. "
            "Clean, simple, Mediterranean rustic botanical logo. 16:9 horizontal format. Print-ready."
        )
    },
    {
        "name": "variant_2_refined_b",
        "prompt": (
            "Horizontal 16:9 logo on white background. Two colors only: olive green and golden yellow. "
            "Layout: on the left side, one single botanical sprig of Helichrysum stoechas (immortelle) -- "
            "a single straight stem with narrow leaves and one rounded flower head of tiny yellow flowers at the tip. "
            "On the right side: the text 'Sempre Viva' in large elegant italic serif font in olive green. "
            "The sprig and text are on the same horizontal line, side by side. "
            "Flat, graphic, minimal. No gradients, no extra decoration. Rustic Mediterranean style. Print-ready."
        )
    },
]

for item in prompts:
    print(f"Generating {item['name']}...")
    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=item["prompt"],
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                output_mime_type="image/png",
            )
        )

        if not response.generated_images:
            print("  No images returned")
            continue

        img_data = response.generated_images[0].image.image_bytes
        filepath = output_dir / f"{item['name']}.png"
        filepath.write_bytes(img_data)
        print(f"  Saved: {filepath}")

    except Exception as e:
        print(f"  Error: {e}")

print("Done!")
