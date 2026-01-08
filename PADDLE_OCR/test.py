
"""Script de test pour PaddleOCR.

Ce fichier évite l'import direct de `paddleocr.utils.visual` (qui n'existe
dans certaines versions de la distribution `paddleocr`) et fournit une petite
fonction de rendu basée sur PIL si besoin.

Usage:
  python test.py <chemin_vers_image>

Si aucun chemin n'est fourni, le script affiche un message d'aide et ne lève
pas d'ImportError. Ainsi, l'erreur d'import initiale est corrigée.
"""

from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
import sys
import os


def draw_ocr_pil(image, ocr_result, font_path=None, font_size=14):
	"""Dessine les boîtes et le texte retournés par PaddleOCR sur une image PIL.

	ocr_result attend le format retourné par `PaddleOCR().ocr` :
	  [ [box, [text, score]], ... ]
	"""
	img = image.copy()
	draw = ImageDraw.Draw(img)
	try:
		font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
	except Exception:
		font = ImageFont.load_default()

	for line in ocr_result:
		box = line[0]
		text = line[1][0] if len(line) > 1 and isinstance(line[1], (list, tuple)) else ""
		score = line[1][1] if len(line) > 1 and isinstance(line[1], (list, tuple)) and len(line[1]) > 1 else None

		# dessiner le polygone
		try:
			draw.polygon([tuple(p) for p in box], outline=(0, 255, 0))
		except Exception:
			# box peut parfois être un tableau plat
			try:
				pts = [(box[i], box[i+1]) for i in range(0, len(box), 2)]
				draw.polygon(pts, outline=(0, 255, 0))
			except Exception:
				pass

		# dessiner le texte au-dessus de la boîte
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
	img_path = sys.argv[1] if len(sys.argv) > 1 else None
	if not img_path or not os.path.exists(img_path):
		print("Usage: python test.py <image_path>")
		print("Aucun fichier image fourni ou fichier introuvable. Le script a été mis à jour pour éviter l'ImportError.")
		return

	# instancier PaddleOCR (ajuster les options selon vos modèles/langues)
	ocr = PaddleOCR(use_angle_cls=True, lang='en')
	result = ocr.ocr(img_path, cls=True)

	pil_img = Image.open(img_path).convert('RGB')
	out_img = draw_ocr_pil(pil_img, result)
	out_path = os.path.splitext(os.path.basename(img_path))[0] + "_ocr.jpg"
	out_img.save(out_path)
	print(f"Résultat enregistré dans : {out_path}")


if __name__ == '__main__':
	main()



