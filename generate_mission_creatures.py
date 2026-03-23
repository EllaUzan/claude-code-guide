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
        "file": "preview_unicorn_monkey.png",
        "emoji": "🦄",
        "prompt": (
            f"A small round monkey with a single glittery unicorn horn on its head, "
            f"proudly riding on the back of a large calm swan, "
            f"the monkey sits upright and confident like it absolutely belongs there, "
            f"the swan is graceful and unbothered, "
            f"the energy of 'yes this is completely normal and I am thriving'. {STYLE}"
        ),
    },
    {
        "file": "preview_rhino_tutu.png",
        "emoji": "🩰",
        "prompt": (
            f"A chubby round rhinoceros wearing a delicate pink tutu ballet skirt, "
            f"standing on tiptoe in a ballet pose with tiny arms raised gracefully, "
            f"completely serious expression — this rhino is a professional ballerina "
            f"and does not find this unusual at all, "
            f"the energy of total commitment to the art. {STYLE}"
        ),
    },
    {
        "file": "preview_zebra_rabbit.png",
        "emoji": "🐇",
        "prompt": (
            f"A fluffy rabbit covered in bold zebra stripes instead of plain white fur, "
            f"wearing a small dapper bow tie at the neck, "
            f"sitting upright with a dignified expression, very proud of its unique look, "
            f"the energy of someone who dressed themselves and has no notes. {STYLE}"
        ),
    },
]

print("🎨 Generating mission creatures...\n")

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

print("👀 שלושת היצורים בתיקייה — מחכים לאישור לפני שמכניסים לסלייד")
