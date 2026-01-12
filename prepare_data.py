import os, shutil, random

SRC_IMG = os.path.join('training','train','images')
SRC_LABEL = os.path.join('training','train','labels')
OUT_BASE = os.path.join('training','split')
TRAIN_DIR = os.path.join(OUT_BASE,'train')
VAL_DIR = os.path.join(OUT_BASE,'val')
os.makedirs(os.path.join(TRAIN_DIR,'images'), exist_ok=True)
os.makedirs(os.path.join(TRAIN_DIR,'labels'), exist_ok=True)
os.makedirs(os.path.join(VAL_DIR,'images'), exist_ok=True)
os.makedirs(os.path.join(VAL_DIR,'labels'), exist_ok=True)

images = [f for f in os.listdir(SRC_IMG) if f.lower().endswith(('.jpg','.jpeg','.png'))]
images.sort()
random.seed(42)
random.shuffle(images)
split = int(0.8 * len(images))
train_imgs = images[:split]
val_imgs = images[split:]

def copy_set(img_list, target_dir):
    for img in img_list:
        src_img = os.path.join(SRC_IMG, img)
        shutil.copy2(src_img, os.path.join(target_dir,'images', img))
        label_name = os.path.splitext(img)[0] + '.txt'
        src_lbl = os.path.join(SRC_LABEL, label_name)
        dst_lbl = os.path.join(target_dir,'labels', label_name)
        if os.path.exists(src_lbl):
            shutil.copy2(src_lbl, dst_lbl)
        else:
            open(dst_lbl,'w').close()

copy_set(train_imgs, TRAIN_DIR)
copy_set(val_imgs, VAL_DIR)

# write data_split.yaml with absolute paths
abs_train = os.path.abspath(os.path.join(TRAIN_DIR,'images')).replace('\\','/')
abs_val = os.path.abspath(os.path.join(VAL_DIR,'images')).replace('\\','/')
data_yaml = f"""train: {abs_train}
val: {abs_val}
test: {abs_val}

nc: 3
names: ['Carton', 'Pallets_bad', 'Pallets_good']
"""


out_path = os.path.join('training','data_split.yaml')
with open(out_path,'w', encoding='utf-8') as f:
    f.write(data_yaml)

print('Split créé :', len(train_imgs), 'train,', len(val_imgs), 'val')
print('Fichier de config écrit :', out_path)