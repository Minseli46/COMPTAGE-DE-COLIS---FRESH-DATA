from ultralytics import YOLO
from pathlib import Path
from PIL import Image
import numpy as np
import time

image_path = Path('ft1.jpeg')
output_dir = Path('resultats_tests/fine_tuning_all_epochs')
output_dir.mkdir(parents=True, exist_ok=True)

for epoch in range(50):
    model_path = Path(f'./runs/detect/train14/weights/epoch{epoch}.pt')
    if not model_path.exists():
        print(f"Model {model_path} not found, skipping...")
        continue

    try:
        model = YOLO(str(model_path))
        results = model.predict(source=str(image_path), conf=0.1, save=False, verbose=False)
        if not results:
            print(f"Epoch {epoch}: no results.")
            continue
        r = results[0]

        
        img = None
        if hasattr(r, 'plot'):
            img = r.plot()
        elif hasattr(r, 'orig_img'):
            img = r.orig_img
        elif hasattr(r, 'orig_imgs'):
            img = r.orig_imgs[0]

        if img is None:
            print(f"Epoch {epoch}: could not obtain plotted image.")
            continue

        if isinstance(img, np.ndarray):
            img_pil = Image.fromarray(img)
        else:
            img_pil = Image.open(img) if isinstance(img, (str, Path)) else None
            if img_pil is None:
                print(f"Epoch {epoch}: unknown image type, skipping.")
                continue

        dest = output_dir / f'epoch{epoch}{".jpg"}'
        if dest.exists():
            dest = output_dir / f'epoch{epoch}_{int(time.time())}.jpg'
        img_pil.save(dest)
        print(f"Epoch {epoch} done -> {dest.name}")

    except Exception as e:
        print(f"Epoch {epoch} error: {e}")

print("All tests completed. Check 'resultats_tests/fine_tuning_all_epochs'.")