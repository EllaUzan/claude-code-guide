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
    "oil painting style, painterly thick brushstrokes, whimsical fantasy art, "
    "soft dreamy background, chubby exaggerated proportions, absurdly round and fat body, "
    "magical glowing details, pastel pinks and dusty mauves and soft teals, "
    "cute but slightly unhinged expression, fluffy fur texture, "
    "full body portrait, white or soft dreamy background, no text, no watermark, "
    "highly detailed painterly illustration, charming and funny creature"
)

creatures = [
    {
        "filename": "part2_slide1_crossroads.png",
        "label": "Slide 1 — crossroads creature",
        "prompt": (
            "An absurdly fat and round magical creature, extremely chubby with tiny stubby legs, "
            "standing at a crossroads holding a tiny map upside down, "
            "three or four signposts around it pointing in wildly different directions, "
            "the creature looks mildly puzzled but completely unbothered, "
            "big watery expressive eyes full of gentle confusion, "
            "little pink bow or accessory, rolls of chubby fur everywhere, "
            "endearing and ridiculous, lost but cozy about it. "
            f"{STYLE}"
        )
    },
    {
        "filename": "part2_slide2_hacker.png",
        "label": "Slide 2 — hacker creature",
        "prompt": (
            "An absurdly round and fat magical fluffy creature wearing a tiny dark hoodie, "
            "the hoodie barely fits over its enormous chubby body, "
            "sitting in front of a tiny glowing black screen looking extremely cozy, "
            "holding a steaming cup of tea with tiny stubby paws, "
            "big sleepy half-closed eyes, completely harmless and soft despite the dramatic hacker vibe, "
            "little glowing sparkles around it, aggressively non-threatening, "
            "rolls of fluff spilling everywhere, adorably ridiculous. "
            f"{STYLE}"
        )
    },
    {
        "filename": "part2_slide3_cockpit.png",
        "label": "Slide 3 — cockpit creature",
        "prompt": (
            "An enormously fat and round magical creature squeezed into a tiny pilot seat, "
            "its chubby body overflows the seat on all sides, "
            "surrounded by hundreds of colorful glowing buttons and levers, "
            "wearing a tiny helmet that sits comically on top of its round head, "
            "one tiny stubby paw hovering with great drama over a big red button, "
            "expression of intense concentration while clearly having no idea what anything does, "
            "rolls of soft fur, wide determined eyes, completely out of its depth but very committed. "
            f"{STYLE}"
        )
    },
    {
        "filename": "part2_slide4_trio.png",
        "label": "Slide 4 — three creatures",
        "prompt": (
            "Three absurdly chubby round magical creatures standing side by side, all very fat and fluffy, "
            "right creature is beaming with a huge warm smile, waving a tiny stubby arm, wearing a little pink bow, very approachable, "
            "middle creature has arms crossed with a serious no-nonsense expression, still incredibly round and soft, "
            "left creature is wearing a tiny suit jacket and miniature glasses, holding a comically small briefcase, looks very important, "
            "all three are equally round and ridiculous, different personalities same chubby body type, "
            "group portrait, magical glowing aura around all three. "
            f"{STYLE}"
        )
    },
]

for c in creatures:
    print(f"\n🎨 Generating: {c['label']}...")
    try:
        result = fal_client.subscribe(
            "fal-ai/imagen4",
            arguments={
                "prompt": c["prompt"],
                "image_size": "portrait_4_3",
                "num_images": 1,
            },
            with_logs=True,
            on_queue_update=lambda u: print(f"   ↳ {u.status}") if hasattr(u, "status") else None,
        )
        image_url = result["images"][0]["url"]
        out_path = OUTPUT_DIR / c["filename"]
        resp = requests.get(image_url, timeout=60)
        resp.raise_for_status()
        out_path.write_bytes(resp.content)
        print(f"✅ Saved: {out_path.name}")
    except Exception as e:
        print(f"❌ Failed: {e}")

print("\n🎉 Done! All part 2 creatures generated.")
