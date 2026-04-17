import os
import sys
from pathlib import Path

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
    print("GEMINI_API_KEY not found.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

output_dir = Path("natasha-personal/SempreViva")
output_dir.mkdir(parents=True, exist_ok=True)

prompts = [
    {
        "name": "variant_1_wreath",
        "prompt": (
            "A rectangular 16:9 horizontal logo for an Airbnb apartment called 'Sempre Viva'. "
            "Two-color design using warm golden yellow and deep terracotta on a cream white background. "
            "Style: rustic Mediterranean graphic illustration, flat design, minimal. "
            "Central composition: a circular wreath made of Helichrysum stoechas (immortelle) flowers -- "
            "small round golden yellow flowers with straw-like papery petals, on slender stems with narrow leaves. "
            "Inside the wreath, elegant serif typography 'Sempre Viva' in terracotta. "
            "Below the name, small subtitle text 'Appartamenti'. "
            "Clean white background. Print-ready, no gradients, no more than 2 colors."
        )
    },
    {
        "name": "variant_2_horizontal_branch",
        "prompt": (
            "A rectangular 16:9 horizontal logo for an Airbnb apartment called 'Sempre Viva'. "
            "Two-color design: sage green and warm ochre/golden yellow on ivory white background. "
            "Style: rustic Mediterranean botanical illustration, clean graphic lines, floral. "
            "Layout: horizontal -- a long decorative branch of Helichrysum stoechas (immortelle) with "
            "clusters of small round yellow flowers and narrow grey-green leaves stretches across the full width. "
            "The text 'Sempre Viva' is centered in large elegant italic serif font in sage green, "
            "placed alongside or below the branch. "
            "Light, airy, countryside Mediterranean feel. No gradients, flat botanical illustration, print-ready."
        )
    },
    {
        "name": "variant_3_minimal_emblem",
        "prompt": (
            "A rectangular 16:9 horizontal logo for an Airbnb apartment called 'Sempre Viva'. "
            "Two-color design: dusty terracotta and golden yellow on white background. "
            "Style: Mediterranean rustic, graphic emblem, vintage botanical. "
            "Design: a simple framed rectangular emblem with a single large Helichrysum stoechas "
            "(immortelle) flower in full bloom -- round yellow flower head with papery petals -- "
            "as the central motif. Below or beside the flower: bold serif text 'SEMPRE VIVA' "
            "with a thin decorative line. Small tagline 'Affitti brevi'. "
            "Feels like a handcrafted Mediterranean stamp or label. No gradients, 2 colors max, print-ready."
        )
    },
    {
        "name": "variant_4_arch_composition",
        "prompt": (
            "A rectangular 16:9 horizontal logo for an Airbnb apartment called 'Sempre Viva'. "
            "Two-color design: deep olive green and warm yellow on clean white background. "
            "Style: rustic Mediterranean, illustrated, floral, village feel, like a hand-drawn sign. "
            "Layout: an arched decorative frame made of Helichrysum stoechas (immortelle) flower stems -- "
            "long thin stems topped with small round golden flower clusters -- "
            "forming a natural canopy arch over the text. "
            "Under the arch: 'Sempre Viva' in a large readable hand-lettered style serif font. "
            "Small decorative dots or simple sun motif as accent. "
            "Mediterranean summer countryside atmosphere. Flat illustration, no gradients, 2 colors, print-ready."
        )
    },
]

for i, item in enumerate(prompts, 1):
    print(f"\nGenerating variant {i}/4: {item['name']}...")
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
            print(f"  No images returned for variant {i}")
            continue

        img_data = response.generated_images[0].image.image_bytes
        filepath = output_dir / f"{item['name']}.png"
        filepath.write_bytes(img_data)
        print(f"  Saved: {filepath}")

    except Exception as e:
        print(f"  Error: {e}")

print("\nDone!")
