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
    "folk art animal illustration, bold graphic outlines, vibrant colors — bright pinks warm oranges vivid greens rich yellows, "
    "playful patterns on fur like dots and stripes and florals, flat illustration with subtle paper texture, "
    "children's book style, white background, full body portrait, character has personality and expressive face, "
    "simple clothing or accessory detail, no text, no watermark"
)

creatures = [
    {
        "file": "bear_unicorn.png",
        "emoji": "🦄",
        "prompt": (
            f"A cheerful round bear wearing a colorful striped outfit, with a tiny glowing horn on its head, "
            f"standing upright, bright wide eyes full of wonder, very expressive and charming. {STYLE}"
        ),
    },
    {
        "file": "chatgpt_girl.png",
        "emoji": "💬",
        "prompt": (
            f"A sweet fluffy cat sitting comfortably far away, waving hello from a distance, "
            f"bright spotted or striped fur pattern, friendly but clearly staying put in her own spot, "
            f"cozy homebody energy. {STYLE}"
        ),
    },
    {
        "file": "claude_code_girl.png",
        "emoji": "💻",
        "prompt": (
            f"A bold colorful fox or rabbit rolling up her sleeves, ready to get to work, "
            f"bright striped or dotted fur, carrying a tiny tool or notebook, "
            f"confident energetic expression, clearly here to help. {STYLE}"
        ),
    },
    {
        "file": "lost_girl.png",
        "emoji": "🗺️",
        "prompt": (
            f"A small round bird or hedgehog with bright patterned feathers or spines, "
            f"looking slightly puzzled and overwhelmed, surrounded by tiny question marks, "
            f"endearing confused expression, holding a tiny crumpled map. {STYLE}"
        ),
    },
    {
        "file": "fluffy_helper.png",
        "emoji": "🧹",
        "prompt": (
            f"A very round fluffy creature — bright green or pink with polka dot pattern — "
            f"wearing a tiny apron, holding a broom or mop with great enthusiasm, "
            f"eager helpful expression, big bright eyes full of excitement, ready to work. {STYLE}"
        ),
    },
    {
        "file": "drumming_goat.png",
        "emoji": "🥁",
        "prompt": (
            f"An extremely chubby goat with bright spotted or striped pattern, almost perfectly round body, "
            f"tiny stubby legs, ridiculous small wings, playing a snare drum dramatically, "
            f"big dopey expressive eyes, slightly goofy announcement energy, ugly-cute and lovable. {STYLE}"
        ),
    },
    {
        "file": "installer_creature.png",
        "emoji": "🔧",
        "prompt": (
            f"A chubby little mole or hamster with vivid dotted or striped fur, "
            f"wearing a tiny hard hat, holding a wrench, very official proud expression, "
            f"carrying a small toolbox, round belly, extremely competent tiny worker energy. {STYLE}"
        ),
    },
    {
        "file": "folder_creature.png",
        "emoji": "📁",
        "prompt": (
            f"A small cozy round bear or rabbit with bright patterned fur sitting peacefully "
            f"inside an open wooden box or crate, looking content and focused only on what is inside, "
            f"the area outside the box is softly shadowy, the creature is happily in its own little world. {STYLE}"
        ),
    },
]

print(f"🎨 Generating {len(creatures)} creatures with new style...\n")

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

print("🎉 All creatures regenerated!")
