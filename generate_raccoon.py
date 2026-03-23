import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
import fal_client

load_dotenv('/Users/ellauzan/Desktop/קלודי/.env')
fal_key = os.getenv("FAL_KEY")
if not fal_key:
    print("❌ FAL_KEY not found")
    sys.exit(1)
os.environ["FAL_KEY"] = fal_key

OUTPUT_DIR = Path("/Users/ellauzan/Desktop/קלודי/מדריך קלוד קוד/תמונות")
OUTPUT_DIR.mkdir(exist_ok=True)

STYLE = (
    "folk art illustration, textured grainy brush strokes, children's book style, "
    "muted earthy color palette, dusty pinks and warm browns, flat with texture and dimension, "
    "Scandinavian illustration, white background, simple charming character, full body portrait, "
    "no text, no watermark"
)

prompt = (
    f"A chubby round raccoon with tiny delicate transparent fairy wings on its back, "
    f"gleefully making a mess inside an open folder or filing cabinet, "
    f"papers flying everywhere, files scattered, looking very pleased with itself, "
    f"the wings are small and clearly not built for a raccoon of this size, "
    f"expression of pure chaotic joy — this is its calling, "
    f"the energy of 'I was put on this earth to cause exactly this amount of trouble'. {STYLE}"
)

print("🦝 Generating raccoon creature...")

result = fal_client.subscribe(
    "fal-ai/imagen4",
    arguments={
        "prompt": prompt,
        "image_size": "portrait_4_3",
        "num_images": 1,
    },
    with_logs=False,
    on_queue_update=lambda u: print(f"   ↳ {u.status}") if hasattr(u, "status") else None,
)

image_url = result["images"][0]["url"]
out_path = OUTPUT_DIR / "preview_raccoon.png"
resp = requests.get(image_url, timeout=60)
resp.raise_for_status()
out_path.write_bytes(resp.content)
print(f"✅ Saved: {out_path}")
print("👀 preview_raccoon.png בתיקייה — מחכה לאישור")
