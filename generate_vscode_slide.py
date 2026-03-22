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

images = [
    {
        "file": "preview_terminal_pan.png",
        "emoji": "🖤",
        "prompt": (
            f"A small round bear or hedgehog standing and eating directly from a frying pan, "
            f"no table, no plate, no napkin — just the creature and the pan, "
            f"slightly chaotic hair, relaxed practical expression, "
            f"the energy of someone who doesn't need ceremony to get things done, "
            f"simple and unbothered. {STYLE}"
        ),
    },
    {
        "file": "preview_vscode_table.png",
        "emoji": "🔷",
        "prompt": (
            f"The same small round bear or hedgehog sitting at a properly set table, "
            f"eating the exact same food but now on a nice plate with a folded napkin and a small candle, "
            f"content and comfortable, everything visible and organized around them, "
            f"the energy of the same meal — just with ambiance and a view of what's on the plate. {STYLE}"
        ),
    },
]

print("🍳 Generating VS Code slide images...\n")

for img in images:
    print(f"{img['emoji']} Generating {img['file']}...")
    result = fal_client.subscribe(
        "fal-ai/imagen4",
        arguments={
            "prompt": img["prompt"],
            "image_size": "portrait_4_3",
            "num_images": 1,
        },
        with_logs=False,
        on_queue_update=lambda u: print(f"   ↳ {u.status}") if hasattr(u, "status") else None,
    )
    image_url = result["images"][0]["url"]
    out_path = OUTPUT_DIR / img["file"]
    resp = requests.get(image_url, timeout=60)
    resp.raise_for_status()
    out_path.write_bytes(resp.content)
    print(f"   ✅ {out_path.name}\n")

print("👀 שתי תמונות בתיקייה — מחכות לאישור לפני שבונים את הסלייד")
