import os
import shutil
import random

# get files from images_labels dir ending with .jpg
def get_images(path):
    files = []
    for f in os.listdir(path):
        if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg') or f.endswith('.JPG'):
            files.append(f)
    return files


# distribute the images and corresponding labels to train, val and test folders
def distribute(images:list,
               images_dir,
               train_ratio=0.7, 
               test_ratio=0.3,
               zip=False):
    copy_images = images.copy()
    
    # create necessary directories
    output_img_path = os.path.join('output', 'images', 'train')
    output_label_path = os.path.join('output', 'labels', 'train')
    
    output_img_val_path = os.path.join('output', 'images', 'val')
    output_label_val_path = os.path.join('output', 'labels', 'val')
    
    if not os.path.exists(output_img_path):
        os.makedirs(output_img_path)
    if not os.path.exists(output_label_path):
        os.makedirs(output_label_path)
    if not os.path.exists(output_img_val_path):
        os.makedirs(output_img_val_path)
    if not os.path.exists(output_label_val_path):
        os.makedirs(output_label_val_path)
        
    # divide the images and labels into train and test sets randomly
    train_images = random.sample(copy_images, int(len(copy_images)*train_ratio))
    for img in train_images:
        # pop the image from the list
        copy_images.remove(img)
        # get the corresponding label
        label = img.split('.')[0] + '.txt'
        # copy the image and label to the train folder
        shutil.copy(os.path.join(images_dir, img), os.path.join(output_img_path, img))
        shutil.copy(os.path.join(images_dir, label), os.path.join(output_label_path, label))

    for img in copy_images:
        label = img.split('.')[0] + '.txt'
        shutil.copy(os.path.join(images_dir, img), os.path.join(output_img_val_path, img))
        shutil.copy(os.path.join(images_dir, label), os.path.join(output_label_val_path, label))

    if zip:
        # zip output folder
        shutil.make_archive('output', 'zip', 'output')

if __name__ == '__main__':
    images = get_images(path='images_labels')
    distribute(images, images_dir='images_labels', train_ratio=0.75, zip=True)
    
