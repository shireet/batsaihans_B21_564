import pandas as pd
import numpy as np
from PIL import Image
import csv
from math import sqrt
from generate import *
from segmentation import *
from attribute import *
from ast import literal_eval

greek = [
    "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ",
    "μ", "ν", "ξ", "ο", "π", "ρ", "σ","τ","υ","φ","χ","ψ","ω"
]


alphabet='αβγδεζηθικλμνξοπρστυφχψω'

#sentence= 'ελληνικα γραμματα απαντα κοσμουν'
sentence = 'αβγδεζηθικλμνξοπρστυφχψω'
font_path='times-new-roman-greek.ttf'
features=pd.read_csv('input/features.csv')

def hypothesis(img):
    hypothesis = []
    distances = []

    weight = compute_weights(img, 0, img.size[0], 0, img.size[1])/area(img)
    relative_center_x = relative_center (img, 0)
    relative_center_y = relative_center(img, 1)
    relative_inertia_x = relative_inertia (img, 0)
    relative_inertia_y = relative_inertia (img, 1)

    for i in alphabet:
        row = features.loc[features['letter'] == i]
        
        distance = np.sqrt((row['relative_weight'].values[0] - weight)**2 + (row['relative_center_x'].values[0] - relative_center_x)**2 + (row['relative_center_y'].values[0] - relative_center_y)**2 + (row['relative_inertia_x'].values[0] - relative_inertia_x)**2 + (row['relative_inertia_y'].values[0] - relative_inertia_y)**2)
        distances.append(distance)

    
    max_dist = max(distances)
    for letter, distance in zip(alphabet, distances):
        hypothesis.append((letter, (max_dist-distance)/max_dist))
    
    return sorted(hypothesis, key=lambda x: x[1], reverse=True)
    

 


if __name__ == "__main__":
    res = ''
    font_size=52
    font_size = int(input("Enter the font size: "))
    generate_sentence(sentence, 'input/sentence.png', font_size)
    img = Image.open('input/sentence.png').convert('L')
    img_binarized = binarize(np.array(img))
    x_profile, _ = get_profiles(img_binarized)
    letters, _ = split_letters(np.array(img), x_profile)

    for index, letter in enumerate(letters):
        output_path = os.path.join(f"letters/{index}.png")
        Image.fromarray(letter).convert('L').save(output_path)
    with open("output/result.txt", "w") as file:
        for i in range(len(os.listdir("letters"))):
            filename = f"{i}.png"  # Construct the filename
            f = os.path.join("letters", filename)
            img = Image.open(f).convert("L")
            binarized = binarize(np.array(img))
            hyp = hypothesis(img)
            for letter, score in hyp:
                file.write(f"{letter}: {score} ")
            file.write("\n")
            os.remove(f)
            res += hyp[0][0]
    print("Original sentence:  ", sentence.replace(" ", ""))
    print("Predicted sentence: ", res)
            
   




