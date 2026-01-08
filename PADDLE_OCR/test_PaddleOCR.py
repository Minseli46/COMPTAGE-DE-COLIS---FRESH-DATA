try:
    from paddleocr import PaddleOCR
except Exception:
    # Tentative automatique : ajouter le site-packages du venv sibling 'ocr_env' si présent
    import importlib
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    candidate = os.path.join(project_root, 'ocr_env', 'Lib', 'site-packages')
    if os.path.isdir(candidate):
        if candidate not in sys.path:
            sys.path.insert(0, candidate)
        try:
            paddleocr = importlib.import_module('paddleocr')
            PaddleOCR = getattr(paddleocr, 'PaddleOCR')
        except Exception:
            print("Erreur: 'paddleocr' trouvé dans", candidate, "mais l'import a échoué.")
            print("Vérifie que les dépendances (paddlepaddle, etc.) sont installées dans ce venv.")
            raise
    else:
        print("Erreur: impossible d'importer 'paddleocr' (module introuvable et 'ocr_env' non trouvé).")
        print("Astuce: exécute le script avec le python du venv qui contient paddleocr. Exemple (PowerShell):")
        print(f"& \"{os.path.join(project_root,'ocr_env','Scripts','python.exe')}\" \"{os.path.join(current_dir,'test_PaddleOCR.py')}\" IMG_6963.jpeg")
        raise
from PIL import Image, ImageDraw, ImageFont
import os
import sys
import csv


def parse_line(item):
    # Retourne (box, text, score) en essayant plusieurs formes possibles
    box = None
    text = ""
    score = None

    # cas: list/tuple comme [box, [text, score]]
    if isinstance(item, (list, tuple)):
        if len(item) >= 1:
            box = item[0]
        if len(item) >= 2:
            sec = item[1]
            if isinstance(sec, (list, tuple)) and len(sec) >= 1:
                text = sec[0]
                if len(sec) > 1:
                    try:
                        score = float(sec[1])
                    except Exception:
                        score = None
            elif isinstance(sec, dict):
                # ex: {'text':..., 'score':...}
                text = sec.get('text', '')
                score = sec.get('score', sec.get('confidence', None))
            elif isinstance(sec, str):
                text = sec

    # cas: dict comme {'box':..., 'text':..., 'score':...}
    elif isinstance(item, dict):
        box = item.get('box') or item.get('bbox') or item.get('points') or item.get('poly')
        text = item.get('text') or item.get('label') or item.get('transcription') or ""
        score = item.get('score') or item.get('confidence')

    return box, text, score


# Fonction de rendu utilisant PIL (fallback si draw_ocr n'existe pas)
def draw_ocr_pil(image, ocr_result, font_path=None, font_size=14):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    for line in ocr_result:
        box, text, score = parse_line(line)
        if box is None:
            continue

        # dessiner la boîte
        try:
            draw.polygon([tuple(p) for p in box], outline=(0, 255, 0))
        except Exception:
            try:
                pts = [(box[i], box[i+1]) for i in range(0, len(box), 2)]
                draw.polygon(pts, outline=(0, 255, 0))
            except Exception:
                pass

        # dessiner le texte
        try:
            xs = [p[0] for p in box]
            ys = [p[1] for p in box]
            text_pos = (min(xs), max(min(ys) - font_size, 0))
            label = f"{text}" + (f" ({score:.2f})" if score is not None else "")
            draw.text(text_pos, label, fill=(255, 0, 0), font=font)
        except Exception:
            pass

    return img


