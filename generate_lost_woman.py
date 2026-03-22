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
    f"A small charming exhausted woman completely buried and drowning in a giant pile of papers, "
    f"files, laptops, sticky notes and to-do lists stacked way above her head, "
    f"only her tired face and hands visible peeking out from the pile, "
    f"overwhelmed but relatable expression — the universal feeling of too much work and not enough hours, "
    f"slightly chaotic hair, cute mismatched outfit, "
    f"funny and endearing, the energy of 'this is fine' but it is clearly not fine. {STYLE}"
)

print("📂 Generating overwhelmed woman preview...")

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
out_path = OUTPUT_DIR / "preview_lost_woman.png"
resp = requests.get(image_url, timeout=60)
resp.raise_for_status()
out_path.write_bytes(resp.content)
print(f"✅ Saved: {out_path}")
print("👀 preview_lost_woman.png בתיקייה — מחכה לאישור לפני שמחליף")
