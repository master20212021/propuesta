"""
Dulce y Salado — Image Generation Script
Eros Marketing — Powered by DALL-E 3

Generates professional images for the advertising proposal:
1. Logo
2. Caballete (A-Frame sidewalk sign)
3. Horizontal Banner (7ft x 13in)

Usage: python generate_images.py
Requires: OPENAI_API_KEY environment variable
"""

import os
import sys
import time
import requests
from pathlib import Path
from openai import OpenAI

# ----- Configuration -----
OUTPUT_DIR = Path(__file__).parent / "assets" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Get API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("ERROR: Set OPENAI_API_KEY environment variable first")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# ----- Image Definitions -----
IMAGES = [
    {
        "name": "logo_dulce_y_salado",
        "filename": "logo.png",
        "size": "1024x1024",
        "prompt": (
            "Design a premium restaurant brand logo on a clean solid cream-white background. "
            "The brand is called 'DULCE y SALADO' — a Latin street food stand in New York City "
            "that sells handmade empanadas (chicken, beef, cheese, guava with cheese), coffee, "
            "and passion fruit juice. It is located on a sidewalk in front of a hospital. "
            "\n\n"
            "LOGO COMPOSITION (centered, balanced layout):\n"
            "— TOP CENTER: A stylized golden sun icon with short rays, warm and inviting, "
            "symbolizing warmth and fresh-baked goodness.\n"
            "— MAIN TEXT below the sun: 'DULCE' in bold elegant serif font (dark brown #6B4226), "
            "then a small decorative italic 'y' in gold (#FFB830), "
            "then 'SALADO' in the same bold serif font matching 'DULCE'. "
            "The word arrangement should be stacked: DULCE on top, small 'y' in the middle, SALADO below.\n"
            "— DECORATIVE ELEMENTS: Small ornamental wheat/leaf flourishes flanking the text on both sides, "
            "in muted gold (#D4A054). A thin decorative line separator below the name.\n"
            "— TAGLINE below the separator: 'EMPANADAS ARTESANALES • NYC' "
            "in a clean sans-serif font, small, spaced-out tracking, dark brown color.\n"
            "— BOTTOM TAGLINE: 'Sabor que te reconforta' in a flowing calligraphic/script font, "
            "warm red-brown (#8B2500), adding a personal handmade touch.\n"
            "\n"
            "COLOR PALETTE: Deep warm red (#8B2500), golden yellow (#FFB830), "
            "toasted gold (#D4A054), cream (#FFF8E7), dark brown (#6B4226). "
            "Background should be solid clean white or very soft cream.\n"
            "\n"
            "STYLE: Vector-style flat logo design. Think premium artisan food branding — "
            "like a high-end bakery or specialty food shop logo you'd see on packaging, menus, "
            "and signage. Clean, professional, timeless. Symmetrical composition. "
            "NO photographs, NO 3D renders, NO photographic textures. "
            "Purely a 2D graphic logo mark suitable for printing on bags, cups, signs, and uniforms. "
            "Inspired by brands like Empanada Mama, Pret A Manger, or artisan bakery logos."
        ),
    },
    {
        "name": "caballete_aframe",
        "filename": "caballete.png",
        "size": "1024x1792",
        "prompt": (
            "Photorealistic image of an A-frame sidewalk sign (caballete) on a New York City sidewalk, "
            "placed in front of a hospital entrance. The sign is a professional printed board with: "
            "Top: 'DULCE y SALADO' logo with a small sun icon, warm golden and red branding. "
            "Center: A large, extremely appetizing close-up photo of golden crispy empanadas cut in half "
            "showing melted cheese and meat filling, steam rising, looking incredibly delicious and mouthwatering. "
            "Below the empanada image: menu items listed as 'Pollo | Chicken', 'Carne | Beef', 'Queso | Cheese', "
            "'Guayaba con Queso | Guava with Cheese'. "
            "Also showing 'Café | Coffee' and 'Jugo de Maracuyá | Passion Fruit Juice'. "
            "Bottom: 'Sabor que te reconforta' tagline. "
            "The sign board has warm cream and golden yellow background with professional food photography feel. "
            "NYC street setting, natural daylight, people walking in background blur, taxi visible, "
            "hospital building behind. Hyperrealistic food photography style."
        ),
    },
    {
        "name": "banner_horizontal",
        "filename": "banner_horizontal.png",
        "size": "1792x1024",
        "prompt": (
            "Photorealistic horizontal advertising banner for an empanada food stand, dimensions proportional to 7 feet wide by 13 inches tall. "
            "LEFT SIDE: 'DULCE y SALADO' brand logo in warm red and golden typography with a small sun icon, "
            "on a cream background section. "
            "CENTER AND RIGHT: Extremely appetizing food photography showing golden crispy empanadas — "
            "one cut open revealing delicious melted cheese and shredded chicken filling, steam rising. "
            "Next to it, a cup of fresh hot coffee and a glass of passion fruit juice (maracuyá) with condensation. "
            "The background transitions from warm cream on the left to vibrant food photography on the right. "
            "Bottom strip with menu items: '🐔 Pollo · 🥩 Carne · 🧀 Queso · 🍈 Guayaba con Queso · ☕ Café · 🧃 Jugo de Maracuyá'. "
            "Professional food advertising quality, warm lighting, looks absolutely delicious and inviting. "
            "Style: commercial food photography, billboard advertising quality."
        ),
    },
]


def download_image(url: str, filepath: Path) -> bool:
    """Download an image from URL and save to filepath."""
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        filepath.write_bytes(response.content)
        return True
    except Exception as e:
        print(f"  ERROR downloading: {e}")
        return False


def generate_image(image_def: dict) -> bool:
    """Generate a single image using DALL-E 3."""
    name = image_def["name"]
    filename = image_def["filename"]
    filepath = OUTPUT_DIR / filename
    
    print(f"\n{'='*60}")
    print(f"  Generating: {name}")
    print(f"  Size: {image_def['size']}")
    print(f"  Output: {filepath}")
    print(f"{'='*60}")
    
    try:
        print("  Calling DALL-E 3 API...")
        start = time.time()
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_def["prompt"],
            size=image_def["size"],
            quality="hd",
            n=1,
        )
        
        elapsed = time.time() - start
        print(f"  Generated in {elapsed:.1f}s")
        
        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt
        
        print(f"  Revised prompt: {revised_prompt[:120]}...")
        print(f"  Downloading...")
        
        if download_image(image_url, filepath):
            size_kb = filepath.stat().st_size / 1024
            print(f"  ✅ Saved: {filepath} ({size_kb:.0f} KB)")
            return True
        return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("  DULCE Y SALADO — Image Generation")
    print("  Powered by DALL-E 3 | Eros Marketing")
    print("=" * 60)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print(f"Images to generate: {len(IMAGES)}")
    
    results = []
    for i, img in enumerate(IMAGES, 1):
        print(f"\n[{i}/{len(IMAGES)}]", end="")
        success = generate_image(img)
        results.append((img["name"], success))
        
        # Small delay between requests to be polite
        if i < len(IMAGES):
            print("  Waiting 3s before next request...")
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {name}")
    
    successful = sum(1 for _, s in results if s)
    print(f"\n  {successful}/{len(results)} images generated successfully")
    print(f"  Files in: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
