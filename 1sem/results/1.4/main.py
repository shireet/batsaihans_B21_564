import sys
import os
from PIL import Image
import numpy as np
import tempfile

def stretch_image(image, scale):
    width, height = image.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    stretched_image = Image.new("RGB", (new_width, new_height))
    for x in range(new_width):
        for y in range(new_height):
            src_x = int(x / scale)
            src_y = int(y / scale)
            stretched_image.putpixel((x, y), image.getpixel((src_x, src_y)))

    return stretched_image

def compress_image(image, scale):
    width, height = image.size
    new_width = int(width / scale)
    new_height = int(height / scale)
    compressed_image = Image.new("RGB", (new_width, new_height))
    for x in range(new_width):
        for y in range(new_height):
            src_x = int(x * scale)
            src_y = int(y * scale)
            compressed_image.putpixel((x, y), image.getpixel((src_x, src_y)))

    return compressed_image

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

def is_valid_file(path): #check if the file providedd is png and is there
    if not os.path.exists(path):
        print(f"{path} does not exist")
        return False
    if not path.endswith(".png"):
        print(f"{path} is not a PNG file")
        return False
    return True

def choice(choice: dict):
    for key, value in choice.items():
        print(f"{key} - {value}")
    while True:
        user_input = input("Enter your choice: ")
        if user_input in choice.values():
            return user_input
        print("Invalid choice")

def open_image(path):
    return Image.open(path)

def two_step_resampling(image, M, N):
    return compress_image(stretch_image(image, M), N)

def one_step_resampling(image, K: float):
    width, height = image.size
    new_width = int(width * K)
    new_height = int(height * K)
    new_image = Image.new("RGB", (new_width, new_height))
    for x in range(new_width):
        for y in range(new_height):
            src_x = int(x / K)
            src_y = int(y / K)
            new_image.putpixel((x, y), image.getpixel((src_x, src_y)))

    return new_image

def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_image(image, path):
    create_dir_if_not_exists("output")
    image.save(os.path.join("output", path))


operations = {
   'Интерполяция': '1',
    'Децимация': '2',
    'Двухпроходная передискретизация': '3',
    'Однопроходная передискретизация': '4'
}


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("no files provided")
        sys.exit(1)

    for i in range(1, len(sys.argv)):
        if not is_valid_file(sys.argv[i]):
            print(f"Invalid file: {sys.argv[i]}")
            sys.exit(1)    

    selected_operation =  choice(operations)

    if selected_operation == '1':
        print("Enter M")
        scale = safe_number_input(int, 1)
        opened = map(open_image, sys.argv[1:])
        stretched = map(lambda image: stretch_image(image, scale), opened)
        for i, image in enumerate(stretched):
            save_image(image, f"stretched_{os.path.basename(sys.argv[i + 1])}")
    elif selected_operation == '2':
        print("Enter N")
        scale =  safe_number_input(int, 1)
        opened = map( open_image, sys.argv[1:])
        compressed = map(lambda image:  compress_image(image, scale), opened)
        for i, image in enumerate(compressed):
             save_image(image, f"compressed_{os.path.basename(sys.argv[i + 1])}")
    elif selected_operation == '3':
        print("Enter M")
        M =  safe_number_input(int, 1)
        print("Enter N")
        N =  safe_number_input(int, 1)
        opened = map( open_image, sys.argv[1:])
        resampled = map(lambda image:  two_step_resampling(image, M, N), opened)
        for i, image in enumerate(resampled):
             save_image(image, f"two_step_resampled_{os.path.basename(sys.argv[i + 1])}")
    elif selected_operation == '4':
        print("Enter K")
        K =  safe_number_input(float, 0)
        opened = map( open_image, sys.argv[1:])
        resampled = map(lambda image:  one_step_resampling(image, K), opened)
        for i, image in enumerate(resampled):
             save_image(image, f"one_step_resampled_{os.path.basename(sys.argv[i + 1])}")
    else:
        print("Invalid operation")
        sys.exit(1)
    print("Done")
    sys.exit(0)