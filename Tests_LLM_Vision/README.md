# Tests LLM Vision

## Description
Tests des modèles de vision des LLM (Mistral, ChatGPT, Gemini) pour compter les colis.

## Installation
```bash
pip install -r requirements.txt
```

## Configuration des clés API
Avant d'exécuter les tests, configurez vos clés API:

```powershell
# PowerShell (Windows)
$env:OPENAI_API_KEY='votre_clé_openai'
$env:MISTRAL_API_KEY='votre_clé_mistral'
$env:GOOGLE_API_KEY='votre_clé_google'
```

## Utilisation

### Test individuel
```bash
# ChatGPT (GPT-4o)
python test_chatgpt.py

# Mistral (Pixtral)
python test_mistral.py

# Gemini (Gemini 1.5 Flash)
python test_gemini.py
```

### Comparaison de tous les résultats
```bash
python compare_results.py
```

## Résultats
Les résultats sont sauvegardés dans `results/llm_results/`
- `chatgpt_results.json`
- `mistral_results.json`
- `gemini_results.json`

## Coûts estimés
- **ChatGPT (GPT-4o)**: ~$0.01-0.02 par image
- **Mistral (Pixtral)**: ~$0.01 par image
- **Gemini (Flash)**: Gratuit jusqu'à 1500 requêtes/jour

## Notes
- GPT-4o est généralement le plus précis
- Gemini Flash est le plus rapide et gratuit
- Mistral Pixtral offre un bon compromis prix/performance
