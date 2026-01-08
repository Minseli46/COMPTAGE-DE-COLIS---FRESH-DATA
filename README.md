# 🔍 Veille Technologique OCR

Projet de comparaison et d'évaluation de différentes solutions OCR (Optical Character Recognition) pour l'extraction de texte à partir d'images de documents et d'étiquettes.

## 📋 Vue d'ensemble

Ce projet explore plusieurs technologies OCR pour identifier la meilleure solution adaptée à l'extraction de données structurées à partir d'étiquettes et de documents :

- **PaddleOCR** - Solution OCR open-source performante de Baidu
- **Mindee docTR** - Framework OCR moderne basé sur PyTorch/TensorFlow
- **DocVQA** - Modèles de Question-Réponse sur documents (LayoutLMv3, VLM)

## 🗂️ Structure du projet

```
Veille technologique OCR/
│
├── PADDLE_OCR/                    # Implémentation PaddleOCR
│   ├── test_PaddleOCR.py         # Script de test principal
│   ├── ocr_texts.txt             # Résultats textuels extraits
│   ├── ocr_texts_with_scores.csv # Résultats avec scores de confiance
│   └── ocr_env/                  # Environnement virtuel Python
│
├── Mindee_docTR/                 # Implémentation Mindee docTR
│   ├── test_MindeedocTR.py      # Script de test principal
│   ├── doctr_texts.txt          # Résultats textuels extraits
│   ├── doctr_texts_with_meta.csv # Résultats avec métadonnées
│   └── doctr_env/               # Environnement virtuel Python
│
├── DocVQA/                       # Implémentation DocVQA/VLM
│   └── DocVQA.ipynb             # Notebook d'expérimentation
│
├── Image etiquette/              # Dossier contenant les images de test
│
└── results/                      # Dossier des résultats de comparaison
    └── opencv_results/
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation de l'environnement

Chaque solution OCR dispose de son propre environnement virtuel. Suivez les instructions ci-dessous selon la solution que vous souhaitez utiliser.

---

### Option 1 : PaddleOCR

#### 1. Créer et activer l'environnement virtuel

```bash
# Créer l'environnement
python -m venv PADDLE_OCR/ocr_env

# Activer l'environnement (Windows PowerShell)
PADDLE_OCR\ocr_env\Scripts\Activate.ps1

# Activer l'environnement (Windows CMD)
PADDLE_OCR\ocr_env\Scripts\activate.bat

# Activer l'environnement (Linux/macOS)
source PADDLE_OCR/ocr_env/bin/activate
```

#### 2. Installer les dépendances

```bash
pip install paddlepaddle paddleocr pillow
```

#### 3. Utilisation

```bash
cd PADDLE_OCR
python test_PaddleOCR.py votre_image.jpg
```

**Fonctionnalités :**
- Détection de texte dans les images
- Reconnaissance avec scores de confiance
- Visualisation des boîtes englobantes
- Export en TXT et CSV

---

### Option 2 : Mindee docTR

#### 1. Créer et activer l'environnement virtuel

```bash
# Créer l'environnement
python -m venv Mindee_docTR/doctr_env

# Activer l'environnement (Windows PowerShell)
Mindee_docTR\doctr_env\Scripts\Activate.ps1

# Activer l'environnement (Windows CMD)
Mindee_docTR\doctr_env\Scripts\activate.bat

# Activer l'environnement (Linux/macOS)
source Mindee_docTR/doctr_env/bin/activate
```

#### 2. Installer les dépendances

```bash
# Installation avec PyTorch (recommandé)
pip install python-doctr[torch]
pip install matplotlib pillow
```

#### 3. Utilisation

```bash
cd Mindee_docTR
python test_MindeedocTR.py
```

> **Note :** Modifiez le chemin de l'image dans le script avant l'exécution.

**Fonctionnalités :**
- OCR avec détection et reconnaissance
- Visualisation des résultats
- Métadonnées (page, bloc, ligne)
- Export structuré en CSV

---

### Option 3 : DocVQA (Notebooks)

#### 1. Installer Jupyter et les dépendances

```bash
pip install jupyter notebook
pip install easyocr paddlepaddle paddleocr
pip install torch torchvision transformers accelerate datasets pillow
pip install matplotlib opencv-python rapidfuzz python-Levenshtein
```

#### 2. Lancer le notebook

```bash
cd DocVQA
jupyter notebook DocVQA.ipynb
```

**Fonctionnalités :**
- Comparaison EasyOCR vs PaddleOCR
- Modèles VLM/DocVQA (LayoutLMv3)
- Post-traitement avec regex
- Parsing sémantique pour étiquettes
- Question-Réponse sur documents

---

## 📖 Utilisation détaillée

### PaddleOCR - Exemple d'utilisation

```python
from paddleocr import PaddleOCR
from PIL import Image

