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

STYLE = (
    "oil painting style, painterly thick brushstrokes, whimsical fantasy art, "
    "soft dreamy background, chubby exaggerated proportions, absurdly round and fat body, "
    "magical glowing details, pastel pinks and dusty mauves and soft teals, "
    "cute but slightly unhinged expression, fluffy fur texture, "
    "full body portrait, white or soft dreamy background, no text, no watermark, "
    "highly detailed painterly illustration, charming and funny creature"
)

prompt = (
    "An absurdly fat and round magical fluffy creature sitting in front of a glowing computer screen, "
    "both tiny stubby paws pressed together in a prayer or pleading gesture, "
    "eyes squeezed shut with intense hopeful concentration, "
    "expression of desperate optimism — like someone who really really wants something to work, "
    "small magical sparkles floating around it, "
    "rolls of chubby fluff everywhere, tiny stubby legs dangling, "
    "completely endearing and slightly ridiculous, anxious but hopeful vibes. "
    + STYLE
)

print("🤞 Generating install creature...")

result = fal_client.subscribe(
    "fal-ai/imagen4",
    arguments={
        "prompt": prompt,
        "image_size": "portrait_4_3",
        "num_images": 1,
    },
    with_logs=True,
    on_queue_update=lambda u: print(f"   ↳ {u.status}") if hasattr(u, "status") else None,
)

image_url = result["images"][0]["url"]
out_path = OUTPUT_DIR / "part2_install_hope.png"
resp = requests.get(image_url, timeout=60)
resp.raise_for_status()
out_path.write_bytes(resp.content)
print(f"✅ Saved: {out_path.name}")
