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
    "Scandinavian illustration, white background, no text, no watermark"
)

prompt = (
    f"A chubby bear with a single unicorn horn on its forehead, wearing tiny round glasses, "
    f"sitting at a small desk surrounded by tall stacks of folders and files, "
    f"focused and diligent, quietly working, holding a tiny pencil, "
    f"magical and quirky hybrid creature, warm and charming personality. {STYLE}"
)

print("🦄🐻 Generating Bear-Unicorn...")
print(f"Prompt: {prompt[:100]}...")

result = fal_client.subscribe(
    "fal-ai/imagen4",
    arguments={
        "prompt": prompt,
        "image_size": "portrait_4_3",
        "num_images": 1,
    },
    with_logs=True,
    on_queue_update=lambda u: print(f"   ↳ {u.status}") if hasattr(u, "status") else None,
)

image_url = result["images"][0]["url"]
out_path = OUTPUT_DIR / "bear_unicorn.png"

resp = requests.get(image_url, timeout=60)
resp.raise_for_status()
out_path.write_bytes(resp.content)

print(f"✅ Saved: {out_path}")