# Initialiser l'OCR
ocr = PaddleOCR(use_angle_cls=True, lang='fr')

# Analyser une image
result = ocr.ocr('mon_image.jpg', cls=True)

# Afficher les résultats
for line in result[0]:
    box = line[0]
    text = line[1][0]
    score = line[1][1]
    print(f"Texte: {text} (confiance: {score:.2f})")
```

### Mindee docTR - Exemple d'utilisation

```python
from doctr.models import ocr_predictor
from doctr.io import DocumentFile

# Charger le document
doc = DocumentFile.from_images(['mon_image.jpg'])

# Initialiser le prédicteur
predictor = ocr_predictor(pretrained=True)

# Exécuter l'OCR
result = predictor(doc)

# Extraire le texte
for page in result.pages:
    for block in page.blocks:
        for line in block.lines:
            text = " ".join([word.value for word in line.words])
            print(text)
```

---

## 📊 Comparaison des solutions

| Solution | Avantages | Inconvénients | Cas d'usage |
|----------|-----------|---------------|-------------|
| **PaddleOCR** | - Rapide<br>- Multi-lingue<br>- Bons scores | - Nécessite PaddlePaddle | Documents généraux, étiquettes |
| **Mindee docTR** | - Moderne<br>- Bien documenté<br>- PyTorch | - Plus lourd | Documents structurés |
| **DocVQA** | - Question-Réponse<br>- Compréhension sémantique | - Complexe<br>- GPU recommandé | Extraction d'infos spécifiques |

---

## 🛠️ Personnalisation

### Modifier le chemin des images

**PaddleOCR :**
Passez le chemin en argument :
```bash
python test_PaddleOCR.py chemin/vers/votre/image.jpg
```

**Mindee docTR :**
Modifiez la variable `image_path` dans [test_MindeedocTR.py](Mindee_docTR/test_MindeedocTR.py) :
```python
image_path = r"C:\chemin\vers\votre\image.jpg"
```

### Ajuster les paramètres OCR

Consultez la documentation officielle :
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Mindee docTR](https://github.com/mindee/doctr)
- [Transformers (DocVQA)](https://huggingface.co/docs/transformers)

---

## 📄 Formats de sortie

### Fichiers TXT
Texte brut extrait, une ligne par élément détecté.

### Fichiers CSV
Structure avec métadonnées :
- **PaddleOCR** : `text, score`
- **Mindee docTR** : `page_index, block_index, line_index, text`

---

## 🐛 Résolution de problèmes

### Erreur d'import de PaddleOCR

Si vous obtenez une erreur "Module not found: paddleocr" :
1. Vérifiez que l'environnement virtuel est activé
2. Réinstallez : `pip install paddleocr paddlepaddle`

### Erreur CUDA (GPU)

Si vous n'avez pas de GPU NVIDIA :
- **PaddleOCR** : Fonctionne en mode CPU par défaut
- **docTR** : Installez la version CPU de PyTorch
- **DocVQA** : Ajoutez `device='cpu'` lors de l'initialisation du modèle

### Problèmes de chemin Windows

Utilisez des chemins bruts (raw strings) avec le préfixe `r` :
```python
image_path = r"C:\Users\...\image.jpg"
```

---

## 📚 Ressources

- [Documentation PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/README_fr.md)
- [Documentation Mindee docTR](https://mindee.github.io/doctr/)
- [Documentation Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [LayoutLMv3 Paper](https://arxiv.org/abs/2204.08387)

---

## 📝 Licence

Ce projet est un travail de veille technologique à des fins d'évaluation et de comparaison.

---

## 🤝 Contribution

Pour toute question ou amélioration, n'hésitez pas à ouvrir une issue ou une pull request.

---

## 👤 Auteur

Projet de veille technologique OCR - Fresh Data

---

## 🔄 Mises à jour

- **Janvier 2026** : Création du projet de veille
- Comparaison PaddleOCR, Mindee docTR, DocVQA
- Tests sur images d'étiquettes
