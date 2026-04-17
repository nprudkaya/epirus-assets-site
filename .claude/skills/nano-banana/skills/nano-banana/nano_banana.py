#!/usr/bin/env python3
"""
Nano Banana Image Generator
Generates images using Google's Gemini model.
Supports reference images for style transfer.

Requires: pip install google-genai
Requires: GEMINI_API_KEY in .env or environment
"""

import os
import sys
import argparse
import base64
from pathlib import Path
from datetime import datetime


def find_env_file():
    """Search for .env file in current directory and parents."""
    path = Path.cwd()
    while path != path.parent:
        env = path / ".env"
        if env.exists():
            return env
        path = path.parent
    return None


def load_env():
    """Load .env file if found."""
    env_file = find_env_file()
    if env_file:
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value


load_env()

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Installing google-genai...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "-q"])
    from google import genai
    from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment or .env file")
    sys.exit(1)

client = genai.Client(api_key=api_key)


def load_reference_image(image_path: str) -> tuple[bytes, str]:
    """Load reference image and determine mime type."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Reference image not found: {image_path}")

    suffix = path.suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    return path.read_bytes(), mime_types.get(suffix, 'image/jpeg')


def generate_image(prompt: str, reference_path: str = None, model: str = "gemini-2.0-flash-exp", aspect_ratio: str = None, image_size: str = None) -> tuple[bytes, str]:
    """Generate image using Gemini model, optionally with reference."""

    if reference_path:
        ref_data, ref_mime = load_reference_image(reference_path)
        contents = [
            types.Part.from_bytes(data=ref_data, mime_type=ref_mime),
            f"Using the attached image as a style reference, generate: {prompt}"
        ]
    else:
        contents = prompt

    config_kwargs = {
        'response_modalities': ['IMAGE', 'TEXT']
    }
    image_config_kwargs = {}
    if aspect_ratio:
        image_config_kwargs['aspect_ratio'] = aspect_ratio
    if image_size:
        image_config_kwargs['image_size'] = image_size
    if image_config_kwargs:
        config_kwargs['image_config'] = types.ImageConfig(**image_config_kwargs)

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(**config_kwargs)
    )

    if not response.candidates:
        raise Exception("No candidates in response — image may have been blocked")

    candidate = response.candidates[0]
    if hasattr(candidate, 'finish_reason'):
        finish_reason = str(candidate.finish_reason)
        if 'SAFETY' in finish_reason or 'BLOCK' in finish_reason or 'OTHER' in finish_reason:
            raise Exception(f"Image blocked by safety filter: {finish_reason}")

    if not candidate.content or not candidate.content.parts:
        raise Exception("No content in response — try a different prompt")

    for part in candidate.content.parts:
        if part.inline_data is not None:
            return part.inline_data.data, part.inline_data.mime_type

    raise Exception("No image in response — model returned text only")


def main():
    parser = argparse.ArgumentParser(description='Generate images with Nano Banana (Gemini)')
    parser.add_argument('idea', nargs='*', help='Your image idea/prompt')
    parser.add_argument('-r', '--ref', '--reference', dest='reference',
                        help='Path to reference image for style transfer')
    parser.add_argument('-o', '--output', dest='output',
                        help='Output file path (default: auto-generated in current dir)')
    parser.add_argument('--pro', action='store_true',
                        help='Use Gemini Pro (slower but best quality)')
    parser.add_argument('--aspect', '-a', dest='aspect_ratio',
                        help='Aspect ratio (e.g. 16:9, 1:1, 4:3, 9:16)')
    parser.add_argument('--size', '-s', dest='image_size',
                        help='Image size: 0.5K, 1K, 2K, 4K')
    parser.add_argument('--no-open', action='store_true',
                        help='Do not auto-open the generated image')

    args = parser.parse_args()

    if not args.idea:
        print("Usage: python3 nano_banana.py <your image idea>")
        print("       python3 nano_banana.py -r style.jpg 'create similar style'")
        sys.exit(1)

    idea = " ".join(args.idea)

    try:
        model = "gemini-2.0-flash-exp" if not args.pro else "gemini-2.0-flash-exp"
        print(f"Generating: {idea}")
        if args.reference:
            print(f"Reference: {args.reference}")

        image_data, mime_type = generate_image(
            idea, args.reference,
            model=model,
            aspect_ratio=args.aspect_ratio,
            image_size=args.image_size
        )

        ext = "png" if "png" in mime_type else "jpg"
        if args.output:
            filepath = args.output
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filepath = f"nano-banana-{timestamp}.{ext}"

        Path(filepath).write_bytes(image_data)
        print(f"Saved: {filepath}")

        if not args.no_open:
            import subprocess
            import platform
            if platform.system() == "Darwin":
                subprocess.run(['open', filepath])
            elif platform.system() == "Linux":
                subprocess.run(['xdg-open', filepath])

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
