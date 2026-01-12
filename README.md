Détection et Comptage de Colis sur Palettes (YOLOv8)

Cette étape du projet vise à entraîner un modèle d'Intelligence Artificielle (YOLOv8) capable de détecter et compter des colis sur des palettes logistiques, en particulier dans des configurations d'empilement dense.

---

## 1. Acquisition des Données (Dataset)

Nous utilisons une base de données existante (type *Stacked Carton Dataset*) via la plateforme Roboflow pour l'apprentissage initial de la géométrie des empilements.

**Procédure d'installation depuis Roboflow :**

1.  Se rendre sur [Roboflow Universe](https://universe.roboflow.com/).
2.  Dans la barre de recherche, taper des mots-clés comme `pallet boxes` ou `stacked cartons`.
3.  Sélectionner un dataset pertinent (privilégier ceux avec un grand nombre d'images).
4.  Aller dans le menu **DATA -> Dataset** (ou "Download this Dataset").
5.  Sélectionner le format **YOLOv8**.
6.  Choisir l'option **"Download zip to computer"**.
7.  **Action :** Extraire le contenu du ZIP et placer les dossiers dans le répertoire du projet (ex: dossier `raw_data`).

---

## 2. Commandes d'Installation et d'Entraînement

Voici la séquence de commandes pour configurer l'environnement et lancer l'apprentissage du modèle.

### 2.1 Création de l'environnement virtuel
```bash
conda create -n yolo python=3.11 -y
conda activate yolo
```
> **Note :** Cette étape permet de créer un environnement virtuel Python isolé dans VS Code. Cela évite les conflits de versions avec les dépendances installées sur d'autres projets de la machine.

### 2.2 Installation des dépendances
```bash
pip install --upgrade pip
pip install "numpy<2" matplotlib ultralytics
```
> **Note :** Cette partie installe la librairie Ultralytics (YOLO) et ses requis. La mention `"numpy<2"` est particulièrement importante car la version 2.0 de NumPy (sortie récemment) a créé des incompatibilités avec beaucoup de bibliothèques d'IA actuelles.

### 2.3 Préparation des données (Split)
Lancer le script de préparation (ex: `prepare_data.py`) :
```bash
python prepare_data.py
```
> **Note :** Ce script effectue deux actions :
> 1. Mélange et sépare les images brutes en deux dossiers : **Train** (80% pour l'apprentissage) et **Val** (20% pour le test).
> 2. Génère le fichier `training/data_split.yaml`. C'est une version modifiée du fichier original, mettant à jour les chemins d'accès (paths) en absolu pour éviter les erreurs de chemin introuvable.

### 2.4 Lancement de l'entraînement (Training)
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt').train(data='CHEMIN VERS LE data_split.yaml DE LA DATASET TELECHARGEE', epochs=50, imgsz=640, save=True, save_period=1)"
```
> **Note :** Ici, on entraîne le modèle YOLO sur 50 époques avec les données fournies via le `data_split.yaml`.
> * `save_period=1` : Sauvegarde l'état du modèle à chaque époque, utile pour l'analyse.

### 2.5 Validation et Test
```bash
python -c "from ultralytics import YOLO; print(YOLO('runs/detect/train/weights/best.pt').val(data='training/data_split.yaml'))"
```
> **Note :** Ici, on lance une évaluation (validation) du modèle entraîné précédemment. On utilise le fichier `best.pt` (le meilleur résultat obtenu) pour mesurer sa performance réelle sur des images qu'il ne connaît pas (le jeu de validation).

---

## 3. Méthode pour la labellisation manuelle et le Fine-Tuning (Entraîner le modèle sur le cas Réel)

Bien que le modèle soit entraîné sur des milliers d'images de cartons, il peut échouer sur notre cas d'usage spécifique (palettes de fruits et légumes).

### Pourquoi faire du fine-tuning ?
Il existe un **"Domain Gap"** (écart de domaine) entre les datasets publics et la réalité du terrain :
* **Textures différentes :** Les datasets publics contiennent surtout des cartons bruns lisses (type Amazon). Nos palettes contiennent du bois (cagettes), des filets et des cartons colorés/imprimés.

### Tutoriel : Labellisation avec Label Studio
Pour corriger cela, nous utilisons l'outil **Label Studio** pour annoter nos propres images.
*(Source vidéo : [Tutoriel YouTube](https://youtu.be/r0RspiLG260?si=qVeRdpowewCy0Hgv))*

#### 1) Installation et lancement
Ouvrir le terminal et exécuter les commandes suivantes :
```bash
pip install label-studio
label-studio start
```
Une page web s'ouvrira automatiquement (généralement sur `http://localhost:8080`).

#### 2) Connexion
Sur la page de login, cliquer sur **"Sign Up"**. Comme l'outil tourne en local sur votre machine, vous pouvez utiliser des informations fictives (ex: `a@a.com` / `fakepassword`).

#### 3) Création du projet
1.  Cliquer sur **Create Project**.
2.  **Data Import :** Faire glisser vos images ici.
    * *Conseil :* Importer les images par lots de 100 maximum pour éviter les erreurs de chargement.
3.  **Labeling Setup :**
    * Choisir le template **Object Detection with Bounding Boxes**.
    * Supprimer les labels par défaut (Airplane, Car, etc.).
    * Ajouter un nouveau label dans la zone de texte (*Add label names*) : écrire **Carton** (ou le nom exact correspondant à la classe 0 du modèle YOLO visible dans le data.yaml de la dataset choisie sur roboflow pour entraîner le modèle).
    * Cliquer sur **Save**.

#### 4) Labellisation des images
1.  Cliquer sur une image dans la liste pour ouvrir l'interface d'annotation.
2.  Sélectionner le label "Carton" (ou votre classe) en bas de l'écran.
3.  Dessiner des rectangles précis autour de chaque colis visible.
4.  Une fois tous les colis détourés sur une image, cliquer sur **Submit** (ou *Update*) pour passer à la suivante.

#### 5) Export des données
Une fois toutes les images traitées :
1.  Cliquer sur le bouton **Export** en haut à droite.
2.  Sélectionner le format **YOLO with Images** dans la liste.
3.  Cela téléchargera une archive `.zip` contenant les images et les fichiers `.txt` correspondants.

#### 6) Entraînement du modèle
1.  Dézipper l'archive téléchargée.
2.  Intégrer ces nouvelles données (images et labels) dans le dossier du projet pour entraîner à nouveau le modèle YOLO.
3.  Lancer le script `prepare_data.py` pour régénérer le split Train/Val incluant les nouvelles images. (voir **2.3 de la méthodologie sur Github**)
4.  Lancer l'entraînement.
> **Note importante :** Pour cette étape, il ne faut pas repartir du modèle vide (`yolov8n.pt`), mais du modèle déjà entraîné sur le dataset Roboflow (SCD). Cela permet de conserver les acquis précédents.
> ```bash
> python -c "from ultralytics import YOLO; YOLO('CHEMIN DU best.pt DE L'ENTRAINEMENT PRECEDENT').train(data='CHEMIN DU data_split.yaml DES IMAGES LABELLISEES', epochs=50, imgsz=640, save=True, save_period=1)"
> ```
