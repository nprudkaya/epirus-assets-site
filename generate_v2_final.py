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

prompt = (
    "A rectangular 16:9 horizontal logo for an Airbnb apartment called 'Sempre Viva'. "
    "Two-color design: sage green and warm ochre/golden yellow on ivory cream background. "
    "Style: rustic Mediterranean botanical illustration, clean graphic lines, floral, hand-drawn feel. "
    "Upper portion: a long decorative branch of Helichrysum stoechas (immortelle) stretching horizontally across the image, "
    "with narrow grey-green leaves along the stem and exactly one single cluster of small round golden-yellow flowers at one tip of the branch. "
    "Lower portion: the text 'Sempre Viva' in large elegant italic serif font in sage green, centered below the branch. "
    "Light, airy, countryside Mediterranean feel. No gradients, botanical illustration style, print-ready."
)

print("Generating variant_2_final...")
try:
    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="16:9",
            output_mime_type="image/png",
        )
    )

    if not response.generated_images:
        print("No images returned")
        sys.exit(1)

    img_data = response.generated_images[0].image.image_bytes
    filepath = output_dir / "variant_2_final.png"
    filepath.write_bytes(img_data)
    print(f"Saved: {filepath}")

except Exception as e:
    print(f"Error: {e}")
