# Solution 3 : DETR - Modèle pré-entraîné

## Description
Cette solution utilise DETR (DEtection TRansformer) de Facebook, un modèle pré-entraîné sur COCO dataset.

## Installation
```bash
pip install -r requirements.txt
```

## Utilisation
```bash
python detr_detection.py
```

## Avantages
- ✅ Aucun entraînement nécessaire
- ✅ Test immédiat
- ✅ Modèle robuste pré-entraîné
- ✅ Détecte 80+ catégories d'objets

## Configuration
Ajustez le seuil de confiance dans le code (par défaut: 0.5)

## Note
DETR détecte des objets génériques. Les résultats peuvent inclure d'autres objets que les colis.
