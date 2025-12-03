from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import io
import base64
from colorsys import rgb_to_hls

app = Flask(__name__)

def extract_palette(image_file, n_colors=5):
    """Run KMeans on the image and return a list of dicts: {hex, rgb}."""
    image = Image.open(image_file).convert("RGB")
    # Resize for speed and consistency
    image = image.resize((150, 150))
    img_array = np.array(image)
    pixels = img_array.reshape(-1, 3)

    # IMPORTANT: n_clusters = n_colors (this is what needs to change)
    kmeans = KMeans(n_clusters=n_colors, n_init=10, random_state=42)
    kmeans.fit(pixels)
    centers = kmeans.cluster_centers_.astype(int)  # (n_colors, 3)

    palette = []
    for r, g, b in centers:
        hex_code = "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))
        palette.append(
            {
                "hex": hex_code,
                "rgb": (int(r), int(g), int(b)),
            }
        )
    return palette

def analyze_palette(palette):
    """
    Take palette [{hex, rgb}] and compute:
    - average lightness
    - average saturation
    - warm color ratio
    - a simple mood + description
    """
    if not palette:
        return None

    hsls = []
    warm_count = 0

    for color in palette:
        r, g, b = color["rgb"]
        # Normalize to 0–1 for colorsys
        r_n, g_n, b_n = r / 255.0, g / 255.0, b / 255.0
        # rgb_to_hls returns: (h, l, s)
        h, l, s = rgb_to_hls(r_n, g_n, b_n)
        hsls.append({"h": h, "l": l, "s": s})

        # Rough warm vs cool heuristic (reds / oranges / yellows)
        if (0.00 <= h <= 0.08) or (0.08 < h <= 0.20) or (h >= 0.92):
            warm_count += 1

    avg_l = sum(c["l"] for c in hsls) / len(hsls)
    avg_s = sum(c["s"] for c in hsls) / len(hsls)
    warm_ratio = warm_count / len(hsls)

    # Derive a "mood" label based on thresholds
    if avg_l > 0.7 and avg_s < 0.4:
        mood = "Soft & airy"
        tagline = "Light neutrals and gentle tones – calm, minimal aesthetic."
    elif avg_l < 0.4 and avg_s > 0.5:
        mood = "Deep & dramatic"
        tagline = "Bold, high-contrast colors – cinematic and intense."
    elif avg_s < 0.3:
        mood = "Muted & understated"
        tagline = "Desaturated shades – editorial, professional feel."
    elif warm_ratio > 0.6:
        mood = "Warm & inviting"
        tagline = "Cozy, welcoming palette with golden or earthy undertones."
    else:
        mood = "Cool & modern"
        tagline = "Clean, cool-leaning tones – great for tech and product UIs."

    return {
        "avg_lightness": round(avg_l * 100),
        "avg_saturation": round(avg_s * 100),
        "warm_ratio": round(warm_ratio * 100),
        "mood": mood,
        "tagline": tagline,
    }

def image_to_base64(image_file):
    image = Image.open(image_file).convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    img_bytes = buffer.read()
    return base64.b64encode(img_bytes).decode("utf-8")

@app.route("/", methods=["GET", "POST"])
def index():
    colors = None
    img_data = None
    palette_stats = None

    # default palette size
    palette_size = 5

    if request.method == "POST":
        # Read palette size from form
        palette_size_raw = request.form.get("palette_size", "5")
        try:
            palette_size = int(palette_size_raw)
        except ValueError:
            palette_size = 5

        # Clamp between 3 and 8 to avoid weird inputs
        palette_size = max(3, min(8, palette_size))

        file = request.files.get("image")
        if file and file.filename != "":
            file_bytes = file.read()

            # Extract palette (THIS uses palette_size)
            palette = extract_palette(io.BytesIO(file_bytes), n_colors=palette_size)
            palette_stats = analyze_palette(palette)

            colors = [c["hex"] for c in palette]
            img_data = image_to_base64(io.BytesIO(file_bytes))

    return render_template(
        "index.html",
        colors=colors,
        img_data=img_data,
        palette_stats=palette_stats,
        palette_size=palette_size,
    )

if __name__ == "__main__":
    app.run(debug=True)
