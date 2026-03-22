import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
import fal_client

# Load FAL_KEY
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

CHARACTERS = [
    {
        "id": "chatgpt_girl",
        "label": "ChatGPT Girl",
        "prompt": (
            f"A cute generic woman with round glasses, plain simple appearance, "
            f"wearing comfortable home clothes, sitting at home looking friendly but basic, "
            f"holding a phone, slightly plain girl-next-door look, warm smile. {STYLE}"
        ),
    },
    {
        "id": "claude_code_girl",
        "label": "Claude Code Girl",
        "prompt": (
            f"A cool stylish woman with bright pink hair, round glasses, "
            f"a small fluffy cat sitting on top of her head, energetic confident pose, "
            f"hands ready to work, magical and quirky personality, "
            f"a bit fantastical and fun. {STYLE}"
        ),
    },
]

MODEL = "fal-ai/imagen4"

def generate_character(char: dict) -> Path:
    print(f"\n🎨 Generating: {char['label']}...")
    print(f"   Prompt: {char['prompt'][:80]}...")

    result = fal_client.subscribe(
        MODEL,
        arguments={
            "prompt": char["prompt"],
            "image_size": "portrait_4_3",
            "num_images": 1,
        },
        with_logs=True,
        on_queue_update=lambda u: print(f"   ↳ {u.status}") if hasattr(u, "status") else None,
    )

    image_url = result["images"][0]["url"]
    out_path = OUTPUT_DIR / f"{char['id']}.png"

    print(f"   ⬇️  Downloading...")
    resp = requests.get(image_url, timeout=60)
    resp.raise_for_status()
    out_path.write_bytes(resp.content)

    print(f"   ✅ Saved: {out_path.name}")
    return out_path

def main():
    print("═" * 50)
    print("🐾 Character Generator — Claude Code Course")
    print("═" * 50)
    print(f"Model: {MODEL}")
    print(f"Output: {OUTPUT_DIR}")

    for char in CHARACTERS:
        try:
            path = generate_character(char)
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n═" * 50)
    print("✅ Done! Check the תמונות folder.")

if __name__ == "__main__":
    main()
