# 🎨 VibePalette – Smart Image Color Palette Extractor

VibePalette is a sleek **web + machine learning** application that extracts dominant colors from any uploaded image and generates a **vibe profile** based on color science.

🧠 Powered by  
- **KMeans Clustering** (for palette extraction)  
- **HSL Color Analysis** (for mood & tone detection)  
- **Flask + Python** Backend  
- Modern, glass-aesthetic UI ✨  

Perfect for:
- UI/UX designers
- Branding inspiration
- Aesthetic analysis
- Quick color palette generation

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🖼️ Upload any image | Supports JPG & PNG |
| 🎯 KMeans ML model | Extracts 3–8 dominant colors |
| 🎨 Click-to-copy | Copy hex color codes directly |
| 🔍 Vibe Analysis | Determines mood using color science |
| 📊 Stats | Lightness, saturation & warm/cool ratio bars |
| 💎 Premium UI | Minimal + futuristic dark theme with effects |
| 🪄 Drag & Drop | Smooth file upload interaction |

---

## 🧠 How It Works

1️⃣ Image resized for processing  
2️⃣ KMeans clusters pixel colors  
3️⃣ Dominant RGB → **HEX + HSL conversion**  
4️⃣ Color psychology heuristics determine:
- Mood (soft, dramatic, warm, cool…)  
- Description tagline  
- Color composition stats  

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS (custom UI effects, animations)
- **Backend:** Flask (Python)
- **Machine Learning:** scikit-learn (KMeans)
- **Image Processing:** Pillow (PIL)
- **Data:** Pixel RGB values

---

## 📦 Installation & Setup

```bash
git clone https://github.com/yourusername/vibepalette.git
cd vibepalette
 ## 📦 Installation & Setup

Create & activate a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

## ▶️ Run the Project

Install dependencies:

```bash
pip install -r requirements.txt

Run the app:

python app.py


Then open in browser:

http://127.0.0.1:5000/

---

