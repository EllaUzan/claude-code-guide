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
    "Scandinavian illustration, pure white background, simple charming icon, "
    "small centered composition, no text, no watermark, no border"
)

tips = [
    {
        "file": "tip_hebrew.png",
        "emoji": "💬",
        "prompt": (
            f"A tiny round bird or squirrel cheerfully holding up a small speech bubble "
            f"with squiggly lines on it, looking very pleased and talkative, "
            f"simple icon style, centered on white. {STYLE}"
        ),
    },
    {
        "file": "tip_specific.png",
        "emoji": "🎯",
        "prompt": (
            f"A small focused rabbit or mouse holding a magnifying glass very close to a tiny dot, "
            f"extremely concentrated expression, tip of tongue out, squinting one eye, "
            f"simple icon style, centered on white. {STYLE}"
        ),
    },
    {
        "file": "tip_why.png",
        "emoji": "💡",
        "prompt": (
            f"A round little owl sitting with a tiny glowing lightbulb above its head, "
            f"thoughtful curious expression, one eyebrow raised, looking genuinely interested, "
            f"simple icon style, centered on white. {STYLE}"
        ),
    },
    {
        "file": "tip_mistake.png",
        "emoji": "✏️",
        "prompt": (
            f"A chubby little bear holding a big eraser with both hands, "
            f"calm unbothered expression, already erasing something cheerfully, "
            f"no drama at all, simple icon style, centered on white. {STYLE}"
        ),
    },
    {
        "file": "tip_whatchanged.png",
        "emoji": "🔍",
        "prompt": (
            f"A tiny curious cat peeking over the edge of something with wide eyes, "
            f"very alert and inquisitive, just the head and paws visible, "
            f"simple icon style, centered on white. {STYLE}"
        ),
    },
    {
        "file": "tip_small.png",
        "emoji": "🔪",
        "prompt": (
            f"A small determined hedgehog slicing a large round fruit into neat little pieces "
            f"with a tiny knife, very methodical and proud expression, "
            f"simple icon style, centered on white. {STYLE}"
        ),
    },
]

for tip in tips:
    print(f"{tip['emoji']} Generating {tip['file']}...")
    result = fal_client.subscribe(
        "fal-ai/imagen4",
        arguments={
            "prompt": tip["prompt"],
            "image_size": "square_hd",
            "num_images": 1,
        },
        with_logs=False,
        on_queue_update=lambda u: print(f"   ↳ {u.status}") if hasattr(u, "status") else None,
    )
    image_url = result["images"][0]["url"]
    out_path = OUTPUT_DIR / tip["file"]
    resp = requests.get(image_url, timeout=60)
    resp.raise_for_status()
    out_path.write_bytes(resp.content)
    print(f"   ✅ Saved: {out_path}")

print("\n🎉 All 6 tip icons generated!")
