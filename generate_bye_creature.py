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
    f"A chubby round ginger cat with tiny little wings sitting proudly on top of the head of a polka-dot horse, "
    f"the cat is very fat and very ginger and looks completely unbothered by the situation, "
    f"the wings are absurdly small — clearly decorative, not functional, "
    f"the horse has big round polka dots all over its body and a calm accepting expression, "
    f"as if this is simply how life is now and it has made peace with it, "
    f"the energy of two creatures who found each other and decided this works. {STYLE}"
)

print("🐱 Generating bye creature...")

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
out_path = OUTPUT_DIR / "preview_bye_creature.png"
import time
for attempt in range(5):
    resp = requests.get(image_url, timeout=60)
    if resp.status_code == 200:
        break
    print(f"   ↳ retry {attempt+1}...")
    time.sleep(3)
resp.raise_for_status()
out_path.write_bytes(resp.content)
print(f"✅ Saved: {out_path}")
print("👀 preview_bye_creature.png בתיקייה — מחכה לאישור")
