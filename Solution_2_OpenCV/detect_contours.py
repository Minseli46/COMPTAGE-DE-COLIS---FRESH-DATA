import cv2
import numpy as np
from pathlib import Path
import json

def detect_packages_opencv(image_path):
    """Détecter les colis par segmentation et contours"""
    # Lire l'image
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"Erreur: Impossible de charger l'image {image_path}")
        return 0, None, None
    
    original = img.copy()
    
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Réduction du bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Détection de contours multi-méthodes
    # Méthode 1: Canny
    edges = cv2.Canny(blurred, 30, 100)
    
    # Méthode 2: Seuillage adaptatif
    thresh = cv2.adaptiveThreshold(blurred, 255, 
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 11, 2)
    
    # Opérations morphologiques
    kernel = np.ones((3,3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Trouver les contours
    contours, hierarchy = cv2.findContours(morph, 
                                           cv2.RETR_EXTERNAL, 
                                           cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrer les contours par taille
    min_area = 500  # Ajuster selon vos images
    valid_contours = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            # Vérifier si c'est approximativement rectangulaire
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            if len(approx) >= 4:  # Au moins 4 côtés
                valid_contours.append(contour)
                # Dessiner le contour
                cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
    
    # Afficher le nombre
    count = len(valid_contours)
    cv2.putText(img, f'Colis: {count}', (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    
    return count, img, original

def extract_number_from_filename(filename):
    """Extraire le nombre de colis du nom de fichier"""
    import re
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else None

def process_all_images(folder_path='../Palettes', output_folder='../results/opencv_results'):
    """Traiter toutes les images du dossier"""
    # Obtenir le chemin absolu du script
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Construire les chemins absolus
    folder = project_root / 'Palettes'
    output_folder = project_root / 'results' / 'opencv_results'
    
    output_folder.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    if not folder.exists():
        print(f"Erreur: Le dossier {folder} n'existe pas")
        return results
    
    image_files = list(folder.glob('*.jpeg')) + list(folder.glob('*.jpg')) + list(folder.glob('*.png'))
    
    if not image_files:
        print(f"Aucune image trouvée dans {folder_path}")
        return results
    
    for img_file in image_files:
        print(f"\nTraitement de {img_file.name}...")
        count, processed_img, original = detect_packages_opencv(img_file)
        
        if processed_img is None:
            continue
        
        # Extraire le nombre réel du nom de fichier
        real_count = extract_number_from_filename(img_file.name)
        
        accuracy = 'OK' if count == real_count else f'Erreur: {abs(count-real_count)}'
        
        results[img_file.name] = {
            'detected': count,
            'expected': real_count,
            'accuracy': accuracy
        }
        
        # Sauvegarder l'image annotée
        output_path = output_folder / f'annotated_{img_file.name}'
        cv2.imwrite(str(output_path), processed_img)
        
        print(f"Détecté: {count} | Attendu: {real_count} | {accuracy}")
    
    # Sauvegarder les résultats JSON
    json_path = output_folder / 'results.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    return results

if __name__ == "__main__":
    print("="*60)
    print("SOLUTION 2: Détection OpenCV par contours")
    print("="*60)
    
    results = process_all_images()
    
    # Afficher le résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES RÉSULTATS")
    print("="*60)
    for img, data in results.items():
        print(f"{img}: {data['detected']} détectés / {data['expected']} attendus - {data['accuracy']}")
    
    print(f"\nImages annotées sauvegardées dans: results/opencv_results/")
