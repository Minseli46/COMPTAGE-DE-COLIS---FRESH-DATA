from ultralytics import YOLO
from PIL import Image
import os
import json

def test_yolo_on_images(image_folder='../Palettes'):
    """Tester YOLOv8 sur toutes les images de palettes"""
    model = YOLO('yolov8n.pt')  # ou votre modèle entraîné
    
    results_dict = {}
    
    for img_file in os.listdir(image_folder):
        if img_file.endswith(('.jpeg', '.jpg', '.png')):
            img_path = os.path.join(image_folder, img_file)
            
            # Prédiction
            results = model.predict(img_path, save=True)
            
            # Compter les détections
            num_boxes = len(results[0].boxes)
            results_dict[img_file] = num_boxes
            
            print(f"{img_file}: {num_boxes} colis détectés")
    
    # Sauvegarder les résultats
    os.makedirs('../results/yolov8_results', exist_ok=True)
    with open('../results/yolov8_results/results.json', 'w') as f:
        json.dump(results_dict, f, indent=4)
    
    return results_dict

if __name__ == "__main__":
    results = test_yolo_on_images()
