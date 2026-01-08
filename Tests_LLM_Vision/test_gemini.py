import os
import json
from pathlib import Path

try:
    import google.generativeai as genai
    from PIL import Image
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Package google-generativeai non installé. Exécutez: pip install google-generativeai")

def count_packages_gemini(image_path, api_key):
    """Compter les colis avec Gemini Vision"""
    if not GEMINI_AVAILABLE:
        return None, "Package google-generativeai non installé"
    
    genai.configure(api_key=api_key)
    
    # Charger l'image
    img = Image.open(image_path)
    
    # Créer le prompt
    prompt = "Compte exactement le nombre de colis/cartons présents sur cette palette. Réponds uniquement avec le nombre, sans texte supplémentaire."
    
    try:
        # Utiliser gemini-pro-vision pour l'analyse d'images
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # Générer la réponse
        response = model.generate_content([prompt, img])
        answer = response.text
        
        # Extraire le nombre
        try:
            count = int(''.join(filter(str.isdigit, answer)))
        except:
            count = None
        
        return count, answer
    
    except Exception as e:
        return None, f"Erreur API: {str(e)}"

def test_all_images_gemini(folder_path='../Palettes'):
    """Tester Gemini sur toutes les images"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ ERREUR: Définir la variable d'environnement GOOGLE_API_KEY")
        print("Exécutez dans le terminal: $env:GOOGLE_API_KEY='votre_clé'")
        return {}
    
    # Obtenir le chemin absolu
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    folder = project_root / 'Palettes'
    
    results = {}
    
    if not folder.exists():
        print(f"Erreur: Le dossier {folder_path} n'existe pas")
        return results
    
    image_files = list(folder.glob('*.jpeg')) + list(folder.glob('*.jpg')) + list(folder.glob('*.png'))
    
    if not image_files:
        print(f"Aucune image trouvée dans {folder_path}")
        return results
    
    for img_file in image_files:
        print(f"\n🔍 Analyse de {img_file.name} avec Gemini...")
        
        count, raw_answer = count_packages_gemini(img_file, api_key)
        
        # Nombre attendu
        import re
        match = re.search(r'(\d+)', img_file.name)
        expected = int(match.group(1)) if match else None
        
        accuracy = 'OK' if count == expected else f'Erreur: {abs(count-expected) if count else "N/A"}'
        
        results[img_file.name] = {
            'detected': count,
            'expected': expected,
            'raw_answer': raw_answer,
            'accuracy': accuracy
        }
        
        print(f"Détecté: {count} | Attendu: {expected} | {accuracy}")
        print(f"Réponse brute: {raw_answer}")
    
    # Sauvegarder
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_path = project_root / 'results' / 'llm_results'
    output_path.mkdir(parents=True, exist_ok=True)
    
    json_path = output_path / 'gemini_results.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ Résultats sauvegardés dans: {json_path}")
    
    return results

if __name__ == "__main__":
    print("="*60)
    print("TEST GEMINI VISION")
    print("="*60)
    
    results = test_all_images_gemini()
    
    if results:
        print("\n" + "="*60)
        print("RÉSUMÉ")
        print("="*60)
        for img, data in results.items():
            print(f"{img}: {data['accuracy']}")
