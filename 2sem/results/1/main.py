import sys
from PIL import Image
import os
import numpy as np
from math import sqrt

def is_valid_file(path):
    if not os.path.exists(path):
        print(f"{path} does not exist")
        return False
    if not (path.endswith(".png") or path.endswith(".bmp")):
        print(f"{path} is not a PNG or BMP file")
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

def semitone(image):
    image = image.convert("RGB")
    width, height = image.size
    new_image = Image.new("L", (width, height))
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            new_pixel = int(0.3 * r + 0.59 * g + 0.11 * b)
            new_image.putpixel((x, y), new_pixel)
    return new_image





'''
M. H. Najafi, A. Murali, D. J. Lilja and J. Sartori,
"GPU-Accelerated Nick Local Image Thresholding Algorithm,"
 2015 IEEE 21st International Conference on Parallel and Distributed Systems (ICPADS),
 Melbourne, VIC, Australia, 2015, pp. 576-584, doi: 10.1109/ICPADS.2015.78. keywords: 
 {Graphics processing units;Kernel;Instruction sets;Programming;Image processing;
 Memory management;Loading;CUDA GPU Programming;image binarization;GPU acceleration;image thresholding;parallel programming},

'''
from PIL import Image

def NICK_binarization(image, r, k):
    image = semitone(image)
    width, height = image.size
    output = Image.new("1", (width, height))

    for i in range(height):
        print(i)
        for j in range(width):
            sum_val = 0
            square_sum = 0
            index = i * width + j
            window_begin_x = max(0, i - r // 2)
            window_begin_y = max(0, j - r // 2)
            window_end_x = min(height - 1, i + r // 2)
            window_end_y = min(width - 1, j + r // 2)
            window_size = (window_end_x - window_begin_x + 1) * (window_end_y - window_begin_y + 1)

            for x in range(window_begin_x, window_end_x + 1):
                for y in range(window_begin_y, window_end_y + 1):
                    temp = image.getpixel((y, x))  # Corrected indexing
                    sum_val += temp
                    square_sum += temp ** 2

            mean = sum_val / window_size
            threshold = mean + k * sqrt((square_sum - mean ** 2) / window_size)

            if threshold < image.getpixel((j, i)):  # Corrected indexing
                output.putpixel((j, i), 1)  # Corrected indexing
            else:
                output.putpixel((j, i), 0)  # Corrected indexing

    return output


def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_image(image, path):
    create_dir_if_not_exists("output")
    image.save(os.path.join("output", path), "BMP")

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

def change_extention(name: str, new_extention: str):
    return os.path.splitext(name)[0] + new_extention

operations = {
        'Полутон': '1',
        'Бинаризация': '2'
}

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("no files provided")
        sys.exit(1)

    for i in range(1, len(sys.argv)):
        if not is_valid_file(sys.argv[i]):
            print(f"Invalid file: {sys.argv[i]}")
            sys.exit(1)  

    choice = choice(operations)


    if choice == "1":
        result = map(lambda x : semitone(x), map(lambda x: Image.open(x), sys.argv[1:]))
        for i, image in enumerate(result):
            save_image(image, f"semitone_{change_extention(os.path.basename(sys.argv[i + 1]), ".bmp")}")

    elif choice == "2":
        r = safe_number_input(int, 1)
        k = safe_number_input(float, -0.2, 0.2)
        result = map(lambda image: NICK_binarization(image, r, k),  map(Image.open, sys.argv[1:]))
        for i, image in enumerate(result):
            
            save_image(image, f"threshold_{change_extention(os.path.basename(sys.argv[i + 1]), ".bmp")}")
    else:
        print("Invalid operation")
        sys.exit(1)
    print("Done")
    sys.exit(0)

    


