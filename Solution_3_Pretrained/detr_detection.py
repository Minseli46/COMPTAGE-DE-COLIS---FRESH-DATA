from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import torch
from pathlib import Path
import json

def detect_with_detr(image_path, confidence_threshold=0.7):
    """Détecter les objets avec DETR pré-entraîné"""
    print(f"Chargement du modèle DETR...")
    
    # Charger le modèle
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    
    # Charger l'image
    image = Image.open(image_path)
    
    # Préparer l'image
    inputs = processor(images=image, return_tensors="pt")
    
    # Faire la prédiction
    outputs = model(**inputs)
    
    # Convertir les sorties en détections
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs, 
        target_sizes=target_sizes, 
        threshold=confidence_threshold
    )[0]
    
    # Compter les objets (toutes catégories pertinentes)
    count = len(results['scores'])
    
    # Obtenir les labels
    labels = [model.config.id2label[label.item()] for label in results['labels']]
    
    return count, results, labels

def test_all_images_detr(folder_path='../Palettes', confidence_threshold=0.7):
    """Tester DETR sur toutes les images"""
    # Obtenir le chemin absolu du script
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Construire les chemins absolus
    folder = project_root / 'Palettes'
    results_dict = {}
    
    if not folder.exists():
        print(f"Erreur: Le dossier {folder} n'existe pas")
        return results_dict
    
    image_files = list(folder.glob('*.jpeg')) + list(folder.glob('*.jpg')) + list(folder.glob('*.png'))
    
    if not image_files:
        print(f"Aucune image trouvée dans {folder_path}")
        return results_dict
    
    for img_file in image_files:
        print(f"\nAnalyse de {img_file.name}...")
        
        try:
            count, detections, labels = detect_with_detr(img_file, confidence_threshold)
            
            # Extraire le nombre attendu
            import re
            match = re.search(r'(\d+)', img_file.name)
            expected = int(match.group(1)) if match else None
            
            results_dict[img_file.name] = {
                'detected': count,
                'expected': expected,
                'confidence_scores': detections['scores'].tolist(),
                'labels': labels,
                'accuracy': 'OK' if count == expected else f'Erreur: {abs(count-expected)}'
            }
            
            print(f"Détecté: {count} objets | Attendu: {expected}")
            print(f"Labels détectés: {set(labels)}")
            
        except Exception as e:
            print(f"Erreur lors du traitement de {img_file.name}: {e}")
            continue
    
    # Sauvegarder les résultats
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_path = project_root / 'results' / 'pretrained_results'
    output_path.mkdir(parents=True, exist_ok=True)
    
    json_path = output_path / 'detr_results.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results_dict, f, indent=4, ensure_ascii=False)
    
    return results_dict

if __name__ == "__main__":
    print("="*60)
    print("SOLUTION 3: Détection avec DETR pré-entraîné")
    print("="*60)
    
    results = test_all_images_detr(confidence_threshold=0.5)
    
    # Afficher le résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES RÉSULTATS")
    print("="*60)
    for img, data in results.items():
        print(f"{img}: {data['detected']} détectés / {data['expected']} attendus - {data['accuracy']}")
    
    print(f"\nRésultats sauvegardés dans: results/pretrained_results/detr_results.json")
