# Solution 2 : OpenCV - Détection par contours

## Description
Cette solution utilise des techniques de traitement d'image classiques (OpenCV) sans machine learning.

## Installation
```bash
pip install -r requirements.txt
```

## Utilisation
```bash
python detect_contours.py
```

## Avantages
- ✅ Aucun entraînement nécessaire
- ✅ Test immédiat
- ✅ Rapide et léger
- ✅ Fonctionne bien si les colis sont visuellement séparés

## Paramètres ajustables
Dans le fichier `detect_contours.py`, vous pouvez modifier:
- `min_area`: taille minimale d'un contour (ligne 42)
- Seuils Canny: pour la détection de bords (ligne 26)

## Résultats
Les images annotées sont sauvegardées dans `results/opencv_results/`
