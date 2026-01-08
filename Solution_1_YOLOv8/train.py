from ultralytics import YOLO
import os

def train_yolo_model():
    """Entraîner YOLOv8 sur les images de colis"""
    # Charger le modèle pré-entraîné
    model = YOLO('yolov8n.pt')
    
    # Entraîner (nécessite des annotations au format YOLO)
    results = model.train(
        data='colis.yaml',
        epochs=100,
        imgsz=640,
        batch=8,
        name='colis_detector'
    )
    
    return model

if __name__ == "__main__":
    model = train_yolo_model()
    print("Modèle entraîné avec succès!")
