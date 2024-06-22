import cv2
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
from argparse import ArgumentParser

def cartoonize_image(img, src_dir='inputs', dst_dir='outputs'):
    src_path = os.path.join(src_dir, img)
    image_name = os.path.splitext(img)[0] 
    img = cv2.imread(src_path)

    if img is None:
        print(f"Error: Could not open or find the image {src_path}.")
        return
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)
    _, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)

    color = cv2.bilateralFilter(img, d=9, sigmaColor=300, sigmaSpace=300)
    cartoon = cv2.bitwise_and(color, color, mask=mask)

    dst_path = os.path.join(dst_dir, f'{image_name}_cartoon.png')
    cv2.imwrite(dst_path, cartoon)
    return dst_path

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--src_dir', default='inputs')
    parser.add_argument('--dst_dir', default='outputs')
    args = parser.parse_args()

    os.makedirs(args.dst_dir, exist_ok=True)
    images = os.listdir(args.src_dir)
    
    for img in tqdm(images):
        result_path = cartoonize_image(img, args.src_dir, args.dst_dir)

