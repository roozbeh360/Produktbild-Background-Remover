import os

# OPTIONAL (Hugging Face Token):
# Wenn Sie Download-Verzögerungen oder Warnungen erhalten, erstellen Sie einen 
# kostenlosen Token (Berechtigung: Read) unter https://huggingface.co/settings/tokens
# Entfernen Sie das Gatter-Symbol (#) der folgenden Zeile und fügen Sie Ihren Token ein:
# os.environ["HF_TOKEN"] = "hf_ihr_tatsaechlicher_token_hier"

import torch
from PIL import Image
from loadimg import load_img
from nobg import AutoModel, AutoProcessor

# Pfad zum Bilderordner
folder = "./parts_images"
# Name der Logo-Datei
logo_filename = "logo.png"

# KI-Modell und Prozessor laden
model = AutoModel.from_pretrained("feyninc/FeyNobg").eval()
processor = AutoProcessor.from_pretrained("feyninc/FeyNobg")

# Logo laden und auf 100px Breite skalieren (falls vorhanden)
logo_image = None
if os.path.exists(logo_filename):
try:
logo_image = Image.open(logo_filename).convert("RGBA")
logo_max_width = 100
logo_ratio = logo_max_width / logo_image.width
logo_new_height = int(logo_image.height * logo_ratio)
logo_image = logo_image.resize((logo_max_width, logo_new_height), Image.Resampling.LANCZOS)
print("Logo erfolgreich geladen und skaliert.")
except Exception as e:
print(f"Fehler beim Laden des Logos: {e}")
else:
print(f"Warnung: Logo-Datei '{logo_filename}' nicht gefunden. Die dritte Bildvariante wird ohne Logo gespeichert.")

for filename in os.listdir(folder):
# Nur erlaubte Bildformate verarbeiten und bereits generierte Dateien ignorieren
if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp")):
continue
if "_nobg" in filename or "_white" in filename or filename == logo_filename:
continue

input_path = os.path.join(folder, filename)
name, _ = os.path.splitext(filename)

output_path_nobg = os.path.join(folder, f"{name}_nobg.png")
output_path_white = os.path.join(folder, f"{name}_white_1080x1080.png")
output_path_logo = os.path.join(folder, f"{name}_white_with_logo_1080x1080.png")

print("Verarbeite Bild:", filename)

try:
# 1. Bild laden und Hintergrund entfernen
image = load_img(input_path).convert("RGB")
inputs = processor(image, return_tensors="pt")

with torch.no_grad():
outputs = model(pixel_values=inputs["pixel_values"])

alpha = processor.post_process_alpha_matting(
outputs,
target_sizes=[(image.height, image.width)]
)[0]

# Variante 1: Freigestelltes Bild (Transparent, Originalausrichtung) speichern
cutout_image = processor.cutout(image, alpha)
cutout_image.save(output_path_nobg)

# Produktbild für die Studio-Hintergründe um 90 Grad nach rechts drehen
rotated_cutout = cutout_image.transpose(Image.Transpose.ROTATE_270)

# 2. Variante 2: Erstellung des weißen Studio-Hintergrunds (1080x1080px)
white_bg = Image.new("RGBA", (1080, 1080), (255, 255, 255, 255))

# Nutzbereich mit 100px Rand (1080 - 100 - 100 = 880px)
target_area_size = 880

# Proportionale Skalierung berechnen
width_ratio = target_area_size / rotated_cutout.width
height_ratio = target_area_size / rotated_cutout.height
scale_ratio = min(width_ratio, height_ratio)

new_width = int(rotated_cutout.width * scale_ratio)
new_height = int(rotated_cutout.height * scale_ratio)

# Einmalige, hochqualitative Skalierung mit Lanczos-Filter gegen Textunschärfe
resized_product = rotated_cutout.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Zentrierung auf dem 1080px-Balken
offset_x = (1080 - new_width) // 2
offset_y = (1080 - new_height) // 2

# Produkt auf den weißen Hintergrund setzen
white_bg.paste(resized_product, (offset_x, offset_y), resized_product)

# Speichern als JPG/RGB (ohne Alpha-Kanal für E-Commerce optimiert)
white_bg.convert("RGB").save(output_path_white)
print(f"Gespeichert: {output_path_white}")

# 3. Variante 3: Logo hinzufügen (oben links bei X:50, Y:50)
if logo_image is not None:
white_bg_with_logo = white_bg.copy()
white_bg_with_logo.paste(logo_image, (50, 50), logo_image)
white_bg_with_logo.convert("RGB").save(output_path_logo)
print(f"Gespeichert: {output_path_logo}")
else:
white_bg.convert("RGB").save(output_path_logo)

except Exception as e:
print(f"Fehler bei der Verarbeitung von {filename}: {e}")

print("Verarbeitung abgeschlossen.")