def main():
    # 1️⃣ Initialiser le modèle OCR
    ocr = PaddleOCR(use_angle_cls=True, lang='fr')  # 'fr' pour français

    # 2️⃣ Chemin vers ton image (peut être passé en argument)
    # Par défaut, on utilise le fichier IMG_6963.jpeg situé dans le même dossier que ce script.
    default_image = os.path.join(os.path.dirname(__file__), 'IMG_6963.jpeg')
    image_path = sys.argv[1] if len(sys.argv) > 1 else default_image
    if not os.path.exists(image_path):
        print(f"Fichier introuvable : {image_path}\nUsage: python test_PaddleOCR.py <image_path>")
        return

    # 3️⃣ Exécuter l'OCR (ne pas passer d'argument `cls` — indisponible sur cette version)
    result = ocr.ocr(image_path)

    # debug: afficher la structure renvoyée par PaddleOCR (pour diagnostic)
    try:
        print("DEBUG: type(result)=", type(result))
        # afficher un aperçu (quelques premiers éléments)
        if isinstance(result, (list, tuple)):
            first = result[0]
            print("DEBUG: result[0] repr:\n", repr(first)[:2000])
            # afficher les clés/top-level fields s'il s'agit d'un dict
            if isinstance(first, dict):
                print("DEBUG: result[0] keys:\n", list(first.keys()))
                for k in list(first.keys()):
                    try:
                        v = first[k]
                        print(f"  - {k}: type={type(v)}, repr_preview={repr(v)[:200]}\n")
                    except Exception as _:
                        print(f"  - {k}: (cannot repr)\n")
        else:
            print("DEBUG: result repr:\n", repr(result)[:2000])
    except Exception as e:
        print("DEBUG: impossible d'afficher result:", e)

    # normaliser la structure (certaines versions renvoient la liste de lignes directement)
    # Cas spécial : PaddleOCR vX retourne [ { 'rec_texts': [...], 'rec_polys': [...], 'rec_scores': [...] } ]
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and 'rec_texts' in result[0]:
        first = result[0]
        rec_texts = first.get('rec_texts', []) or []
        rec_scores = first.get('rec_scores', []) or []
        rec_polys = first.get('rec_polys', []) or []
        # construire une liste homogène [ [box, [text, score]], ... ]
        lines = []
        for i in range(max(len(rec_polys), len(rec_texts))):
            box = rec_polys[i] if i < len(rec_polys) else None
            text = rec_texts[i] if i < len(rec_texts) else ''
            score = rec_scores[i] if i < len(rec_scores) else None
            # convertir box en liste de tuples si nécessaire
            try:
                box_list = [tuple(p) for p in box] if box is not None else None
            except Exception:
                box_list = box
            lines.append([box_list, [text, score]])
    else:
        lines = result[0] if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list) else result

    # 4️⃣ Afficher le texte reconnu
    def parse_line(item):
        # Retourne (box, text, score) en essayant plusieurs formes possibles
        box = None
        text = ""
        score = None

        # cas: list/tuple comme [box, [text, score]]
        if isinstance(item, (list, tuple)):
            if len(item) >= 1:
                box = item[0]
            if len(item) >= 2:
                sec = item[1]
                if isinstance(sec, (list, tuple)) and len(sec) >= 1:
                    text = sec[0]
                    if len(sec) > 1:
                        try:
                            score = float(sec[1])
                        except Exception:
                            score = None
                elif isinstance(sec, dict):
                    # ex: {'text':..., 'score':...}
                    text = sec.get('text', '')
                    score = sec.get('score', sec.get('confidence', None))
                elif isinstance(sec, str):
                    text = sec

        # cas: dict comme {'box':..., 'text':..., 'score':...}
        elif isinstance(item, dict):
            box = item.get('box') or item.get('bbox') or item.get('points') or item.get('poly')
            text = item.get('text') or item.get('label') or item.get('transcription') or ""
            score = item.get('score') or item.get('confidence')

        return box, text, score

    # Collecter les résultats dans des structures pour sauvegarde
    texts_only = []
    texts_with_scores = []  # tuples (text, score)

    for line in lines:
        box, text, confidence = parse_line(line)
        # normaliser text
        if text is None:
            text = ""
        text_str = str(text).strip()
        # afficher pour l'instant
        if confidence is not None:
            try:
                print(f"{text_str} (confiance : {float(confidence):.2f})")
            except Exception:
                print(f"{text_str} (confiance : {confidence})")
        else:
            print(text_str)

        # n'enregistrer que les lignes non vides
        if text_str != "":
            texts_only.append(text_str)
            # mettre score à vide si None
            texts_with_scores.append((text_str, ("" if confidence is None else float(confidence))))

    # 5️⃣ (Optionnel) Afficher le résultat visuel et l'enregistrer
    pil_image = Image.open(image_path).convert('RGB')
    out_img = draw_ocr_pil(pil_image, lines, font_path=None)
    out_path = 'result_image.jpg'
    out_img.save(out_path)
    print(f"Image OCR enregistrée : {out_path}")

    # ---------- sauvegarder les textes dans deux fichiers ----------
    # 1) fichier texte simple (UTF-8) — une ligne par texte reconnu
    txt_path = 'ocr_texts.txt'
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            for t in texts_only:
                f.write(t + '\n')
        print(f"Fichier texte (sans scores) enregistré : {txt_path}")
    except Exception as e:
        print(f"Erreur en écrivant {txt_path}: {e}")

    # 2) CSV avec texte et score (bon pour Excel/traitement structuré)
    csv_path = 'ocr_texts_with_scores.csv'
    try:
        with open(csv_path, 'w', encoding='utf-8', newline='') as cf:
            writer = csv.writer(cf)
            writer.writerow(['text', 'confidence'])
            for text_val, score_val in texts_with_scores:
                # écrire score vide si inconnu
                writer.writerow([text_val, ("" if score_val == "" else f"{float(score_val):.6f}")])
        print(f"Fichier CSV (avec scores) enregistré : {csv_path}")
    except Exception as e:
        print(f"Erreur en écrivant {csv_path}: {e}")


if __name__ == '__main__':
    main()
