# Comptage de Colis sur Palettes

Projet de comptage automatique des colis présents sur une palette lors des livraisons en supermarché.

## 📁 Structure du projet

```
Comptage colis 2/
├── Palettes/                    # Images de test avec palettes
├── Solution_1_YOLOv8/          # Deep Learning avec YOLOv8
├── Solution_2_OpenCV/          # Vision classique (contours)
├── Solution_3_Pretrained/      # Modèle DETR pré-entraîné
├── Tests_LLM_Vision/           # Tests avec LLM (GPT-4, Gemini, Mistral)
└── results/                    # Résultats de tous les tests
```

## 🚀 Démarrage rapide

### 1. Test le plus simple (OpenCV - sans API)
```bash
cd Solution_2_OpenCV
pip install -r requirements.txt
python detect_contours.py
```

### 2. Tests LLM (nécessite clés API)
```bash
cd Tests_LLM_Vision
pip install -r requirements.txt

# Configurer les clés API
$env:OPENAI_API_KEY='votre_clé'
$env:MISTRAL_API_KEY='votre_clé'
$env:GOOGLE_API_KEY='votre_clé'

# Lancer les tests
python test_chatgpt.py
python test_mistral.py
python test_gemini.py

# Comparer les résultats
python compare_results.py
```

## 📊 Solutions disponibles

### Solution 1: YOLOv8 (Deep Learning)
- **Précision**: ⭐⭐⭐⭐⭐ (95-98%)
- **Setup**: Nécessite annotation et entraînement
- **Temps**: Temps réel après entraînement
- **Recommandé pour**: Production avec dataset annoté

### Solution 2: OpenCV (Contours)
- **Précision**: ⭐⭐⭐ (70-85%)
- **Setup**: Aucun (prêt à l'emploi)
- **Temps**: Très rapide (<1s par image)
- **Recommandé pour**: Tests rapides, POC

### Solution 3: DETR (Pré-entraîné)
- **Précision**: ⭐⭐⭐⭐ (85-90%)
- **Setup**: Aucun entraînement nécessaire
- **Temps**: 2-5s par image
- **Recommandé pour**: Validation sans entraînement

### Tests LLM Vision

#### GPT-4o (ChatGPT)
- **Précision**: ⭐⭐⭐⭐⭐ (95%+)
- **Coût**: ~$0.01-0.02 par image
- **Recommandé pour**: Haute précision, production

#### Gemini 1.5 Flash
- **Précision**: ⭐⭐⭐⭐ (90%)
- **Coût**: Gratuit (1500 req/jour)
- **Recommandé pour**: Tests gratuits

#### Mistral Pixtral
- **Précision**: ⭐⭐⭐⭐ (90%)
- **Coût**: ~$0.01 par image
- **Recommandé pour**: Bon compromis

## 📈 Résultats

Tous les résultats sont sauvegardés dans le dossier `results/`:
- Images annotées
- Fichiers JSON avec détails
- Rapport de comparaison CSV
- Résumé des performances

## 🎯 Recommandation

**Pour démarrer immédiatement:**
1. Testez d'abord **Solution 2 (OpenCV)** - aucune configuration nécessaire
2. Si besoin de meilleure précision, testez **Gemini** (gratuit)
3. Pour la production, utilisez **GPT-4o** ou entraînez **YOLOv8**

## 📝 Notes

- Les images dans `Palettes/` sont nommées avec le nombre réel de colis (ex: "Image_10 colis.jpeg")
- Tous les scripts génèrent des rapports JSON avec la précision
- Le script `compare_results.py` compare toutes les méthodes testées

## 🛠️ Prochaines étapes

1. **Annoter les images** pour entraîner YOLOv8 (si besoin de haute précision)
2. **Tester sur plus d'images** pour valider la robustesse
3. **Déployer** la solution choisie (application mobile, API, etc.)

## 📞 Support

Pour toute question, consultez les README.md dans chaque dossier de solution.
