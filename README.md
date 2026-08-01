# Produktbild-Background-Remover
Dieses Python-Skript wurde für die industrielle Produktfotografie und E-Commerce-Bildverarbeitung entwickelt. Es entfernt vollautomatisch den Hintergrund von Produktfotos und erstellt drei standardisierte Bildvarianten für den Online-Shop.

# Produktbild Image Background Remover & Studio Generator

Dieses Python-Skript automatisiert die Freistellung und standardisierte Aufbereitung von Produktbildern für den E-Commerce (optimiert für Produktbild). Es entfernt den Hintergrund mithilfe von KI-Segmentierung, dreht das Produkt um 90° nach rechts und generiert studiofertige Bilder mit optionalem Branding auf einem weißen $1080 \times 1080$ Pixel Canvas mit einem Sicherheitsabstand von 100 Pixeln.

---

## 🚀 Features

- **Automatischer Hintergrund-Entferner:** Nutzt das KI-Modell `feyninc/FeyNobg`.
- **E-Commerce Standard-Format:** Generiert quadratische Bilder ($1080 \times 1080$ Pixel).
- **Automatisches Drehen:** Rotiert das Produktbild für die Studio-Hintergründe um 90° im Uhrzeigersinn.
- **Präzise Skalierung:** Erhält das Seitenverhältnis und hält 100px Abstand zu allen vier Rändern (Nutzbereich: $880 \times 880$px).
- **Branding-Support:** Fügt das Firmenlogo (`logo.png`) oben links bei den Koordinaten `(50, 50)` mit einer Breite von 100px ein.
- **Optimierte Kantenschärfe:** Verwendet den hochwertigen `Lanczos`-Filter zur Vermeidung unscharfer Texte.
- **Batch-Verarbeitung:** Verarbeitet alle gängigen Bildformate (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`) in einem Rutsch.

---

## 📁 Ordnerstruktur

Richten Sie Ihr Projektverzeichnis vor dem Ausführen des Skripts wie folgt ein:
```text
[Projektordner]/
│
├── processor.py             # Das Hauptskript (Python-Code)
├── loadimg.py               # Lokale Import-Abhängigkeit
├── nobg/ (oder nobg.py)     # Lokales KI-Modul
├── logo.png                 # Ihr Firmenlogo (wird auf 100px Breite skaliert)
└── parts_images/            # Eingabeordner für Original-Produktbilder
```

Falls python nicht erkannt wird, verwenden Sie alternativ den Befehl py --version.

## 💾 Installation der benötigten Bibliotheken (Installation)
Führen Sie die folgenden Schritte in der PowerShell aus, um die notwendigen Pakete (PyTorch, Transformers und Pillow für die Bildverarbeitung) zu installieren.

Schritt 1: Pip aktualisieren

python -m ensurepip --upgrade

Schritt 2: PyTorch (CPU-Version) installieren
Da für die automatische Hintergrundentfernung (KI-Segmentierung) Deep-Learning-Modelle genutzt werden, wird PyTorch benötigt:

python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

### Schritt 3: Weitere Abhängigkeiten installieren

Installieren Sie die Bibliotheken für die KI-Modelle (transformers) und die Bildbearbeitung (pillow):

python -m pip install transformers pillow

## 📁 Vorbereitung der Ordnerstruktur (Vorbereitung)

Richten Sie Ihren Projektordner (z. B. D:\Produktfotos) wie folgt ein:

Skript-Datei: Speichern Sie den unten stehenden Python-Code unter dem Namen processor.py in diesem Ordner.
Lokale Module: Stellen Sie sicher, dass sich die Dateien/Ordner loadimg.py und nobg (bzw. nobg.py) im selben Verzeichnis wie Ihre processor.py befinden.
Bilder-Ordner: Erstellen Sie einen Unterordner namens parts_images und legen Sie dort alle rohen Produktfotos ab.
Logo-Datei: Platzieren Sie Ihre Logo-Datei unter dem Namen logo.png direkt im Hauptordner (neben processor.py).
Hugging Face Token (Optional): Wenn Sie Limitierungswarnungen erhalten, können Sie unter huggingface.co/settings/tokens einen kostenlosen Read-Token erstellen und ihn im Code (Zeile 10) eintragen.

## 🏃‍♂️ Ausführung des Skripts (Verwendung)
Navigieren Sie in der PowerShell in Ihren Projektordner und starten Sie das Skript:

cd "D:\project"
python processor.py

## 📦 Generierte Ausgaben
Für jedes Bild (z.B. motor.jpg) im Ordner parts_images werden drei Dateien erzeugt:

motor_nobg.pngFreigestelltes Bild mit transparentem Hintergrund (Originalausrichtung).
motor_white_1080x1080.pngUm 90° nach rechts gedrehtes Produkt, zentriert auf einem weißen 
1080
×
1080
1080×1080
px großen Canvas (Nutzgröße 
880
×
880
880×880
px, JPG-Format).
motor_white_with_logo_1080x1080.pngDasselbe Bild wie Variante 2, jedoch mit dem Logo (logo.png) oben links bei den Koordinaten (50, 50).
