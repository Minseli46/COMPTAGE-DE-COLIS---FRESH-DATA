from doctr.models import ocr_predictor
from doctr.io import DocumentFile
from doctr.utils.visualization import visualize_page
import matplotlib.pyplot as plt
import csv
import os

# 1️⃣ Indique le chemin de ton image
image_path = r"C:\Users\PAVILION\Documents\FRESH DATA\Mindee_docTR\IMG_6963.jpeg"

# 2️⃣ Charge le document
doc = DocumentFile.from_images([image_path])

# 3️⃣ Initialise le modèle OCR (détection + reconnaissance)
predictor = ocr_predictor(pretrained=True)

# 4️⃣ Exécute la prédiction
result = predictor(doc)

# 5️⃣ Affiche le texte reconnu
exported = result.export()
# préparer les collections pour sauvegarde
texts_only = []
texts_with_meta = []  # tuples (page_idx, block_idx, line_idx, text)
for page in exported["pages"]:
    page_idx = page.get("page_index", exported["pages"].index(page))
    for b_idx, block in enumerate(page["blocks"]):
        for l_idx, line in enumerate(block["lines"]):
            text = " ".join([w["value"] for w in line["words"]])
            text = text.strip()
            print(text)
            if text:
                texts_only.append(text)
                texts_with_meta.append((page_idx, b_idx, l_idx, text))

# visualize_page attend une structure de type dict (exportée), pas l'objet Page.
# Utiliser la version exportée que nous avons déjà calculée ci‑dessus.
page0_dict = exported["pages"][0]
fig = visualize_page(page0_dict, image=doc[0])
plt.tight_layout()
plt.savefig("doctr_result.png", dpi=200)
print("✅ Image OCR annotée sauvegardée : doctr_result.png")

# ---------- Sauvegarder les textes extraits ----------
txt_path = os.path.join(os.getcwd(), "doctr_texts.txt")
try:
    with open(txt_path, "w", encoding="utf-8") as f:
        for t in texts_only:
            f.write(t + "\n")
    print(f"Fichier texte (sans métadonnées) enregistré : {txt_path}")
except Exception as e:
    print(f"Erreur en écrivant {txt_path}: {e}")

csv_path = os.path.join(os.getcwd(), "doctr_texts_with_meta.csv")
try:
    with open(csv_path, "w", encoding="utf-8", newline="") as cf:
        writer = csv.writer(cf)
        writer.writerow(["page_index", "block_index", "line_index", "text"])
        for page_idx, b_idx, l_idx, text in texts_with_meta:
            writer.writerow([page_idx, b_idx, l_idx, text])
    print(f"Fichier CSV (avec métadonnées) enregistré : {csv_path}")
except Exception as e:
    print(f"Erreur en écrivant {csv_path}: {e}")
