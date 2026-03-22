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

creatures = [
    {
        "file": "preview_slide2.png",
        "emoji": "✅",
        "prompt": (
            f"A small fluffy bear or fox standing proudly, sleeves rolled up, "
            f"leaning casually on a tiny finished project or toolbox, "
            f"satisfied done-for-the-day expression, slightly tired but very pleased with itself, "
            f"the energy of someone who already finished before you even asked. {STYLE}"
        ),
    },
    {
        "file": "preview_slide3_chatgpt.png",
        "emoji": "🛋️",
        "prompt": (
            f"A very cozy plump cat or rabbit sitting deep in a big armchair at home, "
            f"wrapped in a blanket, waving hello from far away with one paw, "
            f"clearly not moving anywhere, content and settled in her own space, "
            f"homebody energy, comfortable but distant. {STYLE}"
        ),
    },
    {
        "file": "preview_slide3_claude.png",
        "emoji": "🚪",
        "prompt": (
            f"A friendly energetic fox or hedgehog standing right at a doorstep, "
            f"wearing a little coat and carrying a small bag of tools, "
            f"knocking or ringing the bell, eager ready-to-work expression, "
            f"just arrived and can't wait to start, full of helpful energy. {STYLE}"
        ),
    },
]

print("🎨 Generating preview images (won't replace anything)...\n")

for c in creatures:
    print(f"{c['emoji']} Generating {c['file']}...")
    result = fal_client.subscribe(
        "fal-ai/imagen4",
        arguments={
            "prompt": c["prompt"],
            "image_size": "portrait_4_3",
            "num_images": 1,
        },
        with_logs=False,
        on_queue_update=lambda u: print(f"   ↳ {u.status}") if hasattr(u, "status") else None,
    )
    image_url = result["images"][0]["url"]
    out_path = OUTPUT_DIR / c["file"]
    resp = requests.get(image_url, timeout=60)
    resp.raise_for_status()
    out_path.write_bytes(resp.content)
    print(f"   ✅ {out_path.name}\n")

print("👀 שלוש תמונות בתיקיית תמונות — preview_slide2, preview_slide3_chatgpt, preview_slide3_claude")
print("אפשר לראות ולאשר לפני שמחליפים כלום.")
