import os
import json
from pathlib import Path
import base64

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ Package openai non installé. Exécutez: pip install openai")

def encode_image(image_path):
    """Encoder l'image en base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def count_packages_chatgpt(image_path, api_key):
    """Compter les colis avec GPT-4 Vision"""
    if not OPENAI_AVAILABLE:
        return None, "Package openai non installé"
    
    client = OpenAI(api_key=api_key)
    
    # Encoder l'image
    base64_image = encode_image(image_path)
    
    # Appeler l'API
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # ou "gpt-4-vision-preview"
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Compte précisément le nombre de colis/cartons sur cette palette. Réponds uniquement avec le nombre exact, sans autre texte."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=50
        )
        
        # Extraire la réponse
        answer = response.choices[0].message.content
        
        try:
            count = int(''.join(filter(str.isdigit, answer)))
        except:
            count = None
        
        return count, answer
    
    except Exception as e:
        return None, f"Erreur API: {str(e)}"

def test_all_images_chatgpt(folder_path='../Palettes'):
    """Tester ChatGPT sur toutes les images"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ ERREUR: Définir la variable d'environnement OPENAI_API_KEY")
        print("Exécutez dans le terminal: $env:OPENAI_API_KEY='votre_clé'")
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
        print(f"\n🔍 Analyse de {img_file.name} avec ChatGPT...")
        
        count, raw_answer = count_packages_chatgpt(img_file, api_key)
        
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
    
    json_path = output_path / 'chatgpt_results.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ Résultats sauvegardés dans: {json_path}")
    
    return results

if __name__ == "__main__":
    print("="*60)
    print("TEST CHATGPT VISION (GPT-4o)")
    print("="*60)
    
    results = test_all_images_chatgpt()
    
    if results:
        print("\n" + "="*60)
        print("RÉSUMÉ")
        print("="*60)
        for img, data in results.items():
            print(f"{img}: {data['accuracy']}")
