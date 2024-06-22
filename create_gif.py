"""
Helper script to generate a GIF from input and output images
WARNING: this script pronounces GIF with a hard G...
"""

from PIL import Image
import os
from tqdm import tqdm
from argparse import ArgumentParser


def resize_image(img_path, output_size=(200, 200)):
    img = Image.open(img_path)
    img_resized = img.resize(output_size)
    return img_resized

def create_side_by_side(input_img, output_img):
    width, height = input_img.size
    new_width = width * 2
    side_by_side = Image.new('RGB', (new_width, height))
    side_by_side.paste(input_img, (0, 0))
    side_by_side.paste(output_img, (width, 0))
    return side_by_side

def create_gif(src_dir, dst_dir, gif_name):
    input_images = sorted(os.listdir(src_dir))

    resized_images = []

    for inp_img in tqdm(input_images):
        input_path = os.path.join(src_dir, inp_img)
        output_name = f"{os.path.splitext(inp_img)[0]}_cartoon.png"
        output_path = os.path.join(dst_dir, output_name)

        resized_input = resize_image(input_path)
        resized_output = resize_image(output_path)

        side_by_side_img = create_side_by_side(resized_input, resized_output)
        resized_images.append(side_by_side_img)

    resized_images[0].save(gif_name, save_all=True, append_images=resized_images[1:], duration=500, loop=0)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--src_dir', default='inputs')
    parser.add_argument('--dst_dir', default='outputs')
    parser.add_argument('--file_name', default='cartoon.gif')
    args = parser.parse_args()

    create_gif(args.src_dir, args.dst_dir, args.file_name)
