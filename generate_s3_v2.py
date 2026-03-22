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
        "file": "preview_s3_chatgpt_v2.png",
        "emoji": "📱",
        "prompt": (
            f"A sweet fluffy cat wearing a cozy animal onesie with bear ears, "
            f"sitting inside a glowing phone or tablet screen, waving hello with one paw from far away, "
            f"friendly smile but clearly in her own space and staying there, "
            f"the screen frames her like a little window, warm home visible behind her, "
            f"the energy of a friend you FaceTime — close but far. {STYLE}"
        ),
    },
    {
        "file": "preview_s3_claude_v2.png",
        "emoji": "🛋️",
        "prompt": (
            f"A cheerful fox or rabbit wearing a cozy animal onesie with little ears on the hood, "
            f"sitting comfortably on a couch as if she has already moved in and made herself at home, "
            f"holding a small cup of tea, sleeves slightly rolled, ready to help, "
            f"the energy of a best friend who came over and is already on your sofa — "
            f"present, warm, and completely comfortable in your space. {STYLE}"
        ),
    },
]

print("🎨 Generating slide 3 v2 previews...\n")

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

print("👀 preview_s3_chatgpt_v2 ו-preview_s3_claude_v2 בתיקייה — מחכות לאישור")
