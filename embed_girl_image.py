#!/usr/bin/env python3
"""Embed the girl PNG as a data URL in firefly-girl.html (required for file:// and reliable Three.js textures)."""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "firefly-girl.html"


def main():
    img = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "assets" / "girl.png"
    if not img.is_file():
        sys.exit(f"Image not found: {img}")
    b64 = base64.standard_b64encode(img.read_bytes()).decode("ascii")
    mime = "image/png"
    if img.suffix.lower() in (".jpg", ".jpeg"):
        mime = "image/jpeg"
    elif img.suffix.lower() == ".webp":
        mime = "image/webp"
    data_url = f"data:{mime};base64,{b64}"
    line = f'const GIRL_IMG_URL="{data_url}";'
    text = HTML.read_text(encoding="utf-8")
    new_text, n = re.subn(r'const GIRL_IMG_URL="[^"]*";', line, text, count=1)
    if n != 1:
        sys.exit("Could not find const GIRL_IMG_URL=... in firefly-girl.html")
    HTML.write_text(new_text, encoding="utf-8")
    print(f"Embedded {img} ({len(data_url)} chars) into {HTML.name}")


if __name__ == "__main__":
    main()
