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
        "file": "bear_unicorn.png",
        "emoji": "🦄",
        "prompt": (
            f"A small fluffy bear with a tiny unicorn horn on its head, standing upright on two legs, "
            f"wide curious eyes, soft round body, gentle and magical expression, "
            f"charming and a little ridiculous in the best way. {STYLE}"
        ),
    },
    {
        "file": "chatgpt_girl.png",
        "emoji": "💬",
        "prompt": (
            f"A sweet fluffy cat sitting comfortably at home, waving hello from a distance, "
            f"cozy and settled, clearly staying in her own spot, friendly homebody energy, "
            f"soft round shape, gentle expression. {STYLE}"
        ),
    },
    {
        "file": "claude_code_girl.png",
        "emoji": "💻",
        "prompt": (
            f"A friendly capable fox or rabbit rolling up her sleeves ready to work, "
            f"carrying a tiny notebook or tool, arrived at your doorstep, confident helpful expression, "
            f"clearly here and ready to get things done. {STYLE}"
        ),
    },
    {
        "file": "lost_girl.png",
        "emoji": "🗺️",
        "prompt": (
            f"A small round bird or hedgehog looking slightly puzzled and overwhelmed, "
            f"surrounded by tiny floating question marks, endearing confused expression, "
            f"holding a tiny crumpled map, lost but hopeful. {STYLE}"
        ),
    },
    {
        "file": "fluffy_helper.png",
        "emoji": "🧹",
        "prompt": (
            f"A very fluffy round monster creature wearing a tiny apron, "
            f"holding a mop or broom, eager helpful expression, big bright eyes full of enthusiasm, "
            f"standing ready to work, small and chubby with lots of soft fur or fluff, "
            f"like a friendly housekeeper creature, charming and a little ridiculous in the best way, "
            f"magical quirky helper vibes. {STYLE}"
        ),
    },
    {
        "file": "drumming_goat.png",
        "emoji": "🥁",
        "prompt": (
            f"An extremely chubby derpy goat, almost perfectly round body, stubby little legs, "
            f"tiny ridiculous wings that could never fly, big dopey eyes, slightly goofy expression, "
            f"playing a snare drum with drumsticks doing a dramatic drumroll announcement, "
            f"ugly-cute in the most lovable way, very round and squishy looking, "
            f"like a potato with legs and tiny wings, endearing and ridiculous at the same time. {STYLE}"
        ),
    },
    {
        "file": "installer_creature.png",
        "emoji": "🔧",
        "prompt": (
            f"A chubby little mole or hamster wearing a tiny hard hat and holding a wrench, "
            f"very official and proud expression, round belly, soft fluffy fur, "
            f"carrying a small toolbox, ready to install something important, "
            f"extremely competent tiny worker energy, endearing and slightly ridiculous. {STYLE}"
        ),
    },
]

print(f"♻️  Restoring {len(creatures)} original creatures...\n")

for c in creatures:
    print(f"{c['emoji']} Restoring {c['file']}...")
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

print("✅ All originals restored! folder_creature.png was left untouched.")
