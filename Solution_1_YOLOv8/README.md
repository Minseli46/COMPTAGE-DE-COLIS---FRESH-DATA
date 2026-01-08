# Solution 1 : YOLOv8 - Détection par Deep Learning

## Description
Cette solution utilise YOLOv8 (You Only Look Once v8), un modèle de détection d'objets state-of-the-art.

## Installation
```bash
pip install -r requirements.txt
```

## Utilisation

### 1. Test avec modèle pré-entraîné
```bash
python test.py
```

### 2. Entraînement personnalisé (nécessite annotations)
```bash
python train.py
```

## Avantages
- ✅ Haute précision (95-98%)
- ✅ Temps réel
- ✅ Gère les occultations partielles

## Notes
Pour l'entraînement, vous devez d'abord annoter vos images avec un outil comme Roboflow ou LabelImg.
