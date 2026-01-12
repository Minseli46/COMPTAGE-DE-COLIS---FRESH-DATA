from ultralytics import YOLO

# 1. Charger le modèle que tu as entraîné précédemment
# (Modifie ce chemin selon où ton entraînement a sauvegardé le fichier)
model_path = './runs/detect/train14/weights/best.pt' 
trained_model = YOLO(model_path)

# 2. L'image (ou le dossier d'images) à tester
image_path = './Image (1).jpg'

# 3. Lancer la prédiction
# On ajoute 'project' et 'name' pour savoir où le résultat va être sauvegardé
trained_model.predict(source=image_path, save=True, conf=0.1, project='resultats_tests', name='fine_tuning_best')

print("C'est fait. Vérifie le dossier 'resultats_tests/fine_tuning_best'.")