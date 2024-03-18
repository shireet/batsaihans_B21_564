import sys
from PIL import Image, ImageChops
import os
import numpy as np


def is_valid_file(path):
    if not os.path.exists(path):
        print(f"{path} does not exist")
        return False
    if not (path.endswith(".png") or path.endswith(".bmp")):
        print(f"{path} is not a PNG or BMP file")
        return False
    return True

def safe_number_input(number_type: type, lower_bound=None, upper_bound=None):
    while True:
        try:
            number = number_type(input("Enter a number: "))
            if lower_bound is not None and number < lower_bound:
                raise ValueError(f"Number must be greater than {lower_bound}")
            if upper_bound is not None and number > upper_bound:
                raise ValueError(f"Number must be less than {upper_bound}")
            return number
        except ValueError as e:
            print(e)

def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_image(image, path):
    create_dir_if_not_exists(os.path.dirname(path))
    image.save(path)

def conservative_smoothing(image, filter_size):
    indexer = filter_size // 2
    new_image = image.copy()

    width, height = image.size
    pixels = new_image.load()

    for x in range(width):
        for y in range(height):
            window_values = []
            for i in range(max(0, x - indexer), min(width, x + indexer + 1)):
                for j in range(max(0, y - indexer), min(height, y + indexer + 1)):
                    if (i != x) or (j != y):  
                        window_values.append(image.getpixel((i, j)))
            max_value = max(window_values)
            min_value = min(window_values)
            pixel_value = image.getpixel((x, y))
            if pixel_value > max_value:
                pixels[x, y] = max_value
            elif pixel_value < min_value:
                pixels[x, y] = min_value

    return new_image

def difference_image(image1, image2):
    assert image1.size == image2.size
    difference_image = ImageChops.difference(image1, image2)
    return difference_image



#Conservative smoothing works well for low levels of salt and pepper noise.

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("no files provided")
        sys.exit(1)
    
    for i in range(1, len(sys.argv)):
        if not is_valid_file(sys.argv[i]):
            print(f"Invalid file: {sys.argv[i]}")
            sys.exit(1) 

    k = safe_number_input(int, 1)

    opened = list(map(lambda x: Image.open(x), sys.argv[1:]))
results = list(map(lambda image: conservative_smoothing(image, k), opened))

# Save filtered images
for i, result in enumerate(results):  # Change variable name here
    filename = os.path.basename(opened[i].filename)
    save_image(result, f"output/filtered_{filename}")

diff_images = []

for i in range(len(opened)):
    diff_images.append(difference_image(opened[i], results[i]))

for i, diff_result in enumerate(diff_images):
    filename = os.path.basename(opened[i].filename)
    save_image(diff_result, f"output/difference_{filename}")
    
    
    

    
    