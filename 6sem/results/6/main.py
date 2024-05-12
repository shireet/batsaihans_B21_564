import os
import numpy as np
from PIL import Image

def binarize(image):
    threshold = 127
    return (image < threshold) * 255

def get_profiles(image):
    x_profile = np.sum(image, axis=0)
    y_profile = np.sum(image, axis=1)
    return x_profile, y_profile

def split_letters(image, profile):
    letters = []
    borders = []
    letter_start = 0
    is_space = True

    for i in range(image.shape[1]):
        if profile[i] == 0:
            if not is_space:
                is_space = True
                letter, top, bottom = cut(image[:, letter_start:i])
                letters.append(letter)
                borders.append([(top, letter_start), (top, i), (bottom, letter_start), (bottom, i)])
        else:
            if is_space:
                is_space = False
                letter_start = i
                borders.append(letter_start)
    
    last_letter, top, bottom = cut(image[:, letter_start:image.shape[1] - 1])
    return letters, borders

def cut(letter):
    top = 0
    bottom = letter.shape[0] - 1

    while all(letter[top] == 255):
        top += 1
    while all(letter[bottom] == 255):
        bottom -= 1

    return letter[top:bottom+1], top, bottom

if __name__ == '__main__':
    input_image_path = 'input/wow.png'
    output_directory = 'output'

    img = Image.open(input_image_path).convert('L')
    img_binarized = binarize(np.array(img))
    x_profile, _ = get_profiles(img_binarized)
    letters, _ = split_letters(np.array(img), x_profile)

    os.makedirs(output_directory, exist_ok=True)

    for index, letter in enumerate(letters):
        output_path = os.path.join(output_directory, f"{index}.png")
        Image.fromarray(letter).convert('L').save(output_path)
